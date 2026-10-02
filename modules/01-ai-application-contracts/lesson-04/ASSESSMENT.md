# Fast-Track Session 1 — Assessment

## Completion Check

- [ ] Decision contract implemented
- [ ] Semantic and business validation implemented
- [ ] Safe abstention implemented
- [ ] Malformed output classified safely
- [ ] All 21 tests pass
- [ ] Deterministic experiment completed
- [ ] No booking action performed
- [ ] No secrets or real patient data committed

## Short Review

Answer in one or two sentences each.

### 1. Validation ownership

Why must clinic hours and notice requirements be enforced by application code rather than the model prompt?

**Answer:** because clinic hours and noticerequirements are business rules and are deterministic values.

### 2. Failure layers

Classify each case as schema/runtime, semantic, or business-rule failure:

- Invalid date text
- Correctly formatted date in the past
- Valid future date when the clinic is closed

**Answer:**

- schema/runtime
- business-rule failure
- business-rul failure

### 3. Action boundary

What does `ready_for_slot_lookup` permit, and what does it still not permit?

**Answer:** it permits to proceed to lookup for available slot. It still doesn't permit the booking to proceed or be recorded.

## Clarification Needed

Write `None`, or name one specific concept that still needs explanation.
