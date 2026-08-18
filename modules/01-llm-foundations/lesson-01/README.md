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