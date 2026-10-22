# QA report: remote AI-data jobs tracker

**READY** · 776 rows delivered (776 collected) · generated 2026-10-22T15:54:32+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 776 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 773/776 postings have a country or region |

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
| countries | 99.6% |
| remote | 70.9% |
| open_to_colombia | 99.6% |
| employment_type | 69.7% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 19.1% |
| english_level | 24.5% |
| pay_usd_hour_max | 22.7% |
| pay_usd_year_max | 3.0% |
| hours_per_week | 32.7% |
| evidence | 52.3% |
| extracted_by | 52.3% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 2.6 s · 3.0 req/s

## Notes

- per board: greenhouse:invisibletech 23, greenhouse:labelbox 7, greenhouse:scaleai 174, greenhouse:turing 31, lever:rws 103, workable:huggingface 6, workable:toloka-ai 432
- 776 postings in 554 families; 382 distinct descriptions
- open to Colombia: yes 10, unclear 3, no 763
- rules found (per distinct description): min_years 139, english_level 53, pay_usd_hour_max 34, pay_usd_year_max 19, hours_per_week 116
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +123 new, -557 closed, ~69 changed
