# QA report: remote AI-data jobs tracker

**READY** · 1093 rows delivered (1093 collected) · generated 2026-11-04T18:40:32+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1093 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1090/1093 postings have a country or region |

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
| remote | 78.8% |
| open_to_colombia | 99.7% |
| employment_type | 78.0% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 12.4% |
| english_level | 23.5% |
| pay_usd_hour_max | 22.2% |
| pay_usd_year_max | 2.6% |
| hours_per_week | 29.3% |
| evidence | 44.3% |
| extracted_by | 44.3% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 2.8 s · 2.9 req/s

## Notes

- per board: greenhouse:invisibletech 22, greenhouse:labelbox 10, greenhouse:scaleai 167, greenhouse:turing 42, lever:rws 150, workable:huggingface 6, workable:toloka-ai 696
- 1093 postings in 791 families; 443 distinct descriptions
- open to Colombia: yes 13, unclear 3, no 1077
- rules found (per distinct description): min_years 133, english_level 63, pay_usd_hour_max 36, pay_usd_year_max 24, hours_per_week 125
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +88 new, -59 closed, ~301 changed
