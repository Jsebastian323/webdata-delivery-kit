# QA report: remote AI-data jobs tracker

**READY** · 940 rows delivered (940 collected) · generated 2026-10-24T14:37:00+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 940 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 937/940 postings have a country or region |

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
| remote | 76.1% |
| open_to_colombia | 99.7% |
| employment_type | 75.3% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 14.9% |
| english_level | 20.2% |
| pay_usd_hour_max | 19.6% |
| pay_usd_year_max | 2.6% |
| hours_per_week | 27.0% |
| evidence | 43.9% |
| extracted_by | 43.9% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 2.3 s · 3.4 req/s

## Notes

- per board: greenhouse:invisibletech 23, greenhouse:labelbox 8, greenhouse:scaleai 171, greenhouse:turing 30, lever:rws 137, workable:huggingface 6, workable:toloka-ai 565
- 940 postings in 717 families; 413 distinct descriptions
- open to Colombia: yes 10, unclear 3, no 927
- rules found (per distinct description): min_years 137, english_level 53, pay_usd_hour_max 32, pay_usd_year_max 20, hours_per_week 116
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +71 new, -10 closed, ~9 changed
