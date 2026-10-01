# QA report: remote AI-data jobs tracker

**READY** · 404 rows delivered (404 collected) · generated 2026-10-01T17:24:38+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 404 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 393/404 postings have a country or region |

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
| remote | 38.6% |
| open_to_colombia | 97.3% |
| employment_type | 36.6% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 54.5% |
| english_level | 28.5% |
| pay_usd_hour_max | 24.0% |
| pay_usd_year_max | 7.2% |
| hours_per_week | 34.2% |
| evidence | 71.8% |
| extracted_by | 71.8% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 2.1 s · 3.7 req/s

## Notes

- per board: greenhouse:handshake 6, greenhouse:invisibletech 18, greenhouse:labelbox 10, greenhouse:scaleai 192, greenhouse:turing 30, lever:rws 48, workable:huggingface 8, workable:toloka-ai 92
- 404 postings in 304 families; 322 distinct descriptions
- open to Colombia: yes 8, unclear 11, no 385
- rules found (per distinct description): min_years 149, english_level 46, pay_usd_hour_max 29, pay_usd_year_max 25, hours_per_week 66
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +6 new, -3 closed, ~1 changed
