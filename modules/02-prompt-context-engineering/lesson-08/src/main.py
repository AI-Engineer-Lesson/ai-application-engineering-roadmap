from time import perf_counter
from typing import Any

from google import genai


client = genai.Client()

MODEL = "gemini-3.6-flash"

ALLOWED_CATEGORIES = {
    "BILLING",
    "TECHNICAL",
    "ACCOUNT",
    "FEATURE_REQUEST",
}

ALLOWED_URGENCIES = {
    "LOW",
    "MEDIUM",
    "HIGH",
}


# These examples are demonstrations supplied only to the few-shot prompt.
#
# They must not duplicate the evaluation cases below.
FEW_SHOT_EXAMPLES = [
    {
        "ticket": (
            "My card was charged twice for this month's subscription."
        ),
        "category": "BILLING",
        "urgency": "MEDIUM",
        "reason": (
            "The customer reports a duplicate subscription charge "
            "that requires financial investigation."
        ),
    },
    {
        "ticket": (
            "The dashboard shows an error whenever our team uploads "
            "a monthly report, but manual entry still works."
        ),
        "category": "TECHNICAL",
        "urgency": "MEDIUM",
        "reason": (
            "An existing upload function is broken, although a manual "
            "workaround remains available."
        ),
    },
    {
        "ticket": (
            "I cannot sign in after changing phones, and the recovery "
            "code is rejected."
        ),
        "category": "ACCOUNT",
        "urgency": "HIGH",
        "reason": (
            "The customer is completely unable to access the account "
            "through the available recovery method."
        ),
    },
    {
        "ticket": (
            "Please add an option to export the analytics dashboard "
            "as a CSV file."
        ),
        "category": "FEATURE_REQUEST",
        "urgency": "LOW",
        "reason": (
            "The customer is requesting new export functionality "
            "rather than reporting broken existing behavior."
        ),
    },
]


# This is the small evaluation dataset.
#
# These cases are not included among the few-shot examples.
EVALUATION_CASES: list[dict[str, Any]] = [
    {
        "case_id": "refund_delay",
        "ticket": (
            "My cancellation was approved five days ago, but the refund "
            "has not appeared on my card."
        ),
        "expected_category": "BILLING",
        "expected_urgency": "MEDIUM",
    },
    {
        "case_id": "production_error",
        "ticket": (
            "Our checkout page returns an error for every customer. "
            "We cannot accept any orders."
        ),
        "expected_category": "TECHNICAL",
        "expected_urgency": "HIGH",
    },
    {
        "case_id": "change_email",
        "ticket": (
            "How can I change the email address associated with my account?"
        ),
        "expected_category": "ACCOUNT",
        "expected_urgency": "LOW",
    },
    {
        "case_id": "dark_mode",
        "ticket": (
            "It would be helpful if the admin portal had a dark mode."
        ),
        "expected_category": "FEATURE_REQUEST",
        "expected_urgency": "LOW",
    },
]


def build_base_instruction() -> str:
    """
    Build the stable classification rules shared by both prompt variants.
    """

    return """
You classify synthetic customer-support tickets.

Categories:
- BILLING: Incorrect or duplicate charges, refunds, invoices, subscription pricing, or payment issues.
- TECHNICAL: Errors, broken pages, failed uploads, performance problems, or features not functioning as designed.
- ACCOUNT: Login problems, password resets, email-address changes, locked accounts, or account access and identity settings.
- FEATURE_REQUEST: Requests for new behavior or functionality that does not currently exist.

Urgency:
- HIGH: Complete inability to access a business-critical account, data loss, a security concern, a production-blocking failure, or a failure affecting an imminent deadline. Urgent-sounding words alone do not make a ticket HIGH.
- MEDIUM: Existing functionality is broken or significantly impaired, a financial issue needs investigation, work can continue only with meaningful difficulty, or timely support is needed for a non-production-blocking issue.
- LOW: Suggestions, issues with a workaround, informational requests, or requests with no meaningful operational impact.

Rules:
- Use only the allowed labels.
- Classify the user's primary request.
- Do not invent facts not present in the ticket.
- Return exactly the required output fields.
- Keep REASON to one concise sentence.

Required output:
CATEGORY: BILLING | TECHNICAL | ACCOUNT | FEATURE_REQUEST
URGENCY: LOW | MEDIUM | HIGH
REASON: one concise sentence
""".strip()


def build_examples_text(
    examples: list[dict[str, str]],
) -> str:
    """
    Convert structured demonstrations into prompt text.
    """

    formatted_examples: list[str] = []

    for example in examples:
        formatted_examples.append(
            "Example:\n"
            f"<ticket>\n{example['ticket']}\n</ticket>\n"
            f"CATEGORY: {example['category']}\n"
            f"URGENCY: {example['urgency']}\n"
            f"REASON: {example['reason']}"
        )

    return "\n\n".join(formatted_examples)


