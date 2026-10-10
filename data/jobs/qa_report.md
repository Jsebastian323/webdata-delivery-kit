# QA report: remote AI-data jobs tracker

**READY** · 422 rows delivered (422 collected) · generated 2026-10-10T16:15:35+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 422 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 414/422 postings have a country or region |

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
| countries | 97.9% |
| remote | 42.9% |
| open_to_colombia | 98.1% |
| employment_type | 41.0% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 34.8% |
| english_level | 27.0% |
| pay_usd_hour_max | 22.5% |
| pay_usd_year_max | 7.3% |
| hours_per_week | 34.8% |
| evidence | 72.7% |
| extracted_by | 72.7% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 3.4 s · 2.4 req/s

## Notes

- per board: greenhouse:handshake 9, greenhouse:invisibletech 20, greenhouse:labelbox 8, greenhouse:scaleai 183, greenhouse:turing 29, lever:rws 76, workable:huggingface 6, workable:toloka-ai 91
- 422 postings in 317 families; 341 distinct descriptions
- open to Colombia: yes 8, unclear 8, no 406
- rules found (per distinct description): min_years 144, english_level 44, pay_usd_hour_max 25, pay_usd_year_max 27, hours_per_week 74
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +16 new, -1 closed, ~12 changed
