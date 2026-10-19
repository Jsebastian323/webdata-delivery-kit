# QA report: remote AI-data jobs tracker

**READY** · 1194 rows delivered (1194 collected) · generated 2026-10-19T17:31:37+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1194 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1186/1194 postings have a country or region |

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
| remote | 79.8% |
| open_to_colombia | 99.3% |
| employment_type | 79.0% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 12.5% |
| english_level | 15.9% |
| pay_usd_hour_max | 64.7% |
| pay_usd_year_max | 2.6% |
| hours_per_week | 20.8% |
| evidence | 84.5% |
| extracted_by | 84.5% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 3.2 s · 2.5 req/s

## Notes

- per board: greenhouse:handshake 9, greenhouse:invisibletech 24, greenhouse:labelbox 7, greenhouse:scaleai 181, greenhouse:turing 30, lever:rws 95, workable:huggingface 6, workable:toloka-ai 842
- 1194 postings in 957 families; 387 distinct descriptions
- open to Colombia: yes 10, unclear 8, no 1176
- rules found (per distinct description): min_years 139, english_level 53, pay_usd_hour_max 49, pay_usd_year_max 27, hours_per_week 110
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +55 new, -59 closed, ~23 changed
