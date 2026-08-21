# Lesson 5 Results

## AI Requirement

- **Provider:** Google Gemini API
- **Tier:** Free
- **Model:** `gemini-3.7-flash`
- **Actual cost:** $0
- **Data:** Synthetic only

## Terminology

### Request ID

A unique value assigned to one request. It allows logs from different parts of the application to be connected to the same operation.

### Prompt version

An identifier representing the exact prompt design used by the application, such as `lesson-05-v1`. This helps identify which prompt produced an output.

### Abstention

A controlled decision not to answer because the available evidence is insufficient or conflicting. Abstention is not necessarily an error.

### Quality verdict

The result of checking whether the generated output satisfied the application’s expected behavior. In this lesson, the verdict is either `PASS` or `FAIL`.

### Retryable error

A temporary error for which trying the request again may succeed, such as some timeouts, rate-limit errors, or service outages.

### Non-retryable error

An error that will probably happen again unless the request or configuration is corrected, such as empty input, an invalid API key, or insufficient permission.

### Transport success

The request successfully reached the provider and received a response. This does not automatically mean the generated answer was correct.

### Discriminated union

A TypeScript union whose members contain a shared field with different literal values, such as:

```ts
type RequestRecord =
  | { status: "success"; outputText: string }
  | { status: "error"; error: ErrorDetails };
```

The `status` field allows TypeScript to determine which type of record is being handled.

## Request Summary

| Case          | Status  | Outcome or error code | Quality verdict |       Latency (ms) | Input tokens | Output tokens | Thought tokens |        Paid equivalent |
| ------------- | ------- | --------------------- | --------------- | -----------------: | -----------: | ------------: | -------------: | ---------------------: |
| Supported     | success | answered              | PASS            |         68008.0844 |           37 |            21 |            132 | 0.00010649999999999999 |
| Abstention    | success | abstained             | PASS            |  63664.35990000001 |           56 |             7 |            185 |             0.00006825 |
| Invalid input | error   | invalid_input         | N/A             | 0.2327999999979511 |          N/A |           N/A |            N/A |                    N/A |

## Actual Records

### Supported

This request contains enough evidence to answer the question. It should produce a successful record with an `answered` outcome.

```json
{
  "timestamp": "2026-08-21T15:37:51.795Z",
  "requestId": "baec997e-daf6-4cce-ae6c-b03651cc2844",
  "model": "gemini-3.7-flash",
  "promptVersion": "lesson-05-v1",
  "caseId": "supported",
  "status": "success",
  "outcome": "answered",
  "qualityVerdict": "PASS",
  "latencyMs": 68008.0844,
  "usage": {
    "inputTokens": 37,
    "outputTokens": 21,
    "thoughtTokens": 132,
    "totalTokens": 190
  },
  "paidEquivalentCostUsd": 0.00010649999999999999,
  "actualFreeTierCostUsd": 0,
  "outputText": "Based on the supplied policy, appointments must be cancelled at least 24 hours before their scheduled time."
}
```

### Abstention

This request does not contain the parking-fee information required to answer the question. It should complete successfully but return the expected abstention response.

```json
{
  "timestamp": "2026-08-21T15:38:55.462Z",
  "requestId": "d8b409af-6a84-4a23-b153-1449de4ecf13",
  "model": "gemini-3.7-flash",
  "promptVersion": "lesson-05-v1",
  "caseId": "abstention",
  "status": "success",
  "outcome": "abstained",
  "qualityVerdict": "PASS",
  "latencyMs": 63664.35990000001,
  "usage": {
    "inputTokens": 56,
    "outputTokens": 7,
    "thoughtTokens": 165,
    "totalTokens": 228
  },
  "paidEquivalentCostUsd": 0.00006825,
  "actualFreeTierCostUsd": 0,
  "outputText": "INSUFFICIENT_EVIDENCE"
}
```

### Invalid Input

This request contains only whitespace. Application validation should reject it before calling Gemini and produce a structured error record.

```json
{
  "timestamp": "2026-08-21T15:38:55.462Z",
  "requestId": "935dda1e-0032-4d5d-bcbd-1f1fd98d1fa4",
  "model": "gemini-3.7-flash",
  "promptVersion": "lesson-05-v1",
  "caseId": "invalid-input",
  "status": "error",
  "latencyMs": 0.2327999999979511,
  "error": {
    "code": "invalid_input",
    "name": "ApplicationError",
    "message": "Prompt must not be empty",
    "retryable": false
  }
}
```

# Observations

## 1. Why is the abstention record a success rather than an error?

### Context

The Gemini request completed normally, and the model followed the instruction to avoid inventing missing information. Think about whether refusing to provide an unsupported answer represents broken execution or correct application behavior.

### Terms

- **Abstention:** Deliberately declining to answer when sufficient evidence is unavailable.
- **Execution error:** A technical problem that prevents the operation from completing.

My answer: Because it is a controlled choice to not answer rather, perhaps due to some missing information.

## 2. Why should records include both a request ID and prompt version?

### Context

Imagine investigating an incorrect output in a production system containing thousands of requests and several deployed prompt versions. Consider what each identifier helps you trace.

### Terms

- **Trace:** Follow an operation across logs or application components.
- **Prompt version:** The identifier of the prompt design used for a request.

My answer: I honestly don't know

