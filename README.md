# webdata-delivery-kit

[![ci](https://github.com/Jsebastian323/webdata-delivery-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Jsebastian323/webdata-delivery-kit/actions/workflows/ci.yml)
[![jobs-tracker](https://github.com/Jsebastian323/webdata-delivery-kit/actions/workflows/jobs-tracker.yml/badge.svg)](https://github.com/Jsebastian323/webdata-delivery-kit/actions/workflows/jobs-tracker.yml)

**From a scraping brief to a validated, delivery-ready dataset.**

A small Python toolkit (async `httpx`, BeautifulSoup, Playwright, Pydantic) and three worked cases.
Every run ends in a QA gate: the dataset ships only when its report says **READY**. The gate
checks the schema, unique keys, coverage against the totals the source itself declares,
selector drift, cross-source consistency and fill rates.

How I approach a brief, step by step: [PLAYBOOK.md](PLAYBOOK.md).

## Results from real runs (2026-09-24)

| Case | What it demonstrates | Delivered | Requests | Time | QA |
|---|---|---|---|---|---|
| [1. Books to Scrape](#case-1-books-to-scrape) | hierarchy traversal, pagination, normalization, coverage against declared totals | 1,000 / 1,000 books | 1,081 | 136 s | READY |
| [2. Quotes to Scrape](#case-2-quotes-to-scrape) | 9 strategies over 7 page mechanics return the same dataset | 100 quotes | 332 + 88 browser | 59 s | READY |
| [3. Remote-jobs tracker](#case-3-remote-jobs-tracker) | 3 job-board APIs, 8 companies, repost dedup, evidence-backed requirements, daily diff | 426 postings, 324 families | 8 | 3 s | READY |

All runs: 0 retries, 0 failed requests, robots.txt honored, at most 8 requests/s per host.

## What the QA gate caught while building this

These are the useful part: each one would have shipped a wrong dataset without the gate.

- **A source that repeats itself.** Workable's public widget API returns one entry per location:
  448 entries for 92 real postings. The *unique key* check failed the first run of case 3, and
  the adapter now merges entries by shortcode.
- **A browser helper that quit early.** The first infinite-scroll implementation waited for
  Playwright's `networkidle`, which only describes the initial page load. It stopped at 50 of
  100 quotes. The *cross-source* check against the plain-HTML baseline failed it, and the helper
  now waits for the item count to grow.
- **A gap that is structural, not a bug.** The ViewState search form needs a tag, so it can never
  return the 3 quotes that have none. The check knows that gap and reports it
  ("3 untagged quotes unreachable by design") instead of failing or hiding it.

## Case 1: Books to Scrape

Brief: every book on [books.toscrape.com](https://books.toscrape.com) with UPC, title, category,
prices (GBP), stock, rating, reviews, description and image. CSV + JSON Lines, nothing missing.

- Home page → 50 categories → paginated listings (80 pages) → 1,000 book pages.
- Lenient parsing, strict validation: prices must add up (`excl. tax + tax = price`), ratings
  are 1-5, UPCs are 16 hex chars. A page with a changed layout fails validation with the
  exact field name instead of crashing the run.
- Checks the site makes possible: 1,000/1,000 against the home page's "1000 results", each
  category against its own declared count, 20 items on every listing page but the last
  (selector drift), and the listing category matching the book page breadcrumb.
- Resumable: `wdk books --resume` continues from an append-only checkpoint after a crash.

[`src/wdk/cases/books.py`](src/wdk/cases/books.py)

## Case 2: Quotes to Scrape

[quotes.toscrape.com](https://quotes.toscrape.com) serves the same 100 quotes through very
different mechanics. The brief is one dataset (text, author, tags); every strategy must return
it exactly, and the QA report compares each one against the baseline.

| Strategy | Page mechanic | Technique | Quotes | Requests | Seconds | Matches |
|---|---|---|---|---|---|---|
| html-pagination | server-rendered HTML, 10 pages | BeautifulSoup, follow the Next link | 100 | 10 | 2.0 | baseline |
| js-embedded-json | content written by JavaScript | read the JSON array in the page source | 100 | 10 | 1.6 | yes |
| js-delayed-embedded-json | JavaScript renders after a 10 s timer | same embedded JSON: the timer never has to be waited out | 100 | 10 | 1.7 | yes |
| scroll-api | infinite scroll | call the JSON endpoint the scroll handler calls | 100 | 10 | 1.7 | yes |
| tableful | table layout, author glued to the quote, tags in the next row | pair rows by content pattern, not position | 100 | 10 | 1.7 | yes |
| viewstate-search | ASP.NET-style form: author posts back, then tag, with `__VIEWSTATE` | replay the postbacks with httpx, union the tags per quote | 97 | 270 | 34.2 | yes (3 unreachable by design) |
| login-session | login with a CSRF token | session cookie + hidden token, verify every page | 100 | 12 | 2.0 | yes |
| browser-js | content written by JavaScript | Playwright render | 100 | 70 | 7.1 | yes |
| browser-scroll | infinite scroll | Playwright scroll to the end + capture the XHR JSON | 100 | 18 | 7.1 | yes |

The lesson in numbers: the browser render of `/js` made 7x the requests of reading the JSON
already in the page source, for the same data. The browser runs here only to prove the
shortcuts right.

[`src/wdk/cases/quotes.py`](src/wdk/cases/quotes.py)

## Case 3: Remote-jobs tracker

A real-world case: postings from AI-data companies (Mindrift/Toloka, Scale AI, Turing,
Invisible, Labelbox, Handshake, RWS TrainAI, Hugging Face) through the public endpoints
Workable, Greenhouse and Lever expose for embedding job listings. One request per board.

- **One schema for three APIs**: title, location, ISO countries, remote, published date.
- **Open to Colombia?** `true` when Colombia or a LatAm/worldwide-remote scope is named, `false`
  when only other countries are, `null` when the posting does not say. Today: 10 yes, 11 unclear.
- **Families**: regional reposts are grouped. Mindrift's *Senior Python Data Scraping Engineer*
  is one family of 31 postings.
- **Requirements with evidence**: minimum years of experience, English level, hourly pay,
  annual salary and weekly hours, each stored with the exact sentence that states it. Rules
  run first; regional reposts share descriptions, so 426 postings need only 345 extractions.
  An optional LLM fallback through [OpenRouter](https://openrouter.ai) asks only about fields the
  rules missed *and* the text hints at, within a call budget; a value is kept only if its
  evidence is a literal passage of the posting and contains the value.
- **Change tracking**: a scheduled GitHub Action runs daily and commits `data/jobs/`, so the git
  history is the change log (new, closed and changed postings in
  [`data/jobs/CHANGELOG.md`](data/jobs/CHANGELOG.md)).
- **Reliability rules**: a board that fails is carried over and flagged, never reported as
  "everything closed"; a board that suddenly drops to zero blocks the run; a NOT READY run
  never overwrites the published snapshot.
- Optional Google Sheets output with an idempotent upsert: rows matched by key, columns by
  header name, and an empty value never erases a cell someone filled by hand.

[`src/wdk/cases/jobs/`](src/wdk/cases/jobs/)

## How it fits together

```
brief ──► Pydantic model + DeliverySpec (key, expected count, fill minimums)
                                   │
fetch.py ──► parsers ──► rows ──► quality.py ──► READY? ──► export.py / sheets.py
robots.txt   pure functions,     schema · unique key          CSV · JSON Lines · JSON
pacing       tested on saved     coverage · page yield        Google Sheets
retries      pages               cross-source · fill rates    + qa_report.md
block stop
```

| Module | Responsibility |
|---|---|
| [`fetch.py`](src/wdk/fetch.py) | async client: robots.txt (incl. Crawl-delay), per-host rate limit, retries with backoff + jitter, `Retry-After`, challenge pages stop the run, proxy via `WDK_PROXY` |
| [`browser.py`](src/wdk/browser.py) | Playwright page + infinite-scroll helper (imported only when needed) |
| [`normalize.py`](src/wdk/normalize.py) | strict text, money, number and HTML normalizers |
| [`quality.py`](src/wdk/quality.py) | delivery spec, QA checks, READY / NOT READY report |
| [`export.py`](src/wdk/export.py) · [`sheets.py`](src/wdk/sheets.py) | CSV, JSON Lines, JSON, append-only checkpoint · Google Sheets upsert |
| [`llm.py`](src/wdk/llm.py) | OpenRouter structured extraction with verbatim-evidence guard |

## Run it

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
playwright install chromium        # only for the browser strategies of case 2

wdk books                          # data/books/books.csv, books.jsonl, qa_report.md
wdk quotes                         # add --no-browser to skip Playwright
wdk jobs                           # set OPENROUTER_API_KEY to enable the LLM fallback
pytest                             # offline: saved pages and API payloads
pytest -m live                     # smoke tests against the real sites
```

The exit code is 0 when the report says READY and 2 when it does not, so schedulers and CI notice.

With Docker (the image includes Chromium):

```bash
docker build -t wdk .
docker run --rm -v "$PWD/data:/app/data" wdk quotes
```

Environment variables: `WDK_PROXY` (proxy URL), `OPENROUTER_API_KEY`, `WDK_LLM_MODEL`
(default `anthropic/claude-haiku-4.5`), `WDK_LLM_MAX_CALLS` (default 40),
`GOOGLE_SERVICE_ACCOUNT_JSON` (for `--sheet`).

CSV convention: list values are joined with `|`; the evidence map is written as JSON.

## Responsible scraping

- robots.txt is honored, `Crawl-delay` included, and the user agent names this repo.
- Requests are rate-limited per host even when the site would tolerate more.
- No CAPTCHA solving and no bot-detection evasion: a challenge page raises `Blocked` and the
  run stops. The proxy setting exists for geo-restricted sources, not for getting around blocks.
- Cases 1 and 2 use [toscrape.com](https://toscrape.com), sandboxes built for scraping practice.
  Case 3 uses public job-board endpoints meant for embedding listings, one request per board per day.

## License

[MIT](LICENSE)
