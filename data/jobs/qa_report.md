# QA report: remote AI-data jobs tracker

**READY** · 1232 rows delivered (1232 collected) · generated 2026-10-15T15:37:45+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1232 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1224/1232 postings have a country or region |

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
| countries | 99.3% |
| remote | 80.6% |
| open_to_colombia | 99.4% |
| employment_type | 80.0% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 11.8% |
| english_level | 16.1% |
| pay_usd_hour_max | 72.0% |
| pay_usd_year_max | 2.6% |
| hours_per_week | 18.4% |
| evidence | 90.9% |
| extracted_by | 90.9% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 3.4 s · 2.4 req/s

## Notes

- per board: greenhouse:handshake 9, greenhouse:invisibletech 22, greenhouse:labelbox 8, greenhouse:scaleai 180, greenhouse:turing 28, lever:rws 96, workable:huggingface 6, workable:toloka-ai 883
- 1232 postings in 1033 families; 385 distinct descriptions
- open to Colombia: yes 10, unclear 8, no 1214
- rules found (per distinct description): min_years 136, english_level 54, pay_usd_hour_max 50, pay_usd_year_max 28, hours_per_week 109
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +280 new, -173 closed, ~5 changed
