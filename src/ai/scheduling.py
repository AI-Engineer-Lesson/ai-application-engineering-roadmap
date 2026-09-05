from __future__ import annotations

from datetime import date, time
from typing import Literal

import re

from pydantic import BaseModel, ConfigDict, Field, ValidationError
from pydantic import field_validator, model_validator
from src.ai.context import build_clinic_request, ClinicPolicy
from src.ai.contracts import AIProvider, AIRequest



RequiredBookingField = Literal[
    "patient_name",
    "contact_number",
    "preferred_date",
    "preferred_time",
    "reason_for_visit",
]

RequestType = Literal[
    "general_consultation",
    "follow_up",
]

ExtractionStatus = Literal[
    "ready_for_validation",
    "needs_clarification",
    "out_of_scope",
]

class AppointmentExtraction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: ExtractionStatus= Field(
        description=(
            "Whether all required information was extracted, clarification is "
            "needed, or the request is outside scheduling scope."
        )
    )

    patient_name: str | None = Field(
        default=None,
        description="Patient name is exactly as provided by the user."
    )

    contact_number: str | None = Field(
        default=None,
        description=(
            "Philippine mobile number containing exactly 11 digits and "
            "starting with '09'. Use null when missing or invalid."
        )
    )

    preferred_date: date | None = Field(
        default=None,
        description="Requested appointment date, or null when missing."
    )

    preferred_time: time | None = Field(
        default=None,
        description="Requested appointment time, or null when missing."
    )

    request_type: RequestType | None = Field(
        default= None,
       description= "Supported appointment type, or null when unclear."
    )

    reason_for_visit: str | None  = Field(
        default=None,
        description="Reason for the visit, or null when missing."
    )

    missing_fields: list[RequiredBookingField] = Field(
        default_factory=list,
        description="Requiredfields that are missing or invalid."
    )

    @field_validator("contact_number")
    @classmethod
    def validate_contact_number(cls, value:str | None) -> str | None:
        if value is not None and re.fullmatch(r"09\d{9}", value) is None:
            raise ValueError(
                "contact_number must beging with 09 and contains 11 digits."
            )

        return value

    @model_validator(mode="after")
    def vaidate_status_consistency(self) -> Self:
        required_values = {
            "patient_name": self.patient_name,
            "contact_number": self.contact_number,
            "preferred_date": self.preferred_date,
            "preferred_time": self.preferred_time,
            "reason_for_visit": self.reason_for_visit
        }

        actually_missing = {
            name
            for name, value in required_values.items()
            if value is None
        }

        declared_missing = set(self.missing_fields)

        if self.status == "ready_for_validation":
            if actually_missing:
                raise ValueError(
                    "ready_for_validation requires all required fields."
                )

            if declared_missing:
                raise ValueError(
                    "ready_for_validation cannot declare missing fields."
                )

        if self.status == "needs_clarification":
            if not declared_missing:
                raise ValueError(
                    "needs_clarification requires at least one missing field."
                )

            if not declared_missing.issubset(actually_missing):
                raise ValueError(
                    "missing_fields contains a field that has a value."
                )

        return self

class StructuredOutputError(RuntimeError):
    """Raised when provider output fails application validation."""

def parse_appointment_extraction(
    raw_output:str
) -> AppointmentExtraction:
    try:
        return AppointmentExtraction.model_validate_json(raw_output)
    except ValidationError as exc:
        raise StructuredOutputError(
            "The AI provider returned an invalid scheduling response."
        ) from exc

def build_appointment_extraction_request(
    *,
    policy: ClinicPolicy,
    user_input: str,
    current_date: str,
) -> AIRequest:
    request = build_clinic_request(
        policy=policy,
        user_input=user_input,
        current_date=current_date
    )

    return AIRequest(
        system_instruction=(
            request.system_instruction
            + "\n\n Return only JSON matching the supplied response schema. "
            "Preserve user-provided values. Do not invent or silently correct "
            "missing or invalid information."
        ),
        prompt=request.prompt,
        max_output_tokens=512,
        response_schema=AppointmentExtraction.model_json_schema(),
    )

def extract_appointment_request(
    provider: AIProvider,
    request: AIRequest
) -> AppointmentExtraction:
    response = provider.generate(request)
    return parse_appointment_extraction(response.text)