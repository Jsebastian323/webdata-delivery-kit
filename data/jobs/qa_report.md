# QA report: remote AI-data jobs tracker

**READY** · 426 rows delivered (426 collected) · generated 2026-09-24T22:51:17+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 426 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 415/426 postings have a country or region |

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
| countries | 96.7% |
| remote | 36.9% |
| open_to_colombia | 97.4% |
| employment_type | 34.7% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 57.7% |
| english_level | 26.8% |
| pay_usd_hour_max | 22.5% |
| pay_usd_year_max | 6.6% |
| hours_per_week | 32.4% |
| evidence | 73.7% |
| extracted_by | 73.7% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 18.1 s · 0.4 req/s

## Notes

- per board: greenhouse:handshake 5, greenhouse:invisibletech 17, greenhouse:labelbox 10, greenhouse:scaleai 211, greenhouse:turing 35, lever:rws 48, workable:huggingface 8, workable:toloka-ai 92
- 426 postings in 324 families; 345 distinct descriptions
- open to Colombia: yes 10, unclear 11, no 405
- rules found (per distinct description): min_years 175, english_level 46, pay_usd_hour_max 28, pay_usd_year_max 24, hours_per_week 67
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +426 new, -0 closed, ~0 changed
