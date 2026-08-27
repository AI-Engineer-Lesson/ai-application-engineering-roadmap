# Lesson 7 — Reusable Prompt Templates and Ambiguity Handling

## Overview

This lesson introduces Python for AI application engineering through a reusable Gemini prompt template.

The application evaluates appointment requests and determines whether they are:

- Complete and ready
- Missing critical information
- Ambiguous
- Contradictory

## Learning Objectives

- Set up a Python virtual environment.
- Use Python functions, type hints, dictionaries, lists, loops, and f-strings.
- Build reusable prompt templates.
- Separate stable instructions from request-specific input.
- Identify missing and ambiguous information.
- Detect contradictions.
- Call the Gemini Interactions API from Python.
- Measure request latency.
- Understand why application validation remains necessary.

## Technology

- Python
- Google GenAI SDK
- Gemini Interactions API
- Model: `gemini-3.7-flash`
- Data: Synthetic only
- Actual cost: $0 within free-tier limits

## Project Structure

```text
lesson-07/
├── src/
│   └── main.py
├── lesson.md
├── results.md
├── README.md
└── requirements.txt
```

The local `.venv` directory is excluded from Git.

## Setup

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Configure the Gemini API key:

```powershell
$env:GEMINI_API_KEY="your-api-key"
```

Do not commit the API key.

## Run

```powershell
python src/main.py
```

The program evaluates four requests:

1. Complete
2. Missing date
3. Vague
4. Contradictory

## Reusable Prompt Template

The system instruction is generated using:

```python
def build_system_instruction(
    clinic_name: str,
    allowed_services: list[str],
) -> str:
```

The function accepts configuration values instead of hardcoding one clinic and service list into the reusable logic.

The template defines:

- Administrative role
- Allowed services
- Required fields
- Ambiguity rules
- Contradiction handling
- Clarification limits
- Output contract

## Untrusted User Input

Request-specific content is wrapped separately:

```python
def build_user_input(request_text: str) -> str:
    return f"""
<user_request>
{request_text}
</user_request>
""".strip()
```

Delimiters make the prompt structure clearer, but they are not a complete security boundary.

## Required Fields

A request requires:

- Patient type
- Requested service
- Preferred date
- Preferred time

Missing values are represented as `UNKNOWN`.

## Output Contract

```text
SUMMARY:
STATUS: READY | NEEDS_CLARIFICATION | CONFLICT
SERVICE:
DATE:
TIME:
PATIENT_TYPE:
MISSING:
CONFLICTS:
QUESTIONS:
```

Status meanings:

- `READY`: all required fields are present and consistent
- `NEEDS_CLARIFICATION`: required information is missing or ambiguous
- `CONFLICT`: supplied details contradict each other

This contract is prompt-based and is not yet enforced through a runtime schema.

## Experiment Summary

| Case          | Expected            | Actual                | Invented information? |
| ------------- | ------------------- | --------------------- | --------------------- |
| Complete      | Ready               | `READY`               | No                    |
| Missing date  | Needs clarification | `NEEDS_CLARIFICATION` | No                    |
| Vague         | Needs clarification | `NEEDS_CLARIFICATION` | No                    |
| Contradictory | Conflict            | `CONFLICT`            | No                    |

## Key Findings

### Complete Request

The model recognized that the patient type, service, date, and time were available. It returned `READY` without asking unnecessary questions.

### Missing Date

The model preserved the missing date as `UNKNOWN` and requested clarification instead of inventing one.

### Vague Request

The model recognized that “usual appointment” did not identify a service and “soon” did not identify a date.

It requested the missing:

- Patient type
- Service
- Date
- Time

### Contradictory Request

The model detected the conflict between morning-only availability and a requested time of 3:00 PM.

The conflict must be resolved before application code prepares a booking operation.

## Python Concepts

### Type Hints

```python
def build_user_input(request_text: str) -> str:
```

The type hints communicate that the function expects and returns a string.

Standard Python does not automatically enforce these hints at runtime.

### F-Strings

```python
message = f"Clinic: {clinic_name}"
```

The `f` prefix allows variables and expressions to be inserted into a string.

### Dictionaries

```python
test_case = {
    "case_id": "complete",
    "request_text": "Request text",
}
```

Dictionaries store key-value pairs similarly to JavaScript objects.

### Main Guard

```python
if __name__ == "__main__":
    main()
```

This runs `main()` when the file is executed directly while preventing it from running automatically when imported.

## Template Value Categories

### Stable Instructions

- Administrative role
- Behavioral rules
- Required fields
- Output contract

### Configuration Variables

- Clinic name
- Allowed service list

### Request-Specific Variables

- Current user request
- Patient type
- Requested service
- Preferred date
- Preferred time

## Production Considerations

A model returning `READY` does not prove that an appointment may be booked.

Application code must still:

1. Parse and validate the returned fields.
2. Confirm that required values are present.
3. Verify that the service is supported.
4. Check real clinic availability.
5. Enforce authentication and authorization.
6. Perform the database operation.
7. Verify that the operation succeeded.
8. Only then confirm the appointment.

Prompt templates improve consistency, but they do not replace deterministic application controls.

## Conclusion

Reusable prompt templates centralize behavioral rules and output expectations while allowing configuration and request data to vary.

They help models handle incomplete, vague, and contradictory requests consistently. However, model output remains probabilistic and must be validated before it can affect a real business operation.
