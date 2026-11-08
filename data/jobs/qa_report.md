# QA report: remote AI-data jobs tracker

**READY** · 1193 rows delivered (1193 collected) · generated 2026-11-08T17:06:07+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1193 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1184/1193 postings have a country or region |

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
| employment_type | 79.5% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 12.4% |
| english_level | 23.1% |
| pay_usd_hour_max | 10.2% |
| pay_usd_year_max | 2.4% |
| hours_per_week | 15.3% |
| evidence | 43.0% |
| extracted_by | 43.0% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 2.2 s · 3.7 req/s

## Notes

- per board: greenhouse:invisibletech 20, greenhouse:labelbox 10, greenhouse:scaleai 168, greenhouse:turing 47, lever:rws 125, workable:huggingface 6, workable:toloka-ai 817
- 1193 postings in 772 families; 419 distinct descriptions
- open to Colombia: yes 14, unclear 9, no 1170
- rules found (per distinct description): min_years 142, english_level 47, pay_usd_hour_max 32, pay_usd_year_max 25, hours_per_week 107
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +1 new, -0 closed, ~1 changed
