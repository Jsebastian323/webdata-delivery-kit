# QA report: remote AI-data jobs tracker

**READY** · 1107 rows delivered (1107 collected) · generated 2026-11-13T18:33:57+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1107 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1096/1107 postings have a country or region |

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
| countries | 98.9% |
| remote | 78.2% |
| open_to_colombia | 99.0% |
| employment_type | 77.4% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 13.4% |
| english_level | 16.1% |
| pay_usd_hour_max | 2.3% |
| pay_usd_year_max | 2.8% |
| hours_per_week | 8.2% |
| evidence | 38.1% |
| extracted_by | 38.1% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 13.7 s · 0.6 req/s

## Notes

- per board: greenhouse:invisibletech 20, greenhouse:labelbox 11, greenhouse:scaleai 171, greenhouse:turing 48, lever:rws 132, workable:huggingface 6, workable:toloka-ai 719
- 1107 postings in 777 families; 412 distinct descriptions
- open to Colombia: yes 9, unclear 11, no 1087
- rules found (per distinct description): min_years 142, english_level 25, pay_usd_hour_max 10, pay_usd_year_max 27, hours_per_week 89
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +144 new, -147 closed, ~19 changed
