import { GoogleGenAI } from "@google/genai";
import { performance } from "node:perf_hooks";

const ai = new GoogleGenAI({});
const model = "gemini-3.7-flash";

const input = `
You are assisting a dental clinic administrator.

Summarize this non-clinical inquiry and identify the information that
must be collected before an appointment can be booked:

"I need a checkup sometime next week, preferably after work."
`;

async function main(): Promise<void> {
  const startTime = performance.now();

  try {
    const response = await ai.interactions.create({ model, input });

    const endTime = performance.now();
    const latencyMs = endTime - startTime;

    console.log(
      JSON.stringify(
        {
          timestamp: new Date().toISOString(),
          responseId: response.id,
          model,
          latencyMs,
          usage: response.usage,
          outputText: response.output_text,
        },
        null,
        2,
      ),
    );
  } catch (error: unknown) {
    const latencyMs = performance.now() - startTime;

    const errorRecord = {
      timestamp: new Date().toISOString(),
      model,
      latencyMs,
      status: "api_error",
      error: {
        type: error instanceof Error ? error.name : "UnknownError",
        message:
          error instanceof Error
            ? error.message
            : "An unknown error occurred while calling Gemini.",
      },
    };

    console.error(JSON.stringify(errorRecord, null, 2));
    process.exitCode = 1;
  }
}

void main();
