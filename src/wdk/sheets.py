"""Idempotent upsert of rows into a Google Sheet.

Three rules, learned on a production sync that people also edit by hand:

1. Rows are matched by a key column and updated in place; nothing is appended blindly, so
   re-running a job never duplicates rows.
2. Columns are located by header name, not by letter, so people can reorder or insert columns.
3. An empty value never overwrites a filled cell: the sync fills gaps, it does not erase
   someone's notes.

``worksheet`` is anything with gspread's ``get_all_values``, ``update``, ``batch_update`` and
``append_rows``, which keeps this module testable without Google credentials.
"""

from __future__ import annotations

import json
import os
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass
class UpsertResult:
    inserted: int = 0
    updated: int = 0
    unchanged: int = 0


def column_letter(index: int) -> str:
    """0 -> A, 25 -> Z, 26 -> AA."""
    letters = ""
    index += 1
    while index:
        index, rest = divmod(index - 1, 26)
        letters = chr(65 + rest) + letters
    return letters


def cell_value(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (list, tuple)):
        return "|".join(str(v) for v in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False) if value else ""
    return str(value)


def upsert_rows(worksheet, rows: Sequence[dict], key: str) -> UpsertResult:
    result = UpsertResult()
    values = worksheet.get_all_values()
    header = list(values[0]) if values else []
    wanted = list(dict.fromkeys(name for row in rows for name in row))
    if key not in wanted:
        raise ValueError(f"rows have no {key!r} column")
    missing = [name for name in wanted if name not in header]
    if missing:
        header += missing
        worksheet.update([header], "A1")
    col = {name: i for i, name in enumerate(header)}
    row_of = {line[col[key]]: n for n, line in enumerate(values[1:], start=2) if len(line) > col[key]}

    updates, appends = [], []
    for row in rows:
        cells = {name: cell_value(v) for name, v in row.items()}
        number = row_of.get(cells[key])
        if number is None:
            appends.append([cells.get(name, "") for name in header])
            continue
        current = list(values[number - 1]) + [""] * (len(header) - len(values[number - 1]))
        merged = list(current)
        for name, value in cells.items():
            if value != "":
                merged[col[name]] = value
        if merged == current:
            result.unchanged += 1
        else:
            last = column_letter(len(header) - 1)
            updates.append({"range": f"A{number}:{last}{number}", "values": [merged]})
    if updates:
        worksheet.batch_update(updates)
    if appends:
        worksheet.append_rows(appends, value_input_option="RAW")
    result.updated, result.inserted = len(updates), len(appends)
    return result


def open_worksheet(spreadsheet_id: str, title: str):
    """Open (or create) a worksheet with the service account in GOOGLE_SERVICE_ACCOUNT_JSON."""
    import gspread

    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not raw:
        raise RuntimeError("set GOOGLE_SERVICE_ACCOUNT_JSON to the service account's JSON key")
    client = gspread.service_account_from_dict(json.loads(raw))
    spreadsheet = client.open_by_key(spreadsheet_id)
    try:
        return spreadsheet.worksheet(title)
    except gspread.WorksheetNotFound:
        return spreadsheet.add_worksheet(title=title, rows=1000, cols=30)
