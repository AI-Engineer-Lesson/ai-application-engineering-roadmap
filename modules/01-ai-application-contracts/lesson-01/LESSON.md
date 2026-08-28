# Lesson 1 — Provider-Neutral AI Boundaries, Model Capabilities, Cost, and Latency

## Estimated Time

45–90 minutes

## Goal

Build a small provider-neutral AI boundary and use it to measure one real model request.

The application must not directly depend on Gemini, OpenAI, or another provider outside the provider adapter.

By the end of this lesson, you will have:

- An application-owned AI interface
- A Gemini implementation of that interface
- A provider-independent request and response contract
- Environment-based configuration
- Latency and token-usage measurements
- Estimated request cost
- Deterministic tests that do not call the real provider
- A documented comparison between deterministic and probabilistic behavior

---

## Why This Matters

A basic AI integration often starts like this:

```python
response = provider.models.generate_content(...)
```

This works for an experiment, but it creates problems when used throughout an application:

- Business logic becomes tied to one SDK.
- Provider response formats leak into the application.
- Tests require network access or extensive mocking.
- Changing models becomes risky.
- Token, latency, and cost tracking become inconsistent.
- Provider failures become application failures without a controlled boundary.

A production application should own the contract it needs.

```text
Application
    |
    v
Application-owned AI interface
    |
    v
Provider adapter
    |
    v
External model API
```

The application should understand its own request and response types. Only the adapter should understand the provider SDK.

---

## Learning Objectives

After completing this lesson, you should be able to:

1. Explain why provider SDK objects should not spread through application code.
2. Define provider-independent request and response contracts.
3. Implement an application-owned provider interface.
4. isolate Gemini-specific behavior inside one adapter.
5. Measure latency and token usage.
6. Estimate cost using dated configuration.
7. Test application logic without calling a real model.
8. Separate deterministic application behavior from probabilistic model behavior.

---

# Part 1 — Prepare the Python Environment

Use Python 3.11 or newer.

From the repository root:

```bash
python --version
python -m venv .venv
```

Activate the environment.

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
.venv\Scripts\activate.bat
```

### macOS or Linux

```bash
source .venv/bin/activate
```

Install the initial dependencies:

```bash
python -m pip install --upgrade pip
pip install google-genai python-dotenv pytest
```

Create `requirements.txt`:

```text
google-genai
python-dotenv
pytest
```

Do not include version numbers yet. Dependency locking and reproducible builds will be handled in a later deployment lesson.

---

# Part 2 — Create the Initial Structure

Create the following structure:

```text
.
├── .env.example
├── requirements.txt
├── src/
│   ├── __init__.py
│   └── ai/
│       ├── __init__.py
│       ├── contracts.py
│       ├── pricing.py
│       └── providers/
│           ├── __init__.py
│           └── gemini.py
├── scripts/
│   └── run_lesson_01.py
├── tests/
│   ├── __init__.py
│   ├── test_ai_consumer.py
│   └── test_pricing.py
└── modules/
    └── 01-ai-application-contracts/
        └── lesson-01/
            ├── LESSON.md
            ├── RESULTS.md
            └── ASSESSMENT.md
```

The empty `__init__.py` files make the relevant directories importable Python packages.

---

# Part 3 — Define Application-Owned Contracts

Create `src/ai/contracts.py`:

```python
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class AIRequest:
    prompt: str
    system_instruction: str | None = None
    temperature: float = 0.0
    max_output_tokens: int = 300


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
```

## Observe the Boundary

These types belong to the application.

They do not import:

- Gemini SDK types
- OpenAI SDK types
- Provider-specific token objects
- Provider-specific response objects

The application receives the same `AIResponse` shape regardless of the selected provider.

`Protocol` provides structural typing. A provider implementation satisfies the interface when it implements the required method with the expected shape.

---

# Part 4 — Keep Pricing Time-Sensitive

Provider pricing changes. Avoid scattering permanent-looking prices throughout business logic.

Create `src/ai/pricing.py`:

```python
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
```

## Important Limitation

The calculation is deterministic, but the pricing inputs are not permanent facts.

Before recording a real estimate:

1. Open the official provider pricing page.
2. Find the exact model used.
3. Confirm whether thought or reasoning tokens are billed as output.
4. Record the price, effective date, and source URL in `RESULTS.md`.

Do not guess pricing values.

Official Gemini pricing:

```text
https://ai.google.dev/gemini-api/docs/pricing
```

---

# Part 5 — Implement the Gemini Adapter

Create `src/ai/providers/gemini.py`:

```python
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
            temperature=request.temperature,
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
```

This is the only file in the current implementation that should understand Gemini-specific SDK objects.

If the SDK changes later, most application code should remain unchanged.

---

# Part 6 — Configure the Application Safely

Create `.env.example`:

```dotenv
GEMINI_API_KEY=replace-with-your-api-key
GEMINI_MODEL=replace-with-an-available-model
```

Create a local `.env` with the real values.

The `.env` file must remain ignored by Git.

Verify:

```bash
git status
```

The real `.env` must not appear as an untracked or tracked file.

Do not print the API key in logs, test output, screenshots, or `RESULTS.md`.

---

# Part 7 — Run a Measured Request

Create `scripts/run_lesson_01.py`:

```python
from __future__ import annotations

