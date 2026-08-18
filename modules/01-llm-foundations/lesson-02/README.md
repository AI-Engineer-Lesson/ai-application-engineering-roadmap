# Lesson 2 — Reliable Structured Outputs and Validation

This lesson demonstrates how to convert an unstructured patient inquiry into predictable application data using Gemini structured outputs, JSON Schema, and Zod validation.

## AI Requirement

- **Provider:** Google Gemini API
- **Tier:** Free
- **Model:** `gemini-3.7-flash`
- **OpenAI required:** No
- **Data restriction:** Synthetic or non-sensitive data only

## Learning Objectives

This lesson covers:

- Requesting structured JSON from an LLM
- Defining the expected response using JSON Schema
- Parsing JSON safely
- Validating response structure with Zod
- Applying application-level business rules
- Distinguishing incomplete inquiries from invalid AI outputs
- Preventing an AI response from directly confirming an appointment

## Validation Levels

The application distinguishes three forms of validity:

1. **JSON validity** — The output can be parsed as JSON.
2. **Schema validity** — The output contains the required fields and correct data types.
3. **Business validity** — The field values are logically consistent with the application’s rules.

An incomplete patient inquiry is not automatically a validation failure. It can be a valid structured result with an `incomplete` inquiry status.

## Setup

Install the dependencies:

```bash
npm install
```

Set the Gemini API key in the current PowerShell session:

```powershell
$env:GEMINI_API_KEY="your-api-key"
```

Never commit the API key or place it directly in the source code.

## Run

```bash
npm run lesson
```

The program analyzes three synthetic appointment inquiries:

- A vague inquiry with missing patient and scheduling information
- A complete inquiry containing the minimum required information
- A partial urgent inquiry without an exact date and time

## Expected Results

| Case     | Expected validation status | Expected inquiry status        |
| -------- | -------------------------- | ------------------------------ |
| Vague    | `validation_success`       | `incomplete`                   |
| Complete | `validation_success`       | `ready_for_availability_check` |
| Partial  | `validation_success`       | `incomplete`                   |

The exact wording and token usage may vary because the model’s generated output is probabilistic.

## Readiness Requirements

An inquiry is ready for an availability check only when all of the following are present:

- Patient name
- Contact information
- Known appointment type
- Exact preferred date
- Exact preferred time
- No remaining missing-information entries

`ready_for_availability_check` does not mean the appointment has been booked. The clinic’s actual scheduling system must still confirm that the requested slot is available.

## Lesson Files

- `src/index.ts` — Gemini request, schema validation, and business validation
- `results.md` — experiment results, actual outputs, and knowledge-check answers
- `package.json` — dependencies and lesson command
- `tsconfig.json` — TypeScript configuration

## Important Production Principle

Structured output makes an AI response easier to process, but it does not guarantee that the values are correct. Applications must independently validate generated data and apply their own business rules before taking any action.
