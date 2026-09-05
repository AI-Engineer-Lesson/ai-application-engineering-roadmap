# Lesson 3 Results

## Test Results

```text
==================================================================== test session starts =====================================================================
platform win32 -- Python 3.12.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\arlud\Documents\Practice Projects\ai-application-engineering-roadmap
plugins: anyio-4.14.2
collected 13 items

tests\test_ai_consumer.py .                                                                                                                             [  7%]
tests\test_context.py ....                                                                                                                              [ 38%]
tests\test_pricing.py .                                                                                                                                 [ 46%]
tests\test_scheduling.py .......                                                                                                                        [100%]

===================================================================== 13 passed in 1.81s =====================================================================
```

## Configuration

- **Provider:** Gemini
- **Model:** gemini-3.6-flash
- **Structured-output validation:** Pydantic

## Experiment Results

| Case                   | Expected               | Actual                 | Validation |  Latency |
| ---------------------- | ---------------------- | ---------------------- | ---------- | -------: |
| Complete request       | `ready_for_validation` | `ready_for_validation` | REJECTED   | 23655.78 |
| Missing information    | `needs_clarification`  | `needs_clarification`  | ACCEPTED   | 30075.78 |
| Invalid contact number | Clarify or reject      | `ready_for_validation` | REJECTED   | 34555.07 |
| Out-of-scope request   | `out_of_scope`         | `out_of_scope`         | ACCEPTED   | 38826.06 |

## Important Observations

### Did every response contain syntactically valid JSON?

Yes

### Did every response pass application validation?

No. Both Complete request and invalid contact number failed the application validation layer.

### How was the invalid contact number handled?

The invalid contact number case passed in the AI model, but was rejected by the application validation layer. This indicated the importance of application validation layer when the AI model somehow misses some important requirements.

### Did any result claim that an appointment was booked?

No

## Issues Encountered

An issue with the gemini sdk which does not support response_format. I had help with codex on fixing it.

## Key Takeaway

What is the practical difference between structured generation and runtime validation?

Structured generation helps the model return JSON in the expected shape. Runtime validation checks whether the returned values and relationships satisfy the application's rules. Correctly structured JSON can still contain invalid or contradictory data.
