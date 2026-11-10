# QA report: remote AI-data jobs tracker

**READY** · 1154 rows delivered (1154 collected) · generated 2026-11-10T18:42:28+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1154 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1144/1154 postings have a country or region |

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
| countries | 99.0% |
| remote | 79.4% |
| open_to_colombia | 99.1% |
| employment_type | 78.6% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 12.8% |
| english_level | 19.7% |
| pay_usd_hour_max | 6.4% |
| pay_usd_year_max | 2.6% |
| hours_per_week | 12.3% |
| evidence | 41.0% |
| extracted_by | 41.0% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 2.5 s · 3.2 req/s

## Notes

- per board: greenhouse:invisibletech 20, greenhouse:labelbox 10, greenhouse:scaleai 169, greenhouse:turing 48, lever:rws 132, workable:huggingface 6, workable:toloka-ai 769
- 1154 postings in 777 families; 420 distinct descriptions
- open to Colombia: yes 11, unclear 10, no 1133
- rules found (per distinct description): min_years 142, english_level 37, pay_usd_hour_max 22, pay_usd_year_max 25, hours_per_week 104
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +80 new, -125 closed, ~91 changed
