import { GoogleGenAI } from "@google/genai";
import { performance } from "node:perf_hooks";

const ai = new GoogleGenAI({});
const model = "gemini-3.7-flash";

const paidPricing = {
  inputPerMillionTokensUsd: 0.75,
  outputPerMillionTokensUsd: 3.75,
};

function buildClinicPolicies(count: number): string {
  return Array.from(
    { length: count },
    (_, index) =>
      `Policy ${index + 1}: Patients must confirm administrative details before an appointment is finalized.`,
  ).join("\n");
}

const experiments = [
  {
    caseId: "small",
    policyCount: 1,
  },
  {
    caseId: "medium",
    policyCount: 25,
  },
  {
    caseId: "large",
    policyCount: 100,
  },
];

function estimatePaidEquivalentCost(
  inputTokens: number,
  outputTokens: number,
  thoughtTokens: number,
): number {
  // Calculate input cost using inputPerMillionTokensUsd.
  //
  const inputCostUse =
    (inputTokens / 1_000_000) * paidPricing.inputPerMillionTokensUsd;

  // Calculate output cost using both visible output tokens
  // and thought tokens.
  const outputCostUse =
    ((outputTokens + thoughtTokens) / 1_000_000) *
    paidPricing.outputPerMillionTokensUsd;

  // Return the combined estimated cost.
  return inputCostUse + outputCostUse;
}

async function runExperiment(
  caseId: string,
  policyCount: number,
  inputTokenLimit: number,
): Promise<void> {
  const context = buildClinicPolicies(policyCount);

  const prompt = `
You are assisting with non-clinical dental clinic administration.

Read the synthetic policies below and summarize their shared requirement
in exactly one sentence.

POLICIES
${context}
`;

  // Count the prompt tokens before sending the generation request.
  const countResponse = await ai.models.countTokens({
    model,
    contents: prompt,
  });

  const preflightInputTokens = countResponse.totalTokens;

  const startTime = performance.now();

  // Call ai.interactions.create() using model and prompt.
  const response = await ai.interactions.create({
    model,
    input: prompt,
  });

  const latencyMs = performance.now() - startTime;

  // Read actual input, output, thought, and total tokens from usage.
  // Safely fall back to zero if a value is unavailable.
  const actualInputTokens = response?.usage?.total_input_tokens || 0;
  const outputTokens = response?.usage?.total_output_tokens || 0;
  const thoughtTokens = response?.usage?.total_thought_tokens || 0;
  const totalTokens = response?.usage?.total_tokens || 0;

  // Calculate the percentage of the model's input limit used.
  const inputContextUtilizationPercent =
    (actualInputTokens / inputTokenLimit) * 100;

  // Call estimatePaidEquivalentCost().
  const paidEquivalentCostUsd = estimatePaidEquivalentCost(
    actualInputTokens,
    outputTokens,
    thoughtTokens,
  );

  console.log(
    JSON.stringify(
      {
        timestamp: new Date().toISOString(),
        caseId,
        model,
        policyCount,
        promptCharacters: prompt.length,
        preflightInputTokens,
        actualInputTokens,
        outputTokens,
        thoughtTokens,
        totalTokens,
        inputTokenLimit,
        inputContextUtilizationPercent,
        latencyMs,
        paidEquivalentCostUsd,
        actualFreeTierCostUsd: 0,
        outputText: response?.output_text,
      },
      null,
      2,
    ),
  );
}

async function main(): Promise<void> {
  // Retrieve the current model information with ai.models.get().
  //
  // Read inputTokenLimit and outputTokenLimit.

  const modelInfo = await ai.models.get({ model });
  const inputTokenLimit = modelInfo?.inputTokenLimit || 0;
  const outputTokenLimit = modelInfo?.outputTokenLimit || 0;

  console.log(
    JSON.stringify(
      {
        model,
        inputTokenLimit,
        outputTokenLimit,
      },
      null,
      2,
    ),
  );

  for (const experiment of experiments) {
    await runExperiment(
      experiment.caseId,
      experiment.policyCount,
      inputTokenLimit,
    );
  }
}

void main();
