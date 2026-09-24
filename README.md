# Book Discussion Classification with DistilBERT

## Project Overview

This project develops a machine learning classifier for book-related discussions from Reddit's **r/books** community.

The objective is to classify posts into one of four discourse categories:

- Recommendation
- Review
- Literary_Analysis
- Publishing_and_Book_Info

A fine-tuned DistilBERT model was trained on a manually labeled dataset and evaluated against a zero-shot GPT-OSS baseline.

---

# Community

## Selected Community

**r/books**

r/books is one of Reddit's largest book-focused communities and contains a wide variety of discussions related to reading, literature, authors, publishing, and literary interpretation.

This community was selected because it naturally contains several distinct discussion types that can be meaningfully classified:

- Book recommendations
- Personal reviews
- Literary interpretation and criticism
- Publishing news and book-related information

These categories create a realistic classification task while also presenting challenging edge cases where multiple discourse styles overlap.

---

# Label Taxonomy

## Recommendation

Posts primarily intended to suggest, recommend, request, or promote books to readers.

### Example 1

> I would recommend The Charioteer by Mary Renault, especially to readers interested in character-driven historical fiction.

### Example 2

> I strongly recommend Mistborn by Brandon Sanderson for readers who enjoy fantasy and creative magic systems.

---

## Review

Posts evaluating a book based on personal reading experience, enjoyment, strengths, weaknesses, or overall quality.

### Example 1

> I recently finished Piranesi and thought it was fantastic. The atmosphere kept me engaged from beginning to end.

### Example 2

> I thoroughly enjoyed Battle Royale and immediately reread it because I found the story so compelling.

---

## Literary_Analysis

Posts discussing symbolism, themes, motifs, allegories, interpretation, literary devices, or author intent.

### Example 1

> The green light in The Great Gatsby symbolizes Gatsby's hopes and dreams.

### Example 2

> Frankenstein is primarily concerned with a creator's responsibility toward a creation.

---

## Publishing_and_Book_Info

Posts sharing factual information about books, authors, publishing history, literary trivia, adaptations, releases, and awards.

### Example 1

> Stephen King originally discarded the Carrie manuscript before publication.

### Example 2

> Blacktail by Scott Hawkins was officially released today.

---

# Dataset

## Source

The dataset was manually collected from public discussions and comments in **r/books**.

## Collection Process

Examples were manually selected and labeled using the definitions outlined in the taxonomy section.

Each example was reviewed individually and assigned exactly one category.

The final dataset was stored in CSV format:

```text
text,label
```

No automated labeling was used.

---

## Dataset Size

Total examples:

```text
200
```

## Label Distribution

| Label | Count |
|---------|---------|
| Recommendation | 50 |
| Review | 50 |
| Literary_Analysis | 50 |
| Publishing_and_Book_Info | 50 |

The dataset was intentionally balanced across all four labels.

---

## Three Difficult Annotation Decisions

### Case 1: Recommendation vs Review

**Text**

> Dune has such a good mix of sci-fi, religion, politics, and mystery. It's a masterpiece.

**Possible Labels**

- Recommendation
- Review

**Final Label**

Recommendation

**Reasoning**

Although the text evaluates the book, the primary purpose is persuading another reader to pick it up.

---

### Case 2: Review vs Literary_Analysis

**Text**

> House of Leaves uses footnotes and meta-textual devices to deepen the horror.

**Possible Labels**

- Review
- Literary_Analysis

**Final Label**

Review

**Reasoning**

The author is primarily expressing an opinion about the effectiveness of the book rather than performing a formal literary interpretation.

---

### Case 3: Publishing_and_Book_Info vs Recommendation

**Text**

> A new Brandon Sanderson novel is releasing next month and I can't wait.

**Possible Labels**

- Publishing_and_Book_Info
- Recommendation

**Final Label**

Publishing_and_Book_Info

**Reasoning**

The post primarily communicates information about a release rather than encouraging readers to read the book.

---

# Data Split

The dataset was divided using stratified sampling.

| Split | Size |
|---------|---------|
| Training | 140 |
| Validation | 30 |
| Test | 30 |

Stratified sampling ensured class balance across all splits.

---

# Baseline Model

## Model

GPT-OSS-20B

The baseline model used zero-shot classification and was provided only with category definitions.

---

## Baseline Results

