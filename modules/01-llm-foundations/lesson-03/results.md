# Lesson 3 Results

## AI Requirement

- **Provider:** Google Gemini API
- **Tier:** Free
- **Model:** `gemini-3.7-flash`
- **Actual cost:** $0
- **Data:** Synthetic only

## Model Limits

| Input-token limit | Output-token limit |
| ----------------: | -----------------: |
|         1,048,576 |             65,536 |

## Experiment

| Case   | Policies | Characters | Preflight input tokens | Actual input tokens | Output tokens | Thought tokens | Total tokens |       Latency (ms) |     Context used (%) | Paid equivalent (USD) |
| ------ | -------: | ---------: | ---------------------: | ------------------: | ------------: | -------------: | -----------: | -----------------: | -------------------: | --------------------: |
| Small  |        1 |        267 |                     51 |                  51 |            15 |            312 |          378 |         19899.7129 | 0.004863739013671875 |             0.0012645 |
| Medium |       25 |       2467 |                    451 |                 451 |            12 |            177 |          640 | 3390.7411999999968 | 0.043010711669921875 | 0.0010470000000000002 |
| Large  |      100 |       9368 |                   1727 |                1727 |            11 |             86 |         1824 |         14585.7494 |  0.16469955444335938 | 0.0016589999999999999 |

## Actual Outputs

### Small

```json
{
  "timestamp": "2026-08-21T04:10:29.397Z",
  "caseId": "small",
  "model": "gemini-3.7-flash",
  "policyCount": 1,
  "promptCharacters": 267,
  "preflightInputTokens": 51,
  "actualInputTokens": 51,
  "outputTokens": 15,
  "thoughtTokens": 312,
  "totalTokens": 378,
  "inputTokenLimit": 1048576,
  "inputContextUtilizationPercent": 0.004863739013671875,
  "latencyMs": 19899.7129,
  "paidEquivalentCostUsd": 0.0012645,
  "actualFreeTierCostUsd": 0,
  "outputText": "Patients are required to confirm their administrative details before an appointment can be finalized."
}
```

### Medium

```json
{
  "timestamp": "2026-08-21T04:10:32.888Z",
  "caseId": "medium",
  "model": "gemini-3.7-flash",
  "policyCount": 25,
  "promptCharacters": 2467,
  "preflightInputTokens": 451,
  "actualInputTokens": 451,
  "outputTokens": 12,
  "thoughtTokens": 177,
  "totalTokens": 640,
  "inputTokenLimit": 1048576,
  "inputContextUtilizationPercent": 0.043010711669921875,
  "latencyMs": 3390.7411999999968,
  "paidEquivalentCostUsd": 0.0010470000000000002,
  "actualFreeTierCostUsd": 0,
  "outputText": "Patients must confirm their administrative details before an appointment can be finalized."
}
```

### Large

```json
{
  "timestamp": "2026-08-21T04:10:47.576Z",
  "caseId": "large",
  "model": "gemini-3.7-flash",
  "policyCount": 100,
  "promptCharacters": 9368,
  "preflightInputTokens": 1727,
  "actualInputTokens": 1727,
  "outputTokens": 11,
  "thoughtTokens": 86,
  "totalTokens": 1824,
  "inputTokenLimit": 1048576,
  "inputContextUtilizationPercent": 0.16469955444335938,
  "latencyMs": 14585.7494,
  "paidEquivalentCostUsd": 0.0016589999999999999,
  "actualFreeTierCostUsd": 0,
  "outputText": "Patients must confirm administrative details before an appointment is finalized."
}
```

## Observations

### How did input size affect token usage?

My answer: Input-token usage increased as the number of policies increased. Input tokens dominated the medium and large cases, but not the small case, whose thinking-token usage was substantially higher.

### Did latency consistently increase with input size?

My answer: Latency did not consistently increase with input size in this run. The small case was slowest, the medium case fastest, and the large case second slowest. Multiple runs would be needed to determine whether input size and latency are correlated.

### Were the preflight and actual input-token counts identical? What might explain the result?

My answer: Yes. They matched because both operations processed the same prompt with the same model and tokenizer. They may differ in more complex workflows if additional instructions, tools, cached content, or other context are included during generation.

## Knowledge Check

### 1. Why are tokens not equivalent to words or characters?

My answer: Some words may require diffent number of tokens.

### 2. What is the difference between preflight token counting and response usage?

My answer: Preflight token counting happens before the request while the actual response usage is after the request finishes. Preflight token counting helps the system decide if the prompt fit to system limit and such. While the actual response usage is the record of actual usage.

### 3. Why should a context window be treated as a capacity limit rather than a target?

My answer: Because the goal is to have the smallest but sufficient context, rather than filling it with unecessary context. It is because adding unecessary context may cloud the AI's judgement, which leads to inaccurate response.

### 4. Why should thinking tokens be included when estimating paid output cost?

My answer: Thinking tokens represent computation performed by the model even though they are not visible in the final response. Because Gemini charges them using the output-token rate, they must be added to visible output tokens when estimating output cost.

### 5. Why should a free-tier application still track latency and paid-equivalent cost?

My answer: Paid-equivalent cost helps estimate production expenses, compare models, and prepare for scaling beyond the free tier. Latency tracking helps detect slow requests and performance regressions that affect the user experience.
