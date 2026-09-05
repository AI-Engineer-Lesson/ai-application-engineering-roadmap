import json

import pytest

from src.ai.contracts import AIRequest, AIResponse, TokenUsage
from src.ai.scheduling import (
    extract_appointment_request,
    parse_appointment_extraction,
    StructuredOutoutError)

VALID_EXTRACTION = {
    "status": "ready_for_validation",
    "patient_name": "Ana Cruz",
    "contact_number": "09170000000",
    "preferred_date": "2026-09-04",
    "preferred_time": "14:00:00",
    "request_type": "follow_up",
    "reason_for_visit": "Previous consultation",
    "missing_fields": [],
}


class FakeProvider:
    def __init__(self, output: dict[str, object]) -> None:
        self._output = output

    def generate(self, request: AIRequest) -> AIResponse:
        return AIResponse(
            text=json.dumps(self._output),
            provider="fake",
            model="deterministic-test-model",
            latency_ms=1.0,
            usage=TokenUsage(
                input_tokens=10,
                output_tokens=20
            )
        )

def test_valid_structure_output_is_accepted() -> None:
    result = parse_appointment_extraction(
        json.dumps(VALID_EXTRACTION)
    )

    assert result.status == "ready_for_validation"
    assert result.patient_name == "Ana Cruz"
    assert result.contact_number == "09170000000"

def test_malformed_json_is_rejected() -> None:
    with pytest.raises(StructuredOutoutError):
        parse_appointment_extraction(
            '{"status": "ready_for_validation"}'
        )

def test_unknown_status_is_rejected() -> None:
    invalid = {
        **VALID_EXTRACTION,
        "status": "appointment_confirmed"
    }

    with pytest.raises(StructuredOutoutError):
        parse_appointment_extraction(json.dumps(invalid))


def test_invalid_phone_number_is_rejected() -> None:
    invalid = {
        **VALID_EXTRACTION,
        "contact_number": "0917000000"
    }

    with pytest.raises(StructuredOutoutError):
        parse_appointment_extraction(json.dumps(invalid))

def test_ready_status_requires_all_fields() -> None:
    invalid = {
        **VALID_EXTRACTION,
        "contact_number": None,
        "missing_fields": ["contact_number"]
    }

    with pytest.raises(StructuredOutoutError):
        parse_appointment_extraction(json.dumps(invalid))

def test_clarification_requires_missing_fields() -> None:
    invalid = {
        **VALID_EXTRACTION,
        "status": "needs_clarification",
        "contact_number": None,
        "missing_fields": []
    }

    with pytest.raises(StructuredOutoutError):
        parse_appointment_extraction(json.dumps(invalid))

def test_consumer_accepts_fake_provider() -> None:
    provider = FakeProvider(VALID_EXTRACTION)
    request = AIRequest(
        prompt="Synthetic test",
        response_schema={}
    )

    result = extract_appointment_request(provider, request)

    assert result.status == "ready_for_validation"