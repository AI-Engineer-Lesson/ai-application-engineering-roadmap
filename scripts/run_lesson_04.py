from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, time

from src.ai.decisions import (
    FailureCategory,
    SchedulingRules,
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


@dataclass(frozen=True)
class ExperimentCase:
    name: str
    raw_output: str
    expected_category: FailureCategory
    expected_slot_lookup: bool


def as_json(data: dict[str, object]) -> str:
    return json.dumps(data)


CASES = (
    ExperimentCase(
        name="Valid request",
        raw_output=as_json(VALID_EXTRACTION),
        expected_category=FailureCategory.NONE,
        expected_slot_lookup=True,
    ),
    ExperimentCase(
        name="Missing contact",
        raw_output=as_json(
            {
                **VALID_EXTRACTION,
                "status": "needs_clarification",
                "contact_number": None,
                "missing_fields": ["contact_number"],
            }
        ),
        expected_category=FailureCategory.INSUFFICIENT_INFORMATION,
        expected_slot_lookup=False,
    ),
    ExperimentCase(
        name="Blank patient name",
        raw_output=as_json(
            {
                **VALID_EXTRACTION,
                "patient_name": "   ",
            }
        ),
        expected_category=FailureCategory.SEMANTIC_VALIDATION_FAILED,
        expected_slot_lookup=False,
    ),
    ExperimentCase(
        name="Sunday request",
        raw_output=as_json(
            {
                **VALID_EXTRACTION,
                "preferred_date": "2026-09-06",
            }
        ),
        expected_category=FailureCategory.BUSINESS_RULE_REJECTED,
        expected_slot_lookup=False,
    ),
    ExperimentCase(
        name="Out-of-scope request",
        raw_output=as_json(
            {
                **VALID_EXTRACTION,
                "status": "out_of_scope",
            }
        ),
        expected_category=FailureCategory.OUT_OF_SCOPE,
        expected_slot_lookup=False,
    ),
    ExperimentCase(
        name="Malformed JSON",
        raw_output='{"status": "ready_for_validation"',
        expected_category=FailureCategory.STRUCTURED_OUTPUT_INVALID,
        expected_slot_lookup=False,
    ),
)


def run_case(
    index: int,
    case: ExperimentCase,
) -> bool:
    decision = evaluate_raw_appointment_output(
        case.raw_output,
        rules=RULES,
        current_date=CURRENT_DATE,
    )

    category_matches = (
        decision.failure_category is case.expected_category
    )
    slot_lookup_matches = (
        decision.may_lookup_slots is case.expected_slot_lookup
    )
    passed = category_matches and slot_lookup_matches

    print("=" * 72)
    print(f"Case {index}: {case.name}")
    print(f"Status: {decision.status.value}")
    print(f"Failure category: {decision.failure_category.value}")
    print(f"Slot lookup allowed: {decision.may_lookup_slots}")

    if decision.issues:
        print("Issues:")

        for issue in decision.issues:
            field = f" [{issue.field}]" if issue.field else ""
            print(f"  - {issue.code}{field}: {issue.message}")
    else:
        print("Issues: None")

    print(f"Result: {'PASS' if passed else 'FAIL'}")

    if not category_matches:
        print(
            "  Expected category: "
            f"{case.expected_category.value}"
        )

    if not slot_lookup_matches:
        print(
            "  Expected slot lookup: "
            f"{case.expected_slot_lookup}"
        )

    return passed


def main() -> None:
    passed_count = 0

    for index, case in enumerate(CASES, start=1):
        if run_case(index, case):
            passed_count += 1

    print("=" * 72)
    print(f"Summary: {passed_count}/{len(CASES)} cases passed")

    if passed_count != len(CASES):
        raise SystemExit(1)


if __name__ == "__main__":
    main()