from __summarizer import __summarizer
from keyword_analyzer import KeywordAnalyzer

class AIProcessor:
    """
    SDD_HLD_04_01_AI :: SDD_HLD_AI_001
    
    This class coordinates AI-based note analysis.

    Current supported analysis tasks:
    1. Summarization
    2. Keyword extraction
    """

    MAX_NOTE_SIZE_BYTES = 15 * 1024 * 1024  # 15MB — SRD::T_40

    def __init__(self):
        """
        Initialize the AIProcessor and create instances of the analysis submodules it will use.
        """
        self.__summarizer = __summarizer()
        self.keyword_analyzer = KeywordAnalyzer()

    def check_file_size(self, text):
        """
        SDD_TT_2_005 :: SDD_HLD_AI_001 :: [SRD::T_24, SRD::T_25, SRD::T_40]

        Verify the note is within the supported size limit before analysis.
        SDD_TT_2_005 :: [SRD::T_24, SRD::T_25, SRD::T_40]

        Parameters:
            text (str): The note content to check.

        Returns:
            bool: True if within limits, False if exceeded.
        """

        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")

        if len(text.encode("utf-8")) > self.MAX_NOTE_SIZE_BYTES:
            print("Note exceeds the maximum supported size for analysis (15MB).")
            return False
        return True


    def __summarize_note(self, text, debug=False):
        """
        SDD_TT_2_001 :: SDD_HLD_AI_001 :: [SRD::T_12]

        Generate a summary of the given note text.

        Parameters:
            text (str): Plaintext note content.
            debug (bool): If True, print internal processing details.

        Returns:
            str: The generated summary, or the original text if size limit is exceeded.
        """

        # Validate the text type
        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")

        # Validate the debug type
        if not isinstance(debug, bool):
            raise TypeError("debug must be a boolean.")

        # Check file size before processing
        # Per SDD __appendix: if size exceeded, display the original note
        if not self.check_file_size(text):
            return text

        # Delegate the work to the __summarizer submodule
        return self.__summarizer.__summarize(text, debug=debug)

    def extract_note_keywords(self, text, num_keywords=None, debug=False):
        """
        SDD_TT_2_002 :: SDD_HLD_AI_001 :: [SRD::T_18]
        
        Extract keywords from the given note text.

        Parameters:
            text (str): Plaintext note content.
            num_keywords (int or None): Number of keywords to return.
                                        If None, the analyzer chooses automatically.
            debug (bool): If True, print internal processing details.

        Returns:
            list: A list of extracted keywords, or an empty list if size limit is exceeded.
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

        # Check file size before processing
        if not self.check_file_size(text):
            return []

        # Delegate the work to the KeywordAnalyzer submodule
        return self.keyword_analyzer.extract_keywords(text, num_keywords=num_keywords, debug=debug)