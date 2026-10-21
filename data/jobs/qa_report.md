# QA report: remote AI-data jobs tracker

**READY** · 1210 rows delivered (1210 collected) · generated 2026-10-21T15:59:00+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1210 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1207/1210 postings have a country or region |

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
| countries | 99.8% |
| remote | 80.9% |
| open_to_colombia | 99.8% |
| employment_type | 80.2% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 12.2% |
| english_level | 15.7% |
| pay_usd_hour_max | 60.9% |
| pay_usd_year_max | 2.3% |
| hours_per_week | 21.1% |
| evidence | 80.4% |
| extracted_by | 80.4% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 4.1 s · 1.9 req/s

## Notes

- per board: greenhouse:handshake 4, greenhouse:invisibletech 22, greenhouse:labelbox 7, greenhouse:scaleai 175, greenhouse:turing 32, lever:rws 107, workable:huggingface 6, workable:toloka-ai 857
- 1210 postings in 978 families; 390 distinct descriptions
- open to Colombia: yes 10, unclear 3, no 1197
- rules found (per distinct description): min_years 139, english_level 52, pay_usd_hour_max 48, pay_usd_year_max 24, hours_per_week 116
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +76 new, -69 closed, ~25 changed
