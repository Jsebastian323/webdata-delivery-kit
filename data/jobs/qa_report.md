# QA report: remote AI-data jobs tracker

**READY** · 1192 rows delivered (1192 collected) · generated 2026-11-07T16:52:50+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1192 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1183/1192 postings have a country or region |

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
| countries | 99.2% |
| remote | 80.1% |
| open_to_colombia | 99.2% |
| employment_type | 79.4% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 12.4% |
| english_level | 23.0% |
| pay_usd_hour_max | 10.2% |
| pay_usd_year_max | 2.4% |
| hours_per_week | 15.4% |
| evidence | 43.0% |
| extracted_by | 43.0% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 3.1 s · 2.6 req/s

## Notes

- per board: greenhouse:invisibletech 20, greenhouse:labelbox 10, greenhouse:scaleai 168, greenhouse:turing 47, lever:rws 125, workable:huggingface 6, workable:toloka-ai 816
- 1192 postings in 771 families; 419 distinct descriptions
- open to Colombia: yes 14, unclear 9, no 1169
- rules found (per distinct description): min_years 142, english_level 47, pay_usd_hour_max 32, pay_usd_year_max 25, hours_per_week 107
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +121 new, -63 closed, ~7 changed
