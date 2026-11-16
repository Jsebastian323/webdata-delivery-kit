# QA report: remote AI-data jobs tracker

**READY** · 1036 rows delivered (1036 collected) · generated 2026-11-16T21:04:43+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1036 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1025/1036 postings have a country or region |

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
| remote | 77.2% |
| open_to_colombia | 98.9% |
| employment_type | 76.4% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 13.8% |
| english_level | 17.2% |
| pay_usd_hour_max | 1.8% |
| pay_usd_year_max | 2.9% |
| hours_per_week | 8.7% |
| evidence | 39.8% |
| extracted_by | 39.8% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 1.6 s · 5.1 req/s

## Notes

- per board: greenhouse:invisibletech 20, greenhouse:labelbox 11, greenhouse:scaleai 170, greenhouse:turing 44, lever:rws 140, workable:huggingface 6, workable:toloka-ai 645
- 1036 postings in 703 families; 412 distinct descriptions
- open to Colombia: yes 8, unclear 11, no 1017
- rules found (per distinct description): min_years 139, english_level 25, pay_usd_hour_max 8, pay_usd_year_max 26, hours_per_week 88
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +9 new, -72 closed, ~7 changed
