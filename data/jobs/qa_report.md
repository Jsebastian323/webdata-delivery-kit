# QA report: remote AI-data jobs tracker

**READY** · 455 rows delivered (455 collected) · generated 2026-10-06T17:15:11+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 455 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 447/455 postings have a country or region |

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
| countries | 97.8% |
| remote | 46.2% |
| open_to_colombia | 98.2% |
| employment_type | 44.2% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 55.2% |
| english_level | 35.4% |
| pay_usd_hour_max | 31.4% |
| pay_usd_year_max | 7.0% |
| hours_per_week | 40.0% |
| evidence | 76.3% |
| extracted_by | 76.3% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 2.0 s · 4.1 req/s

## Notes

- per board: greenhouse:handshake 9, greenhouse:invisibletech 18, greenhouse:labelbox 9, greenhouse:scaleai 188, greenhouse:turing 30, lever:rws 56, workable:huggingface 6, workable:toloka-ai 139
- 455 postings in 310 families; 340 distinct descriptions
- open to Colombia: yes 10, unclear 8, no 437
- rules found (per distinct description): min_years 160, english_level 58, pay_usd_hour_max 40, pay_usd_year_max 28, hours_per_week 76
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +75 new, -25 closed, ~8 changed
