"""Requirement extraction from posting text: rules first, the LLM only for what rules missed.

Every value carries its evidence, the passage of the posting that states it. Regional reposts
share one description, so each distinct description is enriched once. The LLM is only asked
about a field when the text contains a hint word for it (no "english" in the text, no English
question), and only within a call budget, spent on the postings most relevant first.
"""

from __future__ import annotations

import asyncio
import hashlib
import re
from collections import Counter
from dataclasses import dataclass, field

from ...llm import FieldSpec, LLMExtractor

FIELDS = (
    FieldSpec("min_years", "minimum years of experience required, as a single integer", "int"),
    FieldSpec("english_level", "required English level exactly as stated (a CEFR code like B2 if given)"),
    FieldSpec("pay_usd_hour_max", "maximum hourly pay in USD, only if stated per hour", "float"),
    FieldSpec("pay_usd_year_max", "maximum annual base salary in USD, only if stated per year", "float"),
    FieldSpec("hours_per_week", "expected weekly hours as stated, e.g. 10-20"),
)
FIELD_NAMES = tuple(f.name for f in FIELDS)

# A field is only worth an LLM call if the text mentions something like it.
_HINTS = {
    "min_years": re.compile(r"\byears?\b", re.I),
    "english_level": re.compile(r"\benglish\b", re.I),
    "pay_usd_hour_max": re.compile(r"per hour|/\s?hr\b|hourly", re.I),
    "pay_usd_year_max": re.compile(r"salary|compensation|annual|per year", re.I),
    "hours_per_week": re.compile(r"hours?\s+(?:per|a|/)\s*week", re.I),
}

_YEARS_RANGE = re.compile(r"\b(\d{1,2})\s*(?:-|–|to)\s*\d{1,2}\s*years?\b[^.\n]{0,80}?\bexperience", re.I)
_YEARS_MIN = re.compile(
    r"\b(\d{1,2})\s*\+?\s*(?:or more\s+)?years?\b[^.\n]{0,80}?\bexperience"
    r"|\bexperience\b[^.\n]{0,40}?\b(\d{1,2})\s*\+?\s*years?\b",
    re.I,
)
_CEFR = re.compile(r"\b([ABC][12])\b")
_ENGLISH_WORDS = ("native", "fluent", "proficient", "advanced", "upper-intermediate", "intermediate")
_HOURLY = re.compile(
    r"(?:\$|US\$\s?|USD\s?)(\d{1,4}(?:\.\d{1,2})?)\s*(?:USD\s*)?(?:/|per|an|a)\s*(?:hour|hr)\b", re.I
)
_YEARLY_RANGE = re.compile(
    r"\$\s?(\d{2,3}(?:,\d{3})+|\d{2,3}[kK])\s*(?:USD\s*)?(?:-|–|—|to)\s*\$?\s?(\d{2,3}(?:,\d{3})+|\d{2,3}[kK])"
)
_HOURS_RANGE = re.compile(r"\b(\d{1,2})\s*(?:-|–|to)\s*(\d{1,2})\s*hours?\s*(?:per|a|/)\s*week", re.I)
_HOURS_SINGLE = re.compile(r"\b(\d{1,2})\s*\+?\s*hours?\s*(?:per|a|/)\s*week", re.I)


@dataclass
class Enrichment:
    values: dict = field(default_factory=dict)
    evidence: dict[str, str] = field(default_factory=dict)
    extracted_by: dict[str, str] = field(default_factory=dict)

    def add(self, name: str, value, evidence: str, by: str) -> None:
        self.values[name] = value
        self.evidence[name] = evidence
        self.extracted_by[name] = by


