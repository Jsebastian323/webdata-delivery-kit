"""Delivery gate: validate a dataset against its spec and write a QA report before anything ships.

A run is READY only when every blocking check passes. Checks every dataset gets:

* schema      - each row validates against the case's Pydantic model
* unique key  - no two rows share the delivery key
* coverage    - rows delivered vs. the count the source itself declares (when it declares one)
* fill rate   - optional per-field minimums (e.g. description filled in 95% of rows)

Cases add their own checks: cross-source consistency, per-page yield (selector drift), etc.
"""

from __future__ import annotations

import datetime as dt
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass, field

from pydantic import BaseModel, ValidationError

from .fetch import FetchStats


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str = ""
    blocking: bool = True

    @property
    def status(self) -> str:
        if self.passed:
            return "PASS"
        return "FAIL" if self.blocking else "WARN"


@dataclass
class RowError:
    index: int
    key: str
    errors: list[str]


@dataclass
class DeliverySpec:
    name: str
    model: type[BaseModel]
    key: tuple[str, ...]
    expected_count: int | None = None
    min_coverage: float = 1.0
    min_fill: dict[str, float] = field(default_factory=dict)


@dataclass
class QAReport:
    spec: str
    rows_in: int
    rows_delivered: int
    checks: list[Check]
    fill_rates: dict[str, float]
    errors: list[RowError]
    fetch: dict | None = None
    elapsed_s: float | None = None
    notes: list[str] = field(default_factory=list)
    generated_at: str = field(
        default_factory=lambda: dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()
    )

    @property
    def ready(self) -> bool:
        return all(check.passed for check in self.checks if check.blocking)

    @property
    def verdict(self) -> str:
        return "READY" if self.ready else "NOT READY"

    def to_dict(self) -> dict:
        data = asdict(self)
        data["verdict"] = self.verdict
        return data

    def to_markdown(self) -> str:
        lines = [
            f"# QA report: {self.spec}",
            "",
            f"**{self.verdict}** · {self.rows_delivered} rows delivered ({self.rows_in} collected)"
            f" · generated {self.generated_at}",
            "",
            "| Check | Result | Detail |",
            "|---|---|---|",
        ]
        lines += [f"| {c.name} | {c.status} | {c.detail} |" for c in self.checks]
        lines += ["", "## Field fill rates", "", "| Field | Filled |", "|---|---|"]
        lines += [f"| {name} | {rate:.1%} |" for name, rate in self.fill_rates.items()]
        if self.fetch:
            status = ", ".join(f"{code}: {n}" for code, n in self.fetch.get("status", {}).items())
            pace = ""
            if self.elapsed_s:
                pace = f" · {self.elapsed_s:.1f} s · {self.fetch['requests'] / self.elapsed_s:.1f} req/s"
            lines += [
                "",
                "## Fetch",
                "",
                f"{self.fetch['requests']} requests · {self.fetch['retries']} retries · "
                f"{self.fetch['failures']} failures · status {{{status}}}{pace}",
            ]
        if self.notes:
            lines += ["", "## Notes", ""] + [f"- {note}" for note in self.notes]
        if self.errors:
            lines += ["", f"## Rows that failed validation ({len(self.errors)})", ""]
            for err in self.errors[:25]:
                lines.append(f"- row {err.index} `{err.key}`: " + "; ".join(err.errors))
            if len(self.errors) > 25:
                lines.append(f"- ... {len(self.errors) - 25} more in qa_report.json")
        return "\n".join(lines) + "\n"


def _key_of(row: dict | BaseModel, key: Sequence[str]) -> tuple:
    get = row.get if isinstance(row, dict) else lambda name: getattr(row, name, None)
    return tuple(get(name) for name in key)


