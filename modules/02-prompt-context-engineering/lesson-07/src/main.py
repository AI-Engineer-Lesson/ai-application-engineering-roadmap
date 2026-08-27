# perf_counter provides a high-precision timer.
# It is appropriate for measuring how long an operation takes.
from time import perf_counter

# Any represents a value whose exact type is not currently restricted.
# We use it for the values stored inside our test-case dictionaries.
from typing import Any

# Import Google's current Gemini SDK.
from google import genai


# genai.Client() automatically reads GEMINI_API_KEY
# from the environment.
client = genai.Client()

# Python constants are commonly written using uppercase names.
# Python does not technically prevent this value from being changed,
# but the uppercase name communicates that it should remain constant.
MODEL = "gemini-3.7-flash"


# A list contains multiple ordered values.
# Each value in this list is a dictionary representing one test case.
#
# A Python dictionary is similar to an object in JavaScript or TypeScript.
TEST_CASES: list[dict[str, Any]] = [
    {
        "case_id": "complete",
        "request_text": (
            "I am a returning patient. Please request a cleaning "
            "on August 28 at 2:00 PM."
        ),
    },
    {
        "case_id": "missing_date",
        "request_text": (
            "I am a new patient and would like an administrative "
            "consultation in the afternoon."
        ),
    },
    {
        "case_id": "vague",
        "request_text": "Please book my usual appointment sometime soon.",
    },
    {
        "case_id": "contradictory",
        "request_text": (
            "I am a returning patient and available only in the morning. "
            "Please request a cleaning at 3:00 PM on August 29."
        ),
    },
]


def build_system_instruction(
    clinic_name: str,
    allowed_services: list[str],
) -> str:
    """
    Build the reusable trusted instruction for the model.

    Args:
        clinic_name:
            The clinic whose configuration is being used.

        allowed_services:
            The services that the clinic accepts.

    Returns:
        A complete system-instruction string.
    """

    # Convert the list of allowed services into a bulleted string.
    #
    # For example:
    #
    # ["cleaning", "follow-up visit"]
    #
    # becomes:
    #
    # - cleaning
    # - follow-up visit
    services_text = "\n".join(
        f"- {service}" for service in allowed_services
    )

    return f"""
You are an administrative appointment-intake assistant for {clinic_name}.
Summarize the user's request and determine whether enough information is
available to prepare an appointment request. You do not perform real bookings.

Allowed services:
{services_text}

The four business-critical fields are:
1. Patient type: new or returning
2. Requested service
3. Preferred date
4. Preferred time

Follow these rules:
- Never invent missing business-critical information. Use UNKNOWN when a
  required value is unavailable.
- Treat vague terms such as "usual" and "soon" as ambiguous unless supplied
  context defines them.
- Identify contradictory information and report it under CONFLICTS.
- Ask no more than three focused clarification questions, and do not ask for
  information that was already clearly supplied.
- Use only a service from the allowed-services list. Report unsupported
  services instead of silently changing them.
- Never claim that an appointment has been confirmed or booked.

Return exactly this readable structure:
SUMMARY:
STATUS: READY | NEEDS_CLARIFICATION | CONFLICT
SERVICE:
DATE:
TIME:
PATIENT_TYPE:
MISSING:
CONFLICTS:
QUESTIONS:

Use READY only when all required fields are available and consistent.
Use NEEDS_CLARIFICATION when a required field is missing or ambiguous.
Use CONFLICT when the request contains information that cannot be satisfied
together. Use UNKNOWN for every missing value.
""".strip()


def build_user_input(request_text: str) -> str:
    """
    Wrap user-controlled content in clearly labelled delimiters.

    Delimiters help communicate the prompt's structure to the model,
    but they do not sanitize the content or create a security boundary.
    """

    # Return request_text inside <user_request> delimiters.
    #
    # Expected shape:
    #
    # <user_request>
    # [the actual request]
    # </user_request>
    return f"<user_request>\n{request_text}\n</user_request>"


def run_case(test_case: dict[str, Any]) -> None:
    """
    Run one test case and print its result.

    The return type is None because the function performs an action
    instead of returning a value to its caller.
    """

    # These are stable configuration values for the fictional clinic.
    clinic_name = "Northstar Dental Clinic"

    allowed_services = [
        "cleaning",
        "administrative consultation",
        "follow-up visit",
    ]

    # Call build_system_instruction() using clinic_name
    # and allowed_services.
    system_instruction = build_system_instruction(clinic_name, allowed_services)

    # Read request_text from the test_case dictionary and pass it
    # to build_user_input().
    input_text = build_user_input(test_case["request_text"])

    # Record the time immediately before the Gemini request.
    started_at = perf_counter()

    # Call client.interactions.create() with:
    #
    # - model=MODEL
    # - system_instruction=system_instruction
    # - input=input_text
    # - store=False
    #
    # Save the returned Interaction object in this variable.
    interaction =  client.interactions.create(
        model=MODEL,
        system_instruction=system_instruction,
        input=input_text,
        store=False,
    )

    # perf_counter() returns seconds.
    # Multiplying the elapsed value by 1,000 converts it to milliseconds.
    latency_ms = (perf_counter() - started_at) * 1000

    # Build a dictionary containing the observable result.
    result = {
        "case_id": test_case["case_id"],
        "model": MODEL,
        "latency_ms": round(latency_ms, 2),

        # Once TODO 5 is implemented, interaction will contain
        # Gemini's response and output_text will contain its
        # final visible answer.
        "output_text": (
            interaction.output_text
            if interaction is not None
            else None
        ),
    }

    # Print a separator so individual test cases are easy to identify.
    print("=" * 70)

    # Printing the dictionary is sufficient for this lesson.
    # Formal JSON serialization will be introduced later.
    print(result)


def main() -> None:
    """
    Run every test case one at a time.
    """

    # A for loop visits each item in TEST_CASES.
    for test_case in TEST_CASES:
        run_case(test_case)


# This condition is true when main.py is executed directly.
# It prevents main() from automatically running if this module
# is imported by another Python file.
if __name__ == "__main__":
    main()
