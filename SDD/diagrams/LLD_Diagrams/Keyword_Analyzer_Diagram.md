```mermaid
classDiagram

class KeywordAnalyzer {
    - keyword_frequencies

    + preprocess_text(text)
    + count_word_frequencies(tokens)
    + get_top_keywords(text)
}
```
