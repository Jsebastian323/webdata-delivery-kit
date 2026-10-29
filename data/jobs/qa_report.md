# QA report: remote AI-data jobs tracker

**READY** · 1063 rows delivered (1063 collected) · generated 2026-10-29T17:27:09+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1063 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1060/1063 postings have a country or region |

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
| countries | 99.7% |
| remote | 78.7% |
| open_to_colombia | 99.7% |
| employment_type | 78.2% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 13.1% |
| english_level | 21.4% |
| pay_usd_hour_max | 20.2% |
| pay_usd_year_max | 2.3% |
| hours_per_week | 27.2% |
| evidence | 42.5% |
| extracted_by | 42.5% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 3.3 s · 2.4 req/s

## Notes

- per board: greenhouse:invisibletech 21, greenhouse:labelbox 10, greenhouse:scaleai 168, greenhouse:turing 33, lever:rws 154, workable:huggingface 6, workable:toloka-ai 671
- 1063 postings in 775 families; 430 distinct descriptions
- open to Colombia: yes 11, unclear 3, no 1049
- rules found (per distinct description): min_years 136, english_level 59, pay_usd_hour_max 31, pay_usd_year_max 20, hours_per_week 119
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +17 new, -21 closed, ~4 changed
