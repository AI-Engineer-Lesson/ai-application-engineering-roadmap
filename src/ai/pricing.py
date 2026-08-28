from dataclasses import dataclass
from datetime import date

from src.ai.contracts import TokenUsage


@dataclass(frozen=True)
class ModelPricing:
    provider: str
    model: str
    input_usd_per_million_tokens: float
    output_usd_per_million_tokens: float
    effective_date: date
    source_url: str


def estimate_cost_usd(
    usage: TokenUsage,
    pricing: ModelPricing,
) -> float:
    input_cost = (
        usage.input_tokens
        / 1_000_000
        * pricing.input_usd_per_million_tokens
    )

    billed_output_tokens = usage.output_tokens + usage.thought_tokens
    output_cost = (
        billed_output_tokens
        / 1_000_000
        * pricing.output_usd_per_million_tokens
    )

    return input_cost + output_cost
