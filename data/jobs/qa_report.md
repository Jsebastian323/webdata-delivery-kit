# QA report: remote AI-data jobs tracker

**READY** · 1108 rows delivered (1108 collected) · generated 2026-11-11T18:44:19+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1108 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1098/1108 postings have a country or region |

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
| remote | 78.4% |
| open_to_colombia | 99.1% |
| employment_type | 77.6% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 13.4% |
| english_level | 16.2% |
| pay_usd_hour_max | 2.4% |
| pay_usd_year_max | 2.7% |
| hours_per_week | 8.5% |
| evidence | 38.4% |
| extracted_by | 38.4% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 5.5 s · 1.5 req/s

## Notes

- per board: greenhouse:invisibletech 20, greenhouse:labelbox 10, greenhouse:scaleai 169, greenhouse:turing 49, lever:rws 133, workable:huggingface 6, workable:toloka-ai 721
- 1108 postings in 775 families; 413 distinct descriptions
- open to Colombia: yes 9, unclear 10, no 1089
- rules found (per distinct description): min_years 142, english_level 26, pay_usd_hour_max 11, pay_usd_year_max 26, hours_per_week 92
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +137 new, -183 closed, ~6 changed
