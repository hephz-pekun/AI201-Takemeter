# Planning Document – Book Discussion Classification

## Community

For this project, I selected the Reddit community **r/books**. This community is one of the largest book-focused discussion forums online and contains a wide variety of text-heavy posts and comments. Members regularly discuss books they have read, recommend books to others, analyze literary themes and symbolism, and share information about authors, publishing, and upcoming releases.

This community is a strong candidate for a classification task because the different types of discussions are common, meaningful to readers, and often have recognizable linguistic patterns. For example, recommendation posts frequently contain phrases such as "I recommend" or "you should read," while literary analysis posts focus on interpretation, symbolism, and themes. These distinctions create a realistic classification problem while still presenting challenging edge cases.

---

## Labels

### 1. Recommendation

**Definition:** Posts or comments whose primary purpose is to suggest, request, or promote books for someone to read.

**Example 1**
> "I would recommend Georges Perec's Life: A User's Manual."

**Example 2**
> "Check out Piranesi. I think it's exactly what you're asking for."

---

### 2. Review

**Definition:** Posts or comments evaluating a book based on personal reading experience, discussing its quality, strengths, weaknesses, or overall enjoyment.

**Example 1**
> "Piranesi was fantastic. Ethereal, dream-like and mysterious."

**Example 2**
> "The Picture of Dorian Gray. I was absolutely flabbergasted how hooked I was three pages in."

---

### 3. Literary_Analysis

**Definition:** Posts or comments that interpret themes, symbolism, character motivations, literary techniques, historical context, or deeper meaning within a work.

**Example 1**
> "The green light in The Great Gatsby represents Gatsby's hopes and dreams."

**Example 2**
> "Frankenstein is more about the responsibility of a creator to his creation than technology run amok."

---

### 4. Publishing_and_Book_Info

**Definition:** Posts or comments whose primary purpose is to share factual information about books, authors, publishing history, book releases, adaptations, awards, or literary trivia.

**Example 1**
> "Blacktail by Scott Hawkins released today."

**Example 2**
> "Stephen King threw the manuscript to Carrie in the trash before it was eventually published."

---

## Hard Edge Cases

### Edge Case 1: Recommendation vs Review

**Example**

> "Dune has such a good mix of sci-fi, religion, politics, and mystery. It's a masterpiece."

This post contains an evaluation of the book, but it is being presented as part of a recommendation.

**Decision Rule**

If the primary goal is convincing someone to read the book, label it **Recommendation**.

If the primary goal is evaluating the quality of a book already read, label it **Review**.

---

### Edge Case 2: Review vs Literary Analysis

**Example**

> "The symbolism in Dorian Gray helps demonstrate the dangers of aestheticism."

This discusses a literary theme while also expressing appreciation for the book.

**Decision Rule**

If the focus is interpreting meaning, themes, symbolism, or literary techniques, label it **Literary_Analysis**.

If the focus is judging whether the book is good or bad, label it **Review**.

---

### Edge Case 3: Publishing_and_Book_Info vs Recommendation

**Example**

> "A new Brandon Sanderson novel is releasing next month and I'm excited to read it."

**Decision Rule**

If the post mainly communicates factual information about a release, publication, adaptation, or author event, label it **Publishing_and_Book_Info**.

If the main purpose is encouraging readers to read the book, label it **Recommendation**.

---

## Data Collection Plan

### Source

Data will be collected from public posts and comments on r/books.

### Collection Method

Examples are collected manually and stored in a CSV file with the following columns:

```text
text,label