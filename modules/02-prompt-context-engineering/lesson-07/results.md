# Lesson 7 Results

## AI Requirement

- **Provider:** Google Gemini API
- **Tier:** Free
- **Model:** `gemini-3.7-flash`
- **Actual cost:** $0
- **Data:** Synthetic only
- **Language:** Python
- **SDK:** `google-genai`

## Experiment Results

| Case          | Expected handling   | Actual status       | Invented critical information? | Questions relevant? | Latency (ms) |
| ------------- | ------------------- | ------------------- | ------------------------------ | ------------------- | -----------: |
| Complete      | Ready               | READY               | No                             | N/A                 |    156059.44 |
| Missing date  | Needs clarification | NEEDS_CLARIFICATION | No                             | Yes                 |     51118.75 |
| Vague         | Needs clarification | NEEDS_CLARIFICATION | No                             | Yes                 |    175071.81 |
| Contradictory | Conflict            | CONFLICT            | No                             | Yes                 |    137461.65 |

Use `Yes`, `No`, or `Partial` for the evaluation columns where appropriate.

## Actual Outputs

### Complete

```json
{
  "case_id": "complete",
  "model": "gemini-3.7-flash",
  "latency_ms": 156059.44,
  "output_text": "SUMMARY: Returning patient requesting an appointment for a cleaning on August 28 at 2:00 PM.\nSTATUS: READY\nSERVICE: cleaning\nDATE: August 28\nTIME: 2:00 PM\nPATIENT_TYPE: returning\nMISSING: None\nCONFLICTS: None\nQUESTIONS: None"
}
```

### Missing Date

```json
{
  "case_id": "missing_date",
  "model": "gemini-3.7-flash",
  "latency_ms": 51118.75,
  "output_text": "SUMMARY: The user is a new patient requesting an administrative consultation in the afternoon, but has not provided a preferred date or a specific appointment time.\nSTATUS: NEEDS_CLARIFICATION\nSERVICE: administrative consultation\nDATE: UNKNOWN\nTIME: afternoon\nPATIENT_TYPE: new\nMISSING: Preferred date, specific preferred time\nCONFLICTS: None\nQUESTIONS:\n1. What date would you prefer for your appointment?\n2. Do you have a specific time in the afternoon that works best for you?"
}
```

### Vague

```json
{
  "case_id": "vague",
  "model": "gemini-3.7-flash",
  "latency_ms": 175071.81,
  "output_text": "SUMMARY: The user requested an unspecified \"usual\" appointment \"sometime soon\" without providing specific service details, dates, times, or explicit patient status.\nSTATUS: NEEDS_CLARIFICATION\nSERVICE: UNKNOWN\nDATE: UNKNOWN\nTIME: UNKNOWN\nPATIENT_TYPE: UNKNOWN\nMISSING: Patient type (new or returning), requested service, preferred date, preferred time\nCONFLICTS: None\nQUESTIONS:\n1. Are you a new or returning patient, and which allowed service would you like to schedule (cleaning, administrative consultation, or follow-up visit)?\n2. What specific date would you prefer for your appointment?\n3. What specific time or time of day works best for you?"
}
```

### Contradictory

```json
{
  "case_id": "contradictory",
  "model": "gemini-3.7-flash",
  "latency_ms": 137461.65,
  "output_text": "SUMMARY: A returning patient is requesting a cleaning on August 29, but provided contradictory time preferences by stating they are only available in the morning while requesting a 3:00 PM appointment.\nSTATUS: CONFLICT\nSERVICE: cleaning\nDATE: August 29\nTIME: 3:00 PM (conflicts with morning-only availability)\nPATIENT_TYPE: returning\nMISSING: None\nCONFLICTS: You stated that you are available only in the morning, but also requested an appointment at 3:00 PM (afternoon).\nQUESTIONS:\n1. Would you prefer to schedule a morning time on August 29, or would you like to keep the 3:00 PM appointment?"
}
```

## Observations

### 1. Complete Request

The complete case supplies the patient type, service, date, and time.

