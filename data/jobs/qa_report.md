# QA report: remote AI-data jobs tracker

**READY** · 476 rows delivered (476 collected) · generated 2026-10-07T17:50:49+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 476 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 468/476 postings have a country or region |

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
| remote | 48.5% |
| open_to_colombia | 98.3% |
| employment_type | 46.8% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 52.5% |
| english_level | 38.4% |
| pay_usd_hour_max | 34.7% |
| pay_usd_year_max | 6.7% |
| hours_per_week | 42.9% |
| evidence | 77.3% |
| extracted_by | 77.3% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 1.9 s · 4.1 req/s

## Notes

- per board: greenhouse:handshake 9, greenhouse:invisibletech 18, greenhouse:labelbox 9, greenhouse:scaleai 187, greenhouse:turing 30, lever:rws 56, workable:huggingface 6, workable:toloka-ai 161
- 476 postings in 310 families; 348 distinct descriptions
- open to Colombia: yes 11, unclear 8, no 457
- rules found (per distinct description): min_years 160, english_level 66, pay_usd_hour_max 48, pay_usd_year_max 28, hours_per_week 84
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +27 new, -6 closed, ~2 changed
