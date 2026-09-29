# QA report: remote AI-data jobs tracker

**READY** · 410 rows delivered (410 collected) · generated 2026-09-29T16:54:41+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 410 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 399/410 postings have a country or region |

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
| countries | 96.8% |
| remote | 38.3% |
| open_to_colombia | 97.3% |
| employment_type | 36.3% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 56.3% |
| english_level | 28.0% |
| pay_usd_hour_max | 23.9% |
| pay_usd_year_max | 6.8% |
| hours_per_week | 33.9% |
| evidence | 72.7% |
| extracted_by | 72.7% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 1.7 s · 4.6 req/s

## Notes

- per board: greenhouse:handshake 5, greenhouse:invisibletech 18, greenhouse:labelbox 10, greenhouse:scaleai 198, greenhouse:turing 30, lever:rws 47, workable:huggingface 8, workable:toloka-ai 94
- 410 postings in 308 families; 328 distinct descriptions
- open to Colombia: yes 8, unclear 11, no 391
- rules found (per distinct description): min_years 159, english_level 46, pay_usd_hour_max 29, pay_usd_year_max 24, hours_per_week 67
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +3 new, -4 closed, ~2 changed
