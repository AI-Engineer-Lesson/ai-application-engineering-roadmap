from datetime import date

import pytest

from src.ai.contracts import TokenUsage
from src.ai.pricing import ModelPricing, estimate_cost_usd


def test_estimate_cost_uses_input_output_and_thought_tokens() -> None:
    usage = TokenUsage(
        input_tokens=1_000_000,
        output_tokens=500_000,
        thought_tokens=500_000,
    )

    pricing = ModelPricing(
        provider="test-provider",
        model="test-model",
        input_usd_per_million_tokens=1.0,
        output_usd_per_million_tokens=2.0,
        effective_date=date(2026, 1, 1),
        source_url="https://example.com/test-pricing",
    )

    cost = estimate_cost_usd(usage, pricing)

    assert cost == pytest.approx(3.0)