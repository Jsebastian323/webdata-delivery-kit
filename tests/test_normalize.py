from decimal import Decimal

import pytest

from wdk.normalize import (
    clean_text,
    first_int,
    fold,
    html_to_text,
    parse_money,
    strip_quote_marks,
    word_to_int,
)


@pytest.mark.parametrize(
    ("raw", "sep", "expected"),
    [
        ("£51.77", ".", Decimal("51.77")),
        ("$1,234.50", ".", Decimal("1234.50")),
        ("$ 1.234.567,89", ",", Decimal("1234567.89")),
        ("COP 25.000", ",", Decimal("25000")),
    ],
)
def test_parse_money(raw, sep, expected):
    assert parse_money(raw, decimal_sep=sep) == expected


def test_parse_money_rejects_text_without_digits():
    with pytest.raises(ValueError):
        parse_money("free")


def test_first_int():
    assert first_int("In stock (22 available)") == 22
    assert first_int("1,000 results") == 1000
    with pytest.raises(ValueError):
        first_int("Out of stock")


def test_word_to_int():
    assert word_to_int("Three") == 3
    with pytest.raises(ValueError):
        word_to_int("Six")


def test_clean_text_normalizes_unicode_and_whitespace():
    decomposed = "Bogotá  D.C.\n"
    assert clean_text(decomposed) == "Bogotá D.C."


def test_fold_ignores_case_and_accents():
    assert fold("BOGOTÁ") == fold("bogota")


def test_strip_quote_marks():
    assert strip_quote_marks("“A day without sunshine is like, you know, night.”") == (
        "A day without sunshine is like, you know, night."
    )


def test_html_to_text_keeps_block_structure():
    html = "<div><h2>About</h2><p>Line one<br>line two</p><ul><li>a</li><li>b</li></ul></div>"
    assert html_to_text(html) == "About\nLine one\nline two\na\nb"
