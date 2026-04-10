import re

class KeywordAnalyzer:
    """
    SDD_HLD_04_01_KEY :: SDD_HLD_KEY_001

    This class extracts important keywords from note text.

    The analyzer follows a simple rule-based NLP approach:
    1. Preprocess the text
    2. Normalize simple plural forms
    3. Remove common stopwords
    4. Count word frequencies
    5. Automatically choose a reasonable number of keywords
    6. Return the most frequent important words
    """

    def __init__(self):
        """
        Initialize the KeywordAnalyzer object.

        We define a basic stopword list so that very common words do not appear as keywords.
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
            "quickly",
            "also",
            "some",
            "may"
        }

    def extract_keywords(self, text, num_keywords=None, debug=False):
        """
        SDD_TT_2_002 :: SDD_HLD_KEY_001 :: [SRD::T_18]

        Extract the most important keywords from the given text.

        Parameters:
            text (str): The full plaintext note content.
            num_keywords (int or None): Number of keywords to return.
                                        If None, the program chooses automatically.
            debug (bool): If True, print internal processing details.

        Returns:
            list: A list of the top keywords.
        """

        # Validate the text type
        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")

        # Validate the keyword count type only if the user provided one
        if num_keywords is not None:
            if not isinstance(num_keywords, int):
                raise TypeError("num_keywords must be an integer or None.")

        # Validate the debug type
        if not isinstance(debug, bool):
            raise TypeError("debug must be a boolean.")

        # Remove leading and trailing whitespace
        text = text.strip()

        # Return an empty list if the text is empty
        if len(text) == 0:
            return []

        # Preprocess the text into filtered words
        words = self._preprocess_words(text)

        if debug:
            print("\n--- PREPROCESSED WORDS ---")
            print(words)

        # If no valid words remain, return an empty list
        if len(words) == 0:
            return []

        # Build the word frequency dictionary
        word_frequencies = self._build_word_frequency(words)

        if debug:
            print("\n--- WORD FREQUENCIES ---")
            for word, count in sorted(word_frequencies.items()):
                print(f"{word}: {count}")

        # If num_keywords was not provided, determine it automatically
        if num_keywords is None:
            num_keywords = self._determine_keyword_count(
                total_words=len(words),
                unique_words=len(word_frequencies)
            )

        # If the user provided num_keywords manually make sure it is at least 1
        if num_keywords < 1:
            num_keywords = 1

        if debug:
            print(f"\nChosen keyword count: {num_keywords}")

        # Separate repeated words from single-occurrence words
        # This lets us prioritize stronger repeated keywords first
        repeated_words = []
        single_words = []

        for word, count in word_frequencies.items():
            if count >= 2:
                repeated_words.append((word, count))
            else:
                single_words.append((word, count))

        # Sort repeated words by:
        # 1. frequency descending
        # 2. alphabetical order ascending
        repeated_words.sort(key=lambda item: (-item[1], item[0]))

        # Sort single-occurrence words alphabetically.
        single_words.sort(key=lambda item: item[0])

        # Combine both lists, prioritizing repeated words first.
        ranked_words = repeated_words + single_words

        if debug:
            print("\n--- RANKED KEYWORDS ---")
            for word, count in ranked_words:
                print(f"{word}: {count}")

        # Keep only the words, not the counts.
        selected_keywords = []

        for word, count in ranked_words[:num_keywords]:
            selected_keywords.append(word)

        if debug:
            print("\n--- SELECTED KEYWORDS ---")
            print(selected_keywords)

        return selected_keywords

    def _preprocess_words(self, text):
        """
        SDD_TT_2_004 :: SDD_HLD_KEY_001
        
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
        SDD_TT_2_004 :: SDD_HLD_KEY_001

        Normalize a word into a simpler base form.

        This is a small rule-based normalization step.
        It mainly helps combine simple plural and singular forms
        without damaging common singular words that naturally end in "s".
        """

        # Convert words ending in "ies" to "y".
        # Example: "libraries" -> "library"
        if len(word) > 3:
            if word.endswith("ies"):
                return word[:-3] + "y"

        # Do not remove the final "s" from words that commonly
        # end in "s" even when singular.
        protected_s_endings = ("ss", "is", "us")

        for ending in protected_s_endings:
            if word.endswith(ending):
                return word

        # Remove a final "s" for simple plural forms.
        # Example: "users" -> "user"
        # Example: "notes" -> "note"
        if len(word) > 3:
            if word.endswith("s"):
                return word[:-1]

        return word

    def _build_word_frequency(self, words):
        """
        SDD_TT_2_004 :: SDD_HLD_KEY_001

        Build a dictionary of word frequencies.

        Returns:
            dict: Maps each word to its number of occurrences.
        """

        frequency = {}

        for word in words:
            if word in frequency:
                frequency[word] += 1
            else:
                frequency[word] = 1

        return frequency

    def _determine_keyword_count(self, total_words, unique_words):
        """
        SDD_TT_2_004 :: SDD_HLD_KEY_001

        Automatically determine a reasonable number of keywords based on the size of the note.

        Parameters:
            total_words (int): Number of processed words in the note.
            unique_words (int): Number of unique important words.

        Returns:
            int: Number of keywords to return.
        """

        if total_words <= 10:
            keyword_count = 3
        elif total_words <= 25:
            keyword_count = 5
        elif total_words <= 50:
            keyword_count = 6
        elif total_words <= 100:
            keyword_count = 7
        else:
            keyword_count = 8

        # Never ask for more keywords than exist.
        if keyword_count > unique_words:
            keyword_count = unique_words

        return keyword_count