import os

from dotenv import load_dotenv

from src.ai.contracts import AIRequest, AIProvider
from src.ai.pricing import ModelPricing, estimate_cost_usd
from src.ai.providers.gemini import GeminiProvider


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
        temperature=0.0,
        max_output_tokens=200,
    )


def run(provider: AIProvider) -> None:
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

    # Add the verified pricing values before enabling this section.
    #
    # pricing = ModelPricing(
    #     provider="gemini",
    #     model=response.model,
    #     input_usd_per_million_tokens=0.0,
    #     output_usd_per_million_tokens=0.0,
    #     effective_date=date(YYYY, MM, DD),
    #     source_url="https://ai.google.dev/gemini-api/docs/pricing",
    # )
    #
    # estimated_cost = estimate_cost_usd(response.usage, pricing)
    # print(f"Estimated cost: ${estimated_cost:.8f}")


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

    run(provider)


if __name__ == "__main__":
    main()
```

Run it from the repository root:

```bash
python -m scripts.run_lesson_01
```

Record the following in `RESULTS.md`:

- Date and time
- Provider
- Exact model identifier
- Prompt
- Model response
- Latency
- Input tokens
- Output tokens
- Thought tokens
- Total observed tokens
- Verified pricing source
- Estimated cost
- Observations

Never record the API key.

---

# Part 8 — Prove That the Consumer Is Provider-Neutral

Create `tests/test_ai_consumer.py`:

```python
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
```

This test does not:

- Require an API key
- Use the internet
- Call Gemini
- Depend on Gemini response objects
- Consume paid tokens

The fake implements the application-owned interface through structural typing.

---

# Part 9 — Test the Deterministic Cost Calculation

Create `tests/test_pricing.py`:

```python
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
```

Run the test suite:

```bash
pytest
```

Expected result:

```text
2 passed
```

Your exact output may include additional environment or timing information.

---

# Part 10 — Run a Small Variability Experiment

Run the real request three times without changing:

- The prompt
- The system instruction
- The model
- The temperature
- The output-token limit

Record each response and measurement in `RESULTS.md`.

Use a comparison table:

| Run | Latency | Input tokens | Output tokens | Thought tokens | Meaningfully different? |
| --: | ------: | -----------: | ------------: | -------------: | ----------------------- |
|   1 |         |              |               |                |                         |
|   2 |         |              |               |                |                         |
|   3 |         |              |               |                |                         |

Then answer:

1. Were the responses textually identical?
2. Were they semantically equivalent?
3. Was latency stable?
4. Was token usage stable?
5. Did `temperature=0.0` make the complete system deterministic?
6. Which observed values can your application control?
7. Which observed values remain controlled by the provider or model?

Temperature zero may reduce variability, but it does not guarantee that a hosted model API will always return identical output.

---

# Part 11 — Deterministic and Probabilistic Responsibilities

Classify each responsibility:

| Responsibility                                  | Expected owner                   |
| ----------------------------------------------- | -------------------------------- |
| Selecting the configured provider               | Application                      |
| Selecting the configured model                  | Application                      |
| Verifying that an API key exists                | Application                      |
| Authorizing a user                              | Application                      |
| Enforcing appointment business rules            | Application                      |
| Producing natural-language output               | Model                            |
| Exact wording of the response                   | Model                            |
| Provider-side processing time                   | Provider                         |
| Measuring elapsed request time                  | Application                      |
| Returning provider token metadata               | Provider                         |
| Calculating estimated cost from recorded prices | Application                      |
| Deciding whether a mutation is allowed          | Application                      |
| Retrying a failed request                       | Application policy               |
| Guaranteeing factual correctness                | Cannot be assumed from the model |

The model may propose or extract information. Deterministic application code must validate anything that affects permissions, stored state, money, or real-world actions.

---

# Required `RESULTS.md`

Create `modules/01-ai-application-contracts/lesson-01/RESULTS.md`:

````markdown
# Lesson 1 Results

## Environment

- Date:
- Python version:
- Operating system:
- Provider:
- Model:
- SDK:
- SDK version:

## Test Result

Command:

```bash
pytest
```
````

Output:

```text
Paste the complete test summary here.
```

## Request Configuration

### System Instruction

```text
Paste the system instruction here.
```

### Prompt

```text
Paste the prompt here.
```

### Parameters

- Temperature:
- Maximum output tokens:

## Variability Experiment

| Run | Latency | Input tokens | Output tokens | Thought tokens | Meaningfully different? |
| --: | ------: | -----------: | ------------: | -------------: | ----------------------- |
|   1 |         |              |               |                |                         |
|   2 |         |              |               |                |                         |
|   3 |         |              |               |                |                         |

### Run 1 Response

```text
Paste the response here.
```

### Run 2 Response

```text
Paste the response here.
```

### Run 3 Response

```text
Paste the response here.
```

## Pricing

- Pricing effective date:
- Official source:
- Input price per one million tokens:
- Output price per one million tokens:
- Treatment of thought/reasoning tokens:
- Estimated cost per run:
- Calculation:

## Analysis

### Were the responses textually identical?

Answer:

### Were they semantically equivalent?

Answer:

### Was latency stable?

Answer:

### Was token usage stable?

Answer:

### Did temperature zero make the complete system deterministic?

Answer:

### What does the application control?

Answer:

### What remains controlled by the provider or model?

Answer:

## Architecture Explanation

Explain why `AIRequest`, `AIResponse`, and `AIProvider` belong to the application instead of the Gemini adapter.

Answer:

## Failure Considerations

Describe the expected application behavior for:

- Missing API key
- Invalid model identifier
- Authentication failure
- Rate limit
- Timeout
- Empty model response
- Missing usage metadata

Answer:

## Additional Observations

Add any unexpected behavior, SDK differences, limitations, or questions discovered during the exercise.

````

---

# Required `ASSESSMENT.md`

Create `modules/01-ai-application-contracts/lesson-01/ASSESSMENT.md`:

```markdown
# Lesson 1 Assessment

