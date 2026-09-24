"""Writers for the formats briefs usually ask for, plus a resumable checkpoint."""

from __future__ import annotations

import csv
import json
from collections.abc import Iterable, Sequence
from pathlib import Path

from pydantic import BaseModel

from .quality import QAReport

LIST_SEPARATOR = "|"


def as_rows(models: Iterable[BaseModel]) -> list[dict]:
    """JSON-safe dicts (Decimal -> str, dates -> ISO) in field order."""
    return [m.model_dump(mode="json") for m in models]


def _cell(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return LIST_SEPARATOR.join(str(v) for v in value)
    return str(value)


def write_csv(rows: Sequence[dict], path: Path, columns: Sequence[str] | None = None) -> Path:
    """UTF-8 CSV. List values are joined with '|' (documented in the README)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    columns = list(columns or (rows[0].keys() if rows else []))
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(columns)
        for row in rows:
            writer.writerow([_cell(row.get(c)) for c in columns])
    return path


def write_jsonl(rows: Iterable[dict], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return path


def write_json(data, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_report(report: QAReport, out_dir: Path) -> Path:
    write_json(report.to_dict(), out_dir / "qa_report.json")
    md = out_dir / "qa_report.md"
    md.write_text(report.to_markdown(), encoding="utf-8")
    return md


class Checkpoint:
    """Append-only JSONL of finished work items, so a crashed run resumes where it stopped.

    One line per item: ``{"key": ..., "value": ...}``. Appending (instead of rewriting a JSON
    file) means a crash mid-write can lose at most the last line, never the whole file.
    """

    def __init__(self, path: Path, *, resume: bool) -> None:
        self.path = path
        self.done: dict[str, dict] = {}
        path.parent.mkdir(parents=True, exist_ok=True)
        if resume and path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    continue  # a torn last line from a crash
                self.done[item["key"]] = item["value"]
        elif path.exists():
            path.unlink()

    def add(self, key: str, value: dict) -> None:
        self.done[key] = value
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"key": key, "value": value}, ensure_ascii=False, default=str) + "\n")

    def remove(self) -> None:
        self.path.unlink(missing_ok=True)
