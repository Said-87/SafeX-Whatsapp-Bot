"""
Response Formatter
Formats chatbot replies based on language.
"""


class ResponseFormatter:

    ENGLISH = {
        "prefix": "SafeX",
        "unknown": (
            "Sorry, I couldn't understand your question. "
            "I'm connecting you with a human representative."
        ),
        "welcome": (
            "Welcome to SafeX! How can I help you today?"
        ),
        "goodbye": (
            "Thank you for contacting SafeX. Have a great day!"
        ),
    }

    URDU = {
        "prefix": "SafeX",
        "unknown": (
            "معذرت، میں آپ کے سوال کو سمجھ نہیں سکا۔ "
            "میں آپ کو ہمارے نمائندے سے جوڑ رہا ہوں۔"
        ),
        "welcome": (
            "SafeX میں خوش آمدید! میں آپ کی کیسے مدد کر سکتا ہوں؟"
        ),
        "goodbye": (
            "SafeX سے رابطہ کرنے کا شکریہ۔ آپ کا دن خوشگوار گزرے۔"
        ),
    }

    @classmethod
    def get_language_pack(cls, language):

        if language.lower() == "ur":
            return cls.URDU

        return cls.ENGLISH


def format_reply(result, language="en"):
    """
    Format FAQ response.
    """

    pack = ResponseFormatter.get_language_pack(language)

    if result["status"] == "success":
        return f'{pack["prefix"]}: {result["reply"]}'

    return pack["unknown"]


def welcome_message(language="en"):

    pack = ResponseFormatter.get_language_pack(language)

    return pack["welcome"]


def goodbye_message(language="en"):

    pack = ResponseFormatter.get_language_pack(language)

    return pack["goodbye"]