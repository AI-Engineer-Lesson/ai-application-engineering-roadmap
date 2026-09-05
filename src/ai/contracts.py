from dataclasses import dataclass
from typing import Mapping, Any, Protocol


@dataclass(frozen=True)
class AIRequest:
    prompt: str
    system_instruction: str | None = None
    max_output_tokens: int = 300
    response_schema: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class TokenUsage:
    input_tokens: int
    output_tokens: int
    thought_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens + self.thought_tokens


@dataclass(frozen=True)
class AIResponse:
    text: str
    provider: str
    model: str
    latency_ms: float
    usage: TokenUsage


class AIProvider(Protocol):
    def generate(self, request: AIRequest) -> AIResponse:
        """Generate a response using an external AI provider."""
        ...