def description_sha1(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def passages(text: str) -> list[str]:
    """Lines split into sentences: short, literal evidence."""
    out: list[str] = []
    for line in text.splitlines():
        out += [s.strip() for s in re.split(r"(?<=[.!?])\s+", line) if s.strip()]
    return out


def _money(token: str) -> float:
    token = token.replace(",", "")
    return float(token[:-1]) * 1000 if token[-1] in "kK" else float(token)


def rules(text: str) -> Enrichment:
    found = Enrichment()
    years: list[tuple[int, str]] = []
    hourly: list[tuple[float, str]] = []
    yearly: list[tuple[float, str]] = []
    for passage in passages(text):
        if match := _YEARS_RANGE.search(passage):
            years.append((int(match.group(1)), passage))
        elif match := _YEARS_MIN.search(passage):
            years.append((int(match.group(1) or match.group(2)), passage))
        hourly += [(float(m.group(1)), passage) for m in _HOURLY.finditer(passage)]
        for m in _YEARLY_RANGE.finditer(passage):
            low, high = _money(m.group(1)), _money(m.group(2))
            if low >= 20000 and high >= low:
                yearly.append((high, passage))
        if "english_level" not in found.values and "english" in passage.lower():
            if cefr := _CEFR.search(passage):
                found.add("english_level", cefr.group(1), passage, "rules")
            elif word := next((w for w in _ENGLISH_WORDS if w in passage.lower()), None):
                found.add("english_level", word, passage, "rules")
        if "hours_per_week" not in found.values:
            if match := _HOURS_RANGE.search(passage):
                found.add("hours_per_week", f"{match.group(1)}-{match.group(2)}", passage, "rules")
            elif match := _HOURS_SINGLE.search(passage):
                found.add("hours_per_week", match.group(1), passage, "rules")
    plausible_years = [(n, p) for n, p in years if 0 < n <= 30]
    # The strictest stated requirement is the one that binds ("3+ years of Python" and
    # "5+ years of relevant experience" means 5).
    for name, candidates in (("min_years", plausible_years), ("pay_usd_hour_max", hourly),
                             ("pay_usd_year_max", yearly)):
        if candidates:
            value, passage = max(candidates, key=lambda c: c[0])
            found.add(name, value, passage, "rules")
    return found


@dataclass
class EnrichStats:
    postings: int = 0
    distinct_descriptions: int = 0
    rule_hits: Counter = field(default_factory=Counter)
    llm_calls: int = 0
    llm_accepted: int = 0
    llm_rejected: int = 0


async def enrich_postings(postings: list[dict], extractor: LLMExtractor | None) -> EnrichStats:
    """Add FIELDS, ``evidence``, ``extracted_by`` and ``description_sha1`` to every posting in place."""
    stats = EnrichStats(postings=len(postings))
    by_digest: dict[str, Enrichment] = {}
    text_of: dict[str, str] = {}
    priority: dict[str, int] = {}
    for posting in postings:
        digest = description_sha1(posting["description"])
        posting["description_sha1"] = digest
        if digest not in by_digest:
            by_digest[digest] = rules(posting["description"])
            text_of[digest] = posting["description"]
        # spend the LLM budget on postings open to Colombia first, then the unclear ones
        rank = {True: 0, None: 1, False: 2}[posting["open_to_colombia"]]
        priority[digest] = min(priority.get(digest, 2), rank)
    stats.distinct_descriptions = len(by_digest)
    for enrichment in by_digest.values():
        stats.rule_hits.update(enrichment.values.keys())

    if extractor is not None:
        todo = []
        for digest in sorted(by_digest, key=lambda d: priority[d]):
            missing = [f for f in FIELDS
                       if f.name not in by_digest[digest].values and _HINTS[f.name].search(text_of[digest])]
            if missing:
                todo.append((digest, missing))
        todo = todo[: extractor.max_calls]
        results = await asyncio.gather(*(extractor.extract(text_of[d], m) for d, m in todo))
        for (digest, _), extraction in zip(todo, results, strict=True):
            stats.llm_calls += 1
            stats.llm_accepted += len(extraction.values)
            stats.llm_rejected += len(extraction.rejected)
            for name, value in extraction.values.items():
                by_digest[digest].add(name, value, extraction.evidence[name], "llm")

    for posting in postings:
        enrichment = by_digest[posting["description_sha1"]]
        for name in FIELD_NAMES:
            posting[name] = enrichment.values.get(name)
        posting["evidence"] = dict(enrichment.evidence)
        posting["extracted_by"] = dict(enrichment.extracted_by)
    return stats
