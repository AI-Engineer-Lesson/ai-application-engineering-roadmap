# Module 1 Reviewer — How Production LLM Applications Work

This reviewer summarizes the essential concepts, formulas, implementation patterns, experiments, and production concerns covered in Lessons 1–5.

## Module Lessons

1. Anatomy of a Production LLM Request
2. Reliable Structured Outputs and Validation
3. Tokens, Context Windows, Latency, and Cost
4. Hallucinations, Evidence Boundaries, and Failure Modes
5. Building an Observable AI Request Pipeline

# 1. Essential Terminology

## Large Language Model

A system trained to predict and generate tokens based on patterns learned from large amounts of data.

An LLM does not retrieve a guaranteed fact for every question. It generates a probable continuation based on its input and learned patterns.

## Token

A unit of text processed by a model.

A token is not necessarily:

- One word
- One character
- One syllable

A common word might be one token, while an unusual word or Unicode character may require several tokens.

## Prompt

The instructions, context, examples, and user data supplied to the model.

## Context Window

The maximum number of tokens a model can process within a request or interaction.

A context window is a capacity limit, not a target. Providing more context does not automatically improve quality.

## Latency

The time between starting a request and receiving its result.

Latency is commonly measured in milliseconds:

```ts
const startedAt = performance.now();
const response = await callModel();
const latencyMs = performance.now() - startedAt;
```

## Probabilistic Output

Output that is generated according to probabilities rather than fixed application logic.

Identical or similar requests may produce different:

- Wording
- Reasoning
- Token usage
- Latency
- Quality

One successful generation does not prove that a feature is reliable.

## Hallucination

A generated factual claim that is unsupported by the evidence available to the application.

A claim may still be a hallucination even when it:

- Sounds reasonable
- Is written confidently
- Is grammatically correct
- Happens to be true elsewhere

## Abstention

A controlled decision not to answer because sufficient or consistent evidence is unavailable.

Abstention is normally a successful application outcome, not a technical failure.

## Transport Success

The model request technically completed and returned a response.

Transport success does not prove that the output is correct.

## Output-Quality Success

The generated output satisfied the application’s defined correctness or business requirements.

## Request ID

A unique identifier assigned to one request. It allows logs from different application components to be connected to the same operation.

## Prompt Version

An identifier for the exact prompt design used by a request.

Prompt versions help determine whether failures or regressions are concentrated in a particular prompt revision.

## Retryable Error

A temporary failure that may succeed when attempted again.

Examples include some:

- Timeouts
- Network interruptions
- Rate limits
- Temporary service outages
- Server errors

## Non-Retryable Error

A failure that requires the request, credentials, permissions, or configuration to change.

Examples include:

- Empty input
- Invalid API key
- Permission denial
- Malformed request

## Discriminated Union

A TypeScript union whose members share a field containing different literal values.

```ts
type RequestRecord =
  | {
      status: "success";
      outputText: string;
    }
  | {
      status: "error";
      error: ErrorDetails;
    };
```

The `status` field allows TypeScript to narrow the record safely:

```ts
if (record.status === "success") {
  console.log(record.outputText);
} else {
  console.error(record.error.message);
}
```

# 2. Anatomy of an LLM Request

A minimal Gemini interaction uses:

```ts
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

const response = await ai.interactions.create({
  model: "gemini-3.7-flash",
  input: prompt,
});
```

A production application must observe more than `output_text`.

Useful operational information includes:

- Request or response identifier
- Model
- Prompt version
- Latency
- Input tokens
- Output tokens
- Thinking tokens
- Total tokens
- Paid-equivalent cost
- Output-quality verdict
- Structured errors

Core principle:

```text
API success ≠ output-quality success
```

# 3. Structured Output and Validation

Structured generation makes model output easier to process, but it does not prove that the generated values are correct.

Validation should occur at multiple levels.

## Level 1: JSON Validity

Can the output be parsed as JSON?

```ts
const parsed = JSON.parse(outputText);
```

Syntactically invalid JSON fails at this level.

## Level 2: Schema Validity

Does the parsed result contain the required fields and data types?

Zod can perform runtime validation:

```ts
const result = schema.safeParse(parsed);

if (!result.success) {
  // Handle schema failure.
}
```

## Level 3: Business Validity

Are the values logically consistent with application rules?

Examples:

- Required scheduling information is present
- Missing-information fields match the actual missing values
- The AI does not mark an appointment as booked
- An availability check is not treated as booking confirmation

Important relationship:

```text
Valid JSON
does not guarantee
valid schema

Valid schema
does not guarantee
valid business meaning

Valid business structure
does not guarantee
the facts are correct
```

