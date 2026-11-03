# QA report: remote AI-data jobs tracker

**READY** · 1064 rows delivered (1064 collected) · generated 2026-11-03T18:28:05+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1064 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1061/1064 postings have a country or region |

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
| countries | 99.6% |
| remote | 78.3% |
| open_to_colombia | 99.7% |
| employment_type | 77.4% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 13.1% |
| english_level | 21.6% |
| pay_usd_hour_max | 20.3% |
| pay_usd_year_max | 2.7% |
| hours_per_week | 27.4% |
| evidence | 43.1% |
| extracted_by | 43.1% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 4.0 s · 2.0 req/s

## Notes

- per board: greenhouse:invisibletech 23, greenhouse:labelbox 10, greenhouse:scaleai 166, greenhouse:turing 41, lever:rws 149, workable:huggingface 6, workable:toloka-ai 669
- 1064 postings in 788 families; 438 distinct descriptions
- open to Colombia: yes 12, unclear 3, no 1049
- rules found (per distinct description): min_years 136, english_level 61, pay_usd_hour_max 33, pay_usd_year_max 25, hours_per_week 122
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +244 new, -247 closed, ~21 changed
