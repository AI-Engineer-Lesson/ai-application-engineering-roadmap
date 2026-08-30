# Lesson 2 Assessment

## Completion Check

- [x] Context builder implemented
- [x] Trusted and untrusted data separated
- [x] Six automated tests passing
- [x] Four model experiments completed
- [x] Direct injection tested
- [x] Indirect injection tested
- [x] Results documented
- [x] No secrets or real patient data committed

---

## Practical Questions

Answer concisely in your own words.

### 1. Trust Hierarchy

Why should a user message saying “SYSTEM OVERRIDE” remain less trusted than clinic policy loaded by the application?

**Answer:** This is to avoid possible leaking of potentially sensitve data. This helps the system remain reliable for its capabilities, while remaining secure.

---

### 2. System-Instruction Boundary

Why must raw user input never be inserted into the system instruction?

**Answer:** This is to avoid the pre-determined system instructions from being overridden by user inputs.

---

### 3. Ambiguity

A user says:

```text
Book me next Friday afternoon.
```

What information should the system clarify before any booking action?

**Answer:** the model will look into the required fields such as patient name, date and time, etc. and ask the patient to provide these information.

---

### 4. Indirect Prompt Injection

How is indirect prompt injection different from direct prompt injection?

Give one example of each.

**Answer:** I'm not sure

---

### 5. Deterministic Protection

Why are labels, JSON serialization, and instructions such as “do not follow untrusted content” insufficient as the only security controls?

## **Answer:** Not sure

### 6. Production Decision

Suppose the model returns:

```text
ACTION: ANSWER
MESSAGE: Your appointment is confirmed.
```

What should the application do with this response?

**Answer:** Not sure

---

## Clarification Needed

What part of the lesson still needs clarification?

- Not sure
