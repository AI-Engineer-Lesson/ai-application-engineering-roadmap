from __future__ import annotations

import time

from google import genai
from google.genai import types

from src.ai.contracts import AIRequest, AIResponse, TokenUsage


class GeminiProvider:
    def __init__(
        self,
        *,
        api_key: str,
        model: str,
        client: genai.Client | None = None,
    ) -> None:
        self._model = model
        self._client = client or genai.Client(api_key=api_key)

    def generate(self, request: AIRequest) -> AIResponse:
        config = types.GenerateContentConfig(
            system_instruction=request.system_instruction,
            max_output_tokens=request.max_output_tokens,
        )

        started_at = time.perf_counter()

        response = self._client.models.generate_content(
            model=self._model,
            contents=request.prompt,
            config=config,
        )

        latency_ms = (time.perf_counter() - started_at) * 1000
        metadata = response.usage_metadata

        usage = TokenUsage(
            input_tokens=getattr(metadata, "prompt_token_count", 0) or 0,
            output_tokens=getattr(metadata, "candidates_token_count", 0) or 0,
            thought_tokens=getattr(metadata, "thoughts_token_count", 0) or 0,
        )

        return AIResponse(
            text=response.text or "",
            provider="gemini",
            model=self._model,
            latency_ms=latency_ms,
            usage=usage,
        )
