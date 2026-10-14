# QA report: remote AI-data jobs tracker

**READY** · 1125 rows delivered (1125 collected) · generated 2026-10-14T15:50:53+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1125 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1117/1125 postings have a country or region |

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
| countries | 99.2% |
| remote | 78.5% |
| open_to_colombia | 99.3% |
| employment_type | 77.8% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 12.4% |
| english_level | 14.7% |
| pay_usd_hour_max | 69.0% |
| pay_usd_year_max | 2.8% |
| hours_per_week | 20.3% |
| evidence | 89.9% |
| extracted_by | 89.9% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 3.2 s · 2.5 req/s

## Notes

- per board: greenhouse:handshake 9, greenhouse:invisibletech 22, greenhouse:labelbox 8, greenhouse:scaleai 183, greenhouse:turing 28, lever:rws 97, workable:huggingface 6, workable:toloka-ai 772
- 1125 postings in 961 families; 385 distinct descriptions
- open to Colombia: yes 10, unclear 8, no 1107
- rules found (per distinct description): min_years 136, english_level 48, pay_usd_hour_max 46, pay_usd_year_max 28, hours_per_week 110
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +604 new, -7 closed, ~38 changed