## Status

- [ ] Implementation complete
- [ ] Real provider request completed
- [ ] Three-run experiment completed
- [ ] Pricing verified from the official source
- [ ] Cost estimate calculated
- [ ] Automated tests passing
- [ ] Results documented
- [ ] Knowledge check answered
- [ ] Ready for review

## Knowledge Check

### 1. Why should the rest of the application not directly depend on Gemini SDK response objects?

Answer:

### 2. What is the difference between the application-owned interface and the Gemini adapter?

Answer:

### 3. Why is a fake provider better than calling the real API in a unit test?

Answer:

### 4. Why should pricing include an effective date and source URL?

Answer:

### 5. Does temperature zero guarantee identical responses? Explain.

Answer:

### 6. Which operations must remain deterministic even when an AI model is involved?

Answer:

### 7. If Gemini changes its usage-metadata field names, which part of this implementation should change?

Answer:

### 8. What information could be lost by converting a provider response into the current `AIResponse` contract?

Answer:

## Completion Evidence

- Test command:
- Test result:
- Real request completed:
- Results file updated:
- Commit hash:

## Reviewer Decision

- [ ] Passed
- [ ] Passed with required corrections
- [ ] Not yet passed

## Reviewer Notes

To be completed during review.
````

---

# Acceptance Criteria

Lesson 1 is complete when:

- [ ] The virtual environment works.
- [ ] The real `.env` is excluded from Git.
- [ ] Application contracts do not import provider SDK types.
- [ ] Gemini-specific code is isolated in its adapter.
- [ ] A real request completes successfully.
- [ ] Three identical-configuration runs are documented.
- [ ] Latency and token usage are recorded.
- [ ] Pricing is verified from an official source.
- [ ] Estimated cost is calculated.
- [ ] Unit tests pass without network access.
- [ ] All knowledge-check questions are answered.
- [ ] No real secrets or sensitive data are committed.

## Stop Point

Once the implementation, `RESULTS.md`, and `ASSESSMENT.md` are complete, stop and request a lesson review before proceeding to Lesson 2.
