# Lesson 3 — Structured Output and Runtime Validation

**Module:** 01 — AI Application Contracts  
**Estimated time:** 60–90 minutes  
**Provider:** Google Gemini  
**Runtime validation:** Pydantic v2

## Goal

Replace informal model output such as:

```text
ACTION: ANSWER
MESSAGE: ...
```

with schema-constrained JSON that is validated by the application before it is used.

This lesson establishes an important production boundary:

```text
Structured generation helps shape the output.
Runtime validation decides whether the application accepts it.
```

Even valid JSON can contain invalid, missing, contradictory, or unsafe values. The application must therefore validate every model response and fail safely when validation does not pass.

## Learning Objectives

By the end of this lesson, you should be able to:

- Define an application-owned response schema.
- Request structured JSON from Gemini.
- Validate provider output using Pydantic.
- Reject malformed JSON, unsupported values, and inconsistent fields.
- Test the consumer without making network requests.
- Distinguish extraction readiness from a completed booking.
- Handle validation failures without performing a business action.

## Core Concepts

### 1. Structured generation

Structured generation asks the provider to return JSON matching a supplied schema. It improves consistency and prevents many formatting problems.

It can help guarantee the response shape supported by the provider, but it does not prove that:

- A phone number is real or acceptable.
- A date is available.
- A request is authorized.
- Required fields are semantically consistent.
- An appointment was actually created.

### 2. Runtime validation

Runtime validation is performed by normal application code after the model responds.

Pydantic parses the JSON and rejects output that violates the application contract. This includes malformed JSON, unknown status values, invalid phone-number formats, extra fields, and contradictory status information.

### 3. Semantic consistency

A response can have valid JSON syntax and still contradict itself:

```json
{
  "status": "ready_for_validation",
  "contact_number": null,
  "missing_fields": ["contact_number"]
}
```

This must be rejected because `ready_for_validation` means every required booking field was extracted, while the same response declares that the contact number is missing.

### 4. Safe failure

When validation fails, the application must:

- Reject the response.
- Perform no booking action.
- Avoid presenting unsupported claims as facts.
- Log the validation problem safely.
- Ask for clarification or retry only under controlled rules.

### 5. Booking boundary

`ready_for_validation` does not mean `appointment_confirmed`.

It only means the model appears to have extracted all required information. Deterministic application code must still:

1. Validate the submitted values.
2. Authenticate and authorize the request.
3. Resolve dates and time zones.
4. Check slot availability.
5. Obtain the user's confirmation.
6. Perform the database transaction.
7. Prevent duplicate requests.
8. Verify that the operation succeeded.
9. Record an audit trail.

## Part 1 — Dependency

Add Pydantic v2 to `requirements.txt`:

```text
pydantic>=2,<3
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Part 2 — Extend the Provider Contract

The provider-neutral `AIRequest` accepts an optional response schema:

```python
from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class AIRequest:
    prompt: str
    system_instruction: str | None = None
    max_output_tokens: int = 300
    response_schema: Mapping[str, Any] | None = None
```

The application owns the generic schema. Individual provider adapters decide how to translate it into provider-specific configuration.

## Part 3 — Configure Gemini Structured Output

The Gemini adapter passes the schema through `response_json_schema` and requests JSON using `response_mime_type`:

```python
def generate(self, request: AIRequest) -> AIResponse:
    config: dict[str, object] = {
        "system_instruction": request.system_instruction,
        "max_output_tokens": request.max_output_tokens,
        "thinking_config": {
            "thinking_level": "low",
        },
    }

    if request.response_schema is not None:
        config["response_mime_type"] = "application/json"
        config["response_json_schema"] = dict(request.response_schema)

    response = self._client.models.generate_content(
        model=self._model,
        contents=request.prompt,
        config=config,
    )
```

Provider-specific configuration stays inside `GeminiProvider`; the rest of the application continues to depend on the generic `AIProvider` contract.

## Part 4 — Application-Owned Scheduling Schema

Create `src/ai/scheduling.py` with an `AppointmentExtraction` Pydantic model.

The schema defines these fields:

| Field | Meaning |
|---|---|
| `status` | Extraction result: ready, needs clarification, or out of scope |
| `patient_name` | Name exactly as supplied by the user |
| `contact_number` | Philippine mobile number beginning with `09` and containing 11 digits |
| `preferred_date` | Requested appointment date |
| `preferred_time` | Requested appointment time |
| `request_type` | Supported clinic request type |
| `reason_for_visit` | User-provided reason for the visit |
| `missing_fields` | Required fields that are missing or invalid |

Use strict field options and forbid unexpected properties:

```python
class AppointmentExtraction(BaseModel):
    model_config = ConfigDict(extra="forbid")
```

The contact number is checked deterministically:

```python
@field_validator("contact_number")
@classmethod
def validate_contact_number(cls, value: str | None) -> str | None:
    if value is not None and re.fullmatch(r"09\d{9}", value) is None:
        raise ValueError(
            "contact_number must begin with 09 and contain 11 digits"
        )

    return value
