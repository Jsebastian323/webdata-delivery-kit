# QA report: remote AI-data jobs tracker

**READY** · 930 rows delivered (930 collected) · generated 2026-11-20T19:08:11+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 930 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 918/930 postings have a country or region |

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
| countries | 98.6% |
| remote | 75.7% |
| open_to_colombia | 98.7% |
| employment_type | 74.8% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 14.7% |
| english_level | 4.4% |
| pay_usd_hour_max | 1.8% |
| pay_usd_year_max | 3.2% |
| hours_per_week | 11.3% |
| evidence | 28.8% |
| extracted_by | 28.8% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 1.8 s · 4.5 req/s

## Notes

- per board: greenhouse:invisibletech 21, greenhouse:labelbox 12, greenhouse:scaleai 167, greenhouse:turing 34, lever:rws 147, workable:huggingface 10, workable:toloka-ai 539
- 930 postings in 683 families; 416 distinct descriptions
- open to Colombia: yes 4, unclear 12, no 914
- rules found (per distinct description): min_years 133, english_level 39, pay_usd_hour_max 6, pay_usd_year_max 26, hours_per_week 102
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +99 new, -137 closed, ~5 changed