## Incomplete Versus Invalid

An inquiry can be incomplete while remaining valid.

For example:

```json
{
  "status": "incomplete",
  "patientName": null,
  "preferredDate": null,
  "missingInformation": ["patientName", "preferredDate"]
}
```

This may be:

- Valid JSON
- Schema-valid
- Business-valid
- Incomplete for the next workflow step

Incomplete business data should not automatically be treated as malformed AI output.

# 4. Tokens and Context Windows

## Preflight Token Count

A preflight count occurs before generation:

```ts
const countResponse = await ai.models.countTokens({
  model,
  contents: prompt,
});

const preflightInputTokens = countResponse.totalTokens ?? 0;
```

It answers:

```text
Can or should the application send this input?
```

Applications can use it to:

- Enforce an input budget
- Prevent context overflow
- Reduce unnecessary cost
- Reject unexpectedly large requests

## Actual Usage

Actual usage is available after generation:

```ts
const inputTokens = response.usage?.total_input_tokens ?? 0;

const outputTokens = response.usage?.total_output_tokens ?? 0;

const thoughtTokens = response.usage?.total_thought_tokens ?? 0;

const totalTokens = response.usage?.total_tokens ?? 0;
```

It answers:

```text
What did the completed request consume?
```

Preflight and actual input counts may match when both operations process the same prompt using the same model and tokenizer.

Do not assume they will always match in more complex workflows involving:

- Additional instructions
- Tools
- Cached content
- Conversation history
- Provider-added context

## Context Utilization

```text
actual input tokens
÷ input-token limit
× 100
```

TypeScript:

```ts
const contextUtilizationPercent = (actualInputTokens / inputTokenLimit) * 100;
```

A low utilization percentage does not prove that every supplied token was useful.

The goal is:

```text
Smallest sufficient context
```

Avoid:

```text
Largest context that fits
```

# 5. Cost Calculation

The Module 1 experiments used these paid-equivalent rates:

```ts
const paidPricing = {
  inputPerMillionTokensUsd: 0.75,
  outputPerMillionTokensUsd: 3.75,
};
```

Provider pricing can change, so production rates should be configured and regularly verified rather than permanently buried in application logic.

## Input Cost

```text
input tokens
÷ 1,000,000
× input rate
```

## Output Cost

Thinking tokens are included:

```text
(output tokens + thinking tokens)
÷ 1,000,000
× output rate
```

## Combined Cost

```ts
function estimatePaidEquivalentCost(usage: TokenUsage): number {
  const inputCost =
    (usage.inputTokens / 1_000_000) * paidPricing.inputPerMillionTokensUsd;

  const outputCost =
    ((usage.outputTokens + usage.thoughtTokens) / 1_000_000) *
    paidPricing.outputPerMillionTokensUsd;

  return inputCost + outputCost;
}
```

Thinking tokens must not be omitted merely because they are invisible in the final answer.

A free-tier application should still track paid-equivalent cost because:

- Free-tier conditions can change
- Production traffic may require paid usage
- Models need fair cost comparisons
- Unexpectedly expensive requests must be detected
- Per-request and per-user budgets may be required

# 6. Evidence-Bounded Generation

Evidence conditions should be distinguished explicitly.

## Sufficient Evidence

The supplied context directly answers the question.

Expected behavior:

```text
Answer using the supplied evidence.
```

## Insufficient Evidence

The required information is absent.

Expected behavior:

```text
INSUFFICIENT_EVIDENCE
```

## Conflicting Evidence

The available records provide incompatible answers.

Expected behavior:

```text
CONFLICTING_EVIDENCE
```

An evidence-bounded prompt may contain:

```text
Use only the supplied evidence.

If the evidence does not answer the question, return:
INSUFFICIENT_EVIDENCE

If the evidence contains incompatible answers, return:
CONFLICTING_EVIDENCE

Do not guess or invent missing details.
```

These instructions reduce hallucination risk but do not eliminate it.

The model may still:

- Misunderstand an instruction
- Miss relevant evidence
- Ignore conflicting evidence
- Produce an unsupported answer
- Fail on unfamiliar or adversarial input

Prompt instructions influence model behavior. They do not enforce behavior deterministically.

# 7. Abstention Versus Error

## Abstention

```text
Request completed
→ model recognized insufficient evidence
→ model returned the required fallback
→ status: success
→ outcome: abstained
```

## Technical Failure

```text
Request attempted
→ timeout, network failure, provider error, or invalid input
→ status: error
```