```

The model validator checks status consistency:

- `ready_for_validation` requires every booking field and an empty `missing_fields` list.
- `needs_clarification` requires at least one declared missing field.
- A field cannot be listed as missing when it already contains a value.

## Part 5 — Parse and Wrap Validation Errors

Provider output is parsed using `model_validate_json`:

```python
class StructuredOutputError(RuntimeError):
    """Raised when provider output fails application validation."""


def parse_appointment_extraction(
    raw_output: str,
) -> AppointmentExtraction:
    try:
        return AppointmentExtraction.model_validate_json(raw_output)
    except ValidationError as exc:
        raise StructuredOutputError(
            "The AI provider returned an invalid scheduling response."
        ) from exc
```

This prevents Pydantic-specific errors from leaking through the application boundary while preserving the original exception as the cause for controlled diagnostics.

## Part 6 — Build the Structured Request

Generate the JSON Schema from the Pydantic model:

```python
response_schema=AppointmentExtraction.model_json_schema()
```

The system instruction should require schema-matching JSON and prohibit invented or silently corrected information:

```text
Return only JSON matching the supplied response schema. Preserve user-provided values. Do not invent or silently correct missing or invalid information.
```

Trusted clinic policy remains separate from untrusted user content, following the trust boundaries established in Lesson 2.

## Part 7 — Deterministic Tests

The test suite covers seven Lesson 3 behaviors:

1. Valid structured output is accepted.
2. Malformed JSON is rejected.
3. An unknown status is rejected.
4. An invalid phone number is rejected.
5. A ready status cannot omit required fields.
6. A clarification status must declare missing fields.
7. The consumer works with a deterministic fake provider.

The malformed-JSON case must be syntactically invalid:

```python
def test_malformed_json_is_rejected() -> None:
    with pytest.raises(StructuredOutputError):
        parse_appointment_extraction(
            '{"status": "ready_for_validation"'
        )
```

The missing closing brace makes parsing fail. By contrast, `{"status": "ready_for_validation"}` is valid JSON syntax but fails later because it does not satisfy the schema.

The `FakeProvider` allows contract and validation tests to run without network access, API keys, latency, or nondeterministic model behavior.

Run:

```bash
pytest
```

Expected total:

```text
13 passed
```

## Part 8 — Live Experiments

Run four synthetic cases using `scripts/run_lesson_03.py`:

| Case | Expected result |
|---|---|
| Complete valid request | `ready_for_validation` |
| Missing information | `needs_clarification` |
| Invalid contact number | Clarification or safe rejection |
| Out-of-scope medical request | `out_of_scope` |

Run:

```bash
python -m scripts.run_lesson_03
```

For every case, record:

- Raw structured output
- Expected and actual status
- Whether Pydantic accepted or rejected it
- Latency and token usage
- Any important discrepancy

The invalid-number case may return `needs_clarification` with a null contact number or fail runtime validation. Both outcomes are safer than accepting or silently correcting the invalid value.

If a seemingly valid request fails validation, the response must still be rejected. Record the failure as evidence that schema-guided generation remains probabilistic and that application validation is necessary. No booking action should occur.

## Results from This Implementation

- All 13 deterministic tests passed.
- All four live experiments returned syntactically valid JSON.
- The missing-information and out-of-scope responses passed runtime validation.
- The invalid contact number was rejected safely by Pydantic.
- The complete request selected the expected status but failed runtime validation, demonstrating that a plausible status does not make the entire response valid.
- No response created or claimed to create an appointment.

## Production Implications

- Treat every model response as untrusted until validated.
- Keep provider configuration behind an adapter.
- Keep schemas owned by the application rather than the provider.
- Use deterministic code for authorization and business rules.
- Restrict tool access and side effects independently of model output.
- Never trigger a booking by searching model text for a status string.
- Preserve validation diagnostics for observability without exposing sensitive data.
- Consider controlled retry limits and explicit fallback behavior in later production work.

## Limitations

- Schema-constrained generation does not guarantee correct business values.
- Pydantic validates only the rules explicitly implemented in the model.
- Phone-number format validation does not prove ownership or reachability.
- Date parsing does not establish slot availability or clinic operating hours.
- No authentication, authorization, confirmation, database write, retry policy, or idempotency protection is implemented yet.
- The exact validation cause for the rejected complete live request was not captured in the recorded result.

## Acceptance Criteria

Lesson 3 is complete when:

- [x] The application owns the response schema.
- [x] The Gemini adapter supports structured JSON output.
- [x] Pydantic runtime validation is implemented.
- [x] Tests run without network access.
- [x] Malformed JSON is rejected.
- [x] Invalid field values are rejected.
- [x] Inconsistent status and field combinations are rejected.
- [x] Four live experiments are documented.
- [x] Invalid structured output fails safely.
- [x] No booking action is performed.
- [x] `RESULTS.md` contains test and experiment evidence.
- [x] `ASSESSMENT.md` explains the core concepts.
- [x] No secrets or real patient data are committed.

## Final Verification

Before committing the lesson, run:

```bash
git diff --check
pytest
python -m scripts.run_lesson_03
```

Then commit the completed Lesson 3 work.

## Key Takeaway

Structured generation improves the shape and consistency of model output. Runtime validation independently checks whether that output satisfies the application's rules. Correctly formatted JSON can still contain invalid or contradictory data, so validation and deterministic business controls remain mandatory.
