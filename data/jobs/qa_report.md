# QA report: remote AI-data jobs tracker

**READY** · 415 rows delivered (415 collected) · generated 2026-09-26T14:59:17+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 415 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 404/415 postings have a country or region |

## Field fill rates

| Field | Filled |
|---|---|
| key | 100.0% |
| source | 100.0% |
| company | 100.0% |
| posting_id | 100.0% |
| title | 100.0% |
| url | 100.0% |
| location | 100.0% |
| countries | 96.6% |
| remote | 37.1% |
| open_to_colombia | 97.3% |
| employment_type | 34.9% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 57.1% |
| english_level | 27.5% |
| pay_usd_hour_max | 23.1% |
| pay_usd_year_max | 6.7% |
| hours_per_week | 32.5% |
| evidence | 72.8% |
| extracted_by | 72.8% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 1.6 s · 4.9 req/s

## Notes

- per board: greenhouse:handshake 5, greenhouse:invisibletech 18, greenhouse:labelbox 10, greenhouse:scaleai 203, greenhouse:turing 34, lever:rws 45, workable:huggingface 8, workable:toloka-ai 92
- 415 postings in 313 families; 334 distinct descriptions
- open to Colombia: yes 10, unclear 11, no 394
- rules found (per distinct description): min_years 166, english_level 46, pay_usd_hour_max 28, pay_usd_year_max 24, hours_per_week 64
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +0 new, -3 closed, ~11 changed
