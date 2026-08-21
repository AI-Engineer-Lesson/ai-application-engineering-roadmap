# Lesson 4 — Hallucinations, Evidence Boundaries, and Failure Modes

This lesson examines how an AI application should respond when supplied evidence is sufficient, missing, or contradictory.

It compares a normal baseline prompt with an evidence-bounded prompt using synthetic clinic policies and Google Gemini.

## Learning Objectives

- Define hallucination in terms of available evidence
- Distinguish sufficient, insufficient, and conflicting evidence
- Design explicit abstention and conflict responses
- Compare conversational answers with machine-detectable fallback values
- Understand why prompt instructions reduce but cannot eliminate hallucinations

## AI Requirement

- **Provider:** Google Gemini API
- **Model:** `gemini-3.7-flash`
- **Tier:** Free
- **Actual cost:** $0 within free-tier limits
- **Data:** Synthetic only
- **External grounding:** Disabled

Do not use real patient information, private clinic records, credentials, or other sensitive information.

## Evidence Conditions

The experiment evaluates three situations:

| Condition             | Description                                       | Expected behavior              |
| --------------------- | ------------------------------------------------- | ------------------------------ |
| Sufficient evidence   | The supplied policy directly answers the question | Answer from evidence           |
| Insufficient evidence | The required information is absent                | Return `INSUFFICIENT_EVIDENCE` |
| Conflicting evidence  | Supplied policies contain incompatible answers    | Return `CONFLICTING_EVIDENCE`  |

## Hallucination Definition

In this application, a hallucination is a generated factual claim that is not supported by the evidence available to the application.

An answer is not proven correct merely because it is:

- Fluent
- Confident
- Plausible
- Grammatically correct
- Potentially true outside the supplied context

Correctness must be evaluated against the evidence available for the request.

## Prompt Modes

### Baseline Prompt

The baseline prompt asks the model to answer using the supplied policies without defining exact fallback behavior.

### Evidence-Bounded Prompt

The bounded prompt requires the model to:

- Use only supplied evidence
- Avoid guessing or inventing policy details
- Return `INSUFFICIENT_EVIDENCE` when information is absent
- Return `CONFLICTING_EVIDENCE` when policies disagree

These sentinel values are easier for application code to detect than conversational explanations.

## Prerequisites

- Node.js
- npm
- A Gemini API key
- TypeScript familiarity

## Installation

From the `lesson-04` directory:

```powershell
npm install
```

## API-Key Setup

Set the Gemini API key for the current PowerShell session:

```powershell
$env:GEMINI_API_KEY="your-api-key"
```

Do not commit API keys or place them directly in source code.

## Run the Experiment

```powershell
npm run lesson
```

The program runs six requests:

```text
3 evidence conditions × 2 prompt modes = 6 requests
```

## Experiment Summary

| Case        | Baseline result                                        | Evidence-bounded result          |
| ----------- | ------------------------------------------------------ | -------------------------------- |
| Supported   | Answered from the 24-hour policy                       | Answered from the 24-hour policy |
| Missing     | Explained that parking-fee information was unavailable | Returned `INSUFFICIENT_EVIDENCE` |
| Conflicting | Presented both the 24-hour and 48-hour policies        | Returned `CONFLICTING_EVIDENCE`  |

All six outputs passed their expected behavior in this experiment.

The baseline prompt did not hallucinate during this run. This result does not prove that it will behave reliably for different inputs or repeated requests.

## Abstention Versus Request Failure

Abstention is a successful application outcome:

```text
Request completed
→ evidence was insufficient or conflicting
→ application declined to provide an unsupported answer
```

Request failure is a technical problem:

```text
Request attempted
→ timeout, rate limit, network error, or invalid response
→ application could not complete the operation
```

These cases require different handling:

- Abstention should display uncertainty or trigger human escalation.
- Technical failure may require logging, retrying, or graceful degradation.

## Project Structure

```text
lesson-04/
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

- All six generated outputs
- Expected and observed behavior
- Verdicts
- Experiment observations
- Knowledge-check answers

## Production Considerations

- Prompt instructions influence model behavior but do not enforce it deterministically.
- One successful request is not evidence of production reliability.
- Missing and conflicting evidence should remain separate application states.
- Abstention should not be reported as a technical error.
- Machine-detectable fallback values are safer than relying entirely on conversational wording.
- High-impact actions should not proceed using unsupported generated claims.
- Representative datasets and repeated evaluations are necessary before deployment.

## Important Takeaway

Evidence-bounded prompts make safe fallback behavior clearer and easier for application code to detect. They reduce hallucination risk, but reliable production systems still require validation, testing, monitoring, and appropriate human escalation.
