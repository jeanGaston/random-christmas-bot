from env import DRAW_PER_PERSON, HISTORY_YEARS, EMAIL_SUBJECT, EMAIL_BODY
from file_io import load_history, save_csv, load_participants
from draw import draw_names
from emailer import send_email
from utils import get_current_time
from datetime import date

def send_all_emails(new_draw):
    """Send the Secret Santa draw results to all participants via email."""
    current_year = date.today().year
    for participant in new_draw:
        name = participant[0]
        receiver_email = participant[1]
        draws = ", ".join(participant[2:])
        message = EMAIL_BODY.format(name=name, draws=draws)
        subject = EMAIL_SUBJECT.format(year=current_year)
        send_email(receiver_email, subject, message)
        print(f"Email sent to {name} ({receiver_email})")

if __name__ == "__main__":
    try:
        # Load data from historical CSVs and this year's participants
        history_data = load_history(HISTORY_YEARS)

        current_year = date.today().year
        current_participants = load_participants()  # Load participants data

        # Perform the draw
        new_draw = draw_names(current_participants, history_data, DRAW_PER_PERSON)
        # Send emails to participants
        send_all_emails(new_draw)

        # Save new draw results
        save_csv(new_draw, current_year)

        print(f"Process completed at {get_current_time()[1]} on {get_current_time()[0]}")

    except Exception as e:
        print(f"Error occurred: {e}")
