```mermaid
classDiagram

class AIProcessor {
    - summarizer
    - keyword_analyzer

    + summarize(note_text)
    + extract_keywords(note_text)
}

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

class KeywordAnalyzer {
    - keyword_frequencies

    + preprocess_text(text)
    + count_word_frequencies(tokens)
    + get_top_keywords(text)
}

AIProcessor --> Summarizer
AIProcessor --> KeywordAnalyzer
```
