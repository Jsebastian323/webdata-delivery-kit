# QA report: remote AI-data jobs tracker

**READY** · 471 rows delivered (471 collected) · generated 2026-10-08T17:53:47+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 471 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 463/471 postings have a country or region |

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
| countries | 98.1% |
| remote | 49.3% |
| open_to_colombia | 98.3% |
| employment_type | 47.6% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 52.2% |
| english_level | 39.1% |
| pay_usd_hour_max | 35.2% |
| pay_usd_year_max | 6.8% |
| hours_per_week | 43.3% |
| evidence | 77.1% |
| extracted_by | 77.1% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 1.8 s · 4.5 req/s

## Notes

- per board: greenhouse:handshake 9, greenhouse:invisibletech 18, greenhouse:labelbox 9, greenhouse:scaleai 181, greenhouse:turing 30, lever:rws 56, workable:huggingface 6, workable:toloka-ai 162
- 471 postings in 304 families; 343 distinct descriptions
- open to Colombia: yes 11, unclear 8, no 452
- rules found (per distinct description): min_years 156, english_level 66, pay_usd_hour_max 48, pay_usd_year_max 28, hours_per_week 83
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +31 new, -36 closed, ~1 changed
