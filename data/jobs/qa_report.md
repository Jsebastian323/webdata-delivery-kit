# QA report: remote AI-data jobs tracker

**READY** · 968 rows delivered (968 collected) · generated 2026-11-19T19:30:14+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 968 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 956/968 postings have a country or region |

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
| countries | 98.7% |
| remote | 76.1% |
| open_to_colombia | 98.8% |
| employment_type | 75.3% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 14.3% |
| english_level | 3.1% |
| pay_usd_hour_max | 1.8% |
| pay_usd_year_max | 3.3% |
| hours_per_week | 9.7% |
| evidence | 26.9% |
| extracted_by | 26.9% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 1.8 s · 4.4 req/s

## Notes

- per board: greenhouse:invisibletech 21, greenhouse:labelbox 12, greenhouse:scaleai 168, greenhouse:turing 38, lever:rws 136, workable:huggingface 6, workable:toloka-ai 587
- 968 postings in 676 families; 409 distinct descriptions
- open to Colombia: yes 4, unclear 12, no 952
- rules found (per distinct description): min_years 134, english_level 28, pay_usd_hour_max 6, pay_usd_year_max 28, hours_per_week 91
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +284 new, -284 closed, ~9 changed
