# Lesson 5 — Building an Observable AI Request Pipeline

This lesson integrates the main concepts from Module 1 into a single observable TypeScript AI request pipeline.

The application records successful answers, controlled abstentions, validation errors, latency, token usage, paid-equivalent cost, prompt versions, request identifiers, and deterministic quality verdicts.

## Learning Objectives

- Build structured success and error records
- Distinguish answered, abstained, and failed requests
- Assign unique request identifiers
- Track model and prompt versions
- Measure request latency
- Record input, output, thinking, and total tokens
- Calculate paid-equivalent cost
- Apply deterministic output-quality checks
- Validate input before calling the model
- Avoid logging raw prompts and sensitive information

## AI Requirement

- **Provider:** Google Gemini API
- **Model:** `gemini-3.7-flash`
- **Tier:** Free
- **Actual cost:** $0 within free-tier limits
- **Data:** Synthetic only

Do not use real patient information, private clinic records, API keys, or other sensitive information in prompts or logs.

## Observable Request Outcomes

The application recognizes three distinct outcomes.

### Answered

The request completed, sufficient evidence was available, and the model produced an answer.

```text
status: success
outcome: answered
qualityVerdict: PASS or FAIL
```

### Abstained

The request completed, but the available evidence was insufficient. The model correctly declined to invent an answer.

```text
status: success
outcome: abstained
qualityVerdict: PASS or FAIL
```

### Error

The application could not execute the request successfully.

```text
status: error
error.code: structured error identifier
error.retryable: true or false
```

An abstention is not a technical failure. It is a controlled and potentially correct application outcome.

## Request Records

The application uses a discriminated union:

```ts
type RequestRecord = SuccessRecord | ErrorRecord;
```

Both record types contain a `status` field:

```ts
if (record.status === "success") {
  console.log(record.outputText);
} else {
  console.error(record.error.message);
}
```

This allows TypeScript to safely determine which fields are available.

## Success Records

A successful record contains:

- Timestamp
- Request ID
- Model
- Prompt version
- Case ID
- Status
- Answered or abstained outcome
- Quality verdict
- Latency
- Token usage
- Paid-equivalent cost
- Actual free-tier cost
- Generated output

Transport success does not guarantee output-quality success. The API may return a valid response that still fails the application’s correctness requirements.

## Error Records

A structured error record contains:

- Timestamp
- Request ID
- Model
- Prompt version
- Case ID
- Error status
- Latency before failure
- Error code
- Error name
- Safe error message
- Retryable classification

Example:

```json
{
  "status": "error",
  "error": {
    "code": "invalid_input",
    "name": "ApplicationError",
    "message": "Prompt must not be empty",
    "retryable": false
  }
}
```

## Request IDs and Prompt Versions

A request ID identifies one specific execution. It helps connect logs created by different parts of the application.

A prompt version identifies the prompt design that produced the output.

Together, they help answer questions such as:

- Which request failed?
- Which prompt version produced the result?
- Did failures increase after a prompt change?
- Are quality problems concentrated in one version?

## Input Validation

The application rejects empty or whitespace-only prompts before contacting Gemini:

```ts
if (!prompt.trim()) {
  throw new ApplicationError(
    "invalid_input",
    "Prompt must not be empty",
    false,
  );
}
```

Early validation:

- Avoids unnecessary API requests
- Reduces latency and cost
- Preserves rate-limit capacity
- Produces clearer application errors
- Prevents invalid work from reaching the provider

## Token Usage

Successful records include:

```ts
type TokenUsage = {
  inputTokens: number;
  outputTokens: number;
  thoughtTokens: number;
  totalTokens: number;
};
```

These values are read from Gemini’s response usage metadata.

## Paid-Equivalent Cost

Input cost is calculated with:

```text
input tokens
÷ 1,000,000
× input-token rate
```

Output cost includes visible output and thinking tokens:

```text
(output tokens + thinking tokens)
÷ 1,000,000
× output-token rate
```

Combined cost:

```text
input cost + output cost
```

Thinking tokens must not be omitted because they are included in paid output usage even when they are not visible in the final answer.

## Deterministic Quality Evaluation

The application does not ask another model to grade the output.

For the supported case, the output must contain:

```text
24 hours
```

For the abstention case, the trimmed output must exactly equal:

```text
INSUFFICIENT_EVIDENCE
```

This separates three measurements:

- **Latency:** How fast was the request?
- **Token usage and cost:** How many resources did it consume?
- **Quality:** Did the output meet the requirement?

A response can be fast and cheap while still being incorrect.

## Retry Classification

Temporary errors may be retryable:

- Network interruptions
- Timeouts
- Rate limits
- Temporary provider outages
- Some server errors

Errors caused by the request or configuration are generally not retryable without correction:

- Empty input
- Invalid API key
- Permission denial
- Malformed request

None of the three core experiment records should be retried:

- The supported request already succeeded.
- The abstention behaved correctly.
- The empty prompt will remain invalid until changed.

## Logging and Privacy

Raw prompts should normally be excluded from production logs because they may contain:

- Personal information
- Confidential business records
- Internal instructions
- Authentication information
- User-provided sensitive content

Prefer logging identifiers, versions, usage measurements, verdicts, and sanitized error information.

## Prerequisites

- Node.js
- npm
- TypeScript
- A Gemini API key

## Installation

From the `lesson-05` directory:

```powershell
npm install
```

## API-Key Setup

Set the Gemini API key for the current PowerShell session:

```powershell
$env:GEMINI_API_KEY="your-api-key"
```

Never commit the API key or place it directly in source code.

## Run the Application

```powershell
npm run lesson
```

The application runs three cases:

| Case          | Expected status | Expected outcome |
| ------------- | --------------- | ---------------- |
| Supported     | `success`       | `answered`       |
| Abstention    | `success`       | `abstained`      |
| Invalid input | `error`         | `invalid_input`  |

## Project Structure

```text
lesson-05/
├── src/
│   └── index.ts
├── package.json
├── package-lock.json
├── tsconfig.json
├── results.md
└── README.md
```

## Results

See [`results.md`](./results.md) for:

- Complete structured request records
- Latency and token measurements
- Paid-equivalent costs
- Quality verdicts
- Observations
- Knowledge-check answers

## Production Considerations

- API success and output quality are separate concerns.
- Abstention should remain distinct from technical failure.
- Prompt and model versions should be recorded.
- Request IDs should remain consistent across retries and services.
- Input validation should happen before provider calls.
- Retry only temporary failures.
- Retry attempts must be limited.
- Exponential backoff and jitter should be used for production retries.
- Raw sensitive prompts should not be logged without a justified retention policy.
- Latency, cost, and quality must be monitored separately.

## Important Takeaway

Production AI applications need more than generated text. Every request should produce enough structured information to explain what ran, what it consumed, whether it satisfied the requirement, and how failures should be handled.
