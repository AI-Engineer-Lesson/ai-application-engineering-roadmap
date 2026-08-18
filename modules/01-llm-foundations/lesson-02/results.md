# Lesson 2 Results

## AI Requirement

- **Provider:** Google Gemini API
- **Tier:** Free
- **Model:** `gemini-3.7-flash`
- **OpenAI required:** No
- **Data restriction:** Synthetic data only

## Experiment

| Case     | Schema valid? | Business valid? | Inquiry status               | Important observation                                                                                                                         |
| -------- | ------------- | --------------- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Vague    | True          | True           | incomplete                   | Majority of the business information required are missing                                                                                     |
| Complete | True          | True            | ready_for_availability_check | Information were extracted from the statement completely.                                                                                     |
| Partial  | True          | True           | incomplete                   | Business information was only partially complete. while the patient's information was complete. it is imposible to extract preferred schedule |

## Actual Outputs

### Vague Inquiry

```json
{
  "timestamp": "2026-08-18T06:19:10.540Z",
  "caseId": "vague",
  "responseId": "v1_ChZXX21EYXM5UV83SFY3d19UMmV6b0NnEhZXX21EYXM5UV83SFY3d19UMmV6b0Nn",
  "model": "gemini-3.7-flash",
  "latencyMs": 13672.9017,
  "usage": {
    "total_tokens": 592,
    "total_input_tokens": 171,
    "input_tokens_by_modality": [
      {
        "modality": "text",
        "tokens": 171
      }
    ],
    "total_cached_tokens": 0,
    "total_output_tokens": 109,
    "total_tool_use_tokens": 0,
    "total_thought_tokens": 312,
    "raw_prompt_token": 618
  },
  "status": "validation_success",
  "inquiryStatus": "incomplete",
  "businessErrors": [],
  "output": {
    "summary": "Patient is requesting a checkup appointment next week, preferably after work hours.",
    "patientName": null,
    "contactInfo": null,
    "appointmentType": "checkup",
    "preferredDate": null,
    "preferredTime": null,
    "missingInformation": [
      "patient name",
      "contact information",
      "exact date",
      "exact time"
    ],
    "readyForAvailabilityCheck": false
  }
}
```

### Complete Inquiry

```json
{
  "timestamp": "2026-08-18T06:29:56.340Z",
  "caseId": "complete",
  "responseId": "v1_Chc0UHVEYXFic0QtS0QwLWtQbmNiZW9RSRIXNFB1RGFxYnNELUtEMC1rUG5jYmVvUUk",
  "model": "gemini-3.6-flash",
  "latencyMs": 7879.3042000000005,
  "usage": {
    "total_tokens": 788,
    "total_input_tokens": 225,
    "input_tokens_by_modality": [
      {
        "modality": "text",
        "tokens": 225
      }
    ],
    "total_cached_tokens": 0,
    "total_output_tokens": 125,
    "total_tool_use_tokens": 0,
    "total_thought_tokens": 438,
    "raw_prompt_token": 672
  },
  "status": "validation_success",
  "inquiryStatus": "ready_for_availability_check",
  "businessErrors": [],
  "output": {
    "summary": "Maria Santos requested a routine dental checkup on August 24, 2026, at 5:30 PM.",
    "patientName": "Maria Santos",
    "contactInfo": "0917-000-0000",
    "appointmentType": "checkup",
    "preferredDate": "2026-08-24",
    "preferredTime": "17:30",
    "missingInformation": [],
    "readyForAvailabilityCheck": true
  }
}
```

### Partial Inquiry

```json
{
  "timestamp": "2026-08-18T06:31:14.941Z",
  "caseId": "partial",
  "responseId": "v1_ChdMX3lEYXU3WkVJbnMycm9QNFpyYmlRURIXTF95RGF1N1pFSW5zMnJvUDRacmJpUVE",
  "model": "gemini-3.6-flash",
  "latencyMs": 26285.488699999998,
  "usage": {
    "total_tokens": 683,
    "total_input_tokens": 198,
    "input_tokens_by_modality": [
      {
        "modality": "text",
        "tokens": 198
      }
    ],
    "total_cached_tokens": 0,
    "total_output_tokens": 107,
    "total_tool_use_tokens": 0,
    "total_thought_tokens": 378,
    "raw_prompt_token": 645
  },
  "status": "validation_success",
  "inquiryStatus": "incomplete",
  "businessErrors": [],
  "output": {
    "summary": "Carlo Reyes requested an urgent appointment for a painful tooth as soon as possible.",
    "patientName": "Carlo Reyes",
    "contactInfo": "carlo.example@example.com",
    "appointmentType": "urgent_concern",
    "preferredDate": null,
    "preferredTime": null,
    "missingInformation": [
      "preferred date",
      "preferred time"
    ],
    "readyForAvailabilityCheck": false
  }
}
```

## Status Definitions

- **Schema valid:** The output contains the required fields with the expected data types.
- **Business valid:** The field values are consistent with the application’s business rules.
- **Incomplete:** More patient or scheduling information must be collected.
- **Ready for availability check:** Enough information exists to check the clinic’s actual schedule.
- **Validation failure:** The generated output violates the schema or business rules.

## Knowledge Check

### 1. What is the difference between valid JSON, schema-valid data, and business-valid data?

My answer: Valid JSON means the output follows JSON syntax and can be parsed. Schema-valid data has the required fields and expected data types. Business-valid data means the values are logically consistent with the application’s rules.

### 2. Why should missing information be represented by `null` instead of an invented or guessed value?

My answer: Missing information should be represented by `null` instead of guessing to avoid unexpected or inaccurate response.

### 3. Why is an incomplete patient inquiry not necessarily a validation failure?

My answer: An incomplete inquiry is not necessarily a validation failure because the AI can correctly represent missing information using null, list the missing fields, and set readiness to false. The output remains valid even though more information must be collected from the patient.

### 4. Why can the AI declare an inquiry ready for an availability check but not confirm the actual appointment?

My answer: The AI can determine whether the required information was provided, but it cannot confirm the appointment because it does not have access to the clinic’s current schedules or booking database.
