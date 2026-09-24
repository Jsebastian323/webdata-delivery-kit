"""Smoke tests against the real sites. Skipped by default; run with ``pytest -m live``."""

import asyncio

import pytest

from wdk.cases import books, quotes
from wdk.cases.jobs import pipeline

pytestmark = pytest.mark.live


def test_books_partial_run_is_ready(tmp_path):
    report = asyncio.run(books.run(tmp_path, max_categories=2))
    assert report.ready, report.to_markdown()
    assert (tmp_path / "books.csv").exists()


def test_quotes_http_strategies_agree(tmp_path):
    report = asyncio.run(quotes.run(tmp_path, use_browser=False))
    assert report.ready, report.to_markdown()
    assert report.rows_delivered == 100


def test_jobs_tracker_runs(tmp_path):
    report = asyncio.run(pipeline.run(tmp_path, use_llm=False))
    assert report.ready, report.to_markdown()
    assert (tmp_path / "postings.json").exists()
