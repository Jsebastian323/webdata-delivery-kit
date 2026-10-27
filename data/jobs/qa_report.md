# QA report: remote AI-data jobs tracker

**READY** · 999 rows delivered (999 collected) · generated 2026-10-27T16:43:13+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 999 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 996/999 postings have a country or region |

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
| remote | 77.3% |
| open_to_colombia | 99.7% |
| employment_type | 76.5% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 14.0% |
| english_level | 19.0% |
| pay_usd_hour_max | 18.5% |
| pay_usd_year_max | 2.6% |
| hours_per_week | 25.4% |
| evidence | 41.6% |
| extracted_by | 41.6% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 3.5 s · 2.3 req/s

## Notes

- per board: greenhouse:invisibletech 23, greenhouse:labelbox 9, greenhouse:scaleai 167, greenhouse:turing 36, lever:rws 148, workable:huggingface 6, workable:toloka-ai 610
- 999 postings in 757 families; 427 distinct descriptions
- open to Colombia: yes 10, unclear 3, no 986
- rules found (per distinct description): min_years 137, english_level 53, pay_usd_hour_max 32, pay_usd_year_max 22, hours_per_week 116
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +64 new, -49 closed, ~13 changed
