import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.env import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL

def send_email(receiver_email, subject, msg):
    """
    Send an email using a simple SMTP relay without authentication.
    :param receiver_email: The recipient's email address.
    :param subject: The email subject.
    :param msg: The email body content.
    """
    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(msg, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
