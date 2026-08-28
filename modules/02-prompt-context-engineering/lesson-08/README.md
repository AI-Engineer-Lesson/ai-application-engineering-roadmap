# Lesson 8 — Few-Shot Prompting and Small Evaluation Datasets

## Overview

This lesson compares zero-shot and few-shot prompting using a synthetic customer-support ticket classifier.

Both prompt variants classify tickets by:

- Category
- Urgency
- A concise reason

The same evaluation dataset and base instructions are used for both variants, allowing the effect of adding examples to be compared more fairly.

## Learning Objectives

- Explain zero-shot and few-shot prompting.
- Build reusable few-shot demonstrations.
- Separate demonstrations from evaluation cases.
- Design a small synthetic evaluation dataset.
- Parse a prompt-level output contract.
- Validate model-generated labels.
- Measure classification accuracy and format compliance.
- Compare prompt variants using recorded evidence.
- Understand the limitations of small evaluation datasets.

## Technology

- Python
- Google GenAI SDK
- Gemini Interactions API
- Model: `gemini-3.6-flash`
- Data: Synthetic only
- Actual cost: $0 within free-tier limits

`gemini-3.6-flash` was used because the available free-tier quota for `gemini-3.7-flash` was exhausted during the lesson.

## Project Structure

```text
lesson-08/
├── src/
│   └── main.py
├── lesson.md
├── results.md
├── README.md
└── requirements.txt
```

The local `.venv` directory and environment secrets are excluded from Git.

## Setup

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Configure the Gemini API key:

```powershell
$env:GEMINI_API_KEY="your-api-key"
```

Run the experiment:

```powershell
python src/main.py
```

## Classification Categories

The application supports four categories:

- `BILLING`: charges, refunds, invoices, subscriptions, and payments
- `TECHNICAL`: errors, broken pages, failed operations, and performance problems
- `ACCOUNT`: login, password, identity settings, and account access
- `FEATURE_REQUEST`: requests for new functionality

## Urgency Levels

- `HIGH`: security concerns, data loss, complete access failures, or production-blocking problems
- `MEDIUM`: financial issues or significantly impaired existing functionality
- `LOW`: suggestions, informational requests, or issues with little operational impact

Urgent-sounding language alone does not automatically produce `HIGH` urgency.

## Output Contract

The prompt requires:

```text
CATEGORY: BILLING | TECHNICAL | ACCOUNT | FEATURE_REQUEST
URGENCY: LOW | MEDIUM | HIGH
REASON: one concise sentence
```

This is a prompt-level contract rather than a schema-enforced response.

Application code must still validate every returned value.

## Zero-Shot Prompting

The zero-shot variant provides:

- Classification rules
- Category definitions
- Urgency definitions
- Output requirements

It does not include completed examples.

Advantages include:

- Fewer input tokens
- Simpler maintenance
- Less risk from incorrect demonstrations

## Few-Shot Prompting

The few-shot variant uses the same base instruction and adds four demonstrations.

Each category has one representative example:

- Billing
- Technical
- Account
- Feature request

The demonstrations show:

- Correct category selection
- Correct urgency selection
- Required formatting
- Appropriate explanation length

Few-shot prompting does not retrain or permanently modify the model. The examples are temporary context supplied with each request.

## Reusable Demonstrations

The demonstrations are stored as structured dictionaries:

```python
FEW_SHOT_EXAMPLES = [
    {
        "ticket": "Example ticket",
        "category": "BILLING",
        "urgency": "MEDIUM",
        "reason": "Example explanation.",
    },
]
```

They are converted into prompt text by:

```python
def build_examples_text(
    examples: list[dict[str, str]],
) -> str:
```

Collecting formatted examples in a list preserves their order. The program then joins them into one prompt section with consistent separators.

## Evaluation Dataset

Four unseen synthetic cases evaluate the prompt variants:

| Case             | Expected category | Expected urgency |
| ---------------- | ----------------- | ---------------- |
| Refund delay     | `BILLING`         | `MEDIUM`         |
| Production error | `TECHNICAL`       | `HIGH`           |
| Change email     | `ACCOUNT`         | `LOW`            |
| Dark mode        | `FEATURE_REQUEST` | `LOW`            |

The evaluation cases do not duplicate the few-shot demonstrations.

This separation reduces evaluation leakage and provides better evidence that the model can apply the demonstrated patterns to unseen inputs.

## Deterministic Evaluation

The model output is parsed into:

- Category
- Urgency
- Reason

The application then performs exact comparisons:

```python
category == test_case["expected_category"]
urgency == test_case["expected_urgency"]
```

It also checks whether:

- The category belongs to the allowed category set
- The urgency belongs to the allowed urgency set
- A non-empty reason is present

Python set membership supports these checks:

```python
category in ALLOWED_CATEGORIES
```

