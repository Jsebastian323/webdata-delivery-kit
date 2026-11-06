# QA report: remote AI-data jobs tracker

**READY** · 1134 rows delivered (1134 collected) · generated 2026-11-06T18:02:22+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1134 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1125/1134 postings have a country or region |

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
| countries | 99.1% |
| remote | 78.9% |
| open_to_colombia | 99.2% |
| employment_type | 78.2% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 13.0% |
| english_level | 19.2% |
| pay_usd_hour_max | 10.6% |
| pay_usd_year_max | 2.6% |
| hours_per_week | 16.0% |
| evidence | 40.1% |
| extracted_by | 40.1% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 3.0 s · 2.7 req/s

## Notes

- per board: greenhouse:invisibletech 20, greenhouse:labelbox 10, greenhouse:scaleai 173, greenhouse:turing 44, lever:rws 120, workable:huggingface 6, workable:toloka-ai 761
- 1134 postings in 769 families; 415 distinct descriptions
- open to Colombia: yes 13, unclear 9, no 1112
- rules found (per distinct description): min_years 141, english_level 45, pay_usd_hour_max 30, pay_usd_year_max 25, hours_per_week 105
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +140 new, -105 closed, ~37 changed
