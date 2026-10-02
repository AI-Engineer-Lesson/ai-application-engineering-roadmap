# Fast-Track Session 1 — Results

## Test Evidence

```text
tests\test_ai_consumer.py .                                                                                           [  4%]
tests\test_context.py ....                                                                                            [ 23%]
tests\test_decisions.py ........                                                                                      [ 61%]
tests\test_pricing.py .                                                                                               [ 66%]
tests\test_scheduling.py .......                                                                                      [100%]

==================================================== 21 passed in 0.98s ====================================================
```

## Decision Matrix

| Case            | Actual category            | Slot lookup allowed? | Passed? |
| --------------- | -------------------------- | :------------------: | :-----: |
| Valid request   | none                       |         True         |   [x]   |
| Missing contact | insufficient_information   |        False         |   [x]   |
| Blank name      | semantic_validation_failed |        False         |   [x]   |
| Sunday request  | business_rule_rejected     |        False         |   [x]   |
| Out of scope    | out_of_scope               |        False         |   [x]   |
| Malformed JSON  | structured_output_invalid  |        False         |   [x]   |

## Key Findings

1. Which inputs passed schema validation but were stopped later?

   **Answer:** The blank patient name passed schema validation but failed semantic validation. The Sunday request contained valid values but was rejected by the clinic's business rules.

2. Did any rejected input allow slot lookup or perform a booking?

   **Answer:** No. Every rejected input returned `may_lookup_slots = False`, and no booking operation was performed.

3. What is the key distinction between model extraction and application decisions?

   **Answer:** The model extracts structured information from the request. Deterministic application code decides whether that information is valid and whether the request may proceed.

## Issues or Deviations

- None
