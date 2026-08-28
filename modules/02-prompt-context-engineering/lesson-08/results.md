# Lesson 8 Results

## AI Requirement

- **Provider:** Google Gemini API
- **Tier:** Free
- **Model:** `gemini-3.6-flash`
- **Actual cost:** $0
- **Data:** Synthetic only
- **Language:** Python
- **SDK:** `google-genai`

## Aggregate Results

| Prompt variant | Category correct | Urgency correct | Format valid |
| -------------- | ---------------: | --------------: | -----------: |
| Zero-shot      |              4/4 |             4/4 |          4/4 |
| Few-shot       |              4/4 |             4/4 |          4/4 |

## Detailed Results

| Case             | Variant   | Expected category | Actual category | Expected urgency | Actual urgency | Format valid? | Latency (ms) |
| ---------------- | --------- | ----------------- | --------------- | ---------------- | -------------- | ------------- | -----------: |
| Refund delay     | Zero-shot | `BILLING`         | BILLING         | `MEDIUM`         | MEDIUM         | True          |      6009.91 |
| Production error | Zero-shot | `TECHNICAL`       | TECHNICAL       | `HIGH`           | HIGH           | True          |       3369.0 |
| Change email     | Zero-shot | `ACCOUNT`         | ACCOUNT         | `LOW`            | LOW            | True          |      4967.68 |
| Dark mode        | Zero-shot | `FEATURE_REQUEST` | FEATURE_REQUEST | `LOW`            | LOW            | True          |       3686.1 |
| Refund delay     | Few-shot  | `BILLING`         | BILLING         | `MEDIUM`         | MEDIUM         | True          |      2682.22 |
| Production error | Few-shot  | `TECHNICAL`       | TECHNICAL       | `HIGH`           | HIGH           | True          |      5652.79 |
| Change email     | Few-shot  | `ACCOUNT`         | ACCOUNT         | `LOW`            | LOW            | True          |      3589.04 |
| Dark mode        | Few-shot  | `FEATURE_REQUEST` | FEATURE_REQUEST | `LOW`            | LOW            | True          |      5555.87 |

## Actual Outputs

### Zero-Shot — Refund Delay

```json
{'case_id': 'refund_delay', 'prompt_variant': 'zero_shot', 'expected_category': 'BILLING', 'actual_category': 'BILLING', 'expected_urgency': 'MEDIUM', 'actual_urgency': 'MEDIUM', 'category_correct': True, 'urgency_correct': True, 'format_valid': True, 'latency_ms': 6009.91, 'output_text': 'CATEGORY: BILLING\nURGENCY: MEDIUM\nREASON: The user is inquiring about a missing refund following a cancellation, which requires a financial investigation.'}
```

### Zero-Shot — Production Error

```json
{'case_id': 'production_error', 'prompt_variant': 'zero_shot', 'expected_category': 'TECHNICAL', 'actual_category': 'TECHNICAL', 'expected_urgency': 'HIGH', 'actual_urgency': 'HIGH', 'category_correct': True, 'urgency_correct': True, 'format_valid': True, 'latency_ms': 3369.0, 'output_text': 'CATEGORY: TECHNICAL\nURGENCY: HIGH\nREASON: The checkout page is completely broken for all customers, causing a production-blocking failure that prevents accepting any orders.'}
```

### Zero-Shot — Change Email

```json
{'case_id': 'change_email', 'prompt_variant': 'zero_shot', 'expected_category': 'ACCOUNT', 'actual_category': 'ACCOUNT', 'expected_urgency': 'LOW', 'actual_urgency': 'LOW', 'category_correct': True, 'urgency_correct': True, 'format_valid': True, 'latency_ms': 4967.68, 'output_text': "CATEGORY: ACCOUNT\nURGENCY: LOW\nREASON: The user is asking for instructions on how to update their account's email address."}
```

### Zero-Shot — Dark Mode

```json
{'case_id': 'dark_mode', 'prompt_variant': 'zero_shot', 'expected_category': 'FEATURE_REQUEST', 'actual_category': 'FEATURE_REQUEST', 'expected_urgency': 'LOW', 'actual_urgency': 'LOW', 'category_correct': True, 'urgency_correct': True, 'format_valid': True, 'latency_ms': 3686.1, 'output_text': 'CATEGORY: FEATURE_REQUEST\nURGENCY: LOW\nREASON: The user is requesting a new dark mode feature for the admin portal, which represents a suggestion with no operational impact.'}
```

### Few-Shot — Refund Delay

```json
{'case_id': 'refund_delay', 'prompt_variant': 'few_shot', 'expected_category': 'BILLING', 'actual_category': 'BILLING', 'expected_urgency': 'MEDIUM', 'actual_urgency': 'MEDIUM', 'category_correct': True, 'urgency_correct': True, 'format_valid': True, 'latency_ms': 2682.22, 'output_text': 'CATEGORY: BILLING\nURGENCY: MEDIUM\nREASON: The customer is reporting an expected refund that has not yet posted to their card, requiring a financial investigation.'}
```

### Few-Shot — Production Error

