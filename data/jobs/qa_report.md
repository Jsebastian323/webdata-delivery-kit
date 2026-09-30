# QA report: remote AI-data jobs tracker

**READY** · 401 rows delivered (401 collected) · generated 2026-09-30T16:50:40+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 401 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 390/401 postings have a country or region |

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
| remote | 38.7% |
| open_to_colombia | 97.3% |
| employment_type | 36.7% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 54.9% |
| english_level | 28.4% |
| pay_usd_hour_max | 23.9% |
| pay_usd_year_max | 6.7% |
| hours_per_week | 34.2% |
| evidence | 71.6% |
| extracted_by | 71.6% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 1.3 s · 6.0 req/s

## Notes

- per board: greenhouse:handshake 5, greenhouse:invisibletech 18, greenhouse:labelbox 10, greenhouse:scaleai 192, greenhouse:turing 29, lever:rws 47, workable:huggingface 8, workable:toloka-ai 92
- 401 postings in 302 families; 319 distinct descriptions
- open to Colombia: yes 8, unclear 11, no 382
- rules found (per distinct description): min_years 149, english_level 45, pay_usd_hour_max 28, pay_usd_year_max 23, hours_per_week 65
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +5 new, -14 closed, ~3 changed
