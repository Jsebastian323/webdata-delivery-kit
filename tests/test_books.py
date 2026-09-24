from decimal import Decimal

import pytest
from pydantic import ValidationError

from wdk.cases.books import BASE_URL, Book, parse_book, parse_home, parse_listing

CATEGORY_URL = BASE_URL + "catalogue/category/books/mystery_3/index.html"
BOOK_URL = BASE_URL + "catalogue/a-light-in-the-attic_1000/index.html"


def test_home_declares_total_and_lists_categories(fixture_text):
    declared, categories = parse_home(fixture_text("books_home.html"))
    assert declared == 1000
    assert len(categories) == 50
    assert categories[0] == ("Travel", BASE_URL + "catalogue/category/books/travel_2/index.html")


def test_listing_page_yields_books_and_next_link(fixture_text):
    listing = parse_listing(fixture_text("books_category.html"), CATEGORY_URL)
    assert len(listing.book_urls) == 20
    assert listing.declared_total == 32
    assert listing.next_url == BASE_URL + "catalogue/category/books/mystery_3/page-2.html"
    assert all(u.startswith(BASE_URL + "catalogue/") for u in listing.book_urls)


def test_last_listing_page_has_no_next(fixture_text):
    url = BASE_URL + "catalogue/category/books/mystery_3/page-2.html"
    listing = parse_listing(fixture_text("books_category_last.html"), url)
    assert listing.next_url is None
    assert len(listing.book_urls) == 12


def test_book_page_parses_and_validates(fixture_text):
    book = Book.model_validate(parse_book(fixture_text("books_detail.html"), BOOK_URL))
    assert book.upc == "a897fe39b1053632"
    assert book.title == "A Light in the Attic"
    assert book.category == "Poetry"
    assert book.price_gbp == Decimal("51.77")
    assert book.in_stock == 22
    assert book.rating == 3
    assert book.reviews == 0
    assert book.description.startswith("It's hard to imagine a world without A Light in the Attic")
    assert str(book.image_url).startswith(BASE_URL + "media/cache/")


def test_changed_markup_fails_validation_with_the_field_name(fixture_text):
    html = fixture_text("books_detail.html").replace("star-rating Three", "star-rating")
    with pytest.raises(ValidationError) as info:
        Book.model_validate(parse_book(html, BOOK_URL))
    assert info.value.errors()[0]["loc"] == ("rating",)


def test_prices_must_add_up(fixture_text):
    row = parse_book(fixture_text("books_detail.html"), BOOK_URL)
    row["tax_gbp"] = Decimal("1.00")
    with pytest.raises(ValidationError, match="price_excl_tax_gbp"):
        Book.model_validate(row)
