# QA report: remote AI-data jobs tracker

**READY** · 976 rows delivered (976 collected) · generated 2026-11-27T20:00:06+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 976 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 964/976 postings have a country or region |

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
| remote | 78.0% |
| open_to_colombia | 98.8% |
| employment_type | 77.4% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 14.0% |
| english_level | 4.3% |
| pay_usd_hour_max | 1.6% |
| pay_usd_year_max | 2.7% |
| hours_per_week | 11.0% |
| evidence | 27.4% |
| extracted_by | 27.4% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 1.5 s · 5.3 req/s

## Notes

- per board: greenhouse:invisibletech 19, greenhouse:labelbox 13, greenhouse:scaleai 158, greenhouse:turing 31, lever:rws 144, workable:huggingface 9, workable:toloka-ai 602
- 976 postings in 680 families; 403 distinct descriptions
- open to Colombia: yes 3, unclear 12, no 961
- rules found (per distinct description): min_years 134, english_level 40, pay_usd_hour_max 6, pay_usd_year_max 22, hours_per_week 106
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +206 new, -192 closed, ~5 changed
