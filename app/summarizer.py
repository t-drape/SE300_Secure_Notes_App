import re

class Summarizer:
    """
    DD_HLD_04_01_SUM :: SDD_HLD_SUM_001

    This class generates an extractive summary from note text.

    The summarizer follows a simple rule-based NLP approach:
    1. Split the text into sentences
    2. Preprocess words
    3. Compute word frequencies
    4. Score each sentence
    5. Automatically choose a reasonable summary length
    6. Return the top-ranked sentences in original order
    """

    def __init__(self):
        """
        Initialize the Summarizer object.

        We define a basic set of stopwords so that very common
        words do not dominate the frequency calculations.
        """
        self.stopwords = {
            "a",
            "an",
            "and",
            "are",
            "as",
            "at",
            "be",
            "but",
            "by",
            "for",
            "from",
            "has",
            "have",
            "he",
            "in",
            "is",
            "it",
            "its",
            "of",
            "on",
            "that",
            "the",
            "to",
            "was",
            "were",
            "will",
            "with",
            "i",
            "you",
            "your",
            "we",
            "they",
            "this",
            "these",
            "those",
            "or",
            "not",
            "can",
            "could",
            "should",
            "would",
            "my",
            "our",
            "their",
            "his",
            "her",
            "them",
            "me",
            "us",
            "more",
            "now",
            "still",
            "one",
            "most",
            "many",
            "very",
            "quickly"
        }

        # Minimum number of processed words a sentence should have so we consider it a good summary candidate
        self.minimum_sentence_length = 4

    def summarize(self, text, debug=False):
        """
        SDD_TT_2_003 :: SDD_HLD_SUM_001 :: [SRD::T_12]

        Generate a summary from the given text.

        Parameters:
            text (str): The full plaintext note content.
            debug (bool): If True, print internal processing details.

        Returns:
            str: A summary made of the highest-ranked sentences.
        """

        # Validate the text type
        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")

        # Validate the debug type
        if not isinstance(debug, bool):
            raise TypeError("debug must be a boolean.")

        # Remove leading and trailing whitespace
        text = text.strip()

        # If the text is empty, return an empty summary
        if len(text) == 0:
            return ""

        # Split the text into sentences
        sentences = self._split_into_sentences(text)

        # If no usable sentences were found, return empty output
        if len(sentences) == 0:
            return ""

        # Automatically determine how many sentences the summary should contain
        num_sentences = self._determine_summary_length(len(sentences))

        if debug:
            print("\n--- SENTENCES ---")
            for index, sentence in enumerate(sentences):
                print(f"{index}: {sentence}")

            print(f"\nChosen summary length: {num_sentences}")

        # If the text already has fewer or equal sentences than requested, return the full text as the summary
        if len(sentences) <= num_sentences:
            # Check if there is any meaningful content before returning
            all_words = self._build_word_frequency(sentences)
            if len(all_words) == 0:
                return ""
            return " ".join(sentences)

        # Build the word frequency dictionary
        word_frequencies = self._build_word_frequency(sentences)

        if debug:
            print("\n--- RAW WORD FREQUENCIES ---")
            for word, count in sorted(word_frequencies.items()):
                print(f"{word}: {count}")

        # If no important words are found, return empty
        if len(word_frequencies) == 0:
            return ""

        # Normalize the frequencies so the scores are more stable
        normalized_frequencies = self._normalize_frequencies(word_frequencies)

        if debug:
            print("\n--- NORMALIZED WORD FREQUENCIES ---")
            for word, score in sorted(normalized_frequencies.items()):
                print(f"{word}: {score:.3f}")

        # Score each sentence
        sentence_scores = self._score_sentences(sentences, normalized_frequencies)

        if debug:
            print("\n--- SENTENCE SCORES ---")
            for index, score in sentence_scores.items():
                print(f"{index}: {score:.3f} -> {sentences[index]}")

        # Select the best sentences
        top_sentences = self._select_top_sentences(sentences, sentence_scores, num_sentences)

        if len(top_sentences) == 0:
            return ""

        if debug:
            print("\n--- SELECTED SUMMARY SENTENCES ---")
            for sentence in top_sentences:
                print(sentence)

        # Join them into one final summary string
        summary = " ".join(top_sentences)

        return summary

    def _split_into_sentences(self, text):
        """
        SDD_TT_2_003 :: SDD_HLD_SUM_001

        Split a block of text into sentences.

        We split on punctuation marks that usually end sentences:
        period .  exclamation mark !  and question mark ? and new lines 
        """

        raw_sentences = re.split(r'(?<=[.!?])\s+|\n+', text)

        sentences = []

        for sentence in raw_sentences:
            cleaned_sentence = sentence.strip()

            if len(cleaned_sentence) > 0:
                sentences.append(cleaned_sentence)

        return sentences

    def _preprocess_words(self, text):
        """
        SDD_TT_2_003 :: SDD_HLD_SUM_001

        Convert text into a cleaned list of words.

        Steps:
        - Convert to lowercase
        - Remove non-letter characters except spaces
        - Split into words
        - Normalize simple plural forms
        - Remove stopwords
        """

        text = text.lower()
        text = re.sub(r'[^a-z\s]', ' ', text)

        words = text.split()

        filtered_words = []

        for word in words:
            normalized_word = self._normalize_word(word)

            if normalized_word not in self.stopwords:
                filtered_words.append(normalized_word)

        return filtered_words

    def _normalize_word(self, word):
        """
        SDD_TT_2_003 :: SDD_HLD_SUM_001

        Normalize a word into a simpler base form.

        This is a small rule-based normalization step.
        It mainly helps combine simple plural and singular forms
        without damaging common singular words that naturally end in "s".
        """

        # Convert words ending in "ies" to "y"
        # Example: "libraries" -> "library"
        if len(word) > 3:
            if word.endswith("ies"):
                return word[:-3] + "y"

        # Do not remove the final "s" from words that commonly end in "s" even when singular
        protected_s_endings = ("ss", "is", "us")

        for ending in protected_s_endings:
            if word.endswith(ending):
                return word

        # Remove a final "s" for simple plural forms
        # Example: "users" -> "user"
        # Example: "notes" -> "note"
        if len(word) > 3:
            if word.endswith("s"):
                return word[:-1]
            
        return word

    def _build_word_frequency(self, sentences):
        """
        SDD_TT_2_003 :: SDD_HLD_SUM_001

        Build a dictionary of important word frequencies.

        Returns:
            dict: Maps each important word to its number of occurrences.
        """

        frequency = {}

        for sentence in sentences:
            words = self._preprocess_words(sentence)

            for word in words:
                if word in frequency:
                    frequency[word] += 1
                else:
                    frequency[word] = 1

        return frequency

    def _normalize_frequencies(self, word_frequencies):
        """
        SDD_TT_2_003 :: SDD_HLD_SUM_001

        Normalize word frequencies so all values fall between 0 and 1.

        Returns:
            dict: Maps each word to a normalized importance score.
        """

        if len(word_frequencies) == 0:
            return {}

        max_frequency = max(word_frequencies.values())

        normalized = {}

        for word, count in word_frequencies.items():
            normalized[word] = count / max_frequency

        return normalized

    def _score_sentences(self, sentences, word_frequencies):
        """
        SDD_TT_2_003 :: SDD_HLD_SUM_001

        Score each sentence using important word frequencies.

        Returns:
            dict: Maps sentence index to sentence score.
        """

        scores = {}

        for index, sentence in enumerate(sentences):
            words = self._preprocess_words(sentence)

            # Reject very short sentences as weak summary candidates
            if len(words) < self.minimum_sentence_length:
                scores[index] = 0
                continue

            score = 0

            for word in words:
                if word in word_frequencies:
                    score += word_frequencies[word]

            # Normalize by processed sentence length
            scores[index] = score / len(words)

        return scores

    def _select_top_sentences(self, sentences, sentence_scores, num_sentences):
        """
        SDD_TT_2_003 :: SDD_HLD_SUM_001
        
        Select the highest-scoring sentences and restore original order.

        Returns:
            list: The chosen summary sentences.
        """

        # Keep only sentences with a meaningful score
        positive_score_indices = []

        for index, score in sentence_scores.items():
            if score > 0:
                positive_score_indices.append(index)

        # If no meaningful sentences exist, return an empty list
        if len(positive_score_indices) == 0:
            return []

        # Rank only the meaningful sentences
        ranked_indices = sorted(positive_score_indices, key=lambda index: sentence_scores[index], reverse=True)

        # Select up to the requested number of sentences
        selected_indices = ranked_indices[:num_sentences]

        # Restore original sentence order for readability
        selected_indices.sort()

        selected_sentences = []

        for index in selected_indices:
            selected_sentences.append(sentences[index])

        return selected_sentences

    def _determine_summary_length(self, total_sentences):
        """
        SDD_TT_2_003 :: SDD_HLD_SUM_001

        Automatically determine a reasonable number of summary sentences based on the length of the original note.

        Parameters:
            total_sentences (int): Total number of sentences in the note.

        Returns:
            int: Number of sentences to include in the summary.
        """

        if total_sentences <= 3:
            return 1

        if total_sentences <= 6:
            return 2

        if total_sentences <= 10:
            return 3

        summary_length = round(total_sentences * 0.3)

        if summary_length < 3:
            summary_length = 3

        if summary_length > 5:
            summary_length = 5

        return summary_length