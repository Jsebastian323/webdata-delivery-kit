# QA report: remote AI-data jobs tracker

**READY** · 1099 rows delivered (1099 collected) · generated 2026-11-15T17:47:16+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1099 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1088/1099 postings have a country or region |

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
| countries | 98.9% |
| remote | 78.4% |
| open_to_colombia | 99.0% |
| employment_type | 77.6% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 13.0% |
| english_level | 16.2% |
| pay_usd_hour_max | 2.0% |
| pay_usd_year_max | 2.6% |
| hours_per_week | 8.3% |
| evidence | 37.8% |
| extracted_by | 37.8% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 2.9 s · 2.7 req/s

## Notes

- per board: greenhouse:invisibletech 20, greenhouse:labelbox 11, greenhouse:scaleai 170, greenhouse:turing 45, lever:rws 132, workable:huggingface 6, workable:toloka-ai 715
- 1099 postings in 772 families; 406 distinct descriptions
- open to Colombia: yes 9, unclear 11, no 1079
- rules found (per distinct description): min_years 139, english_level 25, pay_usd_hour_max 8, pay_usd_year_max 25, hours_per_week 89
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +0 new, -7 closed, ~1 changed
