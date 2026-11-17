# QA report: remote AI-data jobs tracker

**READY** · 953 rows delivered (953 collected) · generated 2026-11-17T19:54:07+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 953 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 942/953 postings have a country or region |

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
| remote | 75.6% |
| open_to_colombia | 98.8% |
| employment_type | 74.6% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 14.8% |
| english_level | 3.0% |
| pay_usd_hour_max | 1.8% |
| pay_usd_year_max | 3.4% |
| hours_per_week | 10.1% |
| evidence | 27.8% |
| extracted_by | 27.8% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 19.1 s · 0.4 req/s

## Notes

- per board: greenhouse:invisibletech 20, greenhouse:labelbox 11, greenhouse:scaleai 167, greenhouse:turing 44, lever:rws 148, workable:huggingface 6, workable:toloka-ai 557
- 953 postings in 698 families; 420 distinct descriptions
- open to Colombia: yes 4, unclear 11, no 938
- rules found (per distinct description): min_years 137, english_level 28, pay_usd_hour_max 6, pay_usd_year_max 28, hours_per_week 94
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +76 new, -159 closed, ~6 changed
