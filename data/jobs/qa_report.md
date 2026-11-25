# QA report: remote AI-data jobs tracker

**READY** · 965 rows delivered (965 collected) · generated 2026-11-25T20:29:41+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 965 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 953/965 postings have a country or region |

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
| countries | 98.7% |
| remote | 77.7% |
| open_to_colombia | 98.8% |
| employment_type | 77.1% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 14.2% |
| english_level | 4.4% |
| pay_usd_hour_max | 1.7% |
| pay_usd_year_max | 2.7% |
| hours_per_week | 11.1% |
| evidence | 27.7% |
| extracted_by | 27.7% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 2.3 s · 3.5 req/s

## Notes

- per board: greenhouse:invisibletech 20, greenhouse:labelbox 13, greenhouse:scaleai 157, greenhouse:turing 31, lever:rws 148, workable:huggingface 10, workable:toloka-ai 586
- 965 postings in 671 families; 405 distinct descriptions
- open to Colombia: yes 3, unclear 12, no 950
- rules found (per distinct description): min_years 134, english_level 40, pay_usd_hour_max 6, pay_usd_year_max 22, hours_per_week 106
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +76 new, -78 closed, ~3 changed
