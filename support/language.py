"""
Language Detection Module
Supports English and Urdu detection.
"""

from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0


class LanguageDetector:

    SUPPORTED = {
        "en": "English",
        "ur": "Urdu"
    }

    @staticmethod
    def contains_urdu(text):
        """
        Check if text contains Urdu script.
        """

        for ch in text:
            if "\u0600" <= ch <= "\u06FF":
                return True

        return False

    @classmethod
    def detect(cls, message):

        if not message:
            return "en"

        message = message.strip()

        if len(message) == 0:
            return "en"

        # Urdu Unicode detection
        if cls.contains_urdu(message):
            return "ur"

        try:

            language = detect(message)

            if language in cls.SUPPORTED:
                return language

        except LangDetectException:
            pass

        except Exception:
            pass

        return "en"

    @classmethod
    def language_name(cls, code):

        return cls.SUPPORTED.get(
            code.lower(),
            "English"
        )

    @classmethod
    def is_urdu(cls, message):

        return cls.detect(message) == "ur"

    @classmethod
    def is_english(cls, message):

        return cls.detect(message) == "en"


# ---------------------------------
# Wrapper Functions
# ---------------------------------

def detect_language(message):
    return LanguageDetector.detect(message)


def get_reply_language(code):
    return LanguageDetector.language_name(code)