```mermaid
classDiagram

class Summarizer {
    - sentence_scores
    - word_frequencies

    + split_sentences(text)
    + preprocess_text(text)
    + compute_word_frequencies(tokens)
    + score_sentences(sentences)
    + select_top_sentences(sentence_scores)
    + generate_summary(text)
}
```
