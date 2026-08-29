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
- **Maximum output tokens:** `512`

### Prompt

```text
A patient says: "I want an appointment sometime next week." In two short sentences, explain what information is still needed before an appointment can be requested.
```

---

## Experiment Results

| Run | Latency (ms) | Input tokens | Output tokens | Thought tokens | Total observed tokens | Estimated cost |
| --: | -----------: | -----------: | ------------: | -------------: | --------------------: | -------------: |
|   1 |     13592.76 |           50 |            44 |            406 |                   500 |    $0.00172500 |
|   2 |      7872.87 |           50 |            40 |            368 |                   458 |    $0.00156750 |
|   3 |     17219.33 |           50 |            45 |            341 |                   436 |    $0.00148500 |

### Run 1 Response

```text
Provider: gemini
Model: gemini-3.6-flash
Latency: 13592.76 ms
Input tokens: 50
Output tokens: 44
Thought tokens: 406
Total observed tokens: 500

Response:
To process the request, we still need the patient's full name, date of birth, and preferred dates and times. Additionally, we need to know the reason for the visit so we can select the appropriate provider.
Estimated cost: $0.00172500
```

### Run 2 Response

```text
Provider: gemini
Model: gemini-3.6-flash
Latency: 7872.87 ms
Input tokens: 50
Output tokens: 40
Thought tokens: 368
Total observed tokens: 458

Response:
To schedule the appointment, we still need the patient's full contact details and the reason for their visit. We also require their preferred specific days, times, and any provider preferences for next week.
Estimated cost: $0.00156750
```

### Run 3 Response

```text
Provider: gemini
Model: gemini-3.6-flash
Latency: 17219.33 ms
Input tokens: 50
Output tokens: 45
Thought tokens: 341
Total observed tokens: 436

Response:
To schedule the appointment, we still need the patient's contact details and the general reason for their visit to select the appropriate provider. Additionally, we require their specific preferred dates and times during the week to check schedule availability.
Estimated cost: $0.00148500
```

---

## Cost Estimate

- **Pricing checked on:** 29/08/2026
- **Official pricing source:** https://ai.google.dev/gemini-api/docs/pricing#standard_1
- **Input price per 1 million tokens:** $0.75
- **Output price per 1 million tokens:** $3.75
- **Thought tokens billed as:** Output tokens at $3.75 per one million tokens

| Run | Estimated cost |
| --: | -------------: |
|   1 |    $0.00172500 |
|   2 |    $0.00156750 |
|   3 |    $0.00148500 |

---

## Analysis

### Were the responses textually identical?

- No

### Were they semantically equivalent?

- Yes. All three requested the same essential information: patient details, preferred dates and times, and the reason for the visit. Some runs added extra details such as date of birth or provider preference.

### What varied between the runs?

Consider response wording, latency, and token usage.

- The wording, additional requested details, latency, thought-token usage, output-token usage, and estimated cost varied.

---

## Issues Encountered

Record errors, SDK differences, or implementation problems encountered during the lesson.

- Initial responses were truncated because thinking consumed most of the 200-token limit. Increasing the limit to 512 and using low thinking effort produced complete responses.

---

## Key Takeaway

What is the most useful thing you learned from this implementation and experiment?

- Creating Adapter specifically for each Provider helps a lot to make the system run without having to modify a good chunk of the code. setting token usage is also a very helpful learning.
