"""Case 3: remote-jobs tracker for LatAm over public job-board APIs.

Brief: every posting from a list of AI-data companies, normalized to one schema (location,
countries, remote, open to Colombia or not), with the stated requirements (years of experience,
English level, pay, weekly hours) backed by evidence; regional reposts grouped into families;
and what changed since the last run. Runs daily on a schedule and commits its snapshot, so the
git history is the change log ("git scraping").

Reliability rules:
* A board that fails is carried over from the previous snapshot (and flagged), never reported
  as "all closed".
* A board that suddenly returns zero postings blocks the run (an API change, not a hiring freeze).
* A NOT READY run never overwrites the published snapshot.
"""

from __future__ import annotations

import asyncio
import datetime as dt
import hashlib
import json
import logging
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Literal

import httpx
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

from ...export import as_rows, write_csv, write_json, write_report
from ...fetch import Fetcher, FetchError
from ...llm import LLMExtractor, evidence_supported
from ...normalize import fold
from ...quality import Check, DeliverySpec, QAReport, build_report
from .enrich import FIELD_NAMES, enrich_postings
from .sources import Board, fetch_board

log = logging.getLogger("wdk.jobs")

SILENT_BOARD_MIN = 5  # a board that had at least this many postings and now returns 0 is suspect


class Posting(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    source: Literal["workable", "greenhouse", "lever"]
    company: str
    posting_id: str
    title: str = Field(min_length=1)
    url: HttpUrl
    location: str
    countries: tuple[str, ...]
    remote: bool | None
    open_to_colombia: bool | None
    employment_type: str | None
    published: dt.date | None
    family_id: str = Field(pattern=r"^[0-9a-f]{12}$")
    description_sha1: str = Field(pattern=r"^[0-9a-f]{40}$")
    min_years: int | None = Field(default=None, ge=0, le=30)
    english_level: str | None = None
    pay_usd_hour_max: float | None = Field(default=None, gt=0, lt=1000)
    pay_usd_year_max: float | None = Field(default=None, gt=0)
    hours_per_week: str | None = None
    evidence: dict[str, str] = Field(default_factory=dict)
    extracted_by: dict[str, str] = Field(default_factory=dict)

    @field_validator("countries")
    @classmethod
    def _iso_codes(cls, countries: tuple[str, ...]) -> tuple[str, ...]:
        bad = [c for c in countries if not (len(c) == 2 and c.isalpha() and c.isupper())]
        if bad:
            raise ValueError(f"not ISO 3166-1 alpha-2: {bad}")
        return tuple(sorted(set(countries)))


def family_id(company: str, title: str) -> str:
    """Regional reposts of one role share company and title; they become one family."""
    return hashlib.sha1(f"{fold(company)}|{fold(title)}".encode()).hexdigest()[:12]


def load_boards(path: Path | None) -> list[Board]:
    text = (path.read_text(encoding="utf-8") if path
            else resources.files(__package__).joinpath("companies.json").read_text(encoding="utf-8"))
    return [Board(**entry) for entry in json.loads(text)]


def load_snapshot(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    return {p["key"]: p for p in json.loads(path.read_text(encoding="utf-8"))["postings"]}


def board_key(board: Board) -> str:
    return f"{board.source}:{board.board}"


def _board_of(posting_key: str) -> str:
    return posting_key.rsplit(":", 1)[0]


def build_families(postings: list[dict]) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for p in postings:
        groups[p["family_id"]].append(p)
    families = []
    for fid, items in groups.items():
        eligible = [p for p in items if p["open_to_colombia"] is True]
        dates = [p["published"] for p in items if p["published"]]

        def top(name, items=items):
            return max((p[name] for p in items if p[name] is not None), default=None)

        families.append({
            "family_id": fid,
            "company": items[0]["company"],
            "title": items[0]["title"],
            "postings": len(items),
            "countries": sorted({c for p in items for c in p["countries"]}),
            "open_to_colombia": True if eligible else (
                None if any(p["open_to_colombia"] is None for p in items) else False),
            "min_years": top("min_years"),
            "english_level": next((p["english_level"] for p in items if p["english_level"]), None),
            "pay_usd_hour_max": top("pay_usd_hour_max"),
            "pay_usd_year_max": top("pay_usd_year_max"),
            "first_published": min(dates) if dates else None,
            "last_published": max(dates) if dates else None,
            "url": (eligible or items)[0]["url"],
        })
    return sorted(families, key=lambda f: (f["company"], f["title"]))


@dataclass
class Diff:
    new: list[dict]
    closed: list[dict]
    changed: list[dict]


def _signature(p: dict) -> tuple:
    return p["title"], p["location"], p["description_sha1"]


def diff_snapshots(previous: dict[str, dict], current: dict[str, dict]) -> Diff:
    return Diff(
        new=[current[k] for k in sorted(current.keys() - previous.keys())],
        closed=[previous[k] for k in sorted(previous.keys() - current.keys())],
        changed=[current[k] for k in sorted(current.keys() & previous.keys())
                 if _signature(current[k]) != _signature(previous[k])],
    )


def _by_family(postings: list[dict], limit: int = 15) -> list[str]:
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for p in postings:
        groups[(p["company"], p["title"])].append(p)
    lines = []
    for (company, title), items in sorted(groups.items(), key=lambda kv: -len(kv[1]))[:limit]:
        countries = sorted({c for p in items for c in p["countries"]})
        where = f" ({', '.join(countries[:8])}{', ...' if len(countries) > 8 else ''})" if countries else ""
        lines.append(f"- {company} · {title} · {len(items)}{where}")
    if len(groups) > limit:
        lines.append(f"- ... and {len(groups) - limit} more families")
    return lines


def changelog_entry(day: dt.date, current: dict[str, dict], diff: Diff, first_run: bool) -> str:
    families = len({p["family_id"] for p in current.values()})
    if first_run:
        return f"## {day} · first snapshot: {len(current)} postings in {families} families\n"
    lines = [f"## {day} · {len(current)} postings · +{len(diff.new)} new · "
             f"-{len(diff.closed)} closed · ~{len(diff.changed)} changed", ""]
    for label, items in (("New", diff.new), ("Closed", diff.closed), ("Changed", diff.changed)):
        if items:
            lines += [f"**{label}**", "", *_by_family(items), ""]
    return "\n".join(lines).rstrip() + "\n"


def prepend_changelog(path: Path, entry: str) -> None:
    header = "# Changelog\n\nOne entry per scheduled run: postings that appeared, closed or changed.\n\n"
    old = path.read_text(encoding="utf-8") if path.exists() else header
    body = old[len(header):] if old.startswith(header) else old
    path.write_text(header + entry + "\n" + body, encoding="utf-8")


async def _fetch_all(fetcher: Fetcher, boards: list[Board]) -> tuple[dict[str, list[dict]], dict[str, str]]:
    async def one(board: Board):
        try:
            return board, await fetch_board(fetcher, board), None
        except (FetchError, ValueError, KeyError) as exc:
            log.error("board %s failed: %s", board_key(board), exc)
            return board, [], f"{type(exc).__name__}: {exc}"

    results = await asyncio.gather(*(one(b) for b in boards))
    fetched = {board_key(b): postings for b, postings, error in results if error is None}
    failed = {board_key(b): error for b, _, error in results if error is not None}
    return fetched, failed


async def run(
    out_dir: Path,
    *,
    rate: float = 4.0,
    concurrency: int = 4,
    companies_path: Path | None = None,
    sheet_id: str | None = None,
    use_llm: bool = True,
    today: dt.date | None = None,
    transport: httpx.AsyncBaseTransport | None = None,
) -> QAReport:
    """``transport`` lets tests replay saved API responses; production leaves it None."""
    started = time.perf_counter()
    boards = load_boards(companies_path)
    snapshot_path = out_dir / "postings.json"
    previous = load_snapshot(snapshot_path)

    async with Fetcher(rate=rate, concurrency=concurrency, transport=transport) as fetcher:
        fetched, failed = await _fetch_all(fetcher, boards)
        raw = [p for postings in fetched.values() for p in postings]
        for p in raw:
            p["family_id"] = family_id(p["company"], p["title"])
        extractor = None
        llm_fetcher = None
        if use_llm:
            llm_fetcher = Fetcher(rate=2, concurrency=4, respect_robots=False, timeout=90)
            extractor = LLMExtractor.from_env(llm_fetcher)
        try:
            enrich_stats = await enrich_postings(raw, extractor)
        finally:
            if llm_fetcher is not None:
                await llm_fetcher.aclose()
        fetch_stats = fetcher.stats

    unsupported = [
        f"{p['key']}:{name}" for p in raw for name, passage in p["evidence"].items()
        if not evidence_supported(p["description"], passage)
    ]
    for p in raw:
        del p["description"]

    carried = [p for key, p in previous.items() if _board_of(key) in failed]
    counts = Counter(_board_of(p["key"]) for p in raw)
    before = Counter(_board_of(k) for k in previous)
    silent = [b for b, n in before.items() if n >= SILENT_BOARD_MIN and b not in failed and counts[b] == 0]

    checks = [
        Check("every board answered", not failed,
              f"{len(boards) - len(failed)}/{len(boards)} boards"
              + (f"; failed (carried over): {failed}" if failed else ""), blocking=False),
        Check("no board went silent", not silent,
              f"boards that dropped to 0 postings: {silent}" if silent else "no board dropped to zero"),
        Check("evidence is verbatim", not unsupported,
              f"{len(unsupported)} value(s) without a literal passage" if unsupported
              else "every extracted value quotes its posting"),
    ]
    resolved = sum(1 for p in raw if p["countries"] or p["open_to_colombia"] is not None)
    checks.append(Check("location resolved", resolved >= 0.9 * max(len(raw), 1),
                        f"{resolved}/{len(raw)} postings have a country or region", blocking=False))

    spec = DeliverySpec(name="remote AI-data jobs tracker", model=Posting, key=("key",))
    delivered, report = build_report(
        spec, raw + carried, extra_checks=checks, fetch_stats=fetch_stats,
        elapsed_s=time.perf_counter() - started,
    )
    records = as_rows(delivered)
    current = {r["key"]: r for r in records}
    diff = diff_snapshots(previous, current)
    open_co = Counter(r["open_to_colombia"] for r in records)
    families = build_families(records)
    hits = enrich_stats.rule_hits
    report.notes += [
        "per board: " + ", ".join(f"{b} {n}" for b, n in sorted(counts.items())),
        f"{len(records)} postings in {len(families)} families; "
        f"{enrich_stats.distinct_descriptions} distinct descriptions",
        f"open to Colombia: yes {open_co[True]}, unclear {open_co[None]}, no {open_co[False]}",
        "rules found (per distinct description): "
        + ", ".join(f"{name} {hits[name]}" for name in FIELD_NAMES),
        (f"LLM: {enrich_stats.llm_calls} calls, {enrich_stats.llm_accepted} values accepted, "
         f"{enrich_stats.llm_rejected} rejected") if extractor
        else "LLM: off (no OPENROUTER_API_KEY or --no-llm)",
        f"since last snapshot: +{len(diff.new)} new, -{len(diff.closed)} closed, "
        f"~{len(diff.changed)} changed",
    ]
    if carried:
        report.notes.append(f"{len(carried)} postings carried over from failed boards: {sorted(failed)}")

    out_dir.mkdir(parents=True, exist_ok=True)
    if report.ready:
        day = today or dt.date.today()
        write_json({"generated_at": report.generated_at, "boards": [board_key(b) for b in boards],
                    "postings": records}, snapshot_path)
        write_csv(records, out_dir / "postings.csv")
        write_csv(families, out_dir / "families.csv")
        prepend_changelog(out_dir / "CHANGELOG.md", changelog_entry(day, current, diff, not previous))
        if sheet_id:
            from ...sheets import open_worksheet, upsert_rows

            for title, rows, key in (("families", families, "family_id"), ("postings", records, "key")):
                result = upsert_rows(open_worksheet(sheet_id, title), rows, key)
                report.notes.append(f"sheet '{title}': +{result.inserted} inserted, "
                                    f"{result.updated} updated, {result.unchanged} unchanged")
    else:
        report.notes.append("NOT READY: the published snapshot was left untouched")
    write_report(report, out_dir)
    return report
