# Fast-Track Session 1 — Results

## Test Evidence

```text
Paste the final pytest summary here.
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

   **Answer:** Not sure

2. Did any rejected input allow slot lookup or perform a booking?

   **Answer:** No

3. What is the key distinction between model extraction and application decisions?

   **Answer:** Not Sure

## Issues or Deviations

I'd like to be helped to understand on what's going on here
