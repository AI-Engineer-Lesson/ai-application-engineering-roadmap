import json
from datetime import date, time

from src.ai.decisions import (
    DecisionStatus,
    FailureCategory,
    SchedulingRules,
    ValidationDecision,
    evaluate_raw_appointment_output,
)


CURRENT_DATE = date(2026, 9, 5)

RULES = SchedulingRules(
    minimum_notice_days=1,
    maximum_advance_days=60,
    opens_at=time(9, 0),
    closes_at=time(17, 0),
    closed_weekdays=frozenset({6}),
)

VALID_EXTRACTION = {
    "status": "ready_for_validation",
    "patient_name": "Ana Cruz",
    "contact_number": "09170000000",
    "preferred_date": "2026-09-08",
    "preferred_time": "14:00:00",
    "request_type": "follow_up",
    "reason_for_visit": "Previous consultation",
    "missing_fields": [],
}


def evaluate(data: dict[str, object]) -> ValidationDecision:
    return evaluate_raw_appointment_output(
        json.dumps(data),
        rules=RULES,
        current_date=CURRENT_DATE,
    )


def issue_codes(decision: ValidationDecision) -> set[str]:
    return {issue.code for issue in decision.issues}


def test_valid_request_is_ready_for_slot_lookup() -> None:
    decision = evaluate(VALID_EXTRACTION)

    assert decision.status is DecisionStatus.READY_FOR_SLOT_LOOKUP
    assert decision.failure_category is FailureCategory.NONE
    assert decision.issues == ()
    assert decision.may_lookup_slots is True


def test_missing_contact_abstains() -> None:
    data = {
        **VALID_EXTRACTION,
        "status": "needs_clarification",
        "contact_number": None,
        "missing_fields": ["contact_number"],
    }

    decision = evaluate(data)

    assert decision.status is DecisionStatus.ABSTAIN
    assert (
        decision.failure_category
        is FailureCategory.INSUFFICIENT_INFORMATION
    )
    assert "required_field_missing" in issue_codes(decision)
    assert decision.may_lookup_slots is False


def test_out_of_scope_request_abstains() -> None:
    data = {
        **VALID_EXTRACTION,
        "status": "out_of_scope",
    }

    decision = evaluate(data)

    assert decision.status is DecisionStatus.ABSTAIN
    assert decision.failure_category is FailureCategory.OUT_OF_SCOPE
    assert "request_out_of_scope" in issue_codes(decision)
    assert decision.may_lookup_slots is False


def test_blank_patient_name_fails_semantic_validation() -> None:
    data = {
        **VALID_EXTRACTION,
        "patient_name": "   ",
    }

    decision = evaluate(data)

    assert decision.status is DecisionStatus.ABSTAIN
    assert (
        decision.failure_category
        is FailureCategory.SEMANTIC_VALIDATION_FAILED
    )
    assert "patient_name_blank" in issue_codes(decision)
    assert decision.may_lookup_slots is False


def test_past_date_fails_semantic_validation() -> None:
    data = {
        **VALID_EXTRACTION,
        "preferred_date": "2026-09-04",
    }

    decision = evaluate(data)

    assert decision.status is DecisionStatus.ABSTAIN
    assert (
        decision.failure_category
        is FailureCategory.SEMANTIC_VALIDATION_FAILED
    )
    assert "appointment_date_in_past" in issue_codes(decision)
    assert decision.may_lookup_slots is False


def test_same_day_request_fails_minimum_notice_rule() -> None:
    data = {
        **VALID_EXTRACTION,
        "preferred_date": "2026-09-05",
    }

    decision = evaluate(data)

    assert decision.status is DecisionStatus.ABSTAIN
    assert (
        decision.failure_category
        is FailureCategory.BUSINESS_RULE_REJECTED
    )
    assert "minimum_notice_not_met" in issue_codes(decision)
    assert decision.may_lookup_slots is False


def test_sunday_request_fails_closed_day_rule() -> None:
    data = {
        **VALID_EXTRACTION,
        "preferred_date": "2026-09-06",
    }

    decision = evaluate(data)

    assert decision.status is DecisionStatus.ABSTAIN
    assert (
        decision.failure_category
        is FailureCategory.BUSINESS_RULE_REJECTED
    )
    assert "clinic_closed" in issue_codes(decision)
    assert decision.may_lookup_slots is False


def test_malformed_json_abstains_without_raising() -> None:
    malformed_output = '{"status": "ready_for_validation"'

    decision = evaluate_raw_appointment_output(
        malformed_output,
        rules=RULES,
        current_date=CURRENT_DATE,
    )

    assert decision.status is DecisionStatus.ABSTAIN
    assert (
        decision.failure_category
        is FailureCategory.STRUCTURED_OUTPUT_INVALID
    )
    assert "structured_output_invalid" in issue_codes(decision)
    assert decision.may_lookup_slots is False