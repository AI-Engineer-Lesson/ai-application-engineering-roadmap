# Lesson 1 Results

## Test Results

Command:

```bash
pytest
```

Output:

```text
============================================================================================ test session starts =============================================================================================
platform win32 -- Python 3.12.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\arlud\Documents\Practice Projects\ai-application-engineering-roadmap
plugins: anyio-4.14.2
collected 2 items

tests\test_ai_consumer.py .                                                                                                                                                                             [ 50%]
tests\test_pricing.py .                                                                                                                                                                                 [100%]

============================================================================================= 2 passed in 1.73s ==============================================================================================
```

---

## Request Configuration

- **Provider:** Gemini
- **Model:** gemini-3.6-flash
- **Temperature:** `0.0`
- **Maximum output tokens:** `200`

### Prompt

```text
A patient says: "I want an appointment sometime next week." In two short sentences, explain what information is still needed before an appointment can be requested.
```

---

## Experiment Results

| Run | Latency (ms) | Input tokens | Output tokens | Thought tokens | Total observed tokens | Estimated cost |
| --: | -----------: | -----------: | ------------: | -------------: | --------------------: | -------------: |
|   1 |      2823.83 |           50 |            18 |            490 |                   558 |    $0.00194250 |
|   2 |      3382.05 |           50 |            22 |            486 |                   558 |    $0.00018450 |
|   3 |      4614.33 |           50 |            20 |            488 |                   558 |    $0.00018450 |

### Run 1 Response

```text
Provider: gemini
Model: gemini-3.6-flash
Latency: 4642.93 ms
Input tokens: 50
Output tokens: 18
Thought tokens: 490
Total observed tokens: 558

Response:
To schedule your visit, we still need your preferred specific date, time, and the reason
Estimated cost: $0.00194250
```

### Run 2 Response

```text
Provider: gemini
Model: gemini-3.6-flash
Latency: 4564.13 ms
Input tokens: 50
Output tokens: 22
Thought tokens: 486
Total observed tokens: 558

Response:
To process your request, we still need your full name, contact information, and your preferred dates and times.
Estimated cost: $0.00194250
```

### Run 3 Response

```text
Provider: gemini
Model: gemini-3.6-flash
Latency: 9124.53 ms
Input tokens: 50
Output tokens: 20
Thought tokens: 488
Total observed tokens: 558

Response:
To process the request, we still need the patient's full name, contact details, and the
Estimated cost: $0.00194250
```

---

## Cost Estimate

- **Pricing checked on:** 29/08/2026
- **Official pricing source:** https://ai.google.dev/gemini-api/docs/pricing#standard_1
- **Input price per 1 million tokens:** $0.75
- **Output price per 1 million tokens:** $3.75
- **Thought tokens billed as:** per 1M tokens in USD

| Run | Estimated cost |
| --: | -------------: |
|   1 |    $0.00194250 |
|   2 |    $0.00018450 |
|   3 |    $0.00018450 |

---

## Analysis

### Were the responses textually identical?

No

### Were they semantically equivalent?

Not Sure

### What varied between the runs?

Consider response wording, latency, and token usage.

- The output wording were different, some were still cut out due to the set limit. Latency also differ from each run.

---

## Issues Encountered

Record errors, SDK differences, or implementation problems encountered during the lesson.

- Output Truncation

---

## Key Takeaway

What is the most useful thing you learned from this implementation and experiment?

- Creating Adapter specifically for each Provider helps a lot to make the system run without having to modify a good chunk of the code. setting token usage is also a very helpful learning.
