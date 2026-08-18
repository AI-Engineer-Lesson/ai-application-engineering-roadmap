import { GoogleGenAI } from "@google/genai";
import { performance } from "node:perf_hooks";
import * as z from "zod";

const ai = new GoogleGenAI({});
const model = "gemini-3.7-flash";

const datePattern = /^\d{4}-\d{2}-\d{2}$/;
const timePattern = /^([01]\d|2[0-3]):[0-5]\d$/;

const bookingInquiryJsonSchema = {
  type: "object",
  properties: {
    summary: {
      type: "string",
      description: "A concise summary of the appointment inquiry.",
    },
    patientName: {
      type: ["string", "null"],
      description: "The patient's full name, or null when it was not provided.",
    },
    contactInfo: {
      type: ["string", "null"],
      description: "The provided phone number or email, or null when absent.",
    },
    appointmentType: {
      type: "string",
      enum: ["checkup", "cleaning", "urgent_concern", "other", "unknown"],
      description: "The requested appointment category.",
    },
    preferredDate: {
      type: ["string", "null"],
      description:
        "The exact requested date in YYYY-MM-DD format, or null when absent.",
    },
    preferredTime: {
      type: ["string", "null"],
      description:
        "The exact requested time in 24-hour HH:MM format, or null when absent.",
    },
    missingInformation: {
      type: "array",
      items: {
        type: "string",
      },
      description:
        "Information still needed before clinic availability can be checked.",
    },
    readyForAvailabilityCheck: {
      type: "boolean",
      description:
        "True only when the required patient and scheduling details are present.",
    },
  },
  required: [
    "summary",
    "patientName",
    "contactInfo",
    "appointmentType",
    "preferredDate",
    "preferredTime",
    "missingInformation",
    "readyForAvailabilityCheck",
  ],
  additionalProperties: false,
};

const bookingInquirySchema = z.fromJSONSchema(bookingInquiryJsonSchema as any);

type BookingInquiry = {
  summary: string;
  patientName: string | null;
  contactInfo: string | null;
  appointmentType:
    | "checkup"
    | "cleaning"
    | "urgent_concern"
    | "other"
    | "unknown";
  preferredDate: string | null;
  preferredTime: string | null;
  missingInformation: string[];
  readyForAvailabilityCheck: boolean;
};

const inquiries = [
  {
    caseId: "vague",
    text: "I need a checkup sometime next week, preferably after work.",
  },
  {
    caseId: "complete",
    text: `
        My name is Maria Santos. I am an existing patient.
        I would like a routine dental checkup on August 24, 2026,
        at 5:30 PM. You can contact me at 0917-000-0000.
      `,
  },
  {
    caseId: "partial",
    text: `
        My name is Carlo Reyes. I have a painful tooth and would
        like to visit as soon as possible. Please contact me at
        carlo.example@example.com.
      `,
  },
];

function validateBusinessRules(inquiry: BookingInquiry): string[] {
  const errors: string[] = [];


  if (inquiry.preferredDate !== null) {
    if (!datePattern.test(inquiry.preferredDate)) {
      errors.push("Invalid preferred date format. Please use YYYY-MM-DD.");
    }
  }


  if (inquiry.preferredTime !== null) {
    if (!timePattern.test(inquiry.preferredTime)) {
      errors.push("Invalid preferred time format. Please use 24-hour HH:MM.");
    }
  }

  const calculatedReadiness =
    inquiry.patientName !== null &&
    inquiry.contactInfo !== null &&
    inquiry.appointmentType !== "unknown" &&
    inquiry.preferredDate !== null &&
    inquiry.preferredTime !== null &&
    inquiry.missingInformation.length === 0;

  if (calculatedReadiness !== inquiry.readyForAvailabilityCheck) {
    errors.push("Inconsistent readiness status.");
  }

  return errors;
}

async function analyzeInquiry(
  caseId: string,
  inquiryText: string,
): Promise<void> {
  const startTime = performance.now();

  const prompt = `
You analyze non-clinical dental appointment inquiries.

Rules:

- Extract only information explicitly provided by the patient.
- Never invent a name, contact detail, date, or time.
- Use null when information was not provided.
- Normalize an explicitly provided date to YYYY-MM-DD.
- Normalize an explicitly provided time to 24-hour HH:MM.
- List all information still required in missingInformation.
- Set readyForAvailabilityCheck to true only when the patient's
  name, contact information, appointment type, exact date, and
  exact time are present.
- Do not claim that an appointment is booked.
- Do not claim that a schedule is available.

Patient inquiry:

${inquiryText}
`;

  try {
    const response = await ai.interactions.create({
      model,
      input: prompt,
      response_format: {
        type: "text",
        mime_type: "application/json",
        schema: bookingInquiryJsonSchema,
      },
    });

    if (typeof response.output_text !== "string") {
      throw new Error("Missing or invalid response.output_text");
    }

    const parsedJson: unknown = JSON.parse(response.output_text);
    const validatedInquiry = bookingInquirySchema.parse(
      parsedJson,
    ) as BookingInquiry;

    const businessErrors = validateBusinessRules(validatedInquiry);

    console.log(
      JSON.stringify(
        {
          timestamp: new Date().toISOString(),
          caseId,
          responseId: response.id,
          model,
          latencyMs: performance.now() - startTime,
          usage: response.usage,
          status:
            businessErrors.length === 0
              ? "validation_success"
              : "validation_failure",
          inquiryStatus: validatedInquiry.readyForAvailabilityCheck
            ? "ready_for_availability_check"
            : "incomplete",
          businessErrors,
          output: validatedInquiry,
        },
        null,
        2,
      ),
    );
  } catch (error: unknown) {
    const isValidationError =
      error instanceof z.ZodError || error instanceof SyntaxError;

    console.error(
      JSON.stringify(
        {
          timestamp: new Date().toISOString(),
          caseId,
          model,
          latencyMs: performance.now() - startTime,
          status: isValidationError ? "validation_failure" : "api_error",
          error: {
            type: error instanceof Error ? error.name : "UnknownError",
            message:
              error instanceof Error
                ? error.message
                : "An unknown error occurred.",
          },
        },
        null,
        2,
      ),
    );

    process.exitCode = 1;
  }
}

async function main(): Promise<void> {
  for (const inquiry of inquiries) {
    await analyzeInquiry(inquiry.caseId, inquiry.text);
  }
}

void main();