This detects unsupported, missing, or misspelled labels.

## Experiment Results

| Prompt variant | Category correct | Urgency correct | Format valid |
| -------------- | ---------------: | --------------: | -----------: |
| Zero-shot      |              4/4 |             4/4 |          4/4 |
| Few-shot       |              4/4 |             4/4 |          4/4 |

Both variants achieved identical results on the small dataset.

Few-shot prompting did not improve observed category accuracy, urgency accuracy, or format compliance during this execution.

## Explanation Comparison

Both variants returned concise reasons with similar focus and length.

Some few-shot responses used wording similar to the demonstrations, including phrases such as:

- “Financial investigation”
- “Rather than reporting an issue”

This suggests that demonstrations can influence wording even when they do not change the final classification.

## Latency Findings

Few-shot prompting was not consistently slower.

It was faster for:

- Refund delay
- Change email

It was slower for:

- Production error
- Dark mode

One execution per case is insufficient for a reliable performance comparison because latency can be affected by:

- Network conditions
- Provider load
- Model-processing variation
- Temporary infrastructure conditions

A stronger comparison would run every case multiple times and calculate average or median latency.

## Prompt Selection

Based only on this experiment, neither prompt variant has an accuracy advantage.

The zero-shot version is currently preferable because it achieved the same observed result while using:

- Fewer input tokens
- Fewer prompt components
- Less maintenance

Few-shot prompting would become more justified if broader testing showed improved consistency or better handling of difficult category boundaries.

## Python Concepts

### Boolean Parameters

```python
def build_system_instruction(use_examples: bool) -> str:
```

The `use_examples` parameter selects whether demonstrations are added.

Both variants share the same base instruction, ensuring that examples are the primary experimental difference.

### List Accumulation

```python
formatted_examples: list[str] = []
formatted_examples.append(formatted_example)
```

`append()` adds one formatted example to the list.

After collecting all demonstrations, `join()` combines them into one string.

### List Comprehensions

```python
variant_results = [
    result
    for result in results
    if result["prompt_variant"] == variant
]
```

This creates a list containing only results for the selected prompt variant.

### Boolean Summation

```python
category_correct = sum(
    result["category_correct"]
    for result in variant_results
)
```

Python treats `True` as `1` and `False` as `0`, allowing `sum()` to count successful evaluations.

## Evaluation Risks

### Incorrect Demonstrations

If a password-reset example is incorrectly labelled `TECHNICAL`, the model may imitate that mistake in later classifications.

Demonstrations must be reviewed as carefully as application code.

### Evaluation Leakage

Using an evaluation case as a prompt demonstration shows the model the expected answer before testing it.

A correct response would then provide weak evidence of generalization.

### Imbalanced Examples

If most demonstrations represent `BILLING`, the prompt may bias classifications toward billing while providing insufficient guidance for other categories.

### Incorrect Ground Truth

An incorrect expected label can:

- Make correct model behavior appear wrong
- Make incorrect behavior appear correct
- Produce misleading accuracy measurements

Ground-truth labels require careful human review.

## Limitations

Scoring 4/4 does not prove production readiness.

The dataset does not cover:

- Ambiguous tickets
- Mixed-intent tickets
- Misspellings
- Adversarial input
- Multilingual requests
- Unsupported situations
- Unusual real-world wording
- Repeated-run consistency

The experiment also evaluates each case only once.

A production evaluation would require a larger, representative, reviewed, and versioned regression dataset.

## Prompt Contracts Are Not Guarantees

Even when the prompt restricts allowed labels, the model can still:

- Return an unsupported label
- Misspell a label
- Omit a required field
- Add unexpected content
- Produce malformed output

Application validation is therefore mandatory.

A model response should not directly trigger privileged or irreversible operations.

Schema-enforced structured output will provide stronger format control in a later module, but semantic validation will still remain necessary.

## Production Considerations

- Keep demonstrations separate from evaluation data.
- Use correct, representative, varied examples.
- Version prompts and evaluation datasets.
- Test prompt changes against stable regression cases.
- Validate every model-produced field.
- Safely reject unsupported values.
- Avoid sensitive customer data in examples.
- Measure token growth when adding demonstrations.
- Test repeated executions for consistency.
- Re-evaluate behavior when changing models.
- Do not treat a persuasive explanation as proof of correctness.
- Keep API keys outside source control.

## Conclusion

Few-shot prompting can demonstrate category boundaries, formatting, and expected reasoning patterns. However, examples increase token usage and maintenance requirements, and incorrect examples can teach undesirable behavior.

In this experiment, zero-shot and few-shot prompting both achieved perfect results on four synthetic cases. The evidence therefore does not establish an accuracy winner.

Prompt techniques should be selected through controlled evaluation rather than assumption, and all model output must be validated before being trusted by an application.
