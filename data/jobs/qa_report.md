# QA report: remote AI-data jobs tracker

**READY** · 971 rows delivered (971 collected) · generated 2026-11-23T22:42:41+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 971 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 959/971 postings have a country or region |

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
| remote | 77.3% |
| open_to_colombia | 98.8% |
| employment_type | 76.7% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 14.5% |
| english_level | 4.2% |
| pay_usd_hour_max | 1.8% |
| pay_usd_year_max | 2.8% |
| hours_per_week | 10.6% |
| evidence | 27.5% |
| extracted_by | 27.5% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 3.5 s · 2.3 req/s

## Notes

- per board: greenhouse:invisibletech 21, greenhouse:labelbox 13, greenhouse:scaleai 161, greenhouse:turing 31, lever:rws 147, workable:huggingface 10, workable:toloka-ai 588
- 971 postings in 677 families; 410 distinct descriptions
- open to Colombia: yes 3, unclear 12, no 956
- rules found (per distinct description): min_years 137, english_level 39, pay_usd_hour_max 6, pay_usd_year_max 23, hours_per_week 101
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +3 new, -8 closed, ~10 changed
