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
    if extraction.status == "needs_clarification":
        issues = tuple(
            ValidationIssue(
                code="required_field_missing",
                message=f"The required field '{field}' is missing.",
                field=field,
            )
            for field in extraction.missing_fields
        )
        return abstain(FailureCategory.INSUFFICIENT_INFORMATION, *issues)

    # 2. out_of_scope
    # Return ABSTAIN / OUT_OF_SCOPE with "request_out_of_scope".
    if extraction.status == "out_of_scope":
        return abstain(
            FailureCategory.OUT_OF_SCOPE,
            ValidationIssue(
                code="request_out_of_scope",
                message="The request is outside appointment scheduling scope.",
            ),
        )

    # 3. Semantic validation
    # Reject a blank patient_name or reason_for_visit, a missing
    # request_type/time/date, and a date earlier than current_date.
    # Return SEMANTIC_VALIDATION_FAILED if any semantic issue exists.
    semantic_issues: list[ValidationIssue] = []

    if extraction.patient_name is not None and not extraction.patient_name.strip():
        semantic_issues.append(
            ValidationIssue(
                code="patient_name_blank",
                message="The patient name cannot be blank.",
                field="patient_name",
            )
        )

    if (
        extraction.reason_for_visit is not None
        and not extraction.reason_for_visit.strip()
    ):
        semantic_issues.append(
            ValidationIssue(
                code="reason_for_visit_blank",
                message="The reason for the visit cannot be blank.",
                field="reason_for_visit",
            )
        )

    if extraction.request_type is None:
        semantic_issues.append(
            ValidationIssue(
                code="request_type_missing",
                message="The appointment request type is missing.",
                field="request_type",
            )
        )

    if extraction.preferred_date is None:
        semantic_issues.append(
            ValidationIssue(
                code="required_field_missing",
                message="The preferred appointment date is missing.",
                field="preferred_date",
            )
        )
    elif extraction.preferred_date < current_date:
        semantic_issues.append(
            ValidationIssue(
                code="appointment_date_in_past",
                message="The preferred appointment date cannot be in the past.",
                field="preferred_date",
            )
        )

    if extraction.preferred_time is None:
        semantic_issues.append(
            ValidationIssue(
                code="preferred_time_missing",
                message="The preferred appointment time is missing.",
                field="preferred_time",
            )
        )

    if semantic_issues:
        return abstain(
            FailureCategory.SEMANTIC_VALIDATION_FAILED,
            *semantic_issues,
        )

    # 4. Business rules
    # Enforce minimum_notice_days, maximum_advance_days,
    # closed_weekdays, and opens_at <= preferred_time < closes_at.
    # Return BUSINESS_RULE_REJECTED if any rule fails.
    business_issues: list[ValidationIssue] = []

    # Semantic validation above guarantees that both values are present.
    assert extraction.preferred_date is not None
    assert extraction.preferred_time is not None

    days_until_appointment = (extraction.preferred_date - current_date).days

    if days_until_appointment < rules.minimum_notice_days:
        business_issues.append(
            ValidationIssue(
                code="minimum_notice_not_met",
                message=(
                    "The appointment does not meet the minimum notice "
                    f"of {rules.minimum_notice_days} day(s)."
                ),
                field="preferred_date",
            )
        )

    if days_until_appointment > rules.maximum_advance_days:
        business_issues.append(
            ValidationIssue(
                code="maximum_advance_exceeded",
                message=(
                    "The appointment exceeds the maximum advance window "
                    f"of {rules.maximum_advance_days} day(s)."
                ),
                field="preferred_date",
            )
        )

    if extraction.preferred_date.weekday() in rules.closed_weekdays:
        business_issues.append(
            ValidationIssue(
                code="clinic_closed",
                message="The clinic is closed on the preferred date.",
                field="preferred_date",
            )
        )

    if not rules.opens_at <= extraction.preferred_time < rules.closes_at:
        business_issues.append(
            ValidationIssue(
                code="outside_operating_hours",
                message="The preferred time is outside clinic operating hours.",
                field="preferred_time",
            )
        )

    if business_issues:
        return abstain(
            FailureCategory.BUSINESS_RULE_REJECTED,
            *business_issues,
        )

    # 5. Success
    # Return READY_FOR_SLOT_LOOKUP / NONE with no issues.
    return ValidationDecision(
        status=DecisionStatus.READY_FOR_SLOT_LOOKUP,
        failure_category=FailureCategory.NONE,
    )


def evaluate_raw_appointment_output(
    raw_output: str,
    *,
    rules: SchedulingRules,
    current_date: date,
) -> ValidationDecision:
    """Parse provider output and turn expected validation errors into abstention."""

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
