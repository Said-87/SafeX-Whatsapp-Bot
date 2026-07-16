"""
CRM Module
Stores and manages leads in a CSV file.
"""

import csv
import os
from datetime import datetime

from config import LEADS_FILE


class CRM:

    HEADERS = [
        "name",
        "phone",
        "email",
        "interest",
        "status",
        "created_at"
    ]

    def __init__(self, file_path=LEADS_FILE):
        self.file_path = file_path
        self._initialize()

    def _initialize(self):
        """
        Create the CSV file if it doesn't exist.
        """

        os.makedirs(
            os.path.dirname(self.file_path),
            exist_ok=True
        )

        if not os.path.exists(self.file_path):

            with open(
                self.file_path,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)
                writer.writerow(self.HEADERS)

    def lead_exists(self, phone, email):

        with open(
            self.file_path,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                if row["phone"] == phone:
                    return True

                if (
                    email.lower() != "skip"
                    and row["email"].lower() == email.lower()
                ):
                    return True

        return False

    def save(
        self,
        name,
        phone,
        email,
        interest
    ):

        if self.lead_exists(phone, email):
            return "Lead already exists."

        with open(
            self.file_path,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                name,
                phone,
                email,
                interest,
                "New",
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            ])

        return "Lead saved successfully."

    def get_all(self):

        with open(
            self.file_path,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            return list(reader)

    def total_leads(self):

        return len(self.get_all())

    def latest_leads(self, limit=5):

        leads = self.get_all()

        return leads[-limit:]


crm = CRM()


# -------------------------
# Compatibility Function
# -------------------------

def save_lead(
    name,
    phone,
    email,
    interest
):
    """
    Used by app.py
    """

    return crm.save(
        name,
        phone,
        email,
        interest
    )