Do not retry a correct abstention merely to obtain a different answer. Add missing evidence or escalate the request instead.

# 8. Deterministic Quality Checks

A quality check should represent the application requirement.

Example for a supported answer:

```ts
const passed = outputText.includes("24 hours");
```

Example for required abstention:

```ts
const passed = outputText.trim() === "INSUFFICIENT_EVIDENCE";
```

Deterministic checks are appropriate when success can be expressed through fixed rules.

They are:

- Repeatable
- Fast
- Cheap
- Easy to debug

They may be insufficient for nuanced semantic quality, but they are preferable when exact rules are available.

Quality must be measured separately from:

- Latency
- Token usage
- Cost
- HTTP or transport status

Possible combinations include:

```text
Fast, cheap, and correct
Fast, cheap, and incorrect
Slow, expensive, and correct
Slow, expensive, and incorrect
```

# 9. Observable Request Records

A successful record should contain enough information to explain what happened:

```ts
type SuccessRecord = {
  timestamp: string;
  requestId: string;
  model: string;
  promptVersion: string;
  caseId: string;
  status: "success";
  outcome: "answered" | "abstained";
  qualityVerdict: "PASS" | "FAIL";
  latencyMs: number;
  usage: TokenUsage;
  paidEquivalentCostUsd: number;
  outputText: string;
};
```

A structured error record may use:

```ts
type ErrorRecord = {
  timestamp: string;
  requestId: string;
  model: string;
  promptVersion: string;
  caseId: string;
  status: "error";
  latencyMs: number;
  error: {
    code: string;
    name: string;
    message: string;
    retryable: boolean;
  };
};
```

Do not expose internal stack traces or secrets through user-facing errors.

# 10. Input Validation

Reject invalid input before calling the provider:

```ts
if (!prompt.trim()) {
  throw new ApplicationError(
    "invalid_input",
    "Prompt must not be empty",
    false,
  );
}
```

This is sometimes called **failing fast**: stopping invalid work as early as possible.

Benefits include:

- Lower cost
- Lower latency
- Reduced rate-limit consumption
- Clearer errors
- Less provider dependency
- Easier debugging

# 11. Retry Principles

Retry only when the failure may be temporary.

Generally retryable:

- Network interruption
- Timeout
- Rate limit
- Temporary provider outage
- Some server-side errors

Generally non-retryable without correction:

- Empty input
- Invalid API key
- Permission denial
- Malformed request
- Unsupported operation

Production retries should include:

- Maximum attempt count
- Exponential backoff
- Jitter
- Consistent request or correlation ID
- Logging of attempt numbers
- Idempotency protection for operations with side effects

## Exponential Backoff

Increasing the delay between attempts:

```text
Attempt 1 → wait approximately 1 second
Attempt 2 → wait approximately 2 seconds
Attempt 3 → wait approximately 4 seconds
```

## Jitter

A small random delay added to prevent many clients from retrying simultaneously.

# 12. Logging and Privacy

Raw prompts may contain:

- Personal information
- Confidential business data
- Internal application instructions
- Authentication details
- Uploaded-document content
- User-provided secrets

Prefer logging:

- Request ID
- Model
- Prompt version
- Input size
- Token usage
- Latency
- Cost
- Outcome
- Quality verdict
- Sanitized error details

**Sanitized** means sensitive or unnecessary information has been removed or replaced before storage or display.

If raw prompt logging is genuinely required, define:

- Access control
- Retention period
- Encryption
- Redaction
- Deletion procedures
- User disclosure or consent where appropriate

# 13. Common Failure Modes

## Treating API Success as Product Success

A valid response can still be incorrect or unusable.

## Trusting Structured Output Automatically

Schema-valid data can contain false or inconsistent values.

## Treating Incomplete Data as Invalid

Missing business information can be represented through a valid incomplete state.

## Ignoring Thinking Tokens

This causes output-cost estimates to be understated.

## Filling the Context Window

More context can increase latency, cost, conflict, and retrieval noise.

## Retrying Every Error

Invalid requests will continue failing and waste resources.

## Retrying Abstention

Repeated generation without new evidence can create inconsistent or unsupported answers.

## Logging Sensitive Prompts

Logs often have broader access and longer retention than application data.

## Drawing Conclusions From One Run

One successful experiment does not establish reliability or latency trends.

## Using Confidence as Evidence

The model’s tone does not prove factual correctness.

# 14. Module Experiment Findings

The completed experiments demonstrated that:

