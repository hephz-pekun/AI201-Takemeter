# AI201-Takemeter
# Book Discussion Classification with DistilBERT

## Project Overview

This project builds a text classification model for book-related discussions from Reddit's r/books community.

The goal is to classify posts into one of four discourse categories:

- Recommendation
- Review
- Literary_Analysis
- Publishing_and_Book_Info

A DistilBERT model was fine-tuned on a manually labeled dataset and compared against a zero-shot GPT-OSS baseline.

---

# Community

## Selected Community

r/books

r/books is one of Reddit's largest book-focused communities and contains a diverse set of discussions related to reading, literature, authors, and publishing.

This community was selected because it contains several naturally occurring discussion types that can be meaningfully classified.

Examples include:

- users recommending books
- users reviewing books
- literary analysis and interpretation
- publishing news and book information

These categories create a classification task with clear goals while still containing realistic ambiguity.

---

# Label Taxonomy

## Recommendation

Posts whose primary purpose is recommending, requesting, suggesting, or promoting books.

### Example

> I would recommend Georges Perec's Life: A User's Manual.

### Example

> Check out Piranesi. I think it's exactly what you're looking for.

---

## Review

Posts evaluating a book based on personal reading experience.

### Example

> Piranesi was fantastic. Ethereal, dream-like and mysterious.

### Example

> The Picture of Dorian Gray hooked me immediately.

---

## Literary_Analysis

Posts discussing symbolism, themes, interpretation, literary meaning, or author intent.

### Example

> The green light in The Great Gatsby symbolizes Gatsby's hopes and dreams.

### Example

> Frankenstein is primarily about the responsibility of a creator toward their creation.

---

## Publishing_and_Book_Info

Posts sharing factual information about books, authors, publishing history, releases, literary trivia, awards, or adaptations.

### Example

> Stephen King originally threw the Carrie manuscript in the trash.

### Example

> Blacktail by Scott Hawkins released today.

---

# Dataset

## Source

Data was collected manually from public r/books discussion threads.

## Dataset Size

Total examples:

```
200
```

## Label Distribution

| Label | Count |
|---------|---------|
| Recommendation | 50 |
| Review | 50 |
| Literary_Analysis | 50 |
| Publishing_and_Book_Info | 50 |

The dataset was intentionally balanced to reduce bias toward any single class.

---

# Data Split

The dataset was split using stratified sampling.

| Split | Size |
|---------|---------|
| Train | 140 |
| Validation | 30 |
| Test | 30 |

---

# Baseline Model

## Model

GPT-OSS-20B (Zero-Shot Classification)

The baseline model was provided with label definitions and asked to classify each post without additional training.

## Results

| Metric | Value |
|---------|---------|
| Accuracy | 0.233 |

### Observations

The baseline heavily favored the Review category and frequently predicted Review regardless of input category.

This resulted in:

- High recall for Review
- Extremely poor performance for all other labels

The baseline struggled to distinguish between recommendation, literary analysis, and informational posts without task-specific training.

---

# Fine-Tuned Model

## Model

distilbert-base-uncased

## Hyperparameters

```python
num_train_epochs = 3
learning_rate = 2e-5
train_batch_size = 16
weight_decay = 0.01
warmup_steps = 50
```

## Training Setup

The Hugging Face Trainer API was used for fine-tuning.

Inputs were tokenized using the DistilBERT tokenizer with truncation enabled and a maximum sequence length of 256 tokens.

---

# Evaluation Results

## Accuracy Comparison

| Model | Accuracy |
|---------|---------|
| GPT-OSS Zero-Shot Baseline | 0.233 |
| Fine-Tuned DistilBERT | 0.467 |

## Improvement

```
0.467 - 0.233 = 0.234
```

The fine-tuned model improved overall accuracy by approximately **23.4 percentage points** over the baseline.

---

# Confusion Matrix

confusion_matrix.png

