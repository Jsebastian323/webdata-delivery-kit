"""Case 1: Books to Scrape (https://books.toscrape.com).

Brief: every book in the catalogue with UPC, title, category, prices in GBP, units in stock,
star rating, review count, description and image URL, as CSV and JSON Lines. Nothing missing.

Techniques: hierarchy traversal (home -> 50 categories -> paginated listings -> book pages),
lenient parsing with strict validation, a resumable checkpoint, and the checks this site makes
possible: coverage against the 1,000 results the home page declares, per-category coverage
against each category's declared count, listing-page yield (selector drift), and the category
seen in the listing matching the book page breadcrumb.
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator

from ..export import Checkpoint, as_rows, write_csv, write_jsonl, write_report
from ..fetch import Blocked, Fetcher, FetchError
from ..normalize import clean_text, first_int, parse_money, word_to_int
from ..quality import Check, DeliverySpec, QAReport, build_report, page_yield_check

log = logging.getLogger("wdk.books")

BASE_URL = "https://books.toscrape.com/"
PER_PAGE = 20


class Book(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    upc: str = Field(pattern=r"^[0-9a-f]{16}$")
    title: str = Field(min_length=1)
    category: str = Field(min_length=1)
    price_gbp: Decimal = Field(ge=0, description="Price including tax, as displayed")
    price_excl_tax_gbp: Decimal = Field(ge=0)
    tax_gbp: Decimal = Field(ge=0)
    in_stock: int = Field(ge=0)
    rating: int = Field(ge=1, le=5)
    reviews: int = Field(ge=0)
    description: str | None = None
    image_url: HttpUrl
    url: HttpUrl

    @model_validator(mode="after")
    def _prices_add_up(self) -> Book:
        if self.price_excl_tax_gbp + self.tax_gbp != self.price_gbp:
            raise ValueError("price_excl_tax_gbp + tax_gbp != price_gbp")
        return self


@dataclass
class Listing:
    book_urls: list[str]
    next_url: str | None
    declared_total: int


@dataclass
class CategoryWalk:
    name: str
    declared: int
    book_urls: list[str] = field(default_factory=list)
    page_yields: list[int] = field(default_factory=list)


def _try(parse: Callable, value):
    """Lenient parsing: return None instead of raising, and let the model reject the row.

    A single odd page then shows up in the QA report with the exact field that failed,
    instead of crashing a 1,000-page run.
    """
    try:
        return parse(value)
    except (TypeError, ValueError, KeyError, AttributeError):
        return None


def _declared_count(soup: BeautifulSoup) -> int:
    strong = soup.select_one("form.form-horizontal strong")
    if strong is None:
        raise ValueError("results counter not found; did the listing markup change?")
    return first_int(strong.get_text())


def parse_home(html: str, url: str = BASE_URL) -> tuple[int, list[tuple[str, str]]]:
    """Return (declared number of books, [(category name, category URL)])."""
    soup = BeautifulSoup(html, "lxml")
    categories = [
        (clean_text(a.get_text()), urljoin(url, a["href"]))
        for a in soup.select("div.side_categories ul li ul li a")
    ]
    if not categories:
        raise ValueError("no categories found in the sidebar; did the markup change?")
    return _declared_count(soup), categories


def parse_listing(html: str, url: str) -> Listing:
    soup = BeautifulSoup(html, "lxml")
    next_link = soup.select_one("ul.pager li.next a")
    return Listing(
        book_urls=[urljoin(url, a["href"]) for a in soup.select("article.product_pod h3 a")],
        next_url=urljoin(url, next_link["href"]) if next_link else None,
        declared_total=_declared_count(soup),
    )


def parse_book(html: str, url: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    main = soup.select_one("div.product_main")
    table = {
        clean_text(tr.th.get_text()): clean_text(tr.td.get_text())
        for tr in soup.select("table.table-striped tr")
        if tr.th and tr.td
    }
    stars = main.select_one("p.star-rating") if main else None
    rating_word = next((c for c in (stars.get("class", []) if stars else []) if c != "star-rating"), "")
    crumbs = [clean_text(li.get_text()) for li in soup.select("ul.breadcrumb li")]
    description = soup.select_one("#product_description + p")
    image = soup.select_one("#product_gallery img")
    availability = table.get("Availability", "")
    return {
        "upc": table.get("UPC"),
        "title": clean_text(main.h1.get_text()) if main and main.h1 else None,
        "category": crumbs[2] if len(crumbs) >= 4 else None,
        "price_gbp": _try(parse_money, table.get("Price (incl. tax)")),
        "price_excl_tax_gbp": _try(parse_money, table.get("Price (excl. tax)")),
        "tax_gbp": _try(parse_money, table.get("Tax")),
        "in_stock": _try(first_int, availability) if "In stock" in availability else 0,
        "rating": _try(word_to_int, rating_word),
        "reviews": _try(int, table.get("Number of reviews")),
        "description": clean_text(description.get_text()) if description else None,
        "image_url": urljoin(url, image["src"]) if image and image.get("src") else None,
        "url": url,
    }


async def walk_category(fetcher: Fetcher, name: str, url: str) -> CategoryWalk:
    """Follow a category's pagination to the end, recording how many books each page yields."""
    walk: CategoryWalk | None = None
    next_url: str | None = url
    while next_url:
        listing = parse_listing(await fetcher.get_text(next_url), next_url)
        if walk is None:
            walk = CategoryWalk(name, listing.declared_total)
        walk.book_urls += listing.book_urls
        walk.page_yields.append(len(listing.book_urls))
        next_url = listing.next_url
    assert walk is not None
    return walk