- Similar requests can vary in latency and token usage.
- Larger input produced more input tokens.
- Latency did not increase consistently in a single three-case experiment.
- Preflight and actual input counts matched for the same simple prompts.
- Thinking tokens can dominate the visible output-token count.
- A baseline prompt can abstain correctly, but one success does not prove reliability.
- Evidence-bounded prompts create clearer machine-detectable outcomes.
- An incomplete inquiry can remain schema-valid and business-valid.
- Transport success and output-quality success must be recorded separately.
- Empty input should fail before reaching Gemini.
- None of the answered, correctly abstained, or invalid-input records should be retried unchanged.

# 15. Retrieval-Practice Questions

Answer these without looking at the sections above.

## Question 1

Why does a technically successful API request not guarantee a successful AI feature?

## Question 2

What are the three validation levels used for structured output?

## Question 3

Can an incomplete inquiry still be schema-valid and business-valid? Explain.

## Question 4

What is the difference between preflight token counting and actual response usage?

## Question 5

Why should a context window be treated as a limit rather than a target?

## Question 6

Write the formula for input-context utilization.

## Question 7

Which token categories are included when estimating output cost?

## Question 8

What makes a generated claim a hallucination in an evidence-bounded application?

## Question 9

What is the difference between insufficient and conflicting evidence?

## Question 10

Why is abstention usually represented as success rather than error?

## Question 11

What is the difference between transport success and output-quality success?

## Question 12

Why should request records contain both a request ID and prompt version?

## Question 13

Which failures should generally be retried?

## Question 14

Why should raw prompts normally be excluded from production logs?

## Question 15

Why must latency, cost, and quality be measured separately?

# 16. Answers

## Answer 1

The provider can successfully return text that is incorrect, unsupported, malformed for the business requirement, or otherwise unusable. Technical completion and output quality are separate.

## Answer 2

1. JSON validity
2. Schema validity
3. Business validity

## Answer 3

Yes. An inquiry can follow the correct schema and accurately represent that required business information is missing. Incompleteness is a valid business state.

## Answer 4

Preflight counting estimates input tokens before sending the generation request. Response usage records the tokens actually consumed by a completed request, including output and thinking tokens.

## Answer 5

Filling the window can add irrelevant or contradictory context, increase cost and latency, and make failures harder to understand. The goal is the smallest sufficient context.

## Answer 6

```text
actual input tokens
÷ input-token limit
× 100
```

## Answer 7

Visible output tokens and thinking tokens:

```text
output tokens + thinking tokens
```

## Answer 8

It makes a factual claim that is not supported by the evidence supplied to the application.

## Answer 9

Insufficient evidence means the required information is absent. Conflicting evidence means available records provide incompatible answers.

## Answer 10

The request completed correctly and followed the safety requirement not to invent missing information. It is a controlled outcome rather than an execution failure.

## Answer 11

Transport success means communication with the provider completed. Output-quality success means the returned content satisfied the application’s correctness criteria.

## Answer 12

The request ID traces one execution. The prompt version identifies the prompt design used by that execution. Together, they support debugging and regression analysis.

## Answer 13

Temporary failures such as some timeouts, network interruptions, rate limits, service outages, and server errors. Invalid input, authentication, permission, and malformed-request errors require correction instead.

## Answer 14

Prompts may contain personal, confidential, internal, or authentication information. Storing them increases breach, access, and retention risks.

## Answer 15

They measure different properties. Latency measures speed, token usage and cost measure resource consumption, and quality measures whether the output satisfies the requirement.

# 17. Final Review Checklist

You should now be able to explain or implement the following:

- [ ] Make a Gemini request from TypeScript
- [ ] Measure request latency
- [ ] Read actual token usage
- [ ] Count input tokens before generation
- [ ] Calculate context utilization
- [ ] Calculate input cost
- [ ] Include thinking tokens in output cost
- [ ] Distinguish JSON, schema, and business validity
- [ ] Represent incomplete data without treating it as malformed
- [ ] Define hallucination using available evidence
- [ ] Distinguish sufficient, insufficient, and conflicting evidence
- [ ] Represent abstention separately from failure
- [ ] Apply deterministic output checks
- [ ] Build structured success and error records
- [ ] Use request IDs and prompt versions
- [ ] Classify retryable and non-retryable errors
- [ ] Validate input before provider calls
- [ ] Avoid logging secrets and sensitive raw prompts
- [ ] Explain why one successful run does not prove reliability
- [ ] Measure latency, cost, and quality separately

# Module 1 Core Principle

A production LLM feature is not merely a prompt followed by generated text. It is a monitored, validated, evidence-aware, cost-conscious, and failure-tolerant software system wrapped around a probabilistic model.
