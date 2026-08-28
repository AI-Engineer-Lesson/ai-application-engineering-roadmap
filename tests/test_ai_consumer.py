from src.ai.contracts import AIRequest, AIResponse, TokenUsage
from scripts.run_lesson_01 import run


class FakeProvider:
    def generate(self, request: AIRequest) -> AIResponse:
        return AIResponse(
            text="A preferred date and appointment type are still needed.",
            provider="fake",
            model="deterministic-test-model",
            latency_ms=1.0,
            usage=TokenUsage(
                input_tokens=10,
                output_tokens=8,
                thought_tokens=0,
            ),
        )


def test_run_accepts_provider_independent_implementation(
    capsys,
) -> None:
    run(FakeProvider())

    output = capsys.readouterr().out

    assert "Provider: fake" in output
    assert "Model: deterministic-test-model" in output
    assert "A preferred date" in output