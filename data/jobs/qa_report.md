# QA report: remote AI-data jobs tracker

**READY** · 528 rows delivered (528 collected) · generated 2026-10-13T18:21:52+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 528 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 520/528 postings have a country or region |

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
| countries | 98.3% |
| remote | 54.4% |
| open_to_colombia | 98.5% |
| employment_type | 52.8% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 26.5% |
| english_level | 31.2% |
| pay_usd_hour_max | 32.8% |
| pay_usd_year_max | 6.1% |
| hours_per_week | 44.5% |
| evidence | 78.6% |
| extracted_by | 78.6% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 2.4 s · 3.4 req/s

## Notes

- per board: greenhouse:handshake 9, greenhouse:invisibletech 22, greenhouse:labelbox 8, greenhouse:scaleai 182, greenhouse:turing 28, lever:rws 104, workable:huggingface 6, workable:toloka-ai 169
- 528 postings in 384 families; 375 distinct descriptions
- open to Colombia: yes 10, unclear 8, no 510
- rules found (per distinct description): min_years 136, english_level 49, pay_usd_hour_max 32, pay_usd_year_max 28, hours_per_week 116
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +115 new, -37 closed, ~1 changed
