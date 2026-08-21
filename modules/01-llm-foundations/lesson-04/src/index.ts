import { GoogleGenAI } from "@google/genai";
import { performance } from "node:perf_hooks";

const ai = new GoogleGenAI({});
const model = "gemini-3.7-flash";

type TestCase = {
  caseId: string;
  evidence: string;
  question: string;
  expectedBehavior:
    | "ANSWER_FROM_EVIDENCE"
    | "INSUFFICIENT_EVIDENCE"
    | "CONFLICTING_EVIDENCE";
};

type PromptMode = "baseline" | "evidence-bounded";

const testCases: TestCase[] = [
  {
    caseId: "supported",
    evidence: `
Policy A:
Appointments must be cancelled at least 24 hours before their scheduled time.
`,
    question: "How much notice is required when cancelling an appointment?",
    expectedBehavior: "ANSWER_FROM_EVIDENCE",
  },
  {
    caseId: "missing",
    evidence: `
Policy A:
Patients must confirm their name and contact number before an appointment is finalized.
`,
    question: "How much is the clinic's parking fee?",
    expectedBehavior: "INSUFFICIENT_EVIDENCE",
  },
  {
    caseId: "conflicting",
    evidence: `
Policy A:
Appointments must be cancelled at least 24 hours before their scheduled time.

Policy B:
Appointments must be cancelled at least 48 hours before their scheduled time.
`,
    question: "How much notice is required when cancelling an appointment?",
    expectedBehavior: "CONFLICTING_EVIDENCE",
  },
];

function buildPrompt(testCase: TestCase, mode: PromptMode): string {
  if (mode === "baseline") {
    return `Answer the question using the policies below.

Policies:
${testCase.evidence.trim()}

Question: ${testCase.question}`;
  }

  return `Answer the question using only the supplied policies.

If the policies do not contain enough information to answer the question, respond exactly with INSUFFICIENT_EVIDENCE.
If the policies contain conflicting answers to the question, respond exactly with CONFLICTING_EVIDENCE.
Do not guess or invent policy details.

Policies:
${testCase.evidence.trim()}

Question: ${testCase.question}`;
}

async function runCase(testCase: TestCase, mode: PromptMode): Promise<void> {
  const prompt = buildPrompt(testCase, mode);

  const startedAt = performance.now();

  const response = await ai.interactions.create({
    model,
    input: prompt,
  });

  const latencyMs = performance.now() - startedAt;

  // TODO 5:
  // Read the generated output text.
  const outputText = response?.output_text ?? "";

  console.log(
    JSON.stringify(
      {
        timestamp: new Date().toISOString(),
        caseId: testCase.caseId,
        mode,
        expectedBehavior: testCase.expectedBehavior,
        latencyMs,
        outputText,
      },
      null,
      2,
    ),
  );
}

async function main(): Promise<void> {
  const modes: PromptMode[] = ["baseline", "evidence-bounded"];

  // TODO 6:
  // Run every test case once under each prompt mode.
  for (const mode of modes) {
    for (const testCase of testCases) {
      await runCase(testCase, mode);
    }
  }
}

void main();
