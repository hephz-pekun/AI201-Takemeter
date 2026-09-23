# Book Discussion Classification with DistilBERT

## Project Overview

This project develops a machine learning classifier for book-related discussions from Reddit's **r/books** community.

The goal is to classify posts into one of four discourse categories:

- Recommendation
- Review
- Literary_Analysis
- Publishing_and_Book_Info

A fine-tuned DistilBERT model was trained on a manually labeled dataset and compared against a zero-shot GPT-OSS classification baseline.

---

# Community

## Selected Community

**r/books**

r/books is one of Reddit's largest book-focused communities and contains a diverse variety of discussions related to reading, literature, authors, and publishing.

This community was selected because it naturally contains several distinct forms of discourse:

- Book recommendations
- Reader reviews
- Literary interpretation and criticism
- Publishing facts and book news

These categories create a meaningful classification task while still presenting realistic ambiguity between labels.

---

# Label Taxonomy

## Recommendation

Posts primarily intended to suggest, recommend, request, or promote books to readers.

### Example

> I would recommend The Charioteer by Mary Renault, especially to readers interested in character-driven historical fiction.

### Example

> I strongly recommend Mistborn by Brandon Sanderson for readers who enjoy fantasy and creative magic systems.

---

## Review

Posts evaluating a book based on personal reading experience, enjoyment, strengths, weaknesses, or overall quality.

### Example

> I recently finished Piranesi and thought it was fantastic. The atmosphere kept me engaged from beginning to end.

### Example

> I thoroughly enjoyed Battle Royale and immediately reread it because I found the story so compelling.

---

## Literary_Analysis

Posts discussing symbolism, themes, motifs, allegories, interpretation, literary devices, or author intent.

### Example

> The green light in The Great Gatsby symbolizes Gatsby's hopes and dreams.

### Example

> Frankenstein is primarily concerned with a creator's responsibility toward a creation.

---

## Publishing_and_Book_Info

Posts sharing factual information about books, authors, publishing history, literary trivia, adaptations, releases, and awards.

### Example

> Stephen King originally discarded the Carrie manuscript before publication.

### Example

> Blacktail by Scott Hawkins was officially released today.

---

# Dataset

## Source

The dataset was manually collected and labeled from public discussions in **r/books**.

## Dataset Size

Total examples:

```text
200
```

## Label Distribution

| Label | Count |
|--------|--------|
| Recommendation | 50 |
| Review | 50 |
| Literary_Analysis | 50 |
| Publishing_and_Book_Info | 50 |

The dataset was intentionally balanced across all classes.

---

# Data Split

The dataset was split using stratified sampling.

| Split | Size |
|--------|--------|
| Training | 140 |
| Validation | 30 |
| Test | 30 |

This ensured all labels remained proportionally represented across the training, validation, and test sets.

---

# Baseline Model

## Model

GPT-OSS-20B

The baseline model used zero-shot prompting and was provided only with category definitions.

## Baseline Results

| Metric | Value |
|----------|----------|
| Parseable Responses | 22 / 30 |
| Accuracy | 90.9% |

### Important Note

The GPT-OSS baseline produced valid, parseable predictions for only 22 of the 30 test examples. Because 8 responses could not be parsed automatically into valid category labels, the baseline accuracy is not directly comparable to the fine-tuned model, which was evaluated on the entire test set.


### Baseline Classification Report

| Label | Precision | Recall | F1 |
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

## Training Hyperparameters

```python
num_train_epochs = 3
learning_rate = 2e-5
batch_size = 16
weight_decay = 0.01
warmup_steps = 50
```

## Training Process

The model was fine-tuned using Hugging Face Transformers.

All text was tokenized using the DistilBERT tokenizer with:

```python
max_length = 256
```

The Hugging Face Trainer API was used for training and evaluation.

---

# Fine-Tuned Model Results

## Test Set Performance

| Metric | Value |
|----------|----------|
| Test Examples | 30 |
| Correct Predictions | 21 |
| Wrong Predictions | 9 |
| Accuracy | 70.0% |

## Confusion Matrix

See:

```text
confusion_matrix.png
```

### Confusion Matrix Observations

The model performs strongest on Recommendation and Publishing_and_Book_Info examples.

Most remaining errors occur between:

- Recommendation and Literary_Analysis
- Review and Literary_Analysis

This suggests the greatest challenge comes from posts that combine recommendation language, interpretation, and personal evaluation.

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

The recommendation for *The Charioteer* was correctly classified because the post explicitly uses recommendation language and clearly signals that the author's primary purpose is suggesting a book to potential readers.

---

# Error Analysis

## Error 1

### Text

> I recommend Iron Widow to readers who enjoy science fiction and strong character-driven stories. The novel explores patriarchy while delivering an exciting plot.

