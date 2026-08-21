import { GoogleGenAI } from "@google/genai";
import { performance } from "node:perf_hooks";
import { randomUUID } from "node:crypto";

const ai = new GoogleGenAI({});
const model = "gemini-3.7-flash";
const promptVersion = "lesson-05-v1";

const paidPricing = {
  inputPerMillionTokensUsd: 0.75,
  outputPerMillionTokensUsd: 3.75,
};

type TokenUsage = {
  inputTokens: number;
  outputTokens: number;
  thoughtTokens: number;
  totalTokens: number;
};

type ExpectedBehavior =
  | {
      kind: "contains";
      value: string;
    }
  | {
      kind: "abstain";
      value: "INSUFFICIENT_EVIDENCE";
    };

type SuccessRecord = {
  timestamp: string;
  requestId: string;
  model: string;
  promptVersion: string;
  caseId: string;
  status: "success";
  outcome: "answered" | "abstained";
  qualityVerdict: "PASS" | "FAIL";
  latencyMs: number;
  usage: TokenUsage;
  paidEquivalentCostUsd: number;
  actualFreeTierCostUsd: 0;
  outputText: string;
};

type ErrorRecord = {
  timestamp: string;
  requestId: string;
  model: string;
  promptVersion: string;
  caseId: string;
  status: "error";
  latencyMs: number;
  error: {
    code: string;
    name: string;
    message: string;
    retryable: boolean;
  };
};

type RequestRecord = SuccessRecord | ErrorRecord;

class ApplicationError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly retryable: boolean,
  ) {
    super(message);
    this.name = "ApplicationError";
  }
}

const cases = [
  {
    caseId: "supported",
    prompt: `
Use only the supplied policy.

POLICY
Appointments must be cancelled at least 24 hours before their scheduled time.

QUESTION
How much cancellation notice is required?
`,
    expected: {
      kind: "contains",
      value: "24 hours",
    } satisfies ExpectedBehavior,
  },
  {
    caseId: "abstention",
    prompt: `
Use only the supplied policy.

If the policy does not answer the question, respond exactly with:
INSUFFICIENT_EVIDENCE

POLICY
Patients must confirm their contact number before booking.

QUESTION
How much is the clinic's parking fee?
`,
    expected: {
      kind: "abstain",
      value: "INSUFFICIENT_EVIDENCE",
    } satisfies ExpectedBehavior,
  },
  {
    caseId: "invalid-input",
    prompt: "   ",
    expected: {
      kind: "contains",
      value: "",
    } satisfies ExpectedBehavior,
  },
];

function estimatePaidEquivalentCost(usage: TokenUsage): number {
  // Calculate input cost.
  //
  // Calculate output cost using visible output and thinking tokens.
  //
  // Return their combined cost.

  const inputCost =
    (usage.inputTokens / 1_000_000) * paidPricing.inputPerMillionTokensUsd;
  const outputCost =
    (usage.outputTokens / 1_000_000) * paidPricing.outputPerMillionTokensUsd;
  return inputCost + outputCost;
}

function evaluateOutput(
  outputText: string,
  expected: ExpectedBehavior,
): {
  outcome: "answered" | "abstained";
  qualityVerdict: "PASS" | "FAIL";
} {
  if (expected.kind === "abstain") {
    return {
      outcome: "abstained",
      qualityVerdict: outputText.trim() === expected.value ? "PASS" : "FAIL",
    };
  }

  return {
    outcome: "answered",
    qualityVerdict: outputText.includes(expected.value) ? "PASS" : "FAIL",
  };
}

function normalizeError(error: unknown): ErrorRecord["error"] {
  if (error instanceof ApplicationError) {
    return {
      code: error.code,
      name: error.name,
      message: error.message,
      retryable: error.retryable,
    };
  }

  if (error instanceof Error) {
    return {
      code: "unexpected_error",
      name: error.name,
      message: error.message,
      retryable: false,
    };
  }

  return {
    code: "unknown_error",
    name: "UnknownError",
    message: "An unknown error occurred",
    retryable: false,
  };
}

async function runTrackedRequest(
  caseId: string,
  prompt: string,
  expected: ExpectedBehavior,
): Promise<RequestRecord> {
  const requestId = randomUUID();
  const startedAt = performance.now();

  try {
    // Reject an empty or whitespace-only prompt with:
    if (prompt.trim() === "") {
      throw new ApplicationError(
        "invalid_input",
        "Prompt must not be empty",
        false,
      );
    }

    // Call ai.interactions.create() using model and prompt.
    const response = await ai.interactions.create({
      model,
      input: prompt,
    });

    const latencyMs = performance.now() - startedAt;

    // Safely read input, output, thought, and total tokens.
    const usage: TokenUsage = {
      inputTokens: response.usage?.total_input_tokens ?? 0,
      outputTokens: response.usage?.total_output_tokens ?? 0,
      thoughtTokens: response.usage?.total_thought_tokens ?? 0,
      totalTokens: response.usage?.total_tokens ?? 0,
    };

    const outputText = response.output_text ?? "";

    // Evaluate outputText against expected.
    const evaluation = evaluateOutput(outputText, expected);

    // Return a complete SuccessRecord.
    return {
      timestamp: new Date().toISOString(),
      requestId,
      model,
      promptVersion,
      caseId,
      status: "success",
      outcome: evaluation.outcome,
      qualityVerdict: evaluation.qualityVerdict,
      latencyMs,
      usage,
      paidEquivalentCostUsd: estimatePaidEquivalentCost(usage),
      actualFreeTierCostUsd: 0,
      outputText,
    };
  } catch (error: unknown) {
    const latencyMs = performance.now() - startedAt;

    // Return a complete ErrorRecord using normalizeError().
    return {
      timestamp: new Date().toISOString(),
      requestId,
      model,
      promptVersion,
      caseId,
      status: "error",
      latencyMs,
      error: normalizeError(error),
    };
  }
}

async function main(): Promise<void> {
  for (const testCase of cases) {
    const record = await runTrackedRequest(
      testCase.caseId,
      testCase.prompt,
      testCase.expected,
    );
    console.log(JSON.stringify(record, null, 2));
  }
}

void main();
