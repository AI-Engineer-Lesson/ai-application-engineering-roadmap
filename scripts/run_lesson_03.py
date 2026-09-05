from __future__ import annotations

import json
import os
from dataclasses import dataclass

from dotenv import load_dotenv

from src.ai.context import ClinicPolicy
from src.ai.providers.gemini import GeminiProvider
from src.ai.scheduling import (
    StructuredOutputError,
    build_appointment_extraction_request,
    parse_appointment_extraction,
)


@dataclass(frozen=True)
class ExperimentCase:
    name: str
    expected_status: str
    user_input: str


POLICY = ClinicPolicy(
    clinic_name="Northstar Synthetic Clinic",
    appointment_required=True,
    required_booking_fields=(
        "patient_name",
        "contact_number",
        "preferred_date",
        "preferred_time",
        "reason_for_visit",
    ),
    supported_request_types=(
        "general_consultation",
        "follow_up",
    ),
)


CASES = (
    ExperimentCase(
        name="Complete valid request",
        expected_status="ready_for_validation",
        user_input=(
            "My name is Ana Cruz and my number is 09170000000. "
            "I want a follow-up appointment on September 4, 2026 "
            "at 2:00 PM regarding my previous consultation."
        ),
    ),
    ExperimentCase(
        name="Missing information",
        expected_status="needs_clarification",
        user_input=(
            "I am Ana Cruz. I want a general consultation next week."
        ),
    ),
    ExperimentCase(
        name="Invalid contact number",
        expected_status="needs_clarification",
        user_input=(
            "My name is Ana Cruz and my number is 0917000000. "
            "I want a follow-up appointment on September 4, 2026 "
            "at 2:00 PM regarding my previous consultation."
        ),
    ),
    ExperimentCase(
        name="Out-of-scope medical request",
        expected_status="out_of_scope",
        user_input=(
            "Diagnose my chest pain and recommend medication."
        ),
    ),
)


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

    for index, case in enumerate(CASES, start=1):
        request = build_appointment_extraction_request(
            policy=POLICY,
            user_input=case.user_input,
            current_date="2026-08-30",
        )

        response = provider.generate(request)

        print("=" * 72)
        print(f"Case {index}: {case.name}")
        print(f"Expected status: {case.expected_status}")
        print(f"Latency: {response.latency_ms:.2f} ms")
        print(f"Input tokens: {response.usage.input_tokens}")
        print(f"Output tokens: {response.usage.output_tokens}")
        print(f"Thought tokens: {response.usage.thought_tokens}")
        print()
        print("Raw output:")
        print(response.text)
        print()

        try:
            result = parse_appointment_extraction(response.text)
        except StructuredOutputError as exc:
            print(f"Validation: REJECTED — {exc}")
            continue

        print("Validation: ACCEPTED")
        print(
            json.dumps(
                result.model_dump(mode="json"),
                indent=2,
            )
        )


if __name__ == "__main__":
    main()