### True Label

Recommendation

### Predicted Label

Literary_Analysis

### Why It Failed

The post's primary intent is recommendation, but the phrase:

> explores patriarchy

introduces thematic analysis language.

The model focused on interpretation rather than recommendation intent.

---

## Error 2

### Text

> The burden on Christian's back... the turtle from Grapes of Wrath... the conch from Lord of the Flies...

### True Label

Literary_Analysis

### Predicted Label

Recommendation

### Why It Failed

The example references several literary symbols but does not clearly contain words such as:

- symbolism
- theme
- interpretation
- motif

The lack of explicit analytical language likely confused the classifier.

---

## Error 3

### Text

> House of Leaves is the only book that has ever given me nightmares... The footnotes function as a meta-textual device to deepen the horror.

### True Label

Review

### Predicted Label

Literary_Analysis

### Why It Failed

Although the author is sharing a personal reaction, the discussion focuses heavily on literary techniques and textual structure. As a result, the post resembles literary criticism more than a traditional review.

---

# Common Failure Patterns

## Recommendation vs Literary_Analysis

Recommendation posts that discuss themes, symbolism, or social commentary are often confused with analysis posts.

Example:

> Iron Widow explores patriarchy while delivering an exciting plot.

The model frequently prioritized thematic discussion over recommendation intent.

---

## Review vs Literary_Analysis

Many reviews contain analysis-like language regarding:

- symbolism
- writing style
- worldbuilding
- narrative techniques

This causes certain reviews to resemble literary criticism.

---

## Short Literary Analysis Posts

Some Literary_Analysis examples are concise and rely on implied interpretation rather than explicit analytical vocabulary.

These posts are occasionally misclassified because the model receives fewer cues about the author's intent.

---

# Dataset Refinement

After the initial training run, multiple examples were rewritten to strengthen class-specific signals.

## Recommendation Example

Before:

```text
I recommend Maus.
```

After:

```text
I recommend Maus by Art Spiegelman because it combines graphic storytelling with an important historical narrative.
```

---

## Review Example

Before:

```text
The Terror. Sooo good.
```

After:

```text
I thought The Terror was excellent. The atmosphere and setting made it memorable.
```

---

## Literary_Analysis Example

Before:

```text
The cockroach in Metamorphosis by Kafka...
```

After:

```text
In Kafka's Metamorphosis, the cockroach symbolizes alienation and social rejection.
```

These modifications reduced ambiguity and significantly improved classification performance.

---

# AI Usage

## Label Stress Testing

AI tools were used to generate hypothetical edge cases between labels.

Examples focused on:

- Recommendation vs Review
- Review vs Literary_Analysis
- Recommendation vs Publishing_and_Book_Info

This helped refine classification boundaries.

---

## Annotation Assistance

AI was **not used** to create the final labels.

All dataset examples were manually reviewed and labeled before inclusion in the training set.

---

## Failure Analysis

AI tools were used after training to identify trends in classification errors and provide hypotheses regarding common failure patterns.

All interpretations included in this report were manually reviewed.

---

# Reflection

The most important lesson from this project is that label design is often as important as model selection.

Initial training runs revealed substantial overlap between Recommendation and Review examples. Many recommendation posts contained personal opinions, while many reviews implicitly encouraged readers to pick up a book.

Refining ambiguous examples improved classifier performance and reduced several common sources of confusion.

The final DistilBERT model achieved:

```text
70.0% accuracy
21 / 30 correct predictions
```

on the complete test set.

Most remaining errors occurred in realistic edge cases where recommendations, reviews, and literary analysis naturally overlap.

Future improvements could include:

- Expanding the dataset beyond 200 examples
- Further refining category definitions
- Splitting Publishing_and_Book_Info into narrower subcategories
- Introducing multiple human annotators to measure agreement

Overall, the project demonstrates that fine-tuning a transformer model on a community-specific taxonomy can successfully classify several distinct forms of book-related discourse while also revealing the challenges of categorizing naturally occurring human discussion.

# Stretch Feature: Error Pattern Analysis

## Error Categories

The model's nine remaining errors primarily fell into three categories:

### Recommendation vs Literary_Analysis

Examples:

- Iron Widow
- The burden on Christian's back

These examples contained both recommendation signals and thematic discussion.

### Review vs Literary_Analysis

Examples:

- House of Leaves

These posts discussed literary techniques while simultaneously evaluating the book.

### Literary_Analysis vs Publishing_and_Book_Info

Examples:

- The brook trout at the end of The Road

These posts were shorter and occasionally lacked explicit analytical language.

## Conclusion

Most remaining errors occurred because multiple discourse styles were present within the same post rather than because the model failed to understand the content.
