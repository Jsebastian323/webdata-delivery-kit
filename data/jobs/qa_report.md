# QA report: remote AI-data jobs tracker

**READY** · 407 rows delivered (407 collected) · generated 2026-10-09T17:27:40+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 407 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 399/407 postings have a country or region |

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
| countries | 97.8% |
| remote | 41.3% |
| open_to_colombia | 98.0% |
| employment_type | 39.1% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 32.4% |
| english_level | 27.8% |
| pay_usd_hour_max | 23.3% |
| pay_usd_year_max | 7.6% |
| hours_per_week | 32.7% |
| evidence | 71.7% |
| extracted_by | 71.7% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 1.5 s · 5.4 req/s

## Notes

- per board: greenhouse:handshake 9, greenhouse:invisibletech 19, greenhouse:labelbox 9, greenhouse:scaleai 182, greenhouse:turing 29, lever:rws 62, workable:huggingface 6, workable:toloka-ai 91
- 407 postings in 302 families; 326 distinct descriptions
- open to Colombia: yes 8, unclear 8, no 391
- rules found (per distinct description): min_years 129, english_level 43, pay_usd_hour_max 25, pay_usd_year_max 27, hours_per_week 60
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +32 new, -96 closed, ~30 changed