def validate_rows(rows: Iterable[dict], spec: DeliverySpec) -> tuple[list[BaseModel], list[RowError]]:
    valid: list[BaseModel] = []
    errors: list[RowError] = []
    for index, row in enumerate(rows):
        try:
            valid.append(spec.model.model_validate(row))
        except ValidationError as exc:
            messages = [f"{'.'.join(str(p) for p in e['loc']) or 'row'}: {e['msg']}" for e in exc.errors()]
            errors.append(RowError(index, "|".join(map(str, _key_of(row, spec.key))), messages))
    return valid, errors


def fill_rates(rows: Sequence[BaseModel], model: type[BaseModel]) -> dict[str, float]:
    def filled(value) -> bool:
        return value not in (None, "") and not (isinstance(value, (list, tuple, set, dict)) and not value)

    total = len(rows) or 1
    return {name: sum(filled(getattr(r, name)) for r in rows) / total for name in model.model_fields}


def page_yield_check(name: str, listings: Mapping[str, Sequence[int]], expected: int) -> Check:
    """Selector-drift guard for paginated listings.

    In every listing, each page but the last must yield exactly ``expected`` items and the last
    page between 1 and ``expected``. When a site changes its markup, selectors rarely crash: they
    quietly return zero. This turns that silence into a failed check.
    """
    off = [
        f"{label} p{i + 1}={n}"
        for label, counts in listings.items()
        for i, n in enumerate(counts)
        if (n != expected if i < len(counts) - 1 else not 0 < n <= expected)
    ]
    pages = sum(len(c) for c in listings.values())
    items = sum(sum(c) for c in listings.values())
    detail = f"{len(listings)} listing(s), {pages} pages, {items} items"
    if off:
        detail += "; off-yield: " + ", ".join(off[:8])
    return Check(name, not off, detail)


def build_report(
    spec: DeliverySpec,
    rows: Sequence[dict],
    *,
    extra_checks: Iterable[Check] = (),
    fetch_stats: FetchStats | None = None,
    elapsed_s: float | None = None,
    notes: Iterable[str] = (),
) -> tuple[list[BaseModel], QAReport]:
    """Validate ``rows`` and return (rows to deliver, report). Duplicates are dropped and flagged."""
    valid, errors = validate_rows(rows, spec)
    keys = Counter(_key_of(m, spec.key) for m in valid)
    duplicated = [k for k, n in keys.items() if n > 1]
    delivered, seen = [], set()
    for model in valid:
        k = _key_of(model, spec.key)
        if k not in seen:
            seen.add(k)
            delivered.append(model)

    checks = [
        Check(
            "schema",
            not errors,
            f"{len(errors)} of {len(rows)} rows failed validation" if errors else f"{len(valid)} rows valid",
        ),
        Check(
            "unique key",
            not duplicated,
            f"{len(duplicated)} duplicated key(s), e.g. {duplicated[:3]}"
            if duplicated
            else f"key = {', '.join(spec.key)}",
        ),
    ]
    if spec.expected_count is not None:
        coverage = len(delivered) / spec.expected_count if spec.expected_count else 1.0
        checks.append(
            Check(
                "coverage",
                coverage >= spec.min_coverage,
                f"{len(delivered)}/{spec.expected_count} ({coverage:.1%}, min {spec.min_coverage:.0%})",
            )
        )
    rates = fill_rates(delivered, spec.model)
    for name, minimum in spec.min_fill.items():
        checks.append(
            Check(f"fill rate: {name}", rates[name] >= minimum, f"{rates[name]:.1%} (min {minimum:.0%})")
        )
    if fetch_stats is not None:
        checks.append(
            Check(
                "fetch failures",
                fetch_stats.failures == 0,
                f"{fetch_stats.failures} request(s) failed after retries",
                blocking=False,
            )
        )
    checks.extend(extra_checks)
    report = QAReport(
        spec=spec.name,
        rows_in=len(rows),
        rows_delivered=len(delivered),
        checks=checks,
        fill_rates=rates,
        errors=errors,
        fetch=fetch_stats.as_dict() if fetch_stats else None,
        elapsed_s=round(elapsed_s, 2) if elapsed_s is not None else None,
        notes=list(notes),
    )
    return delivered, report
