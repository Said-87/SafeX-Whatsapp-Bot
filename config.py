"""
Configuration file for SafeX WhatsApp Bot
"""

import os

# ----------------------------------------
# Base Directory
# ----------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------
# Data Directory
# ----------------------------------------

DATA_DIR = os.path.join(BASE_DIR, "data")

FAQ_FILE = os.path.join(DATA_DIR, "faq.csv")
LEADS_FILE = os.path.join(DATA_DIR, "leads.csv")
ANALYTICS_FILE = os.path.join(DATA_DIR, "analytics.csv")

# ----------------------------------------
# Flask
# ----------------------------------------

SECRET_KEY = "safex-secret-key"

DEBUG = True

HOST = "127.0.0.1"

PORT = 5000

# ----------------------------------------
# Languages
# ----------------------------------------

DEFAULT_LANGUAGE = "en"

SUPPORTED_LANGUAGES = [
    "en",
    "ur"
]

# ----------------------------------------
# Lead Keywords
# ----------------------------------------

LEAD_KEYWORDS = [

    "contact",

    "contact sales",

    "contact you",

    "quotation",

    "quote",

    "hire",

    "service",

    "services",

    "project",

    "internship",

    "course",

    "consultation",

    "meeting",

    "call me",

    "i am interested",

    "i'm interested",

    "book consultation",

    "talk to sales",

    "pricing"
]