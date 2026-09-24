"""Case 2: Quotes to Scrape (https://quotes.toscrape.com).

The same 100 quotes sit behind very different page mechanics: server-rendered pagination,
content written by JavaScript, JavaScript on a 10-second timer, infinite scroll, a table-based
layout, an ASP.NET-style form with ViewState, and a login with a CSRF token.

Brief: one clean dataset (text, author, tags). The point of the case is that every strategy
must return the *same* dataset, and the QA report proves it (cross-source consistency). The
cheapest strategy that passes wins; the browser only runs to confirm the shortcuts.
"""

from __future__ import annotations

import asyncio
import importlib.util
import json
import logging
import re
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..export import as_rows, write_csv, write_jsonl, write_report
from ..fetch import Blocked, Fetcher, FetchStats
from ..normalize import clean_text, strip_quote_marks
from ..quality import Check, DeliverySpec, QAReport, build_report

log = logging.getLogger("wdk.quotes")

BASE_URL = "https://quotes.toscrape.com"


class Quote(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    text: str = Field(min_length=1, description="Quote text without the surrounding quote marks")
    author: str = Field(min_length=1)
    tags: tuple[str, ...] = ()

    @field_validator("tags")
    @classmethod
    def _sorted_unique(cls, tags: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(sorted({clean_text(t) for t in tags if clean_text(t)}))


def _row(text: str, author: str, tags) -> dict:
    return {
        "text": strip_quote_marks(text),
        "author": clean_text(author),
        "tags": sorted({clean_text(t) for t in tags if clean_text(t)}),
    }


def _next_link(soup: BeautifulSoup, url: str) -> str | None:
    link = soup.select_one("li.next a")
    return urljoin(url, link["href"]) if link else None


# -- parsers (pure functions, tested against saved pages) -------------------------------------


def parse_quote_divs(html: str, url: str) -> tuple[list[dict], str | None]:
    """Server-rendered and browser-rendered pages: ``div.quote`` blocks plus a Next link."""
    soup = BeautifulSoup(html, "lxml")
    rows = [
        _row(
            q.select_one("span.text").get_text(),
            q.select_one("small.author").get_text(),
            [a.get_text() for a in q.select("a.tag")],
        )
        for q in soup.select("div.quote")
    ]
    return rows, _next_link(soup, url)


_EMBEDDED_DATA = re.compile(r"var\s+data\s*=\s*(\[.*?\]);", re.DOTALL)


def parse_embedded_json(html: str, url: str) -> tuple[list[dict], str | None]:
    """/js and /js-delayed: the quotes ship as a JSON array inside a <script>. No browser needed."""
    match = _EMBEDDED_DATA.search(html)
    if not match:
        raise ValueError(f"no embedded data array on {url}")
    rows = [_row(d["text"], d["author"]["name"], d["tags"]) for d in json.loads(match.group(1))]
    return rows, _next_link(BeautifulSoup(html, "lxml"), url)


def parse_api_page(payload: dict) -> tuple[list[dict], bool]:
    """/api/quotes: the endpoint the infinite-scroll handler calls."""
    rows = [_row(q["text"], q["author"]["name"], q["tags"]) for q in payload["quotes"]]
    return rows, bool(payload["has_next"])


_TABLE_QUOTE = re.compile(r"^(?P<text>.+)\s+Author:\s+(?P<author>.+?)$", re.DOTALL)


def parse_tableful(html: str, url: str) -> tuple[list[dict], str | None]:
    """Table layout: the author is glued to the quote cell and the tags live in the next row.

    Rows are paired by content pattern, never by position, so a stray spacer row cannot shift
    every tag list onto the wrong quote.
    """
    soup = BeautifulSoup(html, "lxml")
    rows: list[dict] = []
    for tr in soup.select("table tr"):
        cells = tr.find_all("td", recursive=False)
        if len(cells) != 1:
            continue  # the first row carries the sidebar in a second, row-spanning cell
        text = clean_text(cells[0].get_text(" "))
        if match := _TABLE_QUOTE.match(text):
            rows.append(_row(match["text"], match["author"], []))
        elif text.startswith("Tags:") and rows:
            rows[-1]["tags"] = sorted({clean_text(a.get_text()) for a in cells[0].select("a")})
    next_link = next((a for a in soup.find_all("a") if clean_text(a.get_text()).startswith("Next")), None)
    return rows, urljoin(url, next_link["href"]) if next_link else None


@dataclass
class SearchForm:
    viewstate: str
    authors: list[str]
    tags: list[str]


def parse_search_form(html: str) -> SearchForm:
    soup = BeautifulSoup(html, "lxml")
    state = soup.select_one("input[name=__VIEWSTATE]")
    if state is None:
        raise ValueError("no __VIEWSTATE on the search form")

    def options(select_id: str) -> list[str]:
        return [o["value"] for o in soup.select(f"select#{select_id} option") if o.get("value")]

    return SearchForm(state["value"], options("author"), options("tag"))


def parse_search_results(html: str) -> list[tuple[str, str, str]]:
    """(text, author, the one tag the search matched) for each result."""
    soup = BeautifulSoup(html, "lxml")
    return [
        (
            strip_quote_marks(q.select_one("span.content").get_text()),
            clean_text(q.select_one("span.author").get_text()),
            clean_text(q.select_one("span.tag").get_text()),
        )
        for q in soup.select("div.quote")
    ]


# -- strategies ---------------------------------------------------------------------------------


class Run:
    """What a strategy gets: the polite fetcher, a counter for browser traffic, and notes."""

    def __init__(self, fetcher: Fetcher) -> None:
        self.fetcher = fetcher
        self.browser_requests = 0
        self.notes: list[str] = []


async def _paginate(run: Run, start: str, parse) -> list[dict]:
    rows: list[dict] = []
    url: str | None = start
    while url:
        page_rows, url = parse(await run.fetcher.get_text(url), url)
        rows += page_rows
    return rows


async def html_pagination(run: Run) -> list[dict]:
    return await _paginate(run, BASE_URL + "/", parse_quote_divs)


async def js_embedded(run: Run) -> list[dict]:
    return await _paginate(run, BASE_URL + "/js/", parse_embedded_json)


async def js_delayed_embedded(run: Run) -> list[dict]:
    return await _paginate(run, BASE_URL + "/js-delayed/", parse_embedded_json)


async def scroll_api(run: Run) -> list[dict]:
    rows: list[dict] = []
    page, has_next = 1, True
    while has_next:
        payload = await run.fetcher.get_json(f"{BASE_URL}/api/quotes", params={"page": page})
        page_rows, has_next = parse_api_page(payload)
        rows += page_rows
        page += 1
    return rows


async def tableful(run: Run) -> list[dict]:
    return await _paginate(run, BASE_URL + "/tableful/", parse_tableful)


async def viewstate_search(run: Run) -> list[dict]:
    """Choosing an author posts the form back and returns that author's tags plus a new
    __VIEWSTATE; submitting author + tag returns the matches, each showing only the searched tag.
    Tags per quote are rebuilt as the union over every search that returned it."""
    form = parse_search_form(await run.fetcher.get_text(BASE_URL + "/search.aspx"))
    found: dict[tuple[str, str], set[str]] = {}

    async def search_author(author: str) -> None:
        page = await run.fetcher.post(
            BASE_URL + "/filter.aspx", data={"author": author, "__VIEWSTATE": form.viewstate}
        )
        author_form = parse_search_form(page.text)
        for tag in author_form.tags:
            result = await run.fetcher.post(
                BASE_URL + "/filter.aspx",
                data={"author": author, "tag": tag, "__VIEWSTATE": author_form.viewstate,
                      "submit_button": "Search"},
            )
            for text, name, shown_tag in parse_search_results(result.text):
                found.setdefault((name, text), set()).add(shown_tag)

    await asyncio.gather(*(search_author(a) for a in form.authors))
    run.notes.append(f"viewstate-search: {len(form.authors)} authors searched")
    return [_row(text, author, tags) for (author, text), tags in found.items()]


async def login_session(run: Run) -> list[dict]:
    """Log in with the CSRF token, then crawl as an authenticated user. Logged-in pages add a
    Goodreads link to every quote; its presence proves the session cookie is being sent."""
    login_form = BeautifulSoup(await run.fetcher.get_text(BASE_URL + "/login"), "lxml")
    token = login_form.select_one("input[name=csrf_token]")["value"]
    home = await run.fetcher.post(
        BASE_URL + "/login", data={"csrf_token": token, "username": "wdk-demo", "password": "wdk-demo"}
    )
    if 'href="/logout"' not in home.text:
        raise RuntimeError("login did not stick")
    rows: list[dict] = []
    url: str | None = BASE_URL + "/"
    while url:
        html = await run.fetcher.get_text(url)
        if "Goodreads page" not in html:
            raise RuntimeError(f"session lost on {url}")
        page_rows, url = parse_quote_divs(html, url)
        rows += page_rows
    return rows


async def browser_js(run: Run) -> list[dict]:
    from ..browser import open_page

    rows: list[dict] = []
    url: str | None = BASE_URL + "/js/"
    async with open_page() as page:
        page.on("request", lambda _request: setattr(run, "browser_requests", run.browser_requests + 1))
        while url:
            await run.fetcher.check_allowed(url)
            await page.goto(url)
            await page.wait_for_selector("div.quote")
            page_rows, url = parse_quote_divs(await page.content(), url)
            rows += page_rows
    return rows


async def browser_scroll(run: Run) -> list[dict]:
    from ..browser import open_page, scroll_to_end

    url = BASE_URL + "/scroll"
    api_responses = []
    async with open_page() as page:
        page.on("request", lambda _request: setattr(run, "browser_requests", run.browser_requests + 1))
        page.on("response", lambda r: api_responses.append(r) if "/api/quotes" in r.url else None)
        await run.fetcher.check_allowed(url)
        await page.goto(url)
        await page.wait_for_selector("div.quote")
        await scroll_to_end(page, "div.quote")
        rows, _ = parse_quote_divs(await page.content(), url)
        captured = [q for r in api_responses for q in (await r.json())["quotes"]]
    run.notes.append(
        f"browser-scroll: {len(rows)} quotes in the DOM, {len(captured)} in the captured XHR JSON "
        f"({len(api_responses)} calls)"
    )
    return rows


@dataclass(frozen=True)
class Strategy:
    name: str
    mechanic: str
    technique: str
    fn: Callable[[Run], Awaitable[list[dict]]]
    browser: bool = False


STRATEGIES = (
    Strategy("html-pagination", "server-rendered HTML, 10 pages", "BeautifulSoup, follow the Next link",
             html_pagination),
    Strategy("js-embedded-json", "content written by JavaScript", "read the JSON array in the page source",
             js_embedded),
    Strategy("js-delayed-embedded-json", "JavaScript renders after a 10 s timer",
             "same embedded JSON: the timer never has to be waited out", js_delayed_embedded),
    Strategy("scroll-api", "infinite scroll", "call the JSON endpoint the scroll handler calls", scroll_api),
    Strategy("tableful", "table layout, author glued to the quote, tags in the next row",
             "pair rows by content pattern, not position", tableful),
    Strategy("viewstate-search", "ASP.NET-style form: author posts back, then tag, with __VIEWSTATE",
             "replay the postbacks with httpx, union the tags per quote", viewstate_search),
    Strategy("login-session", "login with a CSRF token", "session cookie + hidden token, verify every page",
             login_session),
    Strategy("browser-js", "content written by JavaScript", "Playwright render (proves the shortcut)",
             browser_js, browser=True),
    Strategy("browser-scroll", "infinite scroll", "Playwright scroll to the end + capture the XHR JSON",
             browser_scroll, browser=True),
)


# -- execution and consistency ------------------------------------------------------------------


@dataclass
class StrategyResult:
    strategy: Strategy
    rows: list[dict] = field(default_factory=list)
    requests: int = 0
    seconds: float = 0.0
    error: str | None = None
    notes: list[str] = field(default_factory=list)


def _merge(total: FetchStats, part: FetchStats) -> None:
    total.requests += part.requests
    total.robots_requests += part.robots_requests
    total.retries += part.retries
    total.failures += part.failures
    total.bytes_received += part.bytes_received
    total.status.update(part.status)


async def execute(strategy: Strategy, *, rate: float, concurrency: int, total: FetchStats) -> StrategyResult:
    """Run one strategy with its own fetcher (own cookies, own request count)."""
    result = StrategyResult(strategy)
    started = time.perf_counter()
    async with Fetcher(rate=rate, concurrency=concurrency) as fetcher:
        run = Run(fetcher)
        try:
            result.rows = await strategy.fn(run)
        except Blocked:
            raise  # a challenge page stops every strategy, not just this one
        except Exception as exc:  # one broken strategy must not hide the others' results
            log.exception("strategy %s failed", strategy.name)
            result.error = f"{type(exc).__name__}: {exc}"
        result.requests = fetcher.stats.requests + run.browser_requests
        result.notes = run.notes
        _merge(total, fetcher.stats)
    result.seconds = time.perf_counter() - started
    log.info("%-26s %3d rows  %4d requests  %6.1f s", strategy.name, len(result.rows), result.requests,
             result.seconds)
    return result


def _index(rows: list[dict]) -> dict[tuple[str, str], tuple[str, ...]]:
    return {(r["author"], r["text"]): tuple(sorted(r["tags"])) for r in rows}


def consistency_check(
    baseline: list[dict], result: StrategyResult, expected_missing: frozenset = frozenset()
) -> Check:
    """Does this strategy return exactly the baseline dataset (quotes and their tags)?

    ``expected_missing`` lists quotes the mechanic cannot reach by design; they are reported,
    not failed.
    """
    name = f"matches baseline: {result.strategy.name}"
    if result.error:
        return Check(name, False, f"strategy failed: {result.error}")
    base, got = _index(baseline), _index(result.rows)
    missing = base.keys() - got.keys()
    unexplained = missing - expected_missing
    extra = got.keys() - base.keys()
    mismatched = [k for k in base.keys() & got.keys() if base[k] != got[k]]
    duplicates = len(result.rows) - len(got)
    detail = [f"{len(got)} quotes"]
    if missing & expected_missing:
        detail.append(f"{len(missing & expected_missing)} untagged quote(s) unreachable by design")
    for label, items in (("missing", unexplained), ("extra", extra), ("tag mismatch", mismatched)):
        if items:
            detail.append(f"{label}: {len(items)}")
    if duplicates:
        detail.append(f"duplicates: {duplicates}")
    passed = not (unexplained or extra or mismatched or duplicates)
    return Check(name, passed, "; ".join(detail))


def strategies_table(results: list[StrategyResult], checks: dict[str, Check]) -> str:
    lines = [
        "| Strategy | Page mechanic | Technique | Quotes | Requests | Seconds | Matches baseline |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in results:
        check = checks.get(r.strategy.name)
        verdict = "baseline" if check is None else ("yes" if check.passed else "NO")
        if r.error:
            verdict = f"error: {r.error[:60]}"
        lines.append(
            f"| {r.strategy.name} | {r.strategy.mechanic} | {r.strategy.technique} | {len(r.rows)} | "
            f"{r.requests} | {r.seconds:.1f} | {verdict} |"
        )
    return "\n".join(lines) + "\n"


async def run(
    out_dir: Path, *, rate: float = 8.0, concurrency: int = 8, use_browser: bool = True
) -> QAReport:
    started = time.perf_counter()
    total = FetchStats()
    browser_ready = use_browser and importlib.util.find_spec("playwright") is not None
    results: list[StrategyResult] = []
    skipped: list[Check] = []
    for strategy in STRATEGIES:
        if strategy.browser and not browser_ready:
            reason = "--no-browser" if not use_browser else "playwright is not installed"
            skipped.append(Check(f"matches baseline: {strategy.name}", False, f"skipped ({reason})",
                                 blocking=False))
            continue
        results.append(await execute(strategy, rate=rate, concurrency=concurrency, total=total))

    baseline = results[0]
    untagged = frozenset(k for k, tags in _index(baseline.rows).items() if not tags)
    checks = {
        r.strategy.name: consistency_check(
            baseline.rows, r, untagged if r.strategy.name == "viewstate-search" else frozenset()
        )
        for r in results[1:]
    }
    notes = [
        f"{r.strategy.name}: {len(r.rows)} quotes, {r.requests} requests, {r.seconds:.1f} s" for r in results
    ] + [note for r in results for note in r.notes]
    spec = DeliverySpec(name="quotes.toscrape.com (one dataset, many mechanics)", model=Quote,
                        key=("author", "text"))
    extra_checks = [
        Check(
            "baseline strategy", not baseline.error, baseline.error or f"{baseline.strategy.name} ran clean"
        ),
        *checks.values(),
        *skipped,
    ]
    delivered, report = build_report(
        spec, baseline.rows, extra_checks=extra_checks, fetch_stats=total,
        elapsed_s=time.perf_counter() - started, notes=notes,
    )
    data = as_rows(delivered)
    write_csv(data, out_dir / "quotes.csv")
    write_jsonl(data, out_dir / "quotes.jsonl")
    (out_dir / "strategies.md").write_text(strategies_table(results, checks), encoding="utf-8")
    write_report(report, out_dir)
    return report
