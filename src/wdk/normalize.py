"""Strict normalizers: each returns a clean value or raises ValueError.

A value that cannot be parsed should fail validation loudly, not slip into a delivery as a
best guess.
"""

from __future__ import annotations

import re
import unicodedata
from decimal import Decimal, InvalidOperation

from bs4 import BeautifulSoup

_WHITESPACE = re.compile(r"\s+")
_QUOTE_MARKS = "\"'“”‘’«»"
_WORD_NUMBERS = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5}


def clean_text(value: str | None) -> str:
    """NFC-normalize, collapse every run of whitespace (incl. non-breaking spaces) and trim."""
    if value is None:
        return ""
    return _WHITESPACE.sub(" ", unicodedata.normalize("NFC", value)).strip()


def strip_quote_marks(value: str) -> str:
    """'“The world as we have created it…”' -> 'The world as we have created it…'."""
    return clean_text(value).strip(_QUOTE_MARKS).strip()


def fold(value: str) -> str:
    """Case- and accent-insensitive form for matching ('Bogotá' and 'BOGOTA' fold the same)."""
    decomposed = unicodedata.normalize("NFKD", clean_text(value))
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch)).casefold()


def parse_money(value: str, decimal_sep: str = ".") -> Decimal:
    """Parse an amount written with any currency symbol.

    >>> parse_money("£51.77")
    Decimal('51.77')
    >>> parse_money("$ 1.234.567,89", decimal_sep=",")
    Decimal('1234567.89')
    """
    digits = re.sub(r"[^\d.,-]", "", value or "")
    if not re.search(r"\d", digits):
        raise ValueError(f"no amount in {value!r}")
    thousands = "," if decimal_sep == "." else "."
    digits = digits.replace(thousands, "").replace(decimal_sep, ".")
    try:
        return Decimal(digits)
    except InvalidOperation as exc:
        raise ValueError(f"unparseable amount {value!r}") from exc


def first_int(value: str) -> int:
    """'In stock (22 available)' -> 22; '1,000 results' -> 1000."""
    match = re.search(r"\d[\d,]*", value or "")
    if not match:
        raise ValueError(f"no integer in {value!r}")
    return int(match.group().replace(",", ""))


def word_to_int(word: str) -> int:
    """'Three' -> 3 (star ratings are spelled out in class names)."""
    try:
        return _WORD_NUMBERS[word.strip().lower()]
    except KeyError:
        raise ValueError(f"not a number word: {word!r}") from None


def html_to_text(html: str) -> str:
    """Readable plain text from an HTML fragment: block elements become line breaks."""
    soup = BeautifulSoup(html or "", "lxml")
    for br in soup.find_all("br"):
        br.replace_with("\n")
    lines = (clean_text(line) for line in soup.get_text("\n").splitlines())
    return "\n".join(line for line in lines if line)
