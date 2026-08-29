from __future__ import annotations

import os
from urllib import response

from dotenv import load_dotenv

from src.ai.contracts import AIRequest, AIProvider
from src.ai.pricing import ModelPricing, estimate_cost_usd
from src.ai.providers.gemini import GeminiProvider

from datetime import date


def create_request() -> AIRequest:
    return AIRequest(
        system_instruction=(
            "You are an assistant for a fictional clinic. "
            "Do not diagnose conditions or recommend treatments."
        ),
        prompt=(
            "A patient says: 'I want an appointment sometime next week.' "
            "In two short sentences, explain what information is still needed "
            "before an appointment can be requested."
        ),
        max_output_tokens=512,
    )


def run(provider: AIProvider, pricing: ModelPricing | None = None) -> None:
    response = provider.generate(create_request())

    print(f"Provider: {response.provider}")
    print(f"Model: {response.model}")
    print(f"Latency: {response.latency_ms:.2f} ms")
    print(f"Input tokens: {response.usage.input_tokens}")
    print(f"Output tokens: {response.usage.output_tokens}")
    print(f"Thought tokens: {response.usage.thought_tokens}")
    print(f"Total observed tokens: {response.usage.total_tokens}")
    print()
    print("Response:")
    print(response.text)
    
    if pricing is not None:
        estimated_cost = estimate_cost_usd(response.usage, pricing)
        print(f"Estimated cost: ${estimated_cost:.8f}")
 

def main() -> None:
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    if not model:
        raise RuntimeError("GEMINI_MODEL is not configured.")

    provider = GeminiProvider(
        api_key=api_key,
        model=model,
    )
    
    pricing = ModelPricing(
        provider="gemini",
        model=model,
        input_usd_per_million_tokens=0.75,
        output_usd_per_million_tokens=3.75,
        effective_date=date(2026, 8, 29),
        source_url="https://ai.google.dev/gemini-api/docs/pricing",
    )

    run(provider, pricing)


if __name__ == "__main__":
    main()