## 3. Why should raw prompts normally be excluded from production logs?

### Context

Prompts can contain user messages, internal instructions, personal information, confidential business records, or other sensitive data. Consider what could happen if application logs were exposed or retained indefinitely.

### Terms

- **Raw prompt:** The complete, unmodified text sent to the model.
- **Sensitive data:** Information that must be protected, such as personal, confidential, authentication, or business information.
- **Retention:** How long stored information is preserved.

My answer: It is because raw prompts may contain sensitive information. Including them in the production logs will risk exposure to potential data breach or whatsoever.

## 4. Which record would be appropriate to retry, if any?

### Context

The three core cases are:

1. A successful supported answer
2. A successful abstention
3. An empty-input validation error

Retrying the same operation without changing anything is useful only when the failure may be temporary. Decide whether any of these outcomes could change simply by immediately trying again.

### Terms

- **Retry:** Attempt the same operation again after failure.
- **Transient error:** A temporary error that may disappear without changing the request.
- **Validation error:** An error caused by input that does not satisfy application requirements.

My answer: 1 and 2. But I'm not sure.

# Knowledge Check

## 1. What is the difference between transport success and output-quality success?

### Context

An API can return HTTP success and valid text even when the text is factually incorrect or fails the business requirement. Consider the two separate questions:

```text
Did the request technically complete?

Did the result satisfy the application’s expectations?
```

### Terms

- **Transport success:** Successful communication with the external service.
- **Output-quality success:** The generated result passed the application’s quality criteria.
- **Quality criteria:** Rules used to determine whether an output is acceptable.

My answer: The obviouos difference is that tranport success could still happen while it fails on output-quality.

## 2. Why is a discriminated union useful for request records?

### Context

`SuccessRecord` and `ErrorRecord` contain different fields. A success has output, usage, cost, and quality information, while an error has structured error details.

Consider how the `status` field helps TypeScript safely determine which fields are available.

### Terms

- **Union:** A type that permits one of several possible types.
- **Discriminator:** A shared property containing a distinct literal value that identifies a union member.
- **Type narrowing:** TypeScript determining a more specific type after checking a condition.

Example:

```ts
if (record.status === "success") {
  console.log(record.outputText);
} else {
  console.error(record.error.message);
}
```

My answer: Discriminated union is useful to help the system expect different response format, for example when the status is success or fail. Different response status may need to be handledd differently.

## 3. Why should application validation happen before calling the model?

### Context

The invalid-input case contains only whitespace. The application already knows this input cannot produce a useful result, so consider the consequences of sending it to Gemini anyway.

Think about:

- Cost
- Latency
- Rate-limit consumption
- Error clarity
- Unnecessary provider requests

### Terms

- **Application validation:** Checking input against application rules before processing it.
- **Rate limit:** A restriction on how many requests or tokens may be used within a period.
- **Fail fast:** Stop invalid work as early as possible instead of allowing it to proceed through the system.

My answer: This is to help minimize unecessary request, which could potentially increase the usage cost if left unchecked.

## 4. Which errors are generally retryable, and which are not?

### Context

Retrying can help when a failure is temporary, but it can make problems worse when the request itself is invalid.

Classify examples such as:

- Network interruption
- Request timeout
- Rate limit
- Temporary provider outage
- Empty prompt
- Invalid API key
- Permission denial
- Malformed request

### Terms

- **Retryable:** Likely to succeed later without changing the request.
- **Exponential backoff:** Increasing the delay between retry attempts, commonly one second, two seconds, four seconds, and so on.
- **Jitter:** A small random delay added to retries so that many clients do not retry simultaneously.
- **Malformed request:** A request that does not follow the API’s required format.

My answer: Network Interruption, Request Timeout, Rate Limit, and Temporary Provider Outage can be retryable. Empty prompt, Invalid API key, Permission denial, Malformed Request are not retryable.

## 5. Why should output quality be measured separately from latency and token usage?

### Context

Latency and token usage describe performance and resource consumption. Neither one determines whether the generated answer is correct.

Consider these possible combinations:

```text
Fast and cheap, but incorrect
Slow and expensive, but correct
Fast, cheap, and correct
Slow, expensive, and incorrect
```

### Terms

- **Latency:** The time between starting a request and receiving its result.
- **Token usage:** The number of tokens processed or generated.
- **Quality metric:** A measurement indicating whether an output satisfies correctness or business requirements.
- **Tradeoff:** A situation where improving one property may negatively affect another.

My answer: This is to help measure if we've set up the prompt correctly. The less incorrect answers, the better the output quality.

# Final Review Checklist

Before submitting, confirm that:

- [/] The supported case has `status: "success"`
- [/] The supported case has `outcome: "answered"`
- [/] The supported quality verdict is `PASS`
- [/] The abstention case has `status: "success"`
- [/] The abstention case has `outcome: "abstained"`
- [/] The abstention quality verdict is `PASS`
- [/] The invalid-input case has `status: "error"`
- [/] The invalid-input error code is `invalid_input`
- [/] The invalid-input error is not retryable
- [/] Each record contains a request ID
- [/] Each record contains the prompt version
- [/] Successful records contain actual token usage
- [/] Successful records contain paid-equivalent cost
- [/] Raw prompts and API keys are absent from the records
- [/] All four observations are answered
- [/] All five knowledge-check questions are answered
