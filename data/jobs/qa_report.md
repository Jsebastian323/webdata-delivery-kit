# QA report: remote AI-data jobs tracker

**READY** · 418 rows delivered (418 collected) · generated 2026-09-25T15:50:44+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 418 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 407/418 postings have a country or region |

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
| remote | 36.8% |
| open_to_colombia | 97.4% |
| employment_type | 34.7% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 57.4% |
| english_level | 27.3% |
| pay_usd_hour_max | 23.0% |
| pay_usd_year_max | 6.7% |
| hours_per_week | 32.3% |
| evidence | 73.0% |
| extracted_by | 73.0% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 2.4 s · 3.3 req/s

## Notes

- per board: greenhouse:handshake 5, greenhouse:invisibletech 18, greenhouse:labelbox 10, greenhouse:scaleai 206, greenhouse:turing 34, lever:rws 45, workable:huggingface 8, workable:toloka-ai 92
- 418 postings in 316 families; 337 distinct descriptions
- open to Colombia: yes 10, unclear 11, no 397
- rules found (per distinct description): min_years 169, english_level 46, pay_usd_hour_max 28, pay_usd_year_max 24, hours_per_week 64
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +43 new, -49 closed, ~1 changed
