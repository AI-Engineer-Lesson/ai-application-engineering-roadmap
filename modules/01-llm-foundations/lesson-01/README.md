# Lesson 1 — Anatomy of a Production LLM Request

This lesson demonstrates how to call an LLM and observe the operational information needed for a production AI feature.

## AI Requirement

- Provider: Google Gemini API
- Tier: Free
- Model: `gemini-3.7-flash`
- Data restriction: Synthetic or non-sensitive data only

## What the Program Records

- Response ID
- Model name
- Request latency
- Token usage
- Generated output
- Structured API errors

## Setup

Install the dependencies:

```bash
npm install
```

Set the Gemini API key in PowerShell:

```powershell
$env:GEMINI_API_KEY="your-api-key"
```

Never commit the API key or place it directly in the source code.

## Run

```bash
npm run lesson
```

## Lesson Files

- `src/index.ts` — instrumented Gemini request
- `results.md` — three-run experiment and knowledge-check answers
- `package.json` — dependencies and lesson command

## Learning Objective

A technically successful API request does not guarantee a useful AI result. The application must separately observe and validate latency, usage, output quality, and errors.