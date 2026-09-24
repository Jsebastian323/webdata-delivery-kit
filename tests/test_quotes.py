from wdk.cases.quotes import (
    BASE_URL,
    Quote,
    Strategy,
    StrategyResult,
    consistency_check,
    parse_api_page,
    parse_embedded_json,
    parse_quote_divs,
    parse_search_form,
    parse_search_results,
    parse_tableful,
)

EINSTEIN = (
    "The world as we have created it is a process of our thinking. "
    "It cannot be changed without changing our thinking."
)


def _as_index(rows):
    return {(r["author"], r["text"]): tuple(r["tags"]) for r in rows}


def test_server_rendered_page(fixture_text):
    rows, next_url = parse_quote_divs(fixture_text("quotes_page1.html"), BASE_URL + "/")
    assert len(rows) == 10
    assert rows[0] == {"text": EINSTEIN, "author": "Albert Einstein",
                       "tags": ["change", "deep-thoughts", "thinking", "world"]}
    assert next_url == BASE_URL + "/page/2/"


def test_embedded_json_matches_rendered_html(fixture_text):
    html_rows, _ = parse_quote_divs(fixture_text("quotes_page1.html"), BASE_URL + "/")
    js_rows, next_url = parse_embedded_json(fixture_text("quotes_js_page1.html"), BASE_URL + "/js/")
    assert _as_index(js_rows) == _as_index(html_rows)
    assert next_url == BASE_URL + "/js/page/2/"


def test_delayed_page_ships_the_same_data_without_waiting(fixture_text):
    rows, _ = parse_embedded_json(fixture_text("quotes_js_delayed_page1.html"), BASE_URL + "/js-delayed/")
    assert len(rows) == 10 and rows[0]["author"] == "Albert Einstein"


def test_api_page(fixture_json):
    rows, has_next = parse_api_page(fixture_json("quotes_api_page1.json"))
    assert len(rows) == 10 and has_next
    assert rows[0]["text"] == EINSTEIN


def test_tableful_pairs_quote_and_tag_rows(fixture_text):
    html_rows, _ = parse_quote_divs(fixture_text("quotes_page1.html"), BASE_URL + "/")
    rows, next_url = parse_tableful(fixture_text("quotes_tableful_page1.html"), BASE_URL + "/tableful/")
    assert _as_index(rows) == _as_index(html_rows)
    assert next_url == BASE_URL + "/tableful/page/2/"


def test_viewstate_form_and_postback(fixture_text):
    form = parse_search_form(fixture_text("quotes_search.html"))
    assert form.viewstate and len(form.authors) == 50 - 1 and form.tags == []
    after_author = parse_search_form(fixture_text("quotes_search_author.html"))
    assert "inspirational" in after_author.tags
    assert after_author.viewstate != form.viewstate


def test_viewstate_results_show_only_the_searched_tag(fixture_text):
    results = parse_search_results(fixture_text("quotes_search_results.html"))
    assert results
    assert all(author == "Albert Einstein" and tag == "inspirational" for _, author, tag in results)


def test_quote_model_sorts_and_dedupes_tags():
    quote = Quote(text="x", author="y", tags=("b", "a", "b", " "))
    assert quote.tags == ("a", "b")


def _result(rows, error=None):
    return StrategyResult(Strategy("s", "m", "t", fn=None), rows=rows, error=error)


BASELINE = [
    {"text": "one", "author": "A", "tags": ["x"]},
    {"text": "two", "author": "B", "tags": []},
]


def test_consistency_passes_on_identical_data():
    assert consistency_check(BASELINE, _result(list(BASELINE))).passed


def test_consistency_catches_missing_extra_and_tag_drift():
    drifted = [{"text": "one", "author": "A", "tags": ["y"]}, {"text": "three", "author": "C", "tags": []}]
    check = consistency_check(BASELINE, _result(drifted))
    assert not check.passed
    assert "missing: 1" in check.detail and "extra: 1" in check.detail and "tag mismatch: 1" in check.detail


def test_consistency_accepts_gaps_that_are_explained():
    only_tagged = [BASELINE[0]]
    unreachable = frozenset({("B", "two")})
    check = consistency_check(BASELINE, _result(only_tagged), expected_missing=unreachable)
    assert check.passed and "unreachable by design" in check.detail


def test_consistency_flags_duplicates_and_failures():
    assert not consistency_check(BASELINE, _result(BASELINE + BASELINE[:1])).passed
    assert not consistency_check(BASELINE, _result([], error="Blocked: 403")).passed
