# QA report: remote AI-data jobs tracker

**READY** · 411 rows delivered (411 collected) · generated 2026-09-28T18:37:56+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 411 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 400/411 postings have a country or region |

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
| remote | 37.5% |
| open_to_colombia | 97.3% |
| employment_type | 35.5% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 56.7% |
| english_level | 27.5% |
| pay_usd_hour_max | 23.4% |
| pay_usd_year_max | 6.8% |
| hours_per_week | 33.1% |
| evidence | 72.7% |
| extracted_by | 72.7% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 26.2 s · 0.3 req/s

## Notes

- per board: greenhouse:handshake 5, greenhouse:invisibletech 18, greenhouse:labelbox 10, greenhouse:scaleai 200, greenhouse:turing 32, lever:rws 46, workable:huggingface 8, workable:toloka-ai 92
- 411 postings in 309 families; 330 distinct descriptions
- open to Colombia: yes 8, unclear 11, no 392
- rules found (per distinct description): min_years 162, english_level 45, pay_usd_hour_max 28, pay_usd_year_max 24, hours_per_week 65
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +42 new, -46 closed, ~1 changed