The confusion matrix shows that the model performs best when identifying strongly defined categories and struggles most when label boundaries overlap.

---

# Sample Classifications

| Post (truncated) | True label | Predicted | Confidence | Correct? |
|---|---|---|---|---|
| The Charioteer by Mary Renault... | Recommendation | Recommendation | 0.26 | Yes |
| Chuck Palahniuk's Survivor would be my recommendation. | Recommendation | Recommendation | 0.26 | Yes |
| The Expanse started off as a tabletop RPG... | Publishing_and_Book_Info | Publishing_and_Book_Info | 0.28 | Yes |
| Blindsight by Peter Watts and the Bobiverse series... | Recommendation | Publishing_and_Book_Info | 0.27 | No |
| Iron Widow is really good... | Recommendation | Publishing_and_Book_Info | 0.28 | No |

### Example Correct Prediction

"The Charioteer by Mary Renault..." was correctly classified as Recommendation because the primary purpose of the post is suggesting a book to other readers.

---

# Error Analysis

## Error 1

### Text

> Blindsight by Peter Watts and the Bobiverse series by Dennis E Taylor if you're in the sci-fi subs.

### True Label

Recommendation

### Predicted Label

Publishing_and_Book_Info

### Why It Failed

The post is extremely short and lacks explicit recommendation language such as "I recommend" or "you should read."

The model likely focused on the named entities and interpreted the post as informational.

---

## Error 2

### Text

> The brook trout at the end of The Road. They quite clearly represent a beautiful world destroyed by mankind.

### True Label

Literary_Analysis

### Predicted Label

Review

### Why It Failed

The post discusses symbolism, but it also contains evaluative language.

The boundary between literary interpretation and opinion-based discussion is difficult.

---

## Error 3

### Text

> Iron Widow is really good...

### True Label

Recommendation

### Predicted Label

Publishing_and_Book_Info

### Why It Failed

Many recommendation examples contain opinion language that resembles reviews.

This overlap between recommendation and review-style discourse confused the classifier.

---

# Common Failure Patterns

## Recommendation vs Review

This was the most common source of confusion.

Many recommendation posts include personal opinions:

> Dune is a masterpiece.

while many reviews implicitly recommend books:

> I loved this book and couldn't put it down.

As a result, the categories share significant vocabulary.

---

## Recommendation vs Publishing_and_Book_Info

Some recommendation examples consist only of a title and author name.

Without surrounding context, these posts can appear informational rather than recommendatory.

---

## Broad Information Category

Publishing_and_Book_Info includes:

- release announcements
- author information
- publishing history
- literary trivia

This broad category likely reduced consistency within the class and contributed to classification errors.

---

# AI Usage

## Label Stress Testing

AI was used to generate hypothetical borderline examples between:

- Recommendation and Review
- Review and Literary_Analysis
- Recommendation and Publishing_and_Book_Info

This helped refine label definitions before finalizing the dataset.

---

## Annotation Assistance

AI was not used to create the final labels.

All examples in the training dataset were manually reviewed and labeled.

---

## Failure Analysis

AI was used after evaluation to help identify patterns in classification mistakes and suggest explanations for common sources of model confusion.

All conclusions were manually reviewed before inclusion in the report.

---

# Reflection

This project demonstrated that creating a good label taxonomy is often more difficult than training the model itself.

The largest challenge was defining boundaries between Recommendation and Review because real-world Reddit posts frequently contain characteristics of both categories.

Although the fine-tuned model achieved only moderate performance, it substantially outperformed the zero-shot baseline and learned meaningful distinctions between discourse types. The remaining errors largely reflect ambiguity present in the dataset rather than obvious model failures.

Future improvements could include:

- collecting additional examples
- refining label boundaries
- separating publishing news from literary trivia
- increasing the amount of training data for each label

Overall, the project successfully demonstrated that fine-tuning a language model on a community-specific dataset improves performance over a zero-shot baseline.