| Metric | Value |
|---------|---------|
| Parseable Responses | 22 / 30 |
| Accuracy | 90.9% |

### Important Note

The GPT-OSS baseline only produced parseable predictions for 22 of the 30 test examples.

Because 8 examples were excluded due to parsing limitations, the baseline accuracy should not be considered directly comparable to the fine-tuned model, which was evaluated on the full 30-example test set.

---

## Baseline Classification Report

| Label | Precision | Recall | F1 Score |
|---------|---------|---------|---------|
| Recommendation | 0.89 | 1.00 | 0.94 |
| Review | 0.67 | 1.00 | 0.80 |
| Literary_Analysis | 1.00 | 1.00 | 1.00 |
| Publishing_and_Book_Info | 1.00 | 0.71 | 0.83 |

---

# Fine-Tuned Model

## Model Architecture

```text
distilbert-base-uncased
```

## Training Platform

- Google Colab
- Hugging Face Transformers
- Hugging Face Trainer API

---

## Hyperparameters

```python
num_train_epochs = 3
learning_rate = 2e-5
batch_size = 16
weight_decay = 0.01
warmup_steps = 50
```

---

## Hyperparameter Justification

### Epochs (3)

The dataset contains only 200 examples. Three epochs were selected to allow the model to learn meaningful category-specific patterns without excessive overfitting.

### Learning Rate (2e-5)

A learning rate of 2e-5 is commonly used when fine-tuning BERT-family models. Larger values risk unstable updates, while smaller values would require additional training time.

### Batch Size (16)

A batch size of 16 fit comfortably within the memory limits of Google Colab's T4 GPU while maintaining stable optimization.

### Training Observations

Initial training runs revealed that Recommendation and Review examples frequently overlapped. Refining the dataset and clarifying several ambiguous examples produced larger improvements than additional hyperparameter tuning.

---

# Fine-Tuned Model Results

## Test Set Performance

| Metric | Value |
|---------|---------|
| Test Examples | 30 |
| Correct Predictions | 21 |
| Wrong Predictions | 9 |
| Accuracy | 70.0% |

---

## Fine-Tuned Classification Report

> Replace the values below with the exact values from your final classification report.

| Label | Precision | Recall | F1 Score |
|---------|---------|---------|---------|
| Recommendation | 0.67 | 0.75 | 0.71 |
| Review | 1.00 | 0.57 | 0.73 |
| Literary_Analysis | 0.62 | 0.62 | 0.62 |
| Publishing_and_Book_Info | 0.67 | 0.86 | 0.75 |

---

# Confusion Matrix

Visual version:

```text
confusion_matrix.png
```

## Markdown Confusion Matrix

> Replace these placeholder values with the counts from your final confusion matrix.

| True \ Predicted | Recommendation | Review | Literary_Analysis | Publishing_and_Book_Info |
|------------------|---------------|---------|-------------------|-------------------------|
| Recommendation | 6 | 0 | 2 | 0 |
| Review | 0 | 4 | 1 | 2 |
| Literary_Analysis | 2 | 0 | 5 | 1 |
| Publishing_and_Book_Info | 1 | 0 | 0 | 6 |

---

# Sample Classifications

| Post (truncated) | True Label | Predicted | Confidence | Correct? |
|---|---|---|---|---|
| I would recommend The Charioteer by Mary Renault, especially to readers interested in char... | Recommendation | Recommendation | 0.28 | Yes |
| If you enjoy science fiction, I recommend Blindsight by Peter Watts and the Bobiverse seri... | Recommendation | Recommendation | 0.27 | Yes |
| My recommendation would be Survivor by Chuck Palahniuk. I often suggest it to readers who ... | Recommendation | Recommendation | 0.27 | Yes |
| I recommend Iron Widow to readers who enjoy science fiction and strong character-driven st... | Recommendation | Literary_Analysis | 0.26 | No |
| The burden on Christian's back...ooohhhh so easy...In all seriousness - the turtle I suppo... | Literary_Analysis | Recommendation | 0.27 | No |

### Example Correct Prediction

The recommendation for *The Charioteer* was correctly classified because it explicitly uses recommendation language and clearly communicates that the author's purpose is suggesting a book to potential readers.

---

# Error Analysis

## Error 1

### Text

> I recommend Iron Widow to readers who enjoy science fiction and strong character-driven stories. The novel explores patriarchy while delivering an exciting plot.

