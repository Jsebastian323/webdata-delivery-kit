import asyncio
import datetime as dt
import json

import httpx
import pytest

from wdk.cases.jobs import pipeline
from wdk.cases.jobs.enrich import passages, rules
from wdk.cases.jobs.pipeline import build_families, diff_snapshots, family_id
from wdk.cases.jobs.sources import (
    Board,
    countries_in,
    greenhouse_postings,
    lever_postings,
    open_to_colombia,
    workable_postings,
)

MINDRIFT = Board("Mindrift (Toloka)", "workable", "toloka-ai")
TURING = Board("Turing", "greenhouse", "turing")
RWS = Board("RWS (TrainAI)", "lever", "rws")


def test_workable_merges_the_per_location_copies(fixture_json):
    postings = workable_postings(MINDRIFT, fixture_json("workable_widget.json"))
    assert len(postings) == 2  # 8 entries in the payload, 2 real postings
    latam = next(p for p in postings if p["posting_id"] == "A22D741557")
    assert latam["countries"] == ["AR", "BR", "CL", "CO", "MX", "PE"]
    assert latam["open_to_colombia"] is True and latam["remote"] is True
    assert latam["published"] == dt.date(2026, 9, 18)
    assert latam["key"] == "workable:toloka-ai:A22D741557"


def test_greenhouse_unescapes_content_and_reads_locations(fixture_json):
    first, second = greenhouse_postings(TURING, fixture_json("greenhouse_board.json"))
    assert first["countries"] == ["BR", "CO"] and first["open_to_colombia"] is True
    assert second["countries"] == ["US"] and second["open_to_colombia"] is False
    assert "&lt;" not in first["description"] and "<div" not in first["description"]


def test_lever_postings(fixture_json):
    first, second = lever_postings(RWS, fixture_json("lever_board.json"))
    assert first["countries"] == ["US"] and first["remote"] is True
    assert second["countries"] == ["SA"]
    assert isinstance(first["published"], dt.date)
    assert len(first["description"]) > 200


@pytest.mark.parametrize(
    ("location", "expected"),
    [
        ("Bogotá, Colombia", {"CO"}),
        ("San Francisco; New York, NY", {"US"}),
        ("Remote - LATAM", set()),
        ("Colombia, Huila, Colombia; São Paulo, Brazil", {"BR", "CO"}),
    ],
)
def test_countries_in(location, expected):
    assert countries_in(location) == expected


def test_open_to_colombia():
    assert open_to_colombia({"CO", "BR"}, "Bogotá; São Paulo", True) is True
    assert open_to_colombia(set(), "Remote - LATAM", True) is True
    assert open_to_colombia(set(), "Global - Remote", True) is True
    assert open_to_colombia({"US"}, "Remote - US", True) is False
    assert open_to_colombia(set(), "Remote", True) is None


def test_rules_on_a_real_posting(fixture_json):
    job = fixture_json("workable_widget.json")["jobs"][0]
    text = workable_postings(MINDRIFT, {"jobs": [job]})[0]["description"]
    found = rules(text)
    assert found.values == {"min_years": 5, "english_level": "B2", "pay_usd_hour_max": 25.0,
                            "hours_per_week": "10-20"}
    assert all(passage in passages(text) for passage in found.evidence.values())


def test_rules_keep_the_binding_requirement():
    text = "3+ years of Python experience.\nAt least 5+ years of relevant experience in data engineering."
    assert rules(text).values["min_years"] == 5


def test_rules_read_ranges_and_salaries():
    found = rules("3-5 years of professional experience.\nThe range is $120k - $150k per year.")
    assert found.values["min_years"] == 3
    assert found.values["pay_usd_year_max"] == 150000
    assert rules("between $65,000- $70,000 per year").values["pay_usd_year_max"] == 70000


def test_rules_ignore_numbers_without_context():
    assert rules("Founded 12 years ago, we have 300 employees.").values == {}


def _posting(key, title="Data Engineer", countries=("US",), open_co=False, sha="a" * 40, **extra):
    return {"key": key, "company": "Acme", "title": title, "countries": list(countries),
            "open_to_colombia": open_co, "location": ", ".join(countries), "description_sha1": sha,
            "family_id": family_id("Acme", title), "published": "2026-09-01", "min_years": None,
            "english_level": None, "pay_usd_hour_max": None, "pay_usd_year_max": None,
            "url": "https://example.test/" + key, **extra}


