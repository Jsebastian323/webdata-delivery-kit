# QA report: remote AI-data jobs tracker

**READY** · 1165 rows delivered (1165 collected) · generated 2026-10-16T15:23:40+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 1165 rows valid |
| unique key | PASS | key = key |
| fetch failures | PASS | 0 request(s) failed after retries |
| every board answered | PASS | 8/8 boards |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 1157/1165 postings have a country or region |

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
| remote | 79.7% |
| open_to_colombia | 99.3% |
| employment_type | 78.9% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 12.6% |
| english_level | 17.0% |
| pay_usd_hour_max | 67.1% |
| pay_usd_year_max | 2.7% |
| hours_per_week | 21.1% |
| evidence | 87.2% |
| extracted_by | 87.2% |

## Fetch

8 requests · 0 retries · 0 failures · status {200: 8} · 5.0 s · 1.6 req/s

## Notes

- per board: greenhouse:handshake 9, greenhouse:invisibletech 22, greenhouse:labelbox 7, greenhouse:scaleai 179, greenhouse:turing 29, lever:rws 95, workable:huggingface 6, workable:toloka-ai 818
- 1165 postings in 956 families; 386 distinct descriptions
- open to Colombia: yes 11, unclear 8, no 1146
- rules found (per distinct description): min_years 138, english_level 56, pay_usd_hour_max 52, pay_usd_year_max 28, hours_per_week 110
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +104 new, -171 closed, ~67 changed
