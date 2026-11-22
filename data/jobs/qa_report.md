# QA report: remote AI-data jobs tracker

**READY** · 976 rows delivered (976 collected) · generated 2026-11-22T18:37:30+00:00

| Check | Result | Detail |
|---|---|---|
| schema | PASS | 976 rows valid |
| unique key | PASS | key = key |
| fetch failures | WARN | 2 request(s) failed after retries |
| every board answered | WARN | 6/8 boards; failed (carried over): {'workable:toloka-ai': 'FetchError: GET https://apply.workable.com/api/v1/widget/accounts/toloka-ai failed after 5 attempts: GET https://apply.workable.com/api/v1/widget/accounts/toloka-ai -> 429', 'workable:huggingface': 'FetchError: GET https://apply.workable.com/api/v1/widget/accounts/huggingface failed after 5 attempts: GET https://apply.workable.com/api/v1/widget/accounts/huggingface -> 429'} |
| no board went silent | PASS | no board dropped to zero |
| evidence is verbatim | PASS | every extracted value quotes its posting |
| location resolved | PASS | 366/378 postings have a country or region |

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
| remote | 77.0% |
| open_to_colombia | 98.8% |
| employment_type | 76.3% |
| published | 100.0% |
| family_id | 100.0% |
| description_sha1 | 100.0% |
| min_years | 14.2% |
| english_level | 4.2% |
| pay_usd_hour_max | 1.7% |
| pay_usd_year_max | 2.8% |
| hours_per_week | 10.8% |
| evidence | 27.4% |
| extracted_by | 27.4% |

## Fetch

16 requests · 8 retries · 2 failures · status {200: 6, 429: 10} · 240.8 s · 0.1 req/s

## Notes

- per board: greenhouse:invisibletech 21, greenhouse:labelbox 13, greenhouse:scaleai 166, greenhouse:turing 31, lever:rws 147
- 976 postings in 681 families; 368 distinct descriptions
- open to Colombia: yes 3, unclear 12, no 961
- rules found (per distinct description): min_years 134, english_level 38, pay_usd_hour_max 4, pay_usd_year_max 23, hours_per_week 102
- LLM: off (no OPENROUTER_API_KEY or --no-llm)
- since last snapshot: +1 new, -3 closed, ~3 changed
- 598 postings carried over from failed boards: ['workable:huggingface', 'workable:toloka-ai']
