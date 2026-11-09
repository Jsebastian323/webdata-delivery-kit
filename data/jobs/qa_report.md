# QA report: remote AI-data jobs tracker

**READY** · 1199 rows delivered (1199 collected) · generated 2026-11-09T21:28:26+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1199 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1190/1199 postings have a country or region |

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
| remote | 80.1% |
| open_to_colombia | 99.2% |
| employment_type | 79.4% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 12.5% |
| english_level | 22.9% |
| pay_usd_hour_max | 10.2% |
| pay_usd_year_max | 2.4% |
| hours_per_week | 15.8% |
| evidence | 43.5% |
| extracted_by | 43.5% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 17.5 s · 0.5 req/s

## Notes

- per board: greenhouse:invisibletech 20, greenhouse:labelbox 10, greenhouse:scaleai 170, greenhouse:turing 47, lever:rws 131, workable:huggingface 6, workable:toloka-ai 815
- 1199 postings in 781 families; 428 distinct descriptions
- open to Colombia: yes 14, unclear 9, no 1176
- rules found (per distinct description): min_years 144, english_level 47, pay_usd_hour_max 32, pay_usd_year_max 25, hours_per_week 113
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +72 new, -66 closed, ~1 changed
