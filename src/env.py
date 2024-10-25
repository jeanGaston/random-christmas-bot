# Configuration file with SMTP settings and CSV path settings
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 25
SENDER_EMAIL = "santa@example.com"
CSV_PATH = r"path\to\your\csv\files" # Path to the CSV files
CSV_PREFIX = r"secret_santa_DB"  # Prefix for CSV files
HISTORY_YEARS = 2  # Number of past years to consider in the draw
DRAW_PER_PERSON = 2  # Number of recipients per person

# Email content
EMAIL_SUBJECT = "Secret Santa {year} Draw"
EMAIL_BODY = """
Hello {name},

You have been chosen to give gifts to: {draws}.
Feel free to use your imagination and make their Christmas magical!

Merry Christmas!

This email was sent automatically, please do not reply.
"""
