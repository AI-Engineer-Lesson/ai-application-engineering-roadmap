# Lesson 3 — Tokens, Context Windows, Latency, and Cost

This lesson explores how prompt size affects token usage, context-window utilization, latency, and estimated API cost in an AI application.

The experiment sends the same administrative summarization task with small, medium, and large synthetic contexts using Google Gemini.

## Learning Objectives

- Count input tokens before generation
- Record actual token usage after generation
- Measure request latency
- Calculate context-window utilization
- Estimate paid-equivalent input and output costs
- Include thinking tokens in output-cost estimates
- Compare results across different prompt sizes

## AI Requirement

- **Provider:** Google Gemini API
- **Model:** `gemini-3.7-flash`
- **Tier:** Free
- **Actual cost:** $0 within free-tier limits
- **Data:** Synthetic only

Do not use real patient information, private business records, credentials, or other sensitive data.

## Prerequisites

- Node.js installed
- npm installed
- A Gemini API key
- TypeScript familiarity

## Installation

From the `lesson-03` directory, install the dependencies:

```powershell
npm install
```

## API-Key Setup

Set your Gemini API key for the current PowerShell session:

```powershell
$env:GEMINI_API_KEY="your-api-key"
```

Do not commit your API key or place it directly in the source code.

## Run the Experiment

```powershell
npm run lesson
```

The program runs three experiments:

| Case   | Number of policies |
| ------ | -----------------: |
| Small  |                  1 |
| Medium |                 25 |
| Large  |                100 |

Each experiment records:

- Prompt character count
- Preflight input-token count
- Actual input tokens
- Visible output tokens
- Thinking tokens
- Total tokens
- Request latency
- Input-context utilization
- Paid-equivalent cost
- Generated output

## Cost Calculation

Input cost is calculated using:

```text
input tokens ÷ 1,000,000 × input rate
```

Output cost includes both visible output and thinking tokens:

```text
(visible output tokens + thinking tokens)
÷ 1,000,000
× output rate
```

The paid-equivalent cost is tracked for production planning even though the experiment runs within Gemini’s free tier.

## Project Structure

```text
lesson-03/
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

- Model limits
- Experiment measurements
- Generated outputs
- Observations
- Knowledge-check answers

## Important Takeaway

A model’s context window represents its maximum capacity, not a target prompt size. Production applications should provide the smallest context that is sufficient for the task while monitoring quality, latency, token usage, and cost.
