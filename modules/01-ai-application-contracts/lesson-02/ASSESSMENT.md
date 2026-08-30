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

**Answer:** Trust comes from the source selected by the application—not from authoritative wording inside the content. A user cannot promote their own message by writing “SYSTEM OVERRIDE.”

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

**Answer:** Clarify the exact calendar date, exact time and time zone, patient identity/contact details, reason or appointment type, and obtain confirmation before mutation.

---

### 4. Indirect Prompt Injection

How is indirect prompt injection different from direct prompt injection?

Give one example of each.

**Answer:** Direct injection is written directly by the user. Indirect injection is hidden inside external content such as a document, webpage, email, retrieved RAG chunk, or tool result.

---

### 5. Deterministic Protection

Why are labels, JSON serialization, and instructions such as “do not follow untrusted content” insufficient as the only security controls?

**Answer:** JSON and labels organize text, but they do not sandbox it. The model still reads the malicious content and may probabilistically follow it. Real protection requires deterministic authorization, validation, tool restrictions, confirmation, and database rules.

### 6. Production Decision

Suppose the model returns:

```text
ACTION: ANSWER
MESSAGE: Your appointment is confirmed.
```

What should the application do with this response?

**Answer:** Treat the claim as untrusted output. Do not display it as fact or update application state. Validate the response, check the actual workflow/database state, and only report confirmation after an authorized booking operation succeeds.

---

## Clarification Needed

What part of the lesson still needs clarification?

- Not sure