```json
{'case_id': 'production_error', 'prompt_variant': 'few_shot', 'expected_category': 'TECHNICAL', 'actual_category': 'TECHNICAL', 'expected_urgency': 'HIGH', 'actual_urgency': 'HIGH', 'category_correct': True, 'urgency_correct': True, 'format_valid': True, 'latency_ms': 5652.79, 'output_text': 'CATEGORY: TECHNICAL\nURGENCY: HIGH\nREASON: The checkout page is completely broken for all customers, resulting in a production-blocking failure that prevents placing any orders.'}
```

### Few-Shot — Change Email

```json
{'case_id': 'change_email', 'prompt_variant': 'few_shot', 'expected_category': 'ACCOUNT', 'actual_category': 'ACCOUNT', 'expected_urgency': 'LOW', 'actual_urgency': 'LOW', 'category_correct': True, 'urgency_correct': True, 'format_valid': True, 'latency_ms': 3589.04, 'output_text': 'CATEGORY: ACCOUNT\nURGENCY: LOW\nREASON: The user is making an informational request about how to update the email address on their account.'}
```

### Few-Shot — Dark Mode

```json
{'case_id': 'dark_mode', 'prompt_variant': 'few_shot', 'expected_category': 'FEATURE_REQUEST', 'actual_category': 'FEATURE_REQUEST', 'expected_urgency': 'LOW', 'actual_urgency': 'LOW', 'category_correct': True, 'urgency_correct': True, 'format_valid': True, 'latency_ms': 5555.87, 'output_text': 'CATEGORY: FEATURE_REQUEST\nURGENCY: LOW\nREASON: The customer is requesting a new dark mode option for the admin portal rather than reporting an issue.'}
```

## Experiment Analysis

### 1. Classification Comparison

**Question:** Did few-shot prompting improve category or urgency accuracy compared with zero-shot prompting? Support your answer using the recorded totals.

My answer: I don't see any significant improvement on the few-shot prompting when compared to zero-shot prompting.

### 2. Format Compliance

**Question:** Did either prompt variant violate the required output format? If both achieved full compliance, what can and cannot be concluded from only four cases?

My answer: Neither of the prompt variants violated the required output format. I'm not sure.

### 3. Differences in Reasons

**Question:** Compare the zero-shot and few-shot `REASON` values. Did the examples noticeably affect their length, wording, or focus?

My answer: There seems to be no significant difference, I'm not entirely sure.

### 4. Latency

**Question:** Was few-shot prompting consistently slower in this run? Why is one execution per case insufficient for drawing a reliable performance conclusion?

My answer: Not sure

### 5. Recommendation

**Question:** Based only on this experiment, would you use the zero-shot or few-shot version? Explain the tradeoff. It is acceptable to conclude that the current evidence does not establish a meaningful winner.

My answer: The current evidence does not establish a meaningful winner. Although one tradeoff is that it uses more input token, I would still use the few-shot version compared to the zero-shot prompt.

## Python Reflection

### 1. Boolean Parameter

Consider:

```python
def build_system_instruction(use_examples: bool) -> str:
```

**Question:** What behavior does `use_examples` control, and why is sharing the same base instruction important for the experiment?

My answer: `use_examples` controls the boolean value of whether to include the examples along with the system instruction. Sharing the same base instruction is important to show the difference of zero-shot and few-shot prompt.

### 2. List Accumulation

Consider:

```python
formatted_examples: list[str] = []
formatted_examples.append(formatted_example)
```

**Question:** What does `append()` do, and why is a list useful before joining the examples into one string?

My answer: `append()` places the formatted_example string inside the formatted_examples list. To make a separate the data from examples.

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

My answer: I'm not really sure

### 4. Boolean Summation

Consider:

```python
category_correct = sum(
    result["category_correct"]
    for result in variant_results
)
```

**Question:** Why can Python use `sum()` to count the correct Boolean results?

My answer: Not sure

### 5. Set Membership

Consider:

```python
category in ALLOWED_CATEGORIES
```

**Question:** What does this expression check, and why is it useful when validating model output?

My answer: it checks if the category value is present in the ALLOWED_CATEGORIES list.

## Knowledge Check

### 1. Zero-Shot and Few-Shot

**Question:** What is the difference between zero-shot and few-shot prompting? Does few-shot prompting retrain the model?

My answer: Zero-shots does not include examples while few-shot prompting does. Not sure

### 2. Example Quality

One demonstration incorrectly labels a password-reset request as `TECHNICAL`.

**Question:** How could this affect later classifications?

My answer: future password-reset request may be classified as TECHNICAL incorrectly.

### 3. Evaluation Leakage

**Question:** Why should the exact evaluation tickets not also appear among the few-shot examples?

My answer: Not sure

### 4. Balanced Examples

**Question:** What problem could occur if eight demonstrations are `BILLING` and only one represents all other categories?

My answer: Not sure

### 5. Prompt Cost

**Question:** Why can few-shot prompting cost more even when the model produces an answer of the same length?

My answer: few-shot prompting costs more input token, which contributes to the total tokens.

### 6. Ground-Truth Quality

**Question:** If the evaluation dataset contains an incorrect expected label, what happens to the reported accuracy?

My answer: Not sure

### 7. Small Dataset Limitation

**Question:** Why does scoring 4/4 on this dataset not prove that the classifier is production-ready?

My answer: Not sure

### 8. Prompt Contract Versus Schema

**Question:** Why must the application still validate category and urgency even though the prompt explicitly restricts the allowed values?

My answer: The user might say that it's high ugency when it's systematically not.
