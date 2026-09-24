"""Command line entry point: ``wdk books | quotes | jobs``.

Exit code 0 means the QA gate said READY, 2 means NOT READY, 3 means a site showed an
anti-bot challenge and the run stopped (so schedulers and CI notice).
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from pathlib import Path

from .fetch import Blocked


def _common(parser: argparse.ArgumentParser, default_out: str) -> None:
    parser.add_argument("--out", type=Path, default=Path(default_out), help="output folder")
    parser.add_argument("--rate", type=float, default=8.0, help="max requests per second per host")
    parser.add_argument("--concurrency", type=int, default=8, help="max requests in flight")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wdk", description=__doc__.splitlines()[0])
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="case", required=True)

    books = sub.add_parser("books", help="case 1: full catalogue of books.toscrape.com")
    _common(books, "data/books")
    books.add_argument("--resume", action="store_true", help="continue from the last checkpoint")
    books.add_argument("--max-categories", type=int, help="partial run, for quick checks")

    quotes = sub.add_parser("quotes", help="case 2: one dataset behind eight page mechanics")
    _common(quotes, "data/quotes")
    quotes.add_argument("--no-browser", action="store_true", help="skip the Playwright strategies")

    jobs = sub.add_parser("jobs", help="case 3: remote-jobs tracker over public job-board APIs")
    _common(jobs, "data/jobs")
    jobs.add_argument("--companies", type=Path, help="JSON list of boards (default: bundled list)")
    jobs.add_argument("--sheet", help="Google Sheet ID to upsert into (needs GOOGLE_SERVICE_ACCOUNT_JSON)")
    jobs.add_argument("--no-llm", action="store_true", help="deterministic extraction only")
    return parser


async def _dispatch(args: argparse.Namespace):
    if args.case == "books":
        from .cases import books

        return await books.run(
            args.out, rate=args.rate, concurrency=args.concurrency,
            resume=args.resume, max_categories=args.max_categories,
        )
    if args.case == "quotes":
        from .cases import quotes

        return await quotes.run(
            args.out, rate=args.rate, concurrency=args.concurrency, use_browser=not args.no_browser
        )
    from .cases.jobs import pipeline

    return await pipeline.run(
        args.out, rate=args.rate, concurrency=args.concurrency,
        companies_path=args.companies, sheet_id=args.sheet, use_llm=not args.no_llm,
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    try:
        report = asyncio.run(_dispatch(args))
    except Blocked as exc:
        print(
            f"\nSTOPPED: {exc}\nThe site answered with an anti-bot challenge. The kit does not try "
            "to get around it: slow down, check the terms, or ask for access.",
            file=sys.stderr,
        )
        return 3
    print(f"\n{report.spec}: {report.verdict} - {report.rows_delivered} rows -> {args.out / 'qa_report.md'}")
    return 0 if report.ready else 2


if __name__ == "__main__":
    sys.exit(main())
