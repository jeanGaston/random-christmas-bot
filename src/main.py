from config.env import CSV_FILE_PATH, DRAW_PER_PERSON, EMAIL_SUBJECT, EMAIL_BODY
from src.file_io import open_csv, save_csv
from src.draw import draw_names
from src.emailer import send_email
from src.utils import get_current_time
from datetime import date

def send_all_emails(new_draw):
    """Send the Secret Santa draw results to all participants via email."""
    current_year = date.today().year
    for participant in new_draw:
        name = participant[0]
        receiver_email = participant[1]
        draws = ", ".join(participant[2:])  # List of recipients
        message = EMAIL_BODY.format(name=name, draws=draws)
        subject = EMAIL_SUBJECT.format(year=current_year)
        send_email(receiver_email, subject, message)  # Send the email
        print(f"Email sent to {name} ({receiver_email})")

if __name__ == "__main__":
    try:
        # Load previous draw data
        old_draw = open_csv(CSV_FILE_PATH)

        # Perform new draw
        new_draw = draw_names(old_draw, DRAW_PER_PERSON)

        # Send emails to participants
        send_all_emails(new_draw)

        # Save new draw results
        save_csv(new_draw, CSV_FILE_PATH)

        # Output completion time
        print(f"Process completed at {get_current_time()[1]} on {get_current_time()[0]}")

    except Exception as e:
        print(f"Error occurred: {e}")
        # Retry or handle errors
