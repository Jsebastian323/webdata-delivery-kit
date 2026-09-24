# QA report: remote AI-data jobs tracker

**READY** · 424 rows delivered (424 collected) · generated 2026-09-24T23:17:35+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 424 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 413/424 postings have a country or region |

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
| remote | 37.0% |
| open_to_colombia | 97.4% |
| employment_type | 34.9% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 57.5% |
| english_level | 26.9% |
| pay_usd_hour_max | 22.6% |
| pay_usd_year_max | 6.6% |
| hours_per_week | 32.5% |
| evidence | 73.6% |
| extracted_by | 73.6% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 2.5 s · 3.3 req/s

## Notes

- per board: greenhouse:handshake 5, greenhouse:invisibletech 17, greenhouse:labelbox 10, greenhouse:scaleai 209, greenhouse:turing 35, lever:rws 48, workable:huggingface 8, workable:toloka-ai 92
- 424 postings in 322 families; 343 distinct descriptions
- open to Colombia: yes 10, unclear 11, no 403
- rules found (per distinct description): min_years 173, english_level 46, pay_usd_hour_max 28, pay_usd_year_max 24, hours_per_week 67
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +0 new, -2 closed, ~0 changed
