# QA report: remote AI-data jobs tracker

**READY** · 1067 rows delivered (1067 collected) · generated 2026-11-02T20:49:02+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1067 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1064/1067 postings have a country or region |

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
| countries | 99.6% |
| remote | 78.1% |
| open_to_colombia | 99.7% |
| employment_type | 77.3% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 13.3% |
| english_level | 21.3% |
| pay_usd_hour_max | 20.2% |
| pay_usd_year_max | 2.6% |
| hours_per_week | 27.1% |
| evidence | 42.9% |
| extracted_by | 42.9% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 1.8 s · 4.6 req/s

## Notes

- per board: greenhouse:invisibletech 23, greenhouse:labelbox 10, greenhouse:scaleai 169, greenhouse:turing 40, lever:rws 153, workable:huggingface 6, workable:toloka-ai 666
- 1067 postings in 793 families; 442 distinct descriptions
- open to Colombia: yes 12, unclear 3, no 1052
- rules found (per distinct description): min_years 139, english_level 59, pay_usd_hour_max 33, pay_usd_year_max 24, hours_per_week 120
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +204 new, -208 closed, ~174 changed
