# Phase 1 · Module 2 · Lesson 7

## Reusable Prompt Templates and Ambiguity Handling with Python

**Status:** Active  
**Required duration:** approximately 30–45 minutes  
**Language:** Python  
**Difficulty:** Beginner-friendly Python

This is the first Python-based lesson in the AI Application Engineering roadmap.

AI-focused lessons will primarily use Python moving forward. TypeScript will return when it provides a practical advantage, particularly for Next.js integration, frontend applications, and TypeScript-based APIs.

---

## AI Requirement

- **Provider:** Google Gemini API
- **Tier:** Free tier
- **Model:** `gemini-3.7-flash`
- **Data:** Synthetic only
- **Expected actual cost:** $0 within free-tier limits
- **Python SDK:** `google-genai` version 2.3.0 or newer

The Gemini Interactions API supports Python through:

```python
client.interactions.create()
```

The Interactions API is the recommended Gemini interface for new applications.

References:

- [Gemini Interactions API](https://ai.google.dev/gemini-api/docs/interactions-overview)
- [Gemini Python setup](https://ai.google.dev/gemini-api/docs/get-started)
- [Gemini text generation](https://ai.google.dev/gemini-api/docs/text-generation)

---

# 1. Why This Lesson Matters

Production applications should avoid constructing prompts through duplicated strings scattered across different files or API routes.

A reusable prompt template provides one controlled place for:

- Task instructions
- Business rules
- Allowed values
- Ambiguity handling
- Output requirements
- Untrusted user content

Consider this request:

> Book my usual appointment sometime soon.

The application does not know:

- Which service “usual appointment” represents
- Which date “soon” means
- Which time the patient prefers
- Whether the patient is new or returning

These are business-critical details.

Guessing them could cause the application to prepare an incorrect appointment request. The safer behavior is to identify what is missing and ask focused clarification questions.

In this lesson, you will build a reusable Python prompt template and test it against:

1. A complete request
2. A request with a missing date
3. A vague request
4. A contradictory request

---

# 2. Learning Objectives

By the end of this lesson, you should be able to:

- Set up a basic Python project and virtual environment.
- Use Python functions, type hints, lists, dictionaries, loops, and f-strings.
- Build a reusable prompt template.
- Separate stable instructions from request-specific data.
- Identify business-critical fields.
- Instruct an AI model not to invent missing information.
- Handle vague and contradictory requests.
- Call the Gemini Interactions API from Python.
- Measure request latency.
- Explain why application validation remains necessary.

---

# 3. Terminology

## Prompt Template

A reusable prompt structure containing stable instructions and variable values.

For example, the clinic’s administrative rules may remain stable while the clinic name, service list, and current user request are inserted as variables.

## Placeholder

A position in a template where a variable value is inserted.

In a Python f-string:

```python
clinic_name = "Northstar Dental Clinic"
message = f"Clinic: {clinic_name}"
```

`{clinic_name}` is the placeholder.

## Ambiguity

A situation where information has multiple reasonable interpretations or is insufficient for a reliable decision.

Examples:

- “Soon”
- “My usual appointment”
- “Sometime in the afternoon”
- “Use the normal option”

## Business-Critical Field

Information that must be correct before an application may safely prepare or execute an operation.

For this lesson, the business-critical fields are:

- Patient type
- Requested service
- Preferred date
- Preferred time

## Contradiction

Two pieces of information that cannot both be satisfied.

Example:

> I am only available in the morning. Schedule it at 3:00 PM.

## Output Contract

A documented agreement describing the expected structure and meaning of a model response.

In this lesson, the output contract is communicated through the prompt. It is not technically enforced through a schema yet.

Schema-enforced structured output will be covered in Module 3.

---

# 4. Python Concepts Introduced

## 4.1 Type Hints

Consider this function:

```python
def build_user_input(request_text: str) -> str:
    return request_text
```

The first `str` indicates that `request_text` should be a string.

The `-> str` indicates that the function should return a string.

The TypeScript equivalent would look like:

```typescript
function buildUserInput(requestText: string): string {
  return requestText;
}
```

Python normally does not enforce type hints at runtime. They help:

- Developers understand the expected values
- Editors provide better autocomplete
- Static-analysis tools detect possible type mistakes
- Teams document function contracts

## 4.2 Snake Case

Python commonly uses `snake_case`:

```python
clinic_name
allowed_services
build_user_input
```

TypeScript commonly uses `camelCase`:

```typescript
clinicName
allowedServices
buildUserInput
```

## 4.3 Lists

A Python list stores multiple ordered values:

```python
allowed_services = [
    "cleaning",
    "follow-up visit",
]
```

The TypeScript equivalent is:

```typescript
const allowedServices = [
  "cleaning",
  "follow-up visit",
];
```

## 4.4 Dictionaries

A Python dictionary stores key-value pairs. It is similar to a JavaScript or TypeScript object:

```python
test_case = {
    "case_id": "complete",
    "request_text": "Please request a cleaning.",
}
```

Access a value using its key:

```python
case_id = test_case["case_id"]
```

## 4.5 F-Strings

Python f-strings insert variable values into text:

```python
clinic_name = "Northstar Dental Clinic"
message = f"You are an assistant for {clinic_name}."
```

The `f` before the opening quotation mark enables placeholder replacement.

The TypeScript equivalent is:

```typescript
const message = `You are an assistant for ${clinicName}.`;
```

## 4.6 Docstrings

A docstring documents a Python function, class, or module:

```python
def build_message() -> str:
    """
    Build and return an example message.
    """

    return "Example"
```

Unlike an ordinary code comment, development tools can inspect a docstring as documentation for the function.

## 4.7 The Main Guard

Python commonly uses:

```python
if __name__ == "__main__":
    main()
```

When a Python file is executed directly, Python sets its special `__name__` variable to `"__main__"`.

The condition prevents `main()` from running automatically if the file is imported by another Python module later.

---

# 5. Project Structure

The completed lesson should use this structure:

```text
lesson-07/
├── src/
│   └── main.py
├── lesson.md
├── results.md
├── README.md
├── requirements.txt
└── .venv/              # Local only; do not commit
```

File responsibilities:

- `lesson.md` contains the complete lesson instructions.
- `results.md` contains experiment outputs, observations, and answers.
- `README.md` becomes the permanent summary after the lesson passes.
- `src/main.py` contains the runnable implementation.
- `requirements.txt` records the Python dependencies.
- `.venv` contains the local virtual environment and must not be committed.

---

# 6. Required Core Lesson

## Step 1: Create the Lesson Folder

From `modules/02-prompt-context-engineering` in PowerShell:

```powershell
mkdir lesson-07
cd lesson-07
mkdir src
```

Create these files:

```text
lesson.md
results.md
src/main.py
```

Place this lesson inside `lesson.md`.

## Step 2: Create a Virtual Environment

From `lesson-07`:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, the terminal should display something similar to:

```text
(.venv) PS C:\...\lesson-07>
```

### What Is a Virtual Environment?

A virtual environment gives this lesson its own Python packages.

This avoids:

- Polluting the system-wide Python installation
- Conflicting dependency versions between projects
- Accidentally relying on packages installed by another project
- Making the lesson difficult to reproduce elsewhere

If PowerShell prevents the activation script from running, use this for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then try activating the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Step 3: Update `.gitignore`

The repository’s `.gitignore` should include:

```gitignore
.venv/
__pycache__/
*.pyc
.env
```

Do not commit:

- The virtual environment
- Python cache files
- Environment files containing secrets
- Your Gemini API key

## Step 4: Install the Gemini SDK

Install or update the Google GenAI Python SDK:

```powershell
python -m pip install --upgrade "google-genai>=2.3.0"
```

Record the installed dependencies:

```powershell
python -m pip freeze > requirements.txt
```

The environment can later be restored with:

```powershell
python -m pip install -r requirements.txt
```

## Step 5: Configure the Gemini API Key

Set the key for the current PowerShell session:

```powershell
$env:GEMINI_API_KEY="your-api-key"
```

Do not place the actual API key inside `main.py`.

Do not commit it to Git.

---

# 7. Create `src/main.py`

Copy the following starter code into `src/main.py`:

```python
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

    # TODO 1:
    # Return a reusable f-string containing all the required rules.
    #
    # The template must include:
    #
    # - clinic_name
    # - services_text
    # - the administrative role
    # - the four business-critical fields
    # - rules for missing information
    # - rules for vague information
    # - rules for contradictions
    # - a maximum of three clarification questions
    # - a prohibition against claiming a booking is confirmed
    # - the required output contract
    #
    # Use a triple-quoted f-string so the instruction can span
    # multiple lines.
    #
    # Call .strip() on the final string to remove unnecessary
    # whitespace from its beginning and end.
    return ""


def build_user_input(request_text: str) -> str:
    """
    Wrap user-controlled content in clearly labelled delimiters.

    Delimiters help communicate the prompt's structure to the model,
    but they do not sanitize the content or create a security boundary.
    """

    # TODO 2:
    # Return request_text inside <user_request> delimiters.
    #
    # Expected shape:
    #
    # <user_request>
    # [the actual request]
    # </user_request>
    return ""


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

    # TODO 3:
    # Call build_system_instruction() using clinic_name
    # and allowed_services.
    system_instruction = ""

    # TODO 4:
    # Read request_text from the test_case dictionary and pass it
    # to build_user_input().
    input_text = ""

    # Record the time immediately before the Gemini request.
    started_at = perf_counter()

    # TODO 5:
    # Call client.interactions.create() with:
    #
    # - model=MODEL
    # - system_instruction=system_instruction
    # - input=input_text
    # - store=False
    #
    # Save the returned Interaction object in this variable.
    interaction = None

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
```

---

# 8. Implementation Requirements

Complete all five TODOs.

## TODO 1: Build the System Instruction

The system-instruction template must include the following requirements.

### Administrative Role

The model:

- Assists with administrative appointment intake
- Summarizes the user’s request
- Determines whether sufficient information is available
- Does not perform a real booking
- Does not claim a booking is confirmed

### Allowed Services

The allowed-service list must come from the `allowed_services` parameter.

Do not hardcode the services directly inside the reusable template logic.

The existing `services_text` variable has already converted the list into a bulleted string.

Insert it into the f-string:

```python
Allowed services:
{services_text}
```

### Business-Critical Fields

Require these four fields:

1. Patient type: new or returning
2. Requested service
3. Preferred date
4. Preferred time

### Ambiguity Policy

The template must instruct the model to:

- Never invent missing business-critical information.
- Use `UNKNOWN` when a required value is unavailable.
- Treat vague terms such as “usual” and “soon” as ambiguous unless supplied context defines them.
- Identify contradictory information.
- Ask no more than three focused clarification questions.
- Avoid asking for information already clearly supplied.
- Use only a service from the allowed-service list.
- Report unsupported services instead of silently changing them.
- Never claim that an appointment has been confirmed or booked.

### Output Contract

Require this exact readable structure:

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

- `READY`: all required fields are available and consistent.
- `NEEDS_CLARIFICATION`: at least one required field is missing or ambiguous.
- `CONFLICT`: the request contains information that cannot be satisfied together.

Use `UNKNOWN` when a value is missing.

This remains a prompt-level output contract. The model can still violate it.

Module 3 will introduce schema-enforced structured output and runtime validation.

## TODO 2: Build the User Input

Use a triple-quoted f-string:

```python
return f"""
<user_request>
{request_text}
</user_request>
""".strip()
```

The `f` allows Python to insert the value of `request_text`.

The delimiters help the model identify where user-controlled data starts and ends.

However, the delimiters do not:

- Sanitize the content
- Enforce authorization
- Prevent every prompt-injection attempt
- Guarantee correct model behavior

## TODO 3: Build the Stable System Instruction

Call the function using the clinic configuration:

```python
system_instruction = build_system_instruction(
    clinic_name,
    allowed_services,
)
```

Python does not require `const`, `let`, or `var` when defining a variable.

## TODO 4: Build the Request-Specific Input

Read the request from the dictionary:

```python
input_text = build_user_input(test_case["request_text"])
```

The expression:

```python
test_case["request_text"]
```

retrieves the dictionary value stored under the `request_text` key.

## TODO 5: Call Gemini

Use:

```python
interaction = client.interactions.create(
    model=MODEL,
    system_instruction=system_instruction,
    input=input_text,
    store=False,
)
```

Python uses named arguments with `=`.

Unlike a TypeScript object argument, these arguments are not wrapped inside `{}`.

`store=False` makes the experiment stateless. The application does not need Gemini to retain these independent experiment requests for later conversation continuation.

---

# 9. Run the Experiment

From `lesson-07`, ensure the virtual environment is active:

```powershell
.\.venv\Scripts\Activate.ps1
```

Ensure the API key is configured for the current terminal:

```powershell
$env:GEMINI_API_KEY="your-api-key"
```

Run the program:

```powershell
python src/main.py
```

You should receive four results:

1. Complete request
2. Missing-date request
3. Vague request
4. Contradictory request

---

# 10. Expected Conceptual Handling

| Case | Expected status | Reason |
|---|---|---|
| Complete | `READY` | All four required fields are supplied |
| Missing date | `NEEDS_CLARIFICATION` | No calendar date is supplied |
| Vague | `NEEDS_CLARIFICATION` | “Usual” and “soon” are undefined |
| Contradictory | `CONFLICT` | Morning-only availability conflicts with 3:00 PM |

Do not modify the prompt merely to force these exact words.

Evaluate whether the model correctly handled the underlying business situation.

Remember that one successful execution does not establish perfect reliability. Model output is probabilistic and can vary across repeated executions.

---

# 11. Create `results.md`

Copy the following template into `results.md`:

````markdown
# Lesson 7 Results

## AI Requirement

- **Provider:** Google Gemini API
- **Tier:** Free
- **Model:** `gemini-3.7-flash`
- **Actual cost:** $0
- **Data:** Synthetic only
- **Language:** Python
- **SDK:** `google-genai`

## Experiment Results

| Case | Expected handling | Actual status | Invented critical information? | Questions relevant? | Latency (ms) |
|---|---|---|---|---|---:|
| Complete | Ready | | | N/A | |
| Missing date | Needs clarification | | | | |
| Vague | Needs clarification | | | | |
| Contradictory | Conflict | | | | |

Use `Yes`, `No`, or `Partial` for the evaluation columns where appropriate.

## Actual Outputs

### Complete

```text
Paste the output here.
```

### Missing Date

```text
Paste the output here.
```

### Vague

```text
Paste the output here.
```

### Contradictory

```text
Paste the output here.
```

## Observations

### 1. Complete Request

The complete case supplies the patient type, service, date, and time.

**Question:** Did the model recognize that enough information was available without asking unnecessary questions? Explain any unnecessary question it asked.

My answer:

### 2. Missing Date

This request supplies the patient type, service, and general time of day but does not provide a calendar date.

**Question:** Did the model leave the date unknown and request it, or did it invent a date? Why would inventing a date be dangerous?

My answer:

### 3. Vague Request

The phrases “usual appointment” and “soon” depend on information unavailable in the request.

**Question:** Which fields were ambiguous, and what information did the model request to resolve them?

My answer:

### 4. Contradictory Request

The user says they are available only in the morning but requests 3:00 PM.

**Question:** Did the model recognize the contradiction? What must happen before the application prepares a booking operation?

My answer:

## Python Reflection

### 1. Function Type Hints

Consider:

```python
def build_user_input(request_text: str) -> str:
```

**Question:** What do the two `str` type hints communicate? Are they automatically enforced at runtime by standard Python?

My answer:

### 2. F-Strings

Consider:

```python
message = f"Clinic: {clinic_name}"
```

**Question:** What does the `f` before the string allow Python to do?

My answer:

### 3. Main Guard

Consider:

```python
if __name__ == "__main__":
    main()
```

**Question:** Why is this preferable to calling `main()` unconditionally at the bottom of a reusable Python file?

My answer:

## Knowledge Check

### 1. Why Use a Prompt Template?

Imagine three API routes independently construct slightly different clinic prompts.

**Question:** What maintenance and reliability problems could arise compared with using one reusable template?

My answer:

### 2. Which Details May Be Assumed?

A user writes:

> Please give me a short reply and book a cleaning soon.

“Short” concerns writing style, while “soon” affects the requested appointment date.

**Question:** Why might the model interpret “short” approximately but require clarification for “soon”?

My answer:

### 3. Why Is Prompt Validation Insufficient?

The template tells the model to output `READY` only when every required field is available.

**Question:** Why must application code still verify those fields before allowing a booking operation?

My answer:

### 4. What Is a Contradiction?

A request says:

> Tuesday morning works, but schedule it Tuesday at 4:00 PM.

**Question:** Why should the model report a conflict instead of selecting one of the two times?

My answer:

### 5. What Belongs in the Template?

Consider:

- Clinic role and behavioral rules
- Allowed service list
- Current user request
- Output contract
- Specific patient’s preferred date

**Question:** Which values are stable template instructions, configuration variables, and request-specific variables? Explain your grouping.

My answer:
````

---

# 12. Completion Criteria

Submit all of the following:

- [ ] Completed `src/main.py`
- [ ] Created `requirements.txt`
- [ ] Produced four successful Gemini responses
- [ ] Completed the experiment-results table
- [ ] Recorded all four actual outputs
- [ ] Answered all four observation questions
- [ ] Answered all three Python-reflection questions
- [ ] Answered all five knowledge-check questions
- [ ] Confirmed that `.venv` and secrets are excluded from Git

After completing and pushing the lesson, say:

```text
Done. Please check Lesson 7.
```

The review will cover:

- Correctness of the Python implementation
- Understanding of the new Python concepts
- Prompt-template design
- Ambiguity handling
- Contradiction handling
- Application-level validation
- Accuracy of the experiment evaluation

Because this is the first Python lesson, minor style issues will be treated differently from actual conceptual or implementation errors.

After the lesson passes, create the permanent lesson summary in `README.md`.

---

# 13. Optional Extension — Approximately 60 Minutes

Add a second clinic configuration:

```python
CLINIC_CONFIGURATIONS = [
    {
        "clinic_name": "Northstar Dental Clinic",
        "allowed_services": [
            "cleaning",
            "administrative consultation",
        ],
    },
    {
        "clinic_name": "Harbor Physical Therapy",
        "allowed_services": [
            "initial assessment",
            "follow-up session",
        ],
    },
]
```

Use the same `build_system_instruction()` function for both configurations.

Confirm that:

- Clinic names are not hardcoded inside the template.
- Service lists are not hardcoded inside the template.
- The same template logic works for both businesses.
- Each business receives only its own allowed services.

---

# 14. Optional Deep Work — Up to 120 Minutes

Create a deterministic pre-validation structure:

```python
from dataclasses import dataclass


@dataclass
class IntakeFields:
    patient_type: str | None = None
    service: str | None = None
    preferred_date: str | None = None
    preferred_time: str | None = None


@dataclass
class ValidationResult:
    valid: bool
    missing_fields: list[str]
    errors: list[str]
```

A dataclass is a Python class designed primarily to store related data.

It automatically generates useful behavior such as an initializer.

For comparison, this:

```python
@dataclass
class ValidationResult:
    valid: bool
    missing_fields: list[str]
    errors: list[str]
```

serves a similar data-modeling purpose to:

```typescript
type ValidationResult = {
  valid: boolean;
  missingFields: string[];
  errors: string[];
};
```

Compare:

- Fields the model reports as missing
- Fields deterministic validation reports as missing
- Cases where they disagree

Possible test cases:

- Complete input
- Every required field missing individually
- Multiple missing fields
- Unsupported service
- Contradictory time information
- Empty user input

The model’s classification should not override deterministic application validation.

---

# 15. Common Python Mistakes

## Forgetting to Activate the Virtual Environment

If the Gemini package appears to be missing, first check whether `.venv` is active.

Activate it with:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Installing the Wrong Package

Use:

```powershell
python -m pip install google-genai
```

Do not use the older package:

```text
google-generativeai
```

## Forgetting the `f` Prefix

Incorrect:

```python
message = "Clinic: {clinic_name}"
```

This produces the literal text `{clinic_name}`.

Correct:

```python
message = f"Clinic: {clinic_name}"
```

## Using TypeScript Placeholder Syntax

Incorrect Python:

```python
message = f"Clinic: ${clinic_name}"
```

Correct Python:

```python
message = f"Clinic: {clinic_name}"
```

## Incorrect Indentation

Python uses indentation to define blocks.

Incorrect:

```python
def main() -> None:
print("Hello")
```

Correct:

```python
def main() -> None:
    print("Hello")
```

## Using `null` Instead of `None`

Python uses:

```python
value = None
```

JavaScript and TypeScript commonly use:

```typescript
const value = null;
```

## Using Lowercase Boolean Values

Python:

```python
store = False
enabled = True
```

JavaScript and TypeScript:

```typescript
const store = false;
const enabled = true;
```

---

# 16. Production Concerns

- Do not duplicate prompt templates across multiple routes.
- Keep stable behavioral rules separate from request-specific data.
- Treat user input and external documents as untrusted content.
- Do not allow the model to invent business-critical values.
- Do not treat vague natural language as confirmed operational data.
- Do not ask users for information they already supplied.
- Do not assume a prompt-level output contract is guaranteed.
- Validate model output before using it.
- Do not execute a booking solely because the model returned `READY`.
- Check real availability using deterministic application code.
- Enforce authentication and authorization outside the model.
- Restrict tools and database operations according to user permissions.
- Do not log sensitive patient information without an appropriate privacy and retention policy.
- Regression-test prompt-template changes against representative cases.
- Do not commit API keys, `.env` files, or virtual environments.

---

# 17. Core Principle

A reusable prompt template improves consistency, maintainability, and testability. It can guide a model to identify missing or contradictory information, but it cannot guarantee correct output.

Before allowing an operational action, application code must independently validate the required fields, enforce business rules, check authorization, and verify that the real operation succeeded.

---

# Immediate Task

1. Create and activate `.venv`.
2. Install `google-genai`.
3. Create `requirements.txt`.
4. Implement the five TODOs in `src/main.py`.
5. Run all four test cases.
6. Complete `results.md`.
7. Push the lesson.
8. Say: **“Done. Please check Lesson 7.”**