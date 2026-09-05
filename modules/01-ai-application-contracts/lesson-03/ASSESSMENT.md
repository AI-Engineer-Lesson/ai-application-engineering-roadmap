# Lesson 3 Assessment

## Completion Check

- [x] Application-owned response schema implemented
- [x] Gemini adapter supports structured output
- [x] Pydantic runtime validation implemented
- [x] Tests pass without network access
- [x] Malformed JSON is rejected
- [x] Invalid field values are rejected
- [x] Inconsistent status and fields are rejected
- [x] Four live experiments completed
- [x] No booking action is performed

## Practical Questions

### 1. Structured Output

What does Gemini structured output guarantee, and what does it not guarantee?

**Answer:** It guarantees that the output is of the desired format. It does not guarantee that the data values are valid.

### 2. Runtime Validation

Why must the application validate the JSON even when Gemini generated it using a schema?

**Answer:** The response may be of a vald JSON format, and it could also be of the correct format that is accepted by the application. However, the data still needs to pass application validation layer that checks whether each field are of valid values.

### 3. Semantic Consistency

Why should this response be rejected?

```json
{
  "status": "ready_for_validation",
  "contact_number": null,
  "missing_fields": ["contact_number"]
}
```

**Answer:** the status contradicts with the missing fields. In this case, contact number is a required field. while the model may have returned it as ready_for_validation, the application should still reject it.
