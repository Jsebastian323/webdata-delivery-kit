from pydantic import BaseModel, Field

from wdk.quality import Check, DeliverySpec, build_report, page_yield_check


class Item(BaseModel):
    sku: str = Field(min_length=1)
    price: float = Field(ge=0)
    note: str | None = None


SPEC = DeliverySpec(name="items", model=Item, key=("sku",), expected_count=3, min_fill={"note": 0.5})


def test_clean_dataset_is_ready():
    rows = [
        {"sku": "a", "price": 1, "note": "x"},
        {"sku": "b", "price": 2, "note": "y"},
        {"sku": "c", "price": 3},
    ]
    delivered, report = build_report(SPEC, rows)
    assert report.ready
    assert len(delivered) == 3
    assert report.fill_rates["note"] == 2 / 3


def test_invalid_rows_block_delivery_and_are_listed():
    rows = [{"sku": "a", "price": -1}, {"sku": "b", "price": 2}, {"sku": "c", "price": 3}]
    delivered, report = build_report(SPEC, rows)
    assert not report.ready
    assert [e.key for e in report.errors] == ["a"]
    assert "price" in report.errors[0].errors[0]
    assert len(delivered) == 2


def test_duplicates_are_dropped_and_flagged():
    rows = [{"sku": "a", "price": 1}, {"sku": "a", "price": 1}, {"sku": "b", "price": 2}]
    delivered, report = build_report(DeliverySpec("items", Item, ("sku",)), rows)
    assert [d.sku for d in delivered] == ["a", "b"]
    assert not next(c for c in report.checks if c.name == "unique key").passed


def test_coverage_shortfall_blocks_delivery():
    rows = [{"sku": "a", "price": 1, "note": "x"}]
    _, report = build_report(SPEC, rows)
    coverage = next(c for c in report.checks if c.name == "coverage")
    assert not coverage.passed and "1/3" in coverage.detail
    assert report.verdict == "NOT READY"


def test_non_blocking_checks_only_warn():
    rows = [{"sku": "a", "price": 1, "note": "x"}, {"sku": "b", "price": 1, "note": "x"},
            {"sku": "c", "price": 1, "note": "x"}]
    _, report = build_report(SPEC, rows, extra_checks=[Check("advisory", False, blocking=False)])
    assert report.ready
    assert "| advisory | WARN |" in report.to_markdown()


def test_page_yield_catches_silent_selector_breakage():
    assert page_yield_check("yield", {"cat": [20, 20, 7]}, 20).passed
    assert not page_yield_check("yield", {"cat": [20, 0, 7]}, 20).passed
    assert not page_yield_check("yield", {"cat": [20, 20, 0]}, 20).passed
