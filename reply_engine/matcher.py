"""
Smart FAQ Matcher
"""

import re
from difflib import SequenceMatcher

from reply_engine.faq_loader import FAQLoader


class FAQMatcher:

    def __init__(self):

        self.faqs = FAQLoader().get_faqs()

        self.synonyms = {

            "price": ["pricing", "cost", "charges", "quote", "quotation", "budget", "fee"],

            "service": ["services", "solution", "solutions", "development"],

            "internship": ["intern", "career", "job", "vacancy", "hiring", "apply"],

            "contact": ["phone", "email", "address", "location"],

            "website": ["web", "webapp", "portal", "site"],

            "ai": ["artificial", "machine", "ml", "automation"],

            "course": ["training", "bootcamp", "class"],

            "hello": ["hi", "hey", "assalam", "salam", "good", "morning", "afternoon", "evening"],

            "thanks": ["thank", "thankyou", "thx"]
        }

    # --------------------------------------------------

    def preprocess(self, text):

        text = text.lower()

        text = re.sub(r"[^a-z0-9\s]", " ", text)

        words = text.split()

        expanded = []

        for word in words:

            expanded.append(word)

            for key, values in self.synonyms.items():

                if word == key or word in values:

                    expanded.append(key)

        return set(expanded)

    # --------------------------------------------------

    def keyword_set(self, keywords):

        return {

            k.strip().lower()

            for k in keywords.split(",")

            if k.strip()

        }

    # --------------------------------------------------

    def similarity(self, a, b):

        return SequenceMatcher(

            None,

            a,

            b

        ).ratio()

    # --------------------------------------------------

    def get_reply(self, message):

        text = message.lower().strip()

        # ---------------- Greetings ----------------

        greetings = [

            "hi",

            "hello",

            "hey",

            "assalam",

            "salam",

            "good morning",

            "good evening"

        ]

        if any(g in text for g in greetings):

            return {

                "status": "success",

                "reply": (

                    "Hello! 👋 Welcome to SafeX Solutions.\n\n"

                    "How can I help you today?\n\n"

                    "You can ask about:\n"

                    "• Services\n"

                    "• Pricing\n"

                    "• Internship\n"

                    "• Contact\n"

                    "• AI Solutions"

                ),

                "category": "Greeting",

                "confidence": 1.0

            }

        # ---------------- Thanks ----------------

        thanks = [

            "thanks",

            "thank you",

            "thx"

        ]

        if any(t in text for t in thanks):

            return {

                "status": "success",

                "reply": (

                    "You're welcome! 😊\n\n"

                    "If you have any other questions, "

                    "I'm always here to help."

                ),

                "category": "Thanks",

                "confidence": 1.0

            }

        # ---------------- Bye ----------------

        goodbye = [

            "bye",

            "goodbye",

            "see you"

        ]

        if any(x in text for x in goodbye):

            return {

                "status": "success",

                "reply": (

                    "Thank you for contacting SafeX.\n\n"

                    "Have a wonderful day! 👋"

                ),

                "category": "Goodbye",

                "confidence": 1.0

            }

        # ------------------------------------------------

        message_words = self.preprocess(message)

        best_match = None

        best_score = 0

        for _, row in self.faqs.iterrows():

            faq_keywords = self.keyword_set(row["keywords"])

            score = 0

            # keyword match

            score += len(

                message_words.intersection(faq_keywords)

            ) * 2

            # fuzzy match

            for user_word in message_words:

                for faq_word in faq_keywords:

                    if self.similarity(user_word, faq_word) > 0.85:

                        score += 1

            if score > best_score:

                best_score = score

                best_match = row

        if best_match is None or best_score == 0:

            return {

                "status": "not_found",

                "reply": (

                    "I'm sorry, I couldn't find an answer to your question.\n\n"

                    "Please ask about:\n"

                    "• Services\n"

                    "• Pricing\n"

                    "• Internship\n"

                    "• Contact\n"

                    "Or I'll connect you with our team."

                ),

                "category": "Unknown",

                "confidence": 0.0

            }

        confidence = min(

            round(best_score / 6, 2),

            1.0

        )

        return {

            "status": "success",

            "reply": best_match["answer"],

            "category": best_match["category"],

            "confidence": confidence

        }