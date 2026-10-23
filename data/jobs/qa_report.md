# QA report: remote AI-data jobs tracker

**READY** · 879 rows delivered (879 collected) · generated 2026-10-23T15:46:37+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 879 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 876/879 postings have a country or region |

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
| countries | 99.7% |
| remote | 74.3% |
| open_to_colombia | 99.7% |
| employment_type | 73.5% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 15.9% |
| english_level | 21.6% |
| pay_usd_hour_max | 20.9% |
| pay_usd_year_max | 2.7% |
| hours_per_week | 28.9% |
| evidence | 47.0% |
| extracted_by | 47.0% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 22.0 s · 0.4 req/s

## Notes

- per board: greenhouse:invisibletech 23, greenhouse:labelbox 7, greenhouse:scaleai 172, greenhouse:turing 31, lever:rws 135, workable:huggingface 6, workable:toloka-ai 505
- 879 postings in 656 families; 412 distinct descriptions
- open to Colombia: yes 10, unclear 3, no 866
- rules found (per distinct description): min_years 137, english_level 53, pay_usd_hour_max 32, pay_usd_year_max 20, hours_per_week 116
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +115 new, -12 closed, ~86 changed
