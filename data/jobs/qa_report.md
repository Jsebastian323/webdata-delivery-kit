# QA report: remote AI-data jobs tracker

**READY** · 1068 rows delivered (1068 collected) · generated 2026-10-30T17:02:11+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1068 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1065/1068 postings have a country or region |

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
| remote | 78.4% |
| open_to_colombia | 99.7% |
| employment_type | 77.7% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 13.0% |
| english_level | 21.3% |
| pay_usd_hour_max | 20.2% |
| pay_usd_year_max | 2.4% |
| hours_per_week | 27.1% |
| evidence | 42.5% |
| extracted_by | 42.5% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 2.6 s · 3.0 req/s

## Notes

- per board: greenhouse:invisibletech 21, greenhouse:labelbox 10, greenhouse:scaleai 169, greenhouse:turing 38, lever:rws 153, workable:huggingface 6, workable:toloka-ai 671
- 1068 postings in 779 families; 435 distinct descriptions
- open to Colombia: yes 12, unclear 3, no 1053
- rules found (per distinct description): min_years 136, english_level 59, pay_usd_hour_max 33, pay_usd_year_max 22, hours_per_week 120
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +89 new, -84 closed, ~25 changed
