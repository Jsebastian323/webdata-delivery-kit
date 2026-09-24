from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixture_text():
    def load(name: str) -> str:
        return (FIXTURES / name).read_text(encoding="utf-8")

    return load


@pytest.fixture
def fixture_json():
    def load(name: str):
        return json.loads((FIXTURES / name).read_text(encoding="utf-8"))

    return load


class FakeSleep:
    """Records requested sleeps instead of waiting, so retry tests run instantly."""

    def __init__(self) -> None:
        self.calls: list[float] = []

    async def __call__(self, seconds: float) -> None:
        self.calls.append(seconds)


@pytest.fixture
def fake_sleep() -> FakeSleep:
    return FakeSleep()
