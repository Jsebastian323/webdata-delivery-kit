# QA report: remote AI-data jobs tracker

**READY** · 968 rows delivered (968 collected) · generated 2026-11-18T19:25:30+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 968 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 957/968 postings have a country or region |

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
| countries | 98.8% |
| remote | 75.9% |
| open_to_colombia | 98.9% |
| employment_type | 75.0% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 14.5% |
| english_level | 3.0% |
| pay_usd_hour_max | 1.8% |
| pay_usd_year_max | 3.3% |
| hours_per_week | 9.7% |
| evidence | 27.1% |
| extracted_by | 27.1% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 2.7 s · 3.0 req/s

## Notes

- per board: greenhouse:invisibletech 21, greenhouse:labelbox 11, greenhouse:scaleai 167, greenhouse:turing 43, lever:rws 146, workable:huggingface 6, workable:toloka-ai 574
- 968 postings in 674 families; 422 distinct descriptions
- open to Colombia: yes 5, unclear 11, no 952
- rules found (per distinct description): min_years 136, english_level 28, pay_usd_hour_max 6, pay_usd_year_max 28, hours_per_week 92
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +137 new, -122 closed, ~58 changed