def build_system_instruction(use_examples: bool) -> str:
    """
    Build either the zero-shot or few-shot system instruction.

    If use_examples is False, return base_instruction unchanged.
   
    Otherwise:
    1. Call build_examples_text(FEW_SHOT_EXAMPLES).
    2. Add a section explaining that the examples demonstrate
      the intended application of the rules.
    3. Tell the model to classify the new ticket independently.
    4. Insert the formatted examples.
   
    Return the completed string.
    """

    base_instruction = build_base_instruction()

    if not use_examples:
        return base_instruction

    examples_text = build_examples_text(FEW_SHOT_EXAMPLES)

    return f"""
{base_instruction}
The following examples demonstrate the intended application of the rules.
Classify the new ticket independently. Do not copy facts from an example
into the new ticket's result.

{examples_text}
""".strip()


def build_user_input(ticket: str) -> str:
    """
    Wrap one untrusted ticket separately from trusted instructions.
    """

    return f"""
Classify the following new support ticket.

<ticket>
{ticket}
</ticket>
""".strip()


def parse_output(output_text: str) -> dict[str, str | None]:
    """
    Extract expected fields from the prompt-level text contract.

    This parser is intentionally simple. It demonstrates that prompt-based
    formatting can still fail and must be checked by application code.
    """

    parsed: dict[str, str | None] = {
        "category": None,
        "urgency": None,
        "reason": None,
    }

    for line in output_text.splitlines():
        cleaned_line = line.strip()

        if cleaned_line.startswith("CATEGORY:"):
            parsed["category"] = cleaned_line.removeprefix(
                "CATEGORY:"
            ).strip()

        elif cleaned_line.startswith("URGENCY:"):
            parsed["urgency"] = cleaned_line.removeprefix(
                "URGENCY:"
            ).strip()

        elif cleaned_line.startswith("REASON:"):
            parsed["reason"] = cleaned_line.removeprefix(
                "REASON:"
            ).strip()

    return parsed


def evaluate_output(
    test_case: dict[str, Any],
    parsed: dict[str, str | None],
) -> dict[str, bool]:
    """
    Deterministically compare parsed labels with expected labels.
    """

    category = parsed["category"]
    urgency = parsed["urgency"]
    reason = parsed["reason"]

    format_valid = (
        category in ALLOWED_CATEGORIES
        and urgency in ALLOWED_URGENCIES
        and isinstance(reason, str)
        and len(reason) > 0
    )

    return {
        "category_correct": (
            category == test_case["expected_category"]
        ),
        "urgency_correct": (
            urgency == test_case["expected_urgency"]
        ),
        "format_valid": format_valid,
    }


def run_case(
    test_case: dict[str, Any],
    prompt_variant: str,
    use_examples: bool,
) -> dict[str, Any]:
    """
    Run and evaluate one ticket using one prompt variant.
    """

    system_instruction = build_system_instruction(use_examples)
    input_text = build_user_input(test_case["ticket"])

    started_at = perf_counter()

    # Call client.interactions.create() using:
    #
    # - model=MODEL
    # - system_instruction=system_instruction
    # - input=input_text
    # - store=False
    interaction = client.interactions.create(
        model=MODEL,
        system_instruction=system_instruction,
        input=input_text,
        store=False
    )

    latency_ms = (perf_counter() - started_at) * 1000

    output_text = (
        interaction.output_text
        if interaction is not None
        else ""
    )

    parsed = parse_output(output_text)
    evaluation = evaluate_output(test_case, parsed)

    result = {
        "case_id": test_case["case_id"],
        "prompt_variant": prompt_variant,
        "expected_category": test_case["expected_category"],
        "actual_category": parsed["category"],
        "expected_urgency": test_case["expected_urgency"],
        "actual_urgency": parsed["urgency"],
        "category_correct": evaluation["category_correct"],
        "urgency_correct": evaluation["urgency_correct"],
        "format_valid": evaluation["format_valid"],
        "latency_ms": round(latency_ms, 2),
        "output_text": output_text,
    }

    return result


def summarize_results(
    results: list[dict[str, Any]],
) -> None:
    """
    Print deterministic totals for each prompt variant.
    """

    variants = ["zero_shot", "few_shot"]

    for variant in variants:
        variant_results = [
            result
            for result in results
            if result["prompt_variant"] == variant
        ]

        category_correct = sum(
            result["category_correct"]
            for result in variant_results
        )

        urgency_correct = sum(
            result["urgency_correct"]
            for result in variant_results
        )

        format_valid = sum(
            result["format_valid"]
            for result in variant_results
        )

        print("=" * 70)
        print(
            {
                "summary_for": variant,
                "total_cases": len(variant_results),
                "category_correct": category_correct,
                "urgency_correct": urgency_correct,
                "format_valid": format_valid,
            }
        )


def main() -> None:
    """
    Run every evaluation case against both prompt variants.
    """

    all_results: list[dict[str, Any]] = []

    prompt_variants = [
        {
            "name": "zero_shot",
            "use_examples": False,
        },
        {
            "name": "few_shot",
            "use_examples": True,
        },
    ]

    for variant in prompt_variants:
        for test_case in EVALUATION_CASES:
            result = run_case(
                test_case=test_case,
                prompt_variant=variant["name"],
                use_examples=variant["use_examples"],
            )

            all_results.append(result)

            print("=" * 70)
            print(result)

    summarize_results(all_results)


if __name__ == "__main__":
    main()
