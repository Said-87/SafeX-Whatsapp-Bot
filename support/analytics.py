"""
Analytics Module
Logs chats and provides dashboard statistics.
"""

import csv
import os
from collections import Counter
from datetime import datetime

import pandas as pd

from config import ANALYTICS_FILE


class Analytics:

    HEADERS = [
        "timestamp",
        "message",
        "reply",
        "status"
    ]

    def __init__(self, file_path=ANALYTICS_FILE):
        self.file_path = file_path
        self._initialize()

    def _initialize(self):
        """
        Create analytics CSV if it doesn't exist.
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

    def log_chat(
        self,
        message,
        reply,
        status
    ):
        """
        Save a chat record.
        """

        with open(
            self.file_path,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                message,
                reply,
                status
            ])

    def load_data(self):
        """
        Load analytics CSV.
        """

        try:

            return pd.read_csv(self.file_path)

        except Exception:

            return pd.DataFrame(
                columns=self.HEADERS
            )

    def total_chats(self):

        return len(self.load_data())

    def successful_chats(self):

        df = self.load_data()

        if df.empty:
            return 0

        return len(
            df[df["status"] == "Success"]
        )

    def escalated_chats(self):

        df = self.load_data()

        if df.empty:
            return 0

        return len(
            df[df["status"] == "Escalated"]
        )

    def success_rate(self):

        total = self.total_chats()

        if total == 0:
            return 0

        return round(
            (self.successful_chats() / total) * 100,
            2
        )

    def escalation_rate(self):

        total = self.total_chats()

        if total == 0:
            return 0

        return round(
            (self.escalated_chats() / total) * 100,
            2
        )

    def top_queries(self, limit=5):

        df = self.load_data()

        if df.empty:
            return pd.DataFrame(
                columns=["Message", "Count"]
            )

        counter = Counter(df["message"])

        data = counter.most_common(limit)

        return pd.DataFrame(
            data,
            columns=[
                "Message",
                "Count"
            ]
        )

    def recent_chats(self, limit=10):

        df = self.load_data()

        if df.empty:
            return df

        return df.tail(limit)

    def summary(self):

        return {

            "Total Chats":
                self.total_chats(),

            "Successful Chats":
                self.successful_chats(),

            "Escalated Chats":
                self.escalated_chats(),

            "Success Rate":
                self.success_rate(),

            "Escalation Rate":
                self.escalation_rate()
        }


analytics = Analytics()


# -----------------------------------
# Compatibility Functions
# -----------------------------------

def log_chat(
    message,
    reply,
    status
):
    analytics.log_chat(
        message,
        reply,
        status
    )


def load_analytics():
    return analytics.load_data()


def get_summary():
    return analytics.summary()


def top_queries():
    return analytics.top_queries()