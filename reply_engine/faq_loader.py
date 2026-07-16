"""
FAQ Loader
Loads and validates the FAQ dataset.
"""

import os
import pandas as pd

from config import FAQ_FILE


class FAQLoader:
    """
    Loads FAQ data from CSV and performs basic validation.
    """

    REQUIRED_COLUMNS = [
        "keywords",
        "answer",
        "category"
    ]

    def __init__(self, file_path=FAQ_FILE):
        self.file_path = file_path
        self.faq_data = self._load()

    def _load(self):
        """
        Load FAQ CSV.
        """

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(
                f"FAQ file not found:\n{self.file_path}"
            )

        try:
            df = pd.read_csv(self.file_path)

        except Exception as e:
            raise Exception(f"Unable to read FAQ file.\n{e}")

        # Remove completely empty rows
        df = df.dropna(how="all")

        # Validate columns
        missing = [
            col for col in self.REQUIRED_COLUMNS
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing columns in faq.csv: {missing}"
            )

        # Remove rows with missing values
        df = df.dropna(
            subset=self.REQUIRED_COLUMNS
        )

        # Convert to string
        for column in self.REQUIRED_COLUMNS:
            df[column] = df[column].astype(str).str.strip()

        # Remove duplicate FAQs
        df = df.drop_duplicates(
            subset=["keywords", "answer"]
        )

        df.reset_index(
            drop=True,
            inplace=True
        )

        return df

    def get_faqs(self):
        """
        Return FAQ dataframe.
        """
        return self.faq_data.copy()

    def total_questions(self):
        return len(self.faq_data)

    def categories(self):
        return sorted(
            self.faq_data["category"].unique().tolist()
        )