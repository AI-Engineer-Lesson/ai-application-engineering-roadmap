# Fast-Track Session 1 — Deterministic Validation and Safe Decisions

**Repository position:** Module 01, Lesson 04

**Estimated core time:** 45–60 minutes

**Network/API calls:** None

## Outcome

Lesson 3 produced schema-constrained JSON and validated it with Pydantic. This lesson adds the final boundary before the application may look up appointment slots:

```text
Model output → schema validation → semantic validation → business rules → slot lookup
```

You will create a deterministic, side-effect-free decision layer. It may allow **slot lookup**, but it must never book or claim to book an appointment.

## What matters

| Layer | Example failure |
|---|---|
| Schema/runtime | Invalid JSON, wrong type, unknown status |
| Semantic | Blank name, past appointment date |
| Business rule | Clinic closed, outside operating hours |
| Safe abstention | Missing information or out-of-scope request |

The model extracts information. Application code owns the decision.

## 1. Create the decision contract

Create `src/ai/decisions.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time
from enum import StrEnum

from src.ai.scheduling import (
    AppointmentExtraction,
    StructuredOutputError,
    parse_appointment_extraction,
)


class DecisionStatus(StrEnum):
    READY_FOR_SLOT_LOOKUP = "ready_for_slot_lookup"
    ABSTAIN = "abstain"


class FailureCategory(StrEnum):
    NONE = "none"
    INSUFFICIENT_INFORMATION = "insufficient_information"
    OUT_OF_SCOPE = "out_of_scope"
    STRUCTURED_OUTPUT_INVALID = "structured_output_invalid"
    SEMANTIC_VALIDATION_FAILED = "semantic_validation_failed"
    BUSINESS_RULE_REJECTED = "business_rule_rejected"


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    field: str | None = None


@dataclass(frozen=True)
class SchedulingRules:
    minimum_notice_days: int = 1
    maximum_advance_days: int = 60
    opens_at: time = time(9, 0)
    closes_at: time = time(17, 0)
    closed_weekdays: frozenset[int] = frozenset({6})


@dataclass(frozen=True)
class ValidationDecision:
    status: DecisionStatus
    failure_category: FailureCategory
    issues: tuple[ValidationIssue, ...] = ()

    @property
    def may_lookup_slots(self) -> bool:
        return self.status is DecisionStatus.READY_FOR_SLOT_LOOKUP


def abstain(
    category: FailureCategory,
    *issues: ValidationIssue,
) -> ValidationDecision:
    return ValidationDecision(
        status=DecisionStatus.ABSTAIN,
        failure_category=category,
        issues=tuple(issues),
    )
```

## 2. Implement the evaluator

Add:

```python
def evaluate_appointment_extraction(
    extraction: AppointmentExtraction,
    *,
    rules: SchedulingRules,
    current_date: date,
) -> ValidationDecision:
    """Evaluate validated extraction data without side effects."""

    # 1. needs_clarification
    # Return ABSTAIN / INSUFFICIENT_INFORMATION.
    # Add one "required_field_missing" issue per missing field.

    # 2. out_of_scope
    # Return ABSTAIN / OUT_OF_SCOPE with "request_out_of_scope".

    # 3. Semantic validation
    # Reject a blank patient_name or reason_for_visit, a missing
    # request_type/time/date, and a date earlier than current_date.
    # Return SEMANTIC_VALIDATION_FAILED if any semantic issue exists.

    # 4. Business rules
    # Enforce minimum_notice_days, maximum_advance_days,
    # closed_weekdays, and opens_at <= preferred_time < closes_at.
    # Return BUSINESS_RULE_REJECTED if any rule fails.

    # 5. Success
    # Return READY_FOR_SLOT_LOOKUP / NONE with no issues.

    raise NotImplementedError
```

Use stable issue codes:

- `required_field_missing`
- `request_out_of_scope`
- `patient_name_blank`
- `reason_for_visit_blank`
- `request_type_missing`
- `appointment_date_in_past`
- `preferred_time_missing`
- `minimum_notice_not_met`
- `maximum_advance_exceeded`
- `clinic_closed`
- `outside_operating_hours`

Validation order is important: missing information → out of scope → semantic validation → business rules → ready.

For date rules:

```python
days_until_appointment = (preferred_date - current_date).days
```

Python weekdays use Monday `0` through Sunday `6`.

## 3. Convert invalid raw output into a safe decision

Add:

```python
def evaluate_raw_appointment_output(
    raw_output: str,
    *,
    rules: SchedulingRules,
    current_date: date,
) -> ValidationDecision:
    try:
        extraction = parse_appointment_extraction(raw_output)
    except StructuredOutputError:
        return abstain(
            FailureCategory.STRUCTURED_OUTPUT_INVALID,
            ValidationIssue(
                code="structured_output_invalid",
                message="The provider response could not be validated.",
            ),
        )

    return evaluate_appointment_extraction(
        extraction,
        rules=rules,
        current_date=current_date,
    )
```

Catch only the expected boundary exception. Do not hide programming defects with `except Exception`.

## 4. Add eight focused tests

Create `tests/test_decisions.py`. Use a fixed current date and deterministic rules:

```python
CURRENT_DATE = date(2026, 9, 5)

RULES = SchedulingRules(
    minimum_notice_days=1,
    maximum_advance_days=60,
    opens_at=time(9, 0),
    closes_at=time(17, 0),
    closed_weekdays=frozenset({6}),
)
```

Required cases:

1. Valid request → ready for slot lookup.
2. Missing contact → insufficient-information abstention.
3. Out-of-scope request → out-of-scope abstention.
4. Blank patient name → semantic failure.
5. Past date → semantic failure.
6. Same-day request → minimum-notice business rejection.
7. Sunday request → closed-day business rejection.
8. Malformed JSON → structured-output abstention without raising.

For every rejected case, assert:

- status and failure category;
- the relevant issue code;
- `may_lookup_slots is False`.

The valid case must assert `may_lookup_slots is True` and contain no issues.

Your existing 13 tests plus these 8 should produce **21 passing tests**.

## 5. Run one deterministic experiment

Create `scripts/run_lesson_04.py`. Reuse the same date, rules, and representative data as the tests. Print these six cases:

| Case | Expected category | Slot lookup? |
|---|---|:---:|
| Valid request | `none` | Yes |
| Missing contact | `insufficient_information` | No |
| Blank name | `semantic_validation_failed` | No |
| Sunday request | `business_rule_rejected` | No |
| Out of scope | `out_of_scope` | No |
| Malformed JSON | `structured_output_invalid` | No |

Print each decision's status, failure category, `may_lookup_slots`, and issue codes. Do not call Gemini.

## Completion

Run:

```bash
git diff --check
pytest
python -m scripts.run_lesson_04
```

Complete the short `RESULTS.md` and `ASSESSMENT.md`, then commit and push.

Lesson 4 is complete when all 21 tests pass, the experiment matches the table, and no rejected request can advance to slot lookup.
