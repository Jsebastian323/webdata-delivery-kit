# QA report: remote AI-data jobs tracker

**READY** · 978 rows delivered (978 collected) · generated 2026-11-21T18:01:41+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 978 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 966/978 postings have a country or region |

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
| remote | 76.9% |
| open_to_colombia | 98.8% |
| employment_type | 76.2% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 14.3% |
| english_level | 4.2% |
| pay_usd_hour_max | 1.7% |
| pay_usd_year_max | 2.8% |
| hours_per_week | 10.7% |
| evidence | 27.4% |
| extracted_by | 27.4% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 3.4 s · 2.3 req/s

## Notes

- per board: greenhouse:invisibletech 21, greenhouse:labelbox 12, greenhouse:scaleai 169, greenhouse:turing 31, lever:rws 147, workable:huggingface 10, workable:toloka-ai 588
- 978 postings in 683 families; 416 distinct descriptions
- open to Colombia: yes 3, unclear 12, no 963
- rules found (per distinct description): min_years 136, english_level 39, pay_usd_hour_max 6, pay_usd_year_max 23, hours_per_week 102
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +99 new, -51 closed, ~14 changed
