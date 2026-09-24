import asyncio
import json

import httpx

from wdk.fetch import Fetcher
from wdk.llm import FieldSpec, LLMExtractor, evidence_supported, value_in_evidence

POSTING = (
    "At least 5+ years of relevant experience in data engineering.\n"
    "English proficiency: Upper-intermediate (B2) or above (required).\n"
    "Contributors can earn up to $25 per hour equivalent."
)
FIELDS = [
    FieldSpec("min_years", "minimum years of experience", "int"),
    FieldSpec("english_level", "English level"),
    FieldSpec("pay_usd_hour_max", "max hourly pay in USD", "float"),
    FieldSpec("hours_per_week", "weekly hours"),
]


def test_evidence_must_be_a_literal_passage():
    assert evidence_supported(POSTING, "english proficiency:   upper-intermediate (B2)")
    assert not evidence_supported(POSTING, "Fluent English required")
    assert not evidence_supported(POSTING, "B2")  # too short to prove anything
    assert not evidence_supported(POSTING, None)


def test_value_must_be_readable_in_its_evidence():
    assert value_in_evidence(5, "At least 5+ years of relevant experience", "int")
    assert not value_in_evidence(7, "At least 5+ years of relevant experience", "int")
    assert value_in_evidence(25.0, "up to $25 per hour equivalent", "float")
    assert value_in_evidence("B2", "Upper-intermediate (B2) or above", "str")


def _fake_openrouter(answer: dict, seen: list):
    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        body = {"choices": [{"message": {"content": json.dumps(answer)}}]}
        return httpx.Response(200, json=body)

    return httpx.MockTransport(handler)


def test_extractor_keeps_only_evidence_backed_values():
    answer = {
        "min_years": {"value": "5", "evidence": "At least 5+ years of relevant experience"},
        "english_level": {"value": "C1", "evidence": "English proficiency: Upper-intermediate (B2)"},
        "pay_usd_hour_max": {"value": "40", "evidence": "earn up to $40 per hour"},
        "hours_per_week": {"value": None, "evidence": None},
    }
    seen: list[httpx.Request] = []

    async def go():
        fetcher = Fetcher(transport=_fake_openrouter(answer, seen), respect_robots=False, rate=0)
        async with fetcher:
            return await LLMExtractor(fetcher, api_key="test-key").extract(POSTING, FIELDS)

    result = asyncio.run(go())
    assert result.values == {"min_years": 5}
    assert result.rejected == {
        "english_level": "value does not appear in its evidence",
        "pay_usd_hour_max": "evidence is not a passage of the posting",
    }
    payload = json.loads(seen[0].content)
    assert payload["response_format"]["json_schema"]["strict"] is True
    assert payload["temperature"] == 0
    assert seen[0].headers["authorization"] == "Bearer test-key"


def test_call_budget_is_enforced_without_calling_the_api():
    def handler(request):
        raise AssertionError("no call expected once the budget is spent")

    async def go():
        async with Fetcher(transport=httpx.MockTransport(handler), respect_robots=False, rate=0) as fetcher:
            return await LLMExtractor(fetcher, api_key="k", max_calls=0).extract(POSTING, FIELDS[:1])

    result = asyncio.run(go())
    assert result.values == {} and "budget" in result.rejected["min_years"]