async def crawl(
    fetcher: Fetcher, checkpoint: Checkpoint, *, max_categories: int | None = None
) -> tuple[list[dict], list[Check], int | None, list[str]]:
    """Return (raw rows, case-specific checks, declared total, notes)."""
    declared_total, categories = parse_home(await fetcher.get_text(BASE_URL + "index.html"))
    if max_categories is not None:
        categories = categories[:max_categories]
        declared_total = None  # a partial run cannot be held to the full catalogue

    walks = await asyncio.gather(*(walk_category(fetcher, name, url) for name, url in categories))
    listed_category: dict[str, str] = {}
    for walk in walks:
        for book_url in walk.book_urls:
            listed_category.setdefault(book_url, walk.name)

    todo = [u for u in listed_category if u not in checkpoint.done]
    log.info("%d categories, %d books listed, %d already in checkpoint", len(walks), len(listed_category),
             len(listed_category) - len(todo))

    failed: list[str] = []

    async def fetch_book(book_url: str) -> None:
        try:
            checkpoint.add(book_url, parse_book(await fetcher.get_text(book_url), book_url))
        except Blocked:
            raise  # stop the whole run; the checkpoint keeps what was already collected
        except FetchError as exc:
            failed.append(f"{book_url}: {exc}")

    await asyncio.gather(*(fetch_book(u) for u in todo))
    rows = [checkpoint.done[u] for u in listed_category if u in checkpoint.done]

    off_category = [
        r["url"] for r in rows if r.get("category") and r["category"] != listed_category.get(r["url"])
    ]
    short_categories = [
        f"{w.name} ({len(w.book_urls)}/{w.declared})" for w in walks if len(w.book_urls) != w.declared
    ]
    checks = [
        Check(
            "per-category coverage",
            not short_categories,
            f"{len(walks)} categories match their declared counts"
            if not short_categories
            else "short: " + ", ".join(short_categories[:10]),
        ),
        page_yield_check(
            "listing page yield (selector drift)", {w.name: w.page_yields for w in walks}, PER_PAGE
        ),
        Check(
            "category: listing vs breadcrumb",
            not off_category,
            f"{len(rows) - len(off_category)}/{len(rows)} agree"
            + (f"; e.g. {off_category[:3]}" if off_category else ""),
        ),
        Check("book pages fetched", not failed, f"{len(failed)} failed" if failed else "all fetched"),
    ]
    return rows, checks, declared_total, failed[:20]


async def run(
    out_dir: Path,
    *,
    rate: float = 8.0,
    concurrency: int = 8,
    resume: bool = False,
    max_categories: int | None = None,
) -> QAReport:
    started = time.perf_counter()
    checkpoint = Checkpoint(out_dir / ".checkpoint.jsonl", resume=resume)
    async with Fetcher(rate=rate, concurrency=concurrency) as fetcher:
        rows, checks, declared_total, notes = await crawl(fetcher, checkpoint, max_categories=max_categories)
        stats = fetcher.stats
    spec = DeliverySpec(
        name="books.toscrape.com catalogue",
        model=Book,
        key=("upc",),
        expected_count=declared_total,
        min_fill={"description": 0.95},
    )
    delivered, report = build_report(
        spec, rows, extra_checks=checks, fetch_stats=stats,
        elapsed_s=time.perf_counter() - started, notes=notes,
    )
    data = as_rows(delivered)
    write_csv(data, out_dir / "books.csv")
    write_jsonl(data, out_dir / "books.jsonl")
    write_report(report, out_dir)
    if report.ready:
        checkpoint.remove()
    return report
