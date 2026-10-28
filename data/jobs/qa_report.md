# QA report: remote AI-data jobs tracker

**READY** · 1067 rows delivered (1067 collected) · generated 2026-10-28T17:11:22+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1067 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1064/1067 postings have a country or region |

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
| remote | 78.4% |
| open_to_colombia | 99.7% |
| employment_type | 77.8% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 13.2% |
| english_level | 21.2% |
| pay_usd_hour_max | 20.1% |
| pay_usd_year_max | 2.3% |
| hours_per_week | 26.8% |
| evidence | 42.4% |
| extracted_by | 42.4% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 6.8 s · 1.2 req/s

## Notes

- per board: greenhouse:invisibletech 21, greenhouse:labelbox 9, greenhouse:scaleai 170, greenhouse:turing 37, lever:rws 154, workable:huggingface 6, workable:toloka-ai 670
- 1067 postings in 779 families; 436 distinct descriptions
- open to Colombia: yes 11, unclear 3, no 1053
- rules found (per distinct description): min_years 138, english_level 59, pay_usd_hour_max 32, pay_usd_year_max 21, hours_per_week 118
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +139 new, -71 closed, ~35 changed
