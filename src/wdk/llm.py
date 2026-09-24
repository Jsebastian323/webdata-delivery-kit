"""Structured extraction through OpenRouter, guarded by verbatim evidence.

The model must return, for every field, the value AND the exact passage of the source that
states it. A value whose passage is not literally in the source, or whose passage does not
contain the value, is discarded. A missing field is recoverable; an invented one ends up in
a client's spreadsheet.
"""

from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass, field

from .fetch import Fetcher
from .normalize import clean_text, fold

log = logging.getLogger("wdk.llm")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "anthropic/claude-haiku-4.5"
SYSTEM_PROMPT = (
    "You extract facts from job postings. For each requested field return its value and the "
    "exact passage of the posting that states it, copied character for character. If the posting "
    "does not state a field, return null for both. Never infer, estimate or convert units."
)


@dataclass(frozen=True)
class FieldSpec:
    name: str
    description: str
    kind: str = "str"  # "str" | "int" | "float"


@dataclass
class Extraction:
    values: dict = field(default_factory=dict)
    evidence: dict[str, str] = field(default_factory=dict)
    rejected: dict[str, str] = field(default_factory=dict)


def evidence_supported(source: str, evidence: str | None) -> bool:
    """Is ``evidence`` a literal passage of ``source`` (ignoring whitespace and case)?"""
    passage = clean_text(evidence).casefold()
    return len(passage) >= 3 and passage in clean_text(source).casefold()


def value_in_evidence(value, evidence: str, kind: str) -> bool:
    """The value must be readable in its own evidence, or the pairing is fabricated."""
    if kind in ("int", "float"):
        number = f"{float(value):g}"
        return any(f"{float(n):g}" == number for n in re.findall(r"\d+(?:\.\d+)?", evidence.replace(",", "")))
    return fold(str(value)) in fold(evidence)


def _cast(value, kind: str):
    if value is None or value == "":
        return None
    if kind == "int":
        return int(float(value))
    if kind == "float":
        return float(value)
    return clean_text(str(value))


def _response_schema(fields: list[FieldSpec]) -> dict:
    item = {
        "type": "object",
        "properties": {"value": {"type": ["string", "null"]}, "evidence": {"type": ["string", "null"]}},
        "required": ["value", "evidence"],
        "additionalProperties": False,
    }
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "extraction",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {f.name: item for f in fields},
                "required": [f.name for f in fields],
                "additionalProperties": False,
            },
        },
    }


def _parse_json(content: str) -> dict:
    content = content.strip()
    if content.startswith("```"):
        content = content.strip("`").removeprefix("json").strip()
    return json.loads(content)


class LLMExtractor:
    """Calls OpenRouter with a strict JSON schema and keeps only evidence-backed values."""

    def __init__(
        self,
        fetcher: Fetcher,
        *,
        api_key: str,
        model: str | None = None,
        max_calls: int = 40,
        max_chars: int = 12000,
    ) -> None:
        self.fetcher = fetcher
        self.api_key = api_key
        self.model = model or os.getenv("WDK_LLM_MODEL") or DEFAULT_MODEL
        self.max_calls = max_calls
        self.max_chars = max_chars
        self.calls = 0

    @classmethod
    def from_env(cls, fetcher: Fetcher) -> LLMExtractor | None:
        key = os.getenv("OPENROUTER_API_KEY")
        if not key:
            return None
        return cls(fetcher, api_key=key, max_calls=int(os.getenv("WDK_LLM_MAX_CALLS", "40")))

    async def extract(self, text: str, fields: list[FieldSpec]) -> Extraction:
        result = Extraction()
        if not fields:
            return result
        if self.calls >= self.max_calls:
            result.rejected = {f.name: "LLM call budget exhausted" for f in fields}
            return result
        self.calls += 1
        listing = "\n".join(f"- {f.name}: {f.description}" for f in fields)
        payload = {
            "model": self.model,
            "temperature": 0,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Fields:\n{listing}\n\nPosting:\n{text[: self.max_chars]}"},
            ],
            "response_format": _response_schema(fields),
        }
        response = await self.fetcher.post(
            OPENROUTER_URL,
            json=payload,
            headers={"Authorization": f"Bearer {self.api_key}", "X-Title": "webdata-delivery-kit"},
        )
        data = _parse_json(response.json()["choices"][0]["message"]["content"])
        for spec in fields:
            item = data.get(spec.name) or {}
            raw_value, evidence = item.get("value"), item.get("evidence")
            if raw_value in (None, ""):
                continue
            try:
                value = _cast(raw_value, spec.kind)
            except (TypeError, ValueError):
                result.rejected[spec.name] = f"not a {spec.kind}: {raw_value!r}"
                continue
            if not evidence_supported(text, evidence):
                result.rejected[spec.name] = "evidence is not a passage of the posting"
            elif not value_in_evidence(value, evidence, spec.kind):
                result.rejected[spec.name] = "value does not appear in its evidence"
            else:
                result.values[spec.name] = value
                result.evidence[spec.name] = clean_text(evidence)
        if result.rejected:
            log.info("LLM values rejected: %s", result.rejected)
        return result
