SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 25
SENDER_EMAIL = "santa@example.com"
CSV_FILE_PATH = r"secret_santa_DB.csv"
DRAW_PER_PERSON = 2  # Choose 1 or 2 recipients per person

# Email content
EMAIL_SUBJECT = "Secret Santa {year} Draw"
EMAIL_BODY = """
Hello {name},

You have been chosen to give gifts to: {draws}.
Feel free to use your imagination and make their Christmas magical!

Merry Christmas!

This email was sent automatically, please do not reply.
"""