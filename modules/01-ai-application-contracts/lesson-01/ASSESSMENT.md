# Lesson 1 Assessment

## Completion Check

- [ ] Provider-neutral AI contracts implemented
- [ ] Gemini adapter implemented
- [ ] Unit tests passing without a real API call
- [ ] Three real requests recorded in `RESULTS.md`
- [ ] Token usage, latency, and cost analyzed
- [ ] No secrets committed

---

## Practical Questions

Answer concisely in your own words.

### 1. Provider Boundary

Why should application code depend on `AIProvider` instead of directly depending on `GeminiProvider` or Gemini SDK objects?

**Answer:** This is so that when we happen to use different provider, we don't have to make huge changes with the code.

---

### 2. Provider Replacement

If you replaced Gemini with OpenAI, which parts of the current implementation should change, and which parts should remain unchanged?

**Answer:** Add an OpenAIProvider, use it on the main(), don't change everything else.

Write your answer here.

---

### 3. Deterministic vs. Probabilistic

From this lesson, give:

- Two examples of deterministic application behavior
- Two examples of probabilistic or provider-controlled behavior

**Answer:**

Deterministic:

1. Business Rules
2. AI model used

Probabilistic or provider-controlled:

1. Total Token
2. Model Response content

---

### 4. Testing

Why does the unit test use `FakeProvider` instead of making a real Gemini request?

When would a real API test still be useful?

**Answer:** To avoid unecessary API usage.

---

### 5. Untrusted Output

Suppose the model returns:

```text
The patient has been booked for Tuesday at 10:00 AM.
```

Why must the application not assume that the appointment was actually booked?

What deterministic checks or actions are still required?

**Answer:** check in the Database

---

### 6. Failure Handling

If the provider times out or returns an empty response, what should the application do?

**Answer:** Not sure

---

## Self-Check

### What part of the lesson do you understand well?

I'm still getting the hang of it.

### What part still needs clarification?

I'm still getting the hang of it.

---

## Reviewer Decision

To be completed during review.

- [ ] Passed
- [ ] Minor corrections required
- [ ] Revisions required

### Feedback

Reviewer feedback goes here.
