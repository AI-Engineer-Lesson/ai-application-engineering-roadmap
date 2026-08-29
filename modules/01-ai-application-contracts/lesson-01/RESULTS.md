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
|   1 |      2823.83 |           50 |             3 |            193 |                   246 |    $0.00018450 |
|   2 |      3382.05 |           50 |             5 |            191 |                   246 |    $0.00018450 |
|   3 |      4614.33 |           50 |             3 |            193 |                   246 |    $0.00018450 |

### Run 1 Response

```text
Provider: gemini
Model: gemini-3.6-flash
Latency: 2823.83 ms
Input tokens: 50
Output tokens: 3
Thought tokens: 193
Total observed tokens: 246

Response:
To finalize your
Estimated cost: $0.00018450
```

### Run 2 Response

```text
Provider: gemini
Model: gemini-3.6-flash
Latency: 3382.05 ms
Input tokens: 50
Output tokens: 5
Thought tokens: 191
Total observed tokens: 246

Response:
To process your request,
Estimated cost: $0.00018450
```

### Run 3 Response

```text
Provider: gemini
Model: gemini-3.6-flash
Latency: 4614.33 ms
Input tokens: 50
Output tokens: 3
Thought tokens: 193
Total observed tokens: 246

Response:
We need the
Estimated cost: $0.00018450
```

---

## Cost Estimate

- **Pricing checked on:**
- **Official pricing source:**
- **Input price per 1 million tokens:**
- **Output price per 1 million tokens:**
- **Thought tokens billed as:**

| Run | Estimated cost |
| --: | -------------: |
|   1 |                |
|   2 |                |
|   3 |                |

---

## Analysis

### Were the responses textually identical?

No

### Were they semantically equivalent?

Not Sure

### What varied between the runs?

Consider response wording, latency, and token usage.

The response were cut off due to the limit, so I can't say.

### Did setting the temperature to zero make the complete operation deterministic?

Not Sure

---

## Issues Encountered

Record errors, SDK differences, or implementation problems encountered during the lesson.

- None

---

## Key Takeaway

What is the most useful thing you learned from this implementation and experiment?

Creating Adapter specifically for each Provider helps a lot to make the system run without having to modify a good chunk of the code.
