# QA report: remote AI-data jobs tracker

**READY** · 1203 rows delivered (1203 collected) · generated 2026-10-20T15:40:34+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1203 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1195/1203 postings have a country or region |

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
| remote | 79.7% |
| open_to_colombia | 99.3% |
| employment_type | 78.9% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 12.5% |
| english_level | 15.9% |
| pay_usd_hour_max | 64.4% |
| pay_usd_year_max | 2.7% |
| hours_per_week | 20.9% |
| evidence | 84.4% |
| extracted_by | 84.4% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 7.8 s · 1.0 req/s

## Notes

- per board: greenhouse:handshake 9, greenhouse:invisibletech 22, greenhouse:labelbox 7, greenhouse:scaleai 184, greenhouse:turing 32, lever:rws 98, workable:huggingface 6, workable:toloka-ai 845
- 1203 postings in 966 families; 393 distinct descriptions
- open to Colombia: yes 11, unclear 8, no 1184
- rules found (per distinct description): min_years 140, english_level 53, pay_usd_hour_max 50, pay_usd_year_max 28, hours_per_week 113
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +58 new, -49 closed, ~11 changed
