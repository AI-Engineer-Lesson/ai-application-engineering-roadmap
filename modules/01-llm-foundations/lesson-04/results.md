# Lesson 4 Results

## AI Requirement

- **Provider:** Google Gemini API
- **Tier:** Free
- **Model:** `gemini-3.7-flash`
- **Actual cost:** $0
- **Data:** Synthetic only
- **External grounding:** Disabled

## Experiment Results

| Case        | Prompt mode      | Expected behavior     | Observed behavior                                                                          | Verdict |
| ----------- | ---------------- | --------------------- | ------------------------------------------------------------------------------------------ | ------- |
| Supported   | Baseline         | ANSWER_FROM_EVIDENCE  | the response is according to what's provided in the policy                                 | PASS    |
| Supported   | Evidence-bounded | ANSWER_FROM_EVIDENCE  | the response is according to what's provided in the policy                                 | PASS    |
| Missing     | Baseline         | INSUFFICIENT_EVIDENCE | there is no information regarding parking fee, therefore the AI responded appropriately.   | PASS    |
| Missing     | Evidence-bounded | INSUFFICIENT_EVIDENCE | the response text is INSUFFICIENT_EVIDENCE                                                 | PASS    |
| Conflicting | Baseline         | CONFLICTING_EVIDENCE  | there's conflicting information in the policy, but the AI responded with both information. | PASS    |
| Conflicting | Evidence-bounded | CONFLICTING_EVIDENCE  | the response text is CONFLICTING_EVIDENCE                                                  | PASS    |

Use one of these verdicts:

- `PASS`
- `HALLUCINATION`
- `MISSED_CONFLICT`
- `UNNECESSARY_ABSTENTION`
- `OTHER_FAILURE`

## Actual Outputs

### Supported — Baseline

```text
{
  "timestamp": "2026-08-21T08:48:34.864Z",
  "caseId": "supported",
  "mode": "baseline",
  "expectedBehavior": "ANSWER_FROM_EVIDENCE",
  "latencyMs": 64664.443699999996,
  "outputText": "Based on Policy A, at least **24 hours' notice** before the scheduled time is required to cancel an appointment."
}
```

### Supported — Evidence-bounded

```text
{
  "timestamp": "2026-08-21T08:49:33.145Z",
  "caseId": "supported",
  "mode": "evidence-bounded",
  "expectedBehavior": "ANSWER_FROM_EVIDENCE",
  "latencyMs": 44703.19990000001,
  "outputText": "At least 24 hours before the scheduled time."
}
```

### Missing — Baseline

```text
{
  "timestamp": "2026-08-21T08:48:42.842Z",
  "caseId": "missing",
  "mode": "baseline",
  "expectedBehavior": "INSUFFICIENT_EVIDENCE",
  "latencyMs": 7976.312999999995,
  "outputText": "Based on the provided policy, there is no information regarding the clinic's parking fee."
}
```

### Missing — Evidence-bounded

```text
{
  "timestamp": "2026-08-21T08:50:10.347Z",
  "caseId": "missing",
  "mode": "evidence-bounded",
  "expectedBehavior": "INSUFFICIENT_EVIDENCE",
  "latencyMs": 37201.515,
  "outputText": "INSUFFICIENT_EVIDENCE"
}
```

### Conflicting — Baseline

```text
{
  "timestamp": "2026-08-21T08:48:48.441Z",
  "caseId": "conflicting",
  "mode": "baseline",
  "expectedBehavior": "CONFLICTING_EVIDENCE",
  "latencyMs": 5598.641700000007,
  "outputText": "Based on the provided policies, the required notice depends on which policy applies:\n\n* **Policy A:** At least **24 hours** before the scheduled time.\n* **Policy B:** At least **48 hours** before the scheduled time."
}
```

### Conflicting — Evidence-bounded

```text
{
  "timestamp": "2026-08-21T08:50:19.708Z",
  "caseId": "conflicting",
  "mode": "evidence-bounded",
  "expectedBehavior": "CONFLICTING_EVIDENCE",
  "latencyMs": 9360.054999999993,
  "outputText": "CONFLICTING_EVIDENCE"
}
```

## Observations

### Did the baseline prompt answer a question that lacked evidence?

My answer: No. The baseline response correctly stated that the supplied policy did not contain parking-fee information. Therefore, it abstained instead of inventing an answer.

### Did either prompt detect the conflicting policies?

My answer: Both prompts detected the incompatible information. The baseline explained both the 24-hour and 48-hour policies, while the evidence-bounded prompt returned the required CONFLICTING_EVIDENCE sentinel.

### How did the evidence-bounded instructions change behavior?

My answer: The bounded prompt introduced explicit, machine-detectable fallback responses. It returned INSUFFICIENT_EVIDENCE when information was missing and CONFLICTING_EVIDENCE when records disagreed, instead of generating a conversational explanation.

### Can this experiment prove that the bounded prompt will never hallucinate?

My answer: No. The experiment tested only three cases once each. LLM output is probabilistic, and different or adversarial inputs may produce failures. The prompt reduces risk but does not guarantee correctness.

## Knowledge Check

### 1. What makes a generated statement a hallucination in this application?

My answer: A generated factual claim is a hallucination when it is not supported by the evidence available to the application.

### 2. Why is a confident and plausible answer not sufficient evidence of correctness?

My answer: Because AI may halucinate and end up providing inaccurate answer despite sounding confident.

### 3. What is the difference between insufficient evidence and conflicting evidence?

My answer: Insufficient evidence means that there is no evidence as reference to be used, while conflicting evidence have multiple evidence that answers the same question, but the information from the evidences are different.

### 4. Why should an application distinguish abstention from request failure?

My answer: Abstention means the request succeeded, but the application lacked sufficient or consistent evidence to answer safely. Request failure means a technical problem prevented completion, such as a timeout, network error, rate limit, or invalid API response.

### 5. Why can prompt instructions reduce hallucinations without eliminating them?

My answer: Prompt instructions influence model behavior but do not enforce it deterministically. The model can misunderstand, overlook, or fail to follow instructions, especially with ambiguous, unfamiliar, or adversarial input.
