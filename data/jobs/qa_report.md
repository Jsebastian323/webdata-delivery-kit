# QA report: remote AI-data jobs tracker

**READY** · 1071 rows delivered (1071 collected) · generated 2026-10-31T16:08:53+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1071 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1068/1071 postings have a country or region |

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
| remote | 78.2% |
| open_to_colombia | 99.7% |
| employment_type | 77.5% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 13.3% |
| english_level | 21.2% |
| pay_usd_hour_max | 20.2% |
| pay_usd_year_max | 2.4% |
| hours_per_week | 27.0% |
| evidence | 42.7% |
| extracted_by | 42.7% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 2.9 s · 2.7 req/s

## Notes

- per board: greenhouse:invisibletech 22, greenhouse:labelbox 10, greenhouse:scaleai 170, greenhouse:turing 39, lever:rws 153, workable:huggingface 6, workable:toloka-ai 671
- 1071 postings in 782 families; 439 distinct descriptions
- open to Colombia: yes 12, unclear 3, no 1056
- rules found (per distinct description): min_years 139, english_level 59, pay_usd_hour_max 33, pay_usd_year_max 22, hours_per_week 120
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +3 new, -0 closed, ~2 changed