def test_families_group_regional_reposts():
    families = build_families([
        _posting("a:1", countries=("US",), pay_usd_hour_max=40.0),
        _posting("a:2", countries=("CO", "MX"), open_co=True, pay_usd_hour_max=25.0),
        _posting("a:3", title="Designer"),
    ])
    engineer = next(f for f in families if f["title"] == "Data Engineer")
    assert engineer["postings"] == 2 and engineer["countries"] == ["CO", "MX", "US"]
    assert engineer["open_to_colombia"] is True and engineer["pay_usd_hour_max"] == 40.0
    assert engineer["url"] == "https://example.test/a:2"  # links the posting you can apply to


def test_diff_snapshots():
    before = {"a:1": _posting("a:1"), "a:2": _posting("a:2")}
    now = {"a:2": _posting("a:2", sha="b" * 40), "a:3": _posting("a:3")}
    diff = diff_snapshots(before, now)
    assert [p["key"] for p in diff.new] == ["a:3"]
    assert [p["key"] for p in diff.closed] == ["a:1"]
    assert [p["key"] for p in diff.changed] == ["a:2"]


# -- end to end, offline: saved API payloads replayed through a mock transport ---------------------


def _boards_file(tmp_path):
    path = tmp_path / "companies.json"
    path.write_text(json.dumps([
        {"company": "Mindrift (Toloka)", "source": "workable", "board": "toloka-ai"},
        {"company": "Turing", "source": "greenhouse", "board": "turing"},
        {"company": "RWS (TrainAI)", "source": "lever", "board": "rws"},
    ]), encoding="utf-8")
    return path


def _transport(fixture_json, *, lever_status=200, greenhouse_jobs=None, workable_jobs=None):
    workable = fixture_json("workable_widget.json")
    if workable_jobs is not None:
        workable["jobs"] = workable_jobs
    greenhouse = fixture_json("greenhouse_board.json")
    if greenhouse_jobs is not None:
        greenhouse["jobs"] = greenhouse_jobs

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(404)
        if request.url.host == "apply.workable.com":
            return httpx.Response(200, json=workable)
        if request.url.host == "boards-api.greenhouse.io":
            return httpx.Response(200, json=greenhouse)
        if lever_status != 200:
            return httpx.Response(lever_status)
        return httpx.Response(200, json=fixture_json("lever_board.json"))

    return httpx.MockTransport(handler)


def _run(tmp_path, transport, day):
    return asyncio.run(pipeline.run(
        tmp_path / "out", companies_path=_boards_file(tmp_path), use_llm=False, rate=0,
        transport=transport, today=day,
    ))


def _snapshot_keys(tmp_path):
    data = json.loads((tmp_path / "out" / "postings.json").read_text(encoding="utf-8"))
    return {p["key"] for p in data["postings"]}


def test_pipeline_first_run_publishes_a_snapshot(tmp_path, fixture_json):
    report = _run(tmp_path, _transport(fixture_json), dt.date(2026, 9, 24))
    assert report.ready
    assert len(_snapshot_keys(tmp_path)) == 6
    changelog = (tmp_path / "out" / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "2026-09-24 · first snapshot: 6 postings" in changelog


def test_failed_board_is_carried_over_not_closed(tmp_path, fixture_json):
    _run(tmp_path, _transport(fixture_json), dt.date(2026, 9, 24))
    report = _run(tmp_path, _transport(fixture_json, lever_status=404), dt.date(2026, 9, 25))
    assert report.ready  # a warning, not a block
    assert next(c for c in report.checks if c.name == "every board answered").status == "WARN"
    assert len(_snapshot_keys(tmp_path)) == 6
    changelog = (tmp_path / "out" / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "2026-09-25 · 6 postings · +0 new · -0 closed" in changelog


def test_board_that_goes_silent_blocks_and_keeps_the_snapshot(tmp_path, fixture_json, monkeypatch):
    monkeypatch.setattr(pipeline, "SILENT_BOARD_MIN", 1)
    _run(tmp_path, _transport(fixture_json), dt.date(2026, 9, 24))
    before = (tmp_path / "out" / "postings.json").read_text(encoding="utf-8")
    report = _run(tmp_path, _transport(fixture_json, greenhouse_jobs=[]), dt.date(2026, 9, 25))
    assert not report.ready
    assert (tmp_path / "out" / "postings.json").read_text(encoding="utf-8") == before


def test_closed_posting_lands_in_the_changelog(tmp_path, fixture_json):
    _run(tmp_path, _transport(fixture_json), dt.date(2026, 9, 24))
    latam_only = [j for j in fixture_json("workable_widget.json")["jobs"] if j["shortcode"] == "A22D741557"]
    report = _run(tmp_path, _transport(fixture_json, workable_jobs=latam_only), dt.date(2026, 9, 25))
    assert report.ready
    changelog = (tmp_path / "out" / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "-1 closed" in changelog and "Freelance Brand Designer" in changelog