**Question:** Did the model recognize that enough information was available without asking unnecessary questions? Explain any unnecessary question it asked.

My answer: Yes. No unnecessary questions asked by the model.

### 2. Missing Date

This request supplies the patient type, service, and general time of day but does not provide a calendar date.

**Question:** Did the model leave the date unknown and request it, or did it invent a date? Why would inventing a date be dangerous?

My answer: The model did not invent a date. Inventing a date would be dangerous because it could be a date that the patient cannot accomodate, or conflicting with the clinic schedules.

### 3. Vague Request

The phrases “usual appointment” and “soon” depend on information unavailable in the request.

**Question:** Which fields were ambiguous, and what information did the model request to resolve them?

My answer: The ambiguous or missing fields were the patient type, requested service, preferred date, and preferred time. “Usual appointment” does not identify a service, while “soon” does not identify a date. The model asked whether the patient was new or returning, which service they wanted, and their preferred date and time.

### 4. Contradictory Request

The user says they are available only in the morning but requests 3:00 PM.

**Question:** Did the model recognize the contradiction? What must happen before the application prepares a booking operation?

My answer: The application must wait for the patient to resolve the conflicting time information. After receiving one consistent time, application code must validate the required fields and check actual clinic availability before preparing a booking operation.

## Python Reflection

### 1. Function Type Hints

Consider:

```python
def build_user_input(request_text: str) -> str:
```

**Question:** What do the two `str` type hints communicate? Are they automatically enforced at runtime by standard Python?

My answer: the two `str` type hints indicate that both input and output will be of string type. I don't think they are enforced at runtime, they are merly there to help the developers understand the code input and output, and so to help easily identify type mismatch at a code level.

### 2. F-Strings

Consider:

```python
message = f"Clinic: {clinic_name}"
```

**Question:** What does the `f` before the string allow Python to do?

My answer: I think it allows to accept variables inside the string

### 3. Main Guard

Consider:

```python
if __name__ == "__main__":
    main()
```

**Question:** Why is this preferable to calling `main()` unconditionally at the bottom of a reusable Python file?

My answer: The condition prevents `main()` from running automatically if the file is imported by another Python module later.

## Knowledge Check

### 1. Why Use a Prompt Template?

Imagine three API routes independently construct slightly different clinic prompts.

**Question:** What maintenance and reliability problems could arise compared with using one reusable template?

My answer: Independent prompts can gradually develop different rules, formats, and behavior. A bug fix or business-rule change would have to be applied separately to every route, making it easy to miss one. A reusable template keeps the rules consistent and allows one change to apply everywhere.

### 2. Which Details May Be Assumed?

A user writes:

> Please give me a short reply and book a cleaning soon.

“Short” concerns writing style, while “soon” affects the requested appointment date.

**Question:** Why might the model interpret “short” approximately but require clarification for “soon”?

My answer: the appointment schedule is a required parameter, and `soon` is provides an ambiguous information for it. Although the model might just respond with short messages to satisfy patient's request.

### 3. Why Is Prompt Validation Insufficient?

The template tells the model to output `READY` only when every required field is available.

**Question:** Why must application code still verify those fields before allowing a booking operation?

My answer: It's probably because there's a chance that AI will hallucinate. Aside from that, a code level verification would still be necessary to ensure all business requirements are fulfilled.

### 4. What Is a Contradiction?

A request says:

> Tuesday morning works, but schedule it Tuesday at 4:00 PM.

**Question:** Why should the model report a conflict instead of selecting one of the two times?

My answer: It's because the request contains two time schedules. It would be best to respond with a question asking for one specific schedule.

### 5. What Belongs in the Template?

Consider:

- Clinic role and behavioral rules
- Allowed service list
- Current user request
- Output contract
- Specific patient’s preferred date

**Question:** Which values are stable template instructions, configuration variables, and request-specific variables? Explain your grouping.

My answer: 
    Stable template instructions: clinic role, behavioral rules, output contract
    Configuration variable: allowed service list
    Request-specific variables: current user request and the patient’s preferred date
