# QA report: remote AI-data jobs tracker

**READY** · 1198 rows delivered (1198 collected) · generated 2026-10-18T14:38:28+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1198 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1190/1198 postings have a country or region |

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
| remote | 79.9% |
| open_to_colombia | 99.3% |
| employment_type | 79.1% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 12.4% |
| english_level | 16.5% |
| pay_usd_hour_max | 65.3% |
| pay_usd_year_max | 2.7% |
| hours_per_week | 20.5% |
| evidence | 84.9% |
| extracted_by | 84.9% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 6.1 s · 1.3 req/s

## Notes

- per board: greenhouse:handshake 9, greenhouse:invisibletech 23, greenhouse:labelbox 7, greenhouse:scaleai 182, greenhouse:turing 29, lever:rws 95, workable:huggingface 6, workable:toloka-ai 847
- 1198 postings in 959 families; 390 distinct descriptions
- open to Colombia: yes 10, unclear 8, no 1180
- rules found (per distinct description): min_years 139, english_level 56, pay_usd_hour_max 52, pay_usd_year_max 28, hours_per_week 110
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +0 new, -1 closed, ~0 changed
