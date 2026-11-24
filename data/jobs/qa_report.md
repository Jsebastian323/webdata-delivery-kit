# QA report: remote AI-data jobs tracker

**READY** · 967 rows delivered (967 collected) · generated 2026-11-24T21:19:00+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 967 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 955/967 postings have a country or region |

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
| remote | 77.6% |
| open_to_colombia | 98.8% |
| employment_type | 76.9% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 14.3% |
| english_level | 4.3% |
| pay_usd_hour_max | 1.7% |
| pay_usd_year_max | 2.8% |
| hours_per_week | 11.1% |
| evidence | 27.7% |
| extracted_by | 27.7% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 1.9 s · 4.2 req/s

## Notes

- per board: greenhouse:invisibletech 21, greenhouse:labelbox 13, greenhouse:scaleai 158, greenhouse:turing 31, lever:rws 148, workable:huggingface 10, workable:toloka-ai 586
- 967 postings in 673 families; 407 distinct descriptions
- open to Colombia: yes 3, unclear 12, no 952
- rules found (per distinct description): min_years 135, english_level 40, pay_usd_hour_max 6, pay_usd_year_max 23, hours_per_week 106
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +1 new, -5 closed, ~159 changed
