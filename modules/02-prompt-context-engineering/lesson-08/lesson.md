# Phase 1 · Module 2 · Lesson 8

## Few-Shot Prompting and Small Evaluation Datasets with Python

**Status:** Active  
**Required duration:** approximately 30–45 minutes  
**Language:** Python  
**Difficulty:** Beginner-friendly Python, intermediate prompt engineering

---

## AI Requirement

- **Provider:** Google Gemini API
- **Tier:** Free tier
- **Model:** `gemini-3.6-flash`
- **Model deviation:** Used instead of `gemini-3.7-flash` because the available Gemini 3.7 Flash free-tier quota was exhausted.
- **Data:** Synthetic only
- **Expected actual cost:** $0 within free-tier limits
- **Python SDK:** `google-genai` version 2.3.0 or newer
- **API:** Gemini Interactions API

References:

- [Gemini prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [Gemini text generation](https://ai.google.dev/gemini-api/docs/text-generation)
- [Gemini 3.7 Flash](https://ai.google.dev/gemini-api/docs/models/gemini-3.7-flash)

---

# 1. Why This Lesson Matters

A clear instruction can tell a model what to do, but instructions alone may not communicate every formatting convention, category boundary, or business interpretation.

Suppose a support system must classify tickets into one of these categories:

- `BILLING`
- `TECHNICAL`
- `ACCOUNT`
- `FEATURE_REQUEST`

It must also assign:

- `LOW`
- `MEDIUM`
- `HIGH`

A zero-shot prompt describes these rules without showing examples.

A few-shot prompt includes several correct input-output examples demonstrating how the rules should be applied.

Examples can help clarify:

- The exact output format
- Differences between similar categories
- How urgency should be interpreted
- How short or indirect requests should be handled
- Which details matter and which do not

However, examples also introduce risks.

A poor example can teach the wrong behavior. An unrepresentative example set can bias the model toward certain categories. More examples also consume more input tokens.

In this lesson, you will compare zero-shot and few-shot prompting using the same small evaluation dataset.

You will not decide that few-shot prompting is better merely because it sounds theoretically useful. You will measure whether it improves the observed results.

---

# 2. Learning Objectives

By the end of this lesson, you should be able to:

- Explain zero-shot, one-shot, and few-shot prompting.
- Build reusable examples separately from stable task instructions.
- Choose examples that are correct, representative, and varied.
- Avoid allowing examples to become accidental business rules.
- Build a small synthetic evaluation dataset.
- Run the same cases against two prompt variants.
- Parse a prompt-level output contract.
- Measure classification and format compliance.
- Compare zero-shot and few-shot results.
- Explain why a small successful test does not prove production reliability.
- Identify when few-shot examples are useful and when they add unnecessary cost.

---

# 3. Terminology

## Zero-Shot Prompting

The model receives task instructions but no completed examples.

Example:

```text
Classify this ticket as BILLING, TECHNICAL, ACCOUNT, or FEATURE_REQUEST.
```

## One-Shot Prompting

The model receives one completed example before the actual request.

## Few-Shot Prompting

The model receives a small number of completed examples showing how the task should be performed.

Example:

```text
Example ticket:
I was charged twice.

Example result:
CATEGORY: BILLING
URGENCY: MEDIUM
```

The examples are supplied at request time. The model is not retrained or permanently modified.

## Demonstration

An input-output example included in the prompt.

A demonstration usually contains:

- A representative input
- The expected output
- Correct formatting
- Correct application of the business rules

## Evaluation Dataset

A collection of inputs and expected results used to assess system behavior.

In this lesson, the dataset is:

- Small
- Synthetic
- Stored directly in Python
- Used for learning rather than proving production readiness

## Ground Truth

The expected correct result recorded in the evaluation dataset.

For example:

```python
{
    "expected_category": "TECHNICAL",
    "expected_urgency": "HIGH",
}
```

Ground truth must be reviewed carefully. Incorrect expected values make evaluation misleading.

## Exact-Match Evaluation

A deterministic comparison between the model’s parsed answer and the expected value.

For example:

```python
actual_category == expected_category
```

Exact matching is simple and useful for controlled labels. It is not appropriate for every natural-language task.

## Format Compliance

Whether the output follows the required structure closely enough for the application to parse it.

---

# 4. Zero-Shot Versus Few-Shot

## Zero-Shot Advantages

- Shorter prompt
- Lower input-token usage
- Easier prompt maintenance
- No risk of teaching patterns from incorrect examples
- Often sufficient for simple, clearly defined tasks

## Zero-Shot Limitations

- Category boundaries may remain unclear
- Formatting may vary
- Edge cases may be interpreted differently than intended
- Written rules may be less concrete than examples

## Few-Shot Advantages

- Shows the desired format
- Demonstrates category boundaries
- Communicates tone and level of detail
- Can improve consistency for recurring patterns
- Can clarify business interpretations that are difficult to describe concisely

## Few-Shot Limitations

- Consumes additional input tokens
- Increases prompt maintenance
- Incorrect examples can reinforce incorrect behavior
- Overly similar examples can bias predictions
- Examples may not cover unfamiliar production cases
- Models can still ignore or misapply them

Few-shot prompting is an experimentable technique, not a guarantee.

---

# 5. Selecting Good Examples

A useful example set should be:

## Correct

Every expected answer must follow the intended business rules.

## Representative

Examples should resemble realistic requests the application will receive.

## Varied

Do not provide four examples that all demonstrate the same obvious situation.

## Relevant

Avoid examples unrelated to the actual task.

## Concise

Examples should demonstrate the required pattern without unnecessary content.

## Balanced

One category should not dominate unless that reflects the real production distribution and is intentional.

## Separate from Evaluation Cases

Do not use the exact evaluation inputs as prompt examples.

If the model has already seen the answer to the exact test case in its prompt, the test provides weak evidence of generalization.

---

# 6. Classification Rules

The fictional support system uses these categories.

## `BILLING`

Use for:

- Incorrect charges
- Duplicate charges
- Refund questions
- Invoice questions
- Subscription pricing or payment issues

## `TECHNICAL`

Use for:

- Errors
- Broken pages
- Failed uploads
- Performance problems
- Features that are not functioning as designed

## `ACCOUNT`

Use for:

- Login problems
- Password resets
- Email-address changes
- Locked accounts
- Account access or identity settings

## `FEATURE_REQUEST`

Use when the user asks for new behavior or functionality that does not currently exist.

Examples:

- Add dark mode
- Add CSV export
- Support another integration
- Add a new report

---

# 7. Urgency Rules

## `HIGH`

Use when the request describes:

- Complete inability to access a business-critical account
- Data loss
- A security concern
- A production-blocking failure
- A failure affecting an imminent deadline

Urgent-sounding words alone do not automatically make a ticket `HIGH`.

## `MEDIUM`

Use when:

- Existing functionality is broken or significantly impaired
- A financial issue needs investigation
- Work can continue, but with meaningful difficulty
- The request requires timely support but is not production-blocking

## `LOW`

Use when:

- The request is a suggestion
- The issue has a workaround
- The request is informational
- There is no meaningful operational impact

---

# 8. Output Contract

Require the model to return:

```text
CATEGORY: BILLING | TECHNICAL | ACCOUNT | FEATURE_REQUEST
URGENCY: LOW | MEDIUM | HIGH
REASON: one concise sentence
```

This remains a prompt-level contract.

Your application will parse and evaluate it, but the API does not enforce it through a response schema in this lesson.

Schema-enforced structured output will be introduced in Module 3.

---

# 9. Project Structure

Create:

```text
lesson-08/
├── src/
│   └── main.py
├── lesson.md
├── results.md
├── requirements.txt
└── .venv/              # Local only; do not commit
```

`README.md` will be created only after the lesson passes review.

---

# 10. Setup

## Step 1: Create the Folder

From `modules/02-prompt-context-engineering`:

```powershell
mkdir lesson-08
cd lesson-08
mkdir src
```

Create:

```text
lesson.md
results.md
src/main.py
```

Place this complete lesson inside `lesson.md`.

## Step 2: Create the Virtual Environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Step 3: Install Dependencies

```powershell
python -m pip install --upgrade "google-genai>=2.3.0"
```

Create `requirements.txt` using UTF-8-compatible output:

```powershell
cmd /c "python -m pip freeze > requirements.txt"
```

## Step 4: Configure the API Key

```powershell
$env:GEMINI_API_KEY="your-api-key"
```

Do not commit:

- `.venv`
- `.env`
- Your Gemini API key
- Python cache files

---

# 11. Create `src/main.py`

Copy this starter code:

```python
from time import perf_counter
from typing import Any

from google import genai


client = genai.Client()

MODEL = "gemini-3.7-flash"

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

    # TODO 1:
    # Return a triple-quoted string containing:
    #
    # - The support-ticket classification role
    # - The four category definitions
    # - The three urgency definitions
    # - A rule to use only allowed labels
    # - A rule to classify the user's primary request
    # - A rule not to invent facts
    # - The exact output contract
    # - A rule to make REASON one concise sentence
    #
    # Call .strip() on the final string.
    return ""


def build_examples_text(
    examples: list[dict[str, str]],
) -> str:
    """
    Convert structured demonstrations into prompt text.
    """

    formatted_examples: list[str] = []

    # TODO 2:
    # Loop through examples.
    #
    # For each example, append a string with this structure:
    #
    # Example:
    # <ticket>
    # [ticket text]
    # </ticket>
    # CATEGORY: [category]
    # URGENCY: [urgency]
    # REASON: [reason]
    #
    # Use dictionary access such as:
    #
    # example["ticket"]
    #
    # Append each formatted string to formatted_examples.

    # TODO 3:
    # Join formatted_examples using two newline characters:
    #
    # "\n\n".join(formatted_examples)
    #
    # Return the resulting string.
    return ""


def build_system_instruction(use_examples: bool) -> str:
    """
    Build either the zero-shot or few-shot system instruction.
    """

    base_instruction = build_base_instruction()

    # TODO 4:
    # If use_examples is False, return base_instruction unchanged.
    #
    # Otherwise:
    # 1. Call build_examples_text(FEW_SHOT_EXAMPLES).
    # 2. Add a section explaining that the examples demonstrate
    #    the intended application of the rules.
    # 3. Tell the model to classify the new ticket independently.
    # 4. Insert the formatted examples.
    #
    # Return the completed string.
    return ""


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

    # TODO 5:
    # Call client.interactions.create() using:
    #
    # - model=MODEL
    # - system_instruction=system_instruction
    # - input=input_text
    # - store=False
    interaction = None

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
```

---

# 12. Implementation Requirements

Complete all five TODOs.

## TODO 1: Build the Base Instruction

Your instruction must define the categories and urgency levels from Sections 6 and 7.

A suitable structure is:

```python
return """
You classify synthetic customer-support tickets.

Categories:
- BILLING: ...
- TECHNICAL: ...
- ACCOUNT: ...
- FEATURE_REQUEST: ...

Urgency:
- HIGH: ...
- MEDIUM: ...
- LOW: ...

Rules:
- Use only the allowed labels.
- Classify the ticket's primary request.
- Do not invent facts not present in the ticket.
- Return exactly the required output fields.
- Keep REASON to one concise sentence.

Required output:
CATEGORY: BILLING | TECHNICAL | ACCOUNT | FEATURE_REQUEST
URGENCY: LOW | MEDIUM | HIGH
REASON: one concise sentence
""".strip()
```

Write the complete definitions rather than using the ellipses.

## TODO 2: Format the Examples

Inside the loop:

```python
formatted_example = f"""
Example:
<ticket>
{example["ticket"]}
</ticket>
CATEGORY: {example["category"]}
URGENCY: {example["urgency"]}
REASON: {example["reason"]}
""".strip()

formatted_examples.append(formatted_example)
```

The examples are trusted demonstrations created by the application developer.

They are not user input.

## TODO 3: Join the Examples

```python
return "\n\n".join(formatted_examples)
```

This creates one string containing every demonstration with a blank line between them.

## TODO 4: Build the Prompt Variant

A valid implementation is:

```python
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
```

The zero-shot and few-shot variants must share the same base rules.

The only intended difference is the presence of demonstrations.

This makes the comparison more meaningful.

## TODO 5: Call Gemini

```python
interaction = client.interactions.create(
    model=MODEL,
    system_instruction=system_instruction,
    input=input_text,
    store=False,
)
```

The experiment makes eight calls:

- Four zero-shot
- Four few-shot

---

# 13. Run the Experiment

Ensure the environment is active:

```powershell
.\.venv\Scripts\Activate.ps1
```

Ensure the API key is configured:

```powershell
$env:GEMINI_API_KEY="your-api-key"
```

Run:

```powershell
python src/main.py
```

You should receive:

- Eight individual results
- One zero-shot summary
- One few-shot summary

Do not rerun the experiment repeatedly merely to obtain a preferred result.

Record the first successful complete execution.

A failed API request caused by a network or configuration problem may be retried.

---

# 14. Expected Ground Truth

| Case             | Expected category | Expected urgency | Reason                                                       |
| ---------------- | ----------------- | ---------------- | ------------------------------------------------------------ |
| Refund delay     | `BILLING`         | `MEDIUM`         | The unresolved issue concerns a refund                       |
| Production error | `TECHNICAL`       | `HIGH`           | Checkout is completely blocking customer orders              |
| Change email     | `ACCOUNT`         | `LOW`            | It concerns an account identity setting and is informational |
| Dark mode        | `FEATURE_REQUEST` | `LOW`            | It requests new optional functionality                       |

A model may produce a different concise explanation while still receiving correct category and urgency scores.

---

# 15. Create `results.md`

Copy this template:

````markdown
# Lesson 8 Results

## AI Requirement

- **Provider:** Google Gemini API
- **Tier:** Free
- **Model:** `gemini-3.7-flash`
- **Actual cost:** $0
- **Data:** Synthetic only
- **Language:** Python
- **SDK:** `google-genai`

## Aggregate Results

| Prompt variant | Category correct | Urgency correct | Format valid |
| -------------- | ---------------: | --------------: | -----------: |
| Zero-shot      |               /4 |              /4 |           /4 |
| Few-shot       |               /4 |              /4 |           /4 |

## Detailed Results

| Case             | Variant   | Expected category | Actual category | Expected urgency | Actual urgency | Format valid? | Latency (ms) |
| ---------------- | --------- | ----------------- | --------------- | ---------------- | -------------- | ------------- | -----------: |
| Refund delay     | Zero-shot | `BILLING`         |                 | `MEDIUM`         |                |               |              |
| Production error | Zero-shot | `TECHNICAL`       |                 | `HIGH`           |                |               |              |
| Change email     | Zero-shot | `ACCOUNT`         |                 | `LOW`            |                |               |              |
| Dark mode        | Zero-shot | `FEATURE_REQUEST` |                 | `LOW`            |                |               |              |
| Refund delay     | Few-shot  | `BILLING`         |                 | `MEDIUM`         |                |               |              |
| Production error | Few-shot  | `TECHNICAL`       |                 | `HIGH`           |                |               |              |
| Change email     | Few-shot  | `ACCOUNT`         |                 | `LOW`            |                |               |              |
| Dark mode        | Few-shot  | `FEATURE_REQUEST` |                 | `LOW`            |                |               |              |

## Actual Outputs

### Zero-Shot — Refund Delay

```text
Paste the output here.
```

### Zero-Shot — Production Error

```text
Paste the output here.
```

### Zero-Shot — Change Email

```text
Paste the output here.
```

### Zero-Shot — Dark Mode

```text
Paste the output here.
```

### Few-Shot — Refund Delay

```text
Paste the output here.
```

### Few-Shot — Production Error

```text
Paste the output here.
```

### Few-Shot — Change Email

```text
Paste the output here.
```

### Few-Shot — Dark Mode

```text
Paste the output here.
```

## Experiment Analysis

### 1. Classification Comparison

**Question:** Did few-shot prompting improve category or urgency accuracy compared with zero-shot prompting? Support your answer using the recorded totals.

My answer:

### 2. Format Compliance

**Question:** Did either prompt variant violate the required output format? If both achieved full compliance, what can and cannot be concluded from only four cases?

My answer:

### 3. Differences in Reasons

**Question:** Compare the zero-shot and few-shot `REASON` values. Did the examples noticeably affect their length, wording, or focus?

My answer:

### 4. Latency

**Question:** Was few-shot prompting consistently slower in this run? Why is one execution per case insufficient for drawing a reliable performance conclusion?

My answer:

### 5. Recommendation

**Question:** Based only on this experiment, would you use the zero-shot or few-shot version? Explain the tradeoff. It is acceptable to conclude that the current evidence does not establish a meaningful winner.

My answer:

## Python Reflection

### 1. Boolean Parameter

Consider:

```python
def build_system_instruction(use_examples: bool) -> str:
```

**Question:** What behavior does `use_examples` control, and why is sharing the same base instruction important for the experiment?

My answer:

### 2. List Accumulation

Consider:

```python
formatted_examples: list[str] = []
formatted_examples.append(formatted_example)
```

**Question:** What does `append()` do, and why is a list useful before joining the examples into one string?

My answer:

### 3. Filtering with a List Comprehension

Consider:

```python
variant_results = [
    result
    for result in results
    if result["prompt_variant"] == variant
]
```

**Question:** What values will this expression include?

My answer:

### 4. Boolean Summation

Consider:

```python
category_correct = sum(
    result["category_correct"]
    for result in variant_results
)
```

**Question:** Why can Python use `sum()` to count the correct Boolean results?

My answer:

### 5. Set Membership

Consider:

```python
category in ALLOWED_CATEGORIES
```

**Question:** What does this expression check, and why is it useful when validating model output?

My answer:

## Knowledge Check

### 1. Zero-Shot and Few-Shot

**Question:** What is the difference between zero-shot and few-shot prompting? Does few-shot prompting retrain the model?

My answer:

### 2. Example Quality

One demonstration incorrectly labels a password-reset request as `TECHNICAL`.

**Question:** How could this affect later classifications?

My answer:

### 3. Evaluation Leakage

**Question:** Why should the exact evaluation tickets not also appear among the few-shot examples?

My answer:

### 4. Balanced Examples

**Question:** What problem could occur if eight demonstrations are `BILLING` and only one represents all other categories?

My answer:

### 5. Prompt Cost

**Question:** Why can few-shot prompting cost more even when the model produces an answer of the same length?

My answer:

### 6. Ground-Truth Quality

**Question:** If the evaluation dataset contains an incorrect expected label, what happens to the reported accuracy?

My answer:

### 7. Small Dataset Limitation

**Question:** Why does scoring 4/4 on this dataset not prove that the classifier is production-ready?

My answer:

### 8. Prompt Contract Versus Schema

**Question:** Why must the application still validate category and urgency even though the prompt explicitly restricts the allowed values?

My answer:
````

---

# 16. Completion Criteria

Submit all of the following:

- [ ] Created and activated `.venv`
- [ ] Created UTF-8-compatible `requirements.txt`
- [ ] Completed all five TODOs
- [ ] Ran all four cases with the zero-shot prompt
- [ ] Ran all four cases with the few-shot prompt
- [ ] Recorded all eight outputs
- [ ] Completed the aggregate table
- [ ] Completed the detailed table
- [ ] Answered all five experiment-analysis questions
- [ ] Answered all five Python-reflection questions
- [ ] Answered all eight knowledge-check questions
- [ ] Confirmed that examples do not duplicate evaluation cases
- [ ] Confirmed `.venv`, `.env`, and secrets are excluded from Git
- [ ] Committed and pushed the lesson

After completing it, say:

```text
Done. Please check Lesson 8.
```

Do not create `README.md` yet.

The permanent README will be created after the implementation, results, and answers pass review.

---

# 17. Optional Extension — Approximately 60 Minutes

Add these edge cases:

```python
{
    "case_id": "urgent_word_only",
    "ticket": (
        "URGENT: Please add a compact view to the dashboard whenever possible."
    ),
    "expected_category": "FEATURE_REQUEST",
    "expected_urgency": "LOW",
},
{
    "case_id": "mixed_request",
    "ticket": (
        "I cannot log in, and after this is fixed I would also like dark mode."
    ),
    "expected_category": "ACCOUNT",
    "expected_urgency": "HIGH",
},
```

Evaluate whether the model:

- Avoids assigning `HIGH` only because the word “urgent” appears
- Classifies the primary blocking request in the mixed ticket
- Does not allow the secondary feature request to override the access problem

Explain whether your prompt rules are sufficient or need a carefully written additional demonstration.

Do not add a demonstration that duplicates either test case exactly.

---

# 18. Optional Deep Work — Up to 120 Minutes

Run each case three times for each prompt variant.

Store:

- Variant
- Case ID
- Run number
- Category
- Urgency
- Format validity
- Latency

Calculate:

- Category accuracy
- Urgency accuracy
- Format-compliance rate
- Average latency
- Minimum latency
- Maximum latency
- Number of outputs that changed between runs

This produces:

```text
4 cases × 2 variants × 3 runs = 24 calls
```

Only perform this extension if it remains within your free-tier limits.

Then answer:

1. Did any classification change across repeated runs?
2. Was one prompt variant more consistent?
3. Did few-shot prompting have noticeably higher average latency?
4. Was the sample large enough for a strong production conclusion?
5. What additional cases would be needed before deployment?

---

# 19. Common Mistakes

## Using Evaluation Cases as Examples

This weakens the evaluation because the prompt already contains the exact expected mappings.

## Adding Examples Only to Fix Each Failed Test

This can overfit the prompt to the current dataset without improving general behavior.

## Changing Multiple Variables at Once

If you change instructions, examples, model, and test data simultaneously, you cannot identify what caused a result to improve or regress.

## Using Incorrect Demonstrations

The model may imitate incorrect category boundaries, urgency rules, or formatting.

## Assuming More Examples Are Always Better

More examples consume tokens and can introduce irrelevant or conflicting patterns.

## Relying Only on Natural-Language Reasons

A persuasive explanation does not prove that the assigned category is correct.

## Treating Exact Matching as Suitable for Every Task

Exact matching works well for controlled labels. It is too strict for many open-ended text-generation tasks.

## Treating One Run as a Benchmark

Latency and model output may vary between calls.

## Treating 4/4 as Production Proof

Four synthetic cases cover only a very small portion of possible user behavior.

---

# 20. Production Concerns

- Review every demonstration as carefully as production code.
- Version prompt examples with the application.
- Keep evaluation cases separate from demonstrations.
- Use representative cases from the real domain.
- Remove or anonymize sensitive data before using production tickets.
- Do not place private customer data in examples.
- Track failures by category and scenario, not only overall accuracy.
- Include ambiguous, adversarial, multilingual, misspelled, and mixed-intent cases.
- Test prompt changes against a stable regression dataset.
- Avoid changing the dataset merely to make a prompt appear more accurate.
- Measure input-token growth when adding examples.
- Consider dynamically selecting relevant examples when the full example set becomes large.
- Validate all model-produced labels in application code.
- Reject or safely handle unrecognized values.
- Do not allow classification output alone to perform privileged actions.
- Monitor production distribution changes over time.
- Re-evaluate when changing the model or model version.
- Keep the API key outside source control.

---

# 21. Core Principle

Few-shot examples show a model what successful behavior looks like, but their usefulness must be measured rather than assumed.

Good demonstrations are correct, representative, varied, concise, and separate from the evaluation dataset.

A small evaluation dataset helps detect obvious regressions and compare prompt variants, but it does not prove production reliability. Model outputs must still be parsed, validated, monitored, and tested against broader real-world cases.

---

# Immediate Task

1. Create `lesson-08`.
2. Create and activate `.venv`.
3. Install `google-genai`.
4. Create UTF-8-compatible `requirements.txt`.
5. Implement all five TODOs.
6. Run the zero-shot and few-shot experiments.
7. Complete `results.md`.
8. Commit and push the lesson.
9. Say: **“Done. Please check Lesson 8.”**
