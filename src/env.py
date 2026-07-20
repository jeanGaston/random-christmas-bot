# Configuration is loaded from environment variables (see .env.example),
# so no secrets need to live in this file or in version control.
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.example.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "25"))
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "santa@example.com")
CSV_PATH = os.environ.get("CSV_PATH", r"path\to\your\csv\files")  # Path to the CSV files
CSV_PREFIX = os.environ.get("CSV_PREFIX", "secret_santa_DB")  # Prefix for CSV files
HISTORY_YEARS = int(os.environ.get("HISTORY_YEARS", "2"))  # Number of past years to consider in the draw
DRAW_PER_PERSON = int(os.environ.get("DRAW_PER_PERSON", "2"))  # Number of recipients per person

# Web GUI basic-auth credentials (unset => auth disabled, see webapp/app.py)
WEBAPP_USERNAME = os.environ.get("WEBAPP_USERNAME")
WEBAPP_PASSWORD = os.environ.get("WEBAPP_PASSWORD")

# Email content
EMAIL_SUBJECT = os.environ.get("EMAIL_SUBJECT", "Secret Santa {year} Draw")
EMAIL_BODY = os.environ.get("EMAIL_BODY", """
Hello {name},

You have been chosen to give gifts to: {draws}.
Feel free to use your imagination and make their Christmas magical!

Merry Christmas!

This email was sent automatically, please do not reply.
""")
