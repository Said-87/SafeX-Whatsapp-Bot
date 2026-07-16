"""
Lead Capture Validation
"""

import re


class LeadValidator:

    PHONE_PATTERN = re.compile(r"^(03\d{9}|\+923\d{9})$")

    EMAIL_PATTERN = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    @staticmethod
    def clean_text(text):
        """
        Remove extra spaces.
        """

        if text is None:
            return ""

        return " ".join(text.strip().split())

    @classmethod
    def validate_name(cls, name):
        """
        Validate user name.
        """

        name = cls.clean_text(name)

        if len(name) < 2:
            return False

        if len(name) > 50:
            return False

        return bool(
            re.fullmatch(
                r"[A-Za-z ]+",
                name
            )
        )

    @classmethod
    def validate_phone(cls, phone):
        """
        Validate Pakistani phone numbers.

        Examples:
        03001234567
        +923001234567
        """

        phone = phone.replace(" ", "")

        return bool(
            cls.PHONE_PATTERN.fullmatch(phone)
        )

    @classmethod
    def validate_email(cls, email):
        """
        Validate email.
        """

        email = cls.clean_text(email)

        if email.lower() == "skip":
            return True

        return bool(
            cls.EMAIL_PATTERN.fullmatch(email)
        )


# -------------------------
# Wrapper Functions
# -------------------------

def validate_name(name):
    return LeadValidator.validate_name(name)


def validate_phone(phone):
    return LeadValidator.validate_phone(phone)


def validate_email(email):
    return LeadValidator.validate_email(email)