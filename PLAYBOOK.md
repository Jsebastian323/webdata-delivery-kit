# Playbook: from a scraping brief to a delivered dataset

How I work a data-extraction task, in order. The three cases in this repo follow it end to end.

## 1. Pin down the brief before writing a crawler

- Which fields, in which format (CSV, JSON, Google Sheets), with which types and allowed values.
- What "complete" means: every item the site lists? A declared total? A date range?
- Write it as code first: a Pydantic model (the row) and a `DeliverySpec` (key, expected count,
  minimum fill rates). If the brief can't be written down that way, it isn't clear yet: ask.

## 2. Recon (15 minutes that save hours)

- **robots.txt and terms of service.** If the data is off limits, say so and propose an alternative
  (official API, data provider, the client's own export).
- **Page source.** Search it for a value you can see on screen. Many "JavaScript pages" ship
  their data as a JSON blob in a `<script>` (case 2: `/js`, `/js-delayed`).
- **Network tab.** Scroll, click "next", filter by Fetch/XHR. Infinite scroll and search boxes
  usually call a JSON endpoint you can page through directly (case 2: `/api/quotes`).
- **Totals.** Does the site declare how many items exist ("1000 results")? That number becomes
  the coverage check.
- **Forms and state.** ViewState, CSRF tokens, dependent selects: replay the requests with a
  session before reaching for a browser (case 2: `search.aspx`, `login`).

## 3. Pick the cheapest strategy that is reliable

Public API > JSON embedded in the page > static HTML > headless browser. The browser is the
most expensive and the most fragile option. Case 2 measures it: the Playwright render of `/js`
made 7x the requests of reading the embedded JSON, for the same 100 quotes.

## 4. Build

- **Lenient parsers, strict models.** A parser returns `None` for what it cannot read. The model
  rejects the row and the QA report names the field. One odd page never crashes a 1,000-page run.
- **Parse functions are pure** and tested against saved pages, so tests run offline and fast.
- **One polite fetcher**: robots.txt (incl. `Crawl-delay`), per-host rate limit, retries with
  backoff and jitter, `Retry-After` honored, a challenge page stops the run.
- **Checkpoint long runs** so a crash resumes instead of starting over.

## 5. Verify before delivery: the QA gate

Nothing ships unless the report says READY:

- every row validates against the model, and no key repeats;
- coverage against the count the source declares;
- selector drift: every listing page but the last yields a full page;
- cross-source consistency: two independent routes to the same data must agree;
- fill rates per field, with minimums where the brief needs them.

Then spot-check a handful of random rows against the live page by hand.

## 6. Deliver

- The dataset in the requested format, plus `qa_report.md`.
- Known gaps stated plainly, with the reason (case 2: "3 untagged quotes cannot be reached
  through the search form, by design").
- A one-line command to re-run it.

## 7. Red lines

- No CAPTCHA solving and no bot-detection evasion. A challenge page means stop and talk to the client.
- No logging in to accounts without authorization.
- No personal data beyond what the brief needs.
- Stay within robots.txt and a polite request rate, even when the site would tolerate more.

## A note on AI coding agents

I build with AI coding agents every day. The QA gate is what makes that safe: whatever the agent
writes, nothing is delivered unless the data passes checks that were written from the brief,
not from the code.
