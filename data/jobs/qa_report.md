# QA report: remote AI-data jobs tracker

**READY** · 951 rows delivered (951 collected) · generated 2026-10-25T14:57:59+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 951 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 948/951 postings have a country or region |

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
| remote | 76.2% |
| open_to_colombia | 99.7% |
| employment_type | 75.5% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 14.8% |
| english_level | 20.0% |
| pay_usd_hour_max | 19.3% |
| pay_usd_year_max | 2.6% |
| hours_per_week | 26.7% |
| evidence | 43.6% |
| extracted_by | 43.6% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 2.9 s · 2.7 req/s

## Notes

- per board: greenhouse:invisibletech 23, greenhouse:labelbox 8, greenhouse:scaleai 171, greenhouse:turing 31, lever:rws 137, workable:huggingface 6, workable:toloka-ai 575
- 951 postings in 728 families; 414 distinct descriptions
- open to Colombia: yes 10, unclear 3, no 938
- rules found (per distinct description): min_years 138, english_level 53, pay_usd_hour_max 32, pay_usd_year_max 21, hours_per_week 116
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +73 new, -62 closed, ~2 changed
