# QA report: remote AI-data jobs tracker

**READY** · 1199 rows delivered (1199 collected) · generated 2026-10-17T14:14:17+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1199 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1191/1199 postings have a country or region |

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
| remote | 79.9% |
| open_to_colombia | 99.3% |
| employment_type | 79.1% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 12.4% |
| english_level | 16.5% |
| pay_usd_hour_max | 65.2% |
| pay_usd_year_max | 2.7% |
| hours_per_week | 20.5% |
| evidence | 84.9% |
| extracted_by | 84.9% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 2.5 s · 3.2 req/s

## Notes

- per board: greenhouse:handshake 9, greenhouse:invisibletech 23, greenhouse:labelbox 7, greenhouse:scaleai 182, greenhouse:turing 30, lever:rws 95, workable:huggingface 6, workable:toloka-ai 847
- 1199 postings in 960 families; 391 distinct descriptions
- open to Colombia: yes 11, unclear 8, no 1180
- rules found (per distinct description): min_years 140, english_level 56, pay_usd_hour_max 52, pay_usd_year_max 28, hours_per_week 110
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +35 new, -1 closed, ~1 changed