### True Label

Recommendation

### Predicted Label

Literary_Analysis

### Explanation

The recommendation contains thematic discussion and social commentary. The phrase "explores patriarchy" resembles analytical language, causing the model to prioritize interpretation over recommendation intent.

---

## Error 2

### Text

> The burden on Christian's back... the turtle from Grapes of Wrath... the conch from Lord of the Flies...

### True Label

Literary_Analysis

### Predicted Label

Recommendation

### Explanation

The post references literary symbols but lacks explicit analytical keywords such as:

- symbolism
- theme
- interpretation
- motif

The absence of clear analytical language likely contributed to the error.

---

## Error 3

### Text

> House of Leaves is the only book that has ever given me nightmares... The footnotes function as a meta-textual device to deepen the horror.

### True Label

Review

### Predicted Label

Literary_Analysis

### Explanation

Although the author is sharing a reading experience, the discussion focuses heavily on literary techniques and textual structure. The post therefore resembles literary criticism.

---

# Error Pattern Analysis (Stretch Feature)

## Recommendation vs Literary_Analysis

Many recommendation posts contained thematic discussion.

Examples:

- Iron Widow
- We Need to Talk About Kevin

The model occasionally focused on thematic language rather than recommendation intent.

---

## Review vs Literary_Analysis

Some reviews contained substantial discussion of:

- symbolism
- narrative structure
- literary devices

These posts occasionally appeared closer to literary criticism than personal evaluation.

---

## Literary_Analysis vs Publishing_and_Book_Info

Some examples discussed books, authors, and literary history while also performing interpretation. The overlap occasionally created ambiguity.

---

## Conclusion

Most remaining errors did not stem from obvious misunderstandings. Instead, they occurred because multiple discourse styles frequently coexist within the same post.

---

# Confidence Analysis (Stretch Feature)

Correct predictions typically produced confidence values between:

```text
0.27 – 0.31
```

Incorrect predictions often produced confidence values within the same range.

This suggests that confidence scores were not well calibrated and that the model was sometimes confidently incorrect when category boundaries overlapped.

---

# Interactive Classifier Prototype (Stretch Feature)

A Gradio-based prototype interface was created to demonstrate how the trained model could be used in an interactive application.

Users can enter any book-related discussion post and receive:

- Predicted category
- Model confidence score

Supported categories:

- Recommendation
- Review
- Literary_Analysis
- Publishing_and_Book_Info

Screenshot:

```text
gradio_demo.png
```

This prototype serves as a proof-of-concept deployment for the classifier.

---

# AI Usage

## How AI Was Used

AI tools were used to:

- Generate difficult boundary examples
- Stress-test label definitions
- Suggest rewrites for ambiguous dataset examples
- Identify recurring error patterns
- Assist with interpretation of model failures

---

## AI Outputs That Were Modified or Rejected

Several AI-generated examples blurred the distinction between Recommendation and Review categories.

These examples were either rewritten manually or excluded entirely from the final dataset.

AI-generated labeling suggestions were reviewed manually before acceptance.

---

# Specification Reflection

One of the most important lessons from this project was that dataset and label quality mattered more than model architecture.

The project specification emphasized careful taxonomy design, and the training results confirmed this. Early dataset versions contained many examples that mixed recommendation and review language, making classification substantially harder.

The final implementation diverged slightly from the initial plan because dataset refinement produced larger performance gains than additional hyperparameter tuning.

This project reinforced the idea that high-quality labels and clear category definitions are often more important than selecting a more sophisticated model.

---

# Reflection

The final DistilBERT model achieved:

```text
70.0% test accuracy
21 correct predictions out of 30
```

Most remaining errors occurred in realistic edge cases where recommendation, review, and literary interpretation naturally overlap.

Future improvements could include:

- Expanding the dataset beyond 200 examples
- Refining category definitions
- Separating publishing news from literary trivia
- Adding multiple annotators to measure labeling agreement
- Improving confidence calibration
- Deploying the classifier as a publicly accessible web application

Overall, this project demonstrates how a transformer model can be trained to recognize distinct forms of book-related discourse while also highlighting the challenges of categorizing naturally occurring human discussion.

Demo Video: https://youtu.be/OG03BjKS1Xc?is=G9U1ihN9_b-sEhay
