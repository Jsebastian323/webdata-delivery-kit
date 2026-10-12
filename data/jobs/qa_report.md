# QA report: remote AI-data jobs tracker

**READY** · 450 rows delivered (450 collected) · generated 2026-10-12T20:19:12+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 450 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 442/450 postings have a country or region |

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
| countries | 98.0% |
| remote | 46.2% |
| open_to_colombia | 98.2% |
| employment_type | 44.4% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 33.1% |
| english_level | 31.3% |
| pay_usd_hour_max | 27.1% |
| pay_usd_year_max | 6.9% |
| hours_per_week | 38.7% |
| evidence | 74.7% |
| extracted_by | 74.7% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 2.2 s · 3.6 req/s

## Notes

- per board: greenhouse:handshake 9, greenhouse:invisibletech 20, greenhouse:labelbox 8, greenhouse:scaleai 184, greenhouse:turing 29, lever:rws 76, workable:huggingface 6, workable:toloka-ai 118
- 450 postings in 322 families; 344 distinct descriptions
- open to Colombia: yes 9, unclear 8, no 433
- rules found (per distinct description): min_years 145, english_level 47, pay_usd_hour_max 28, pay_usd_year_max 27, hours_per_week 77
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +52 new, -23 closed, ~0 changed
