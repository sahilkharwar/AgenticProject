import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_medication_email(
    receiver_email,
    medicine,
    dosage
):

    msg = EmailMessage()

    msg["Subject"] = "Medication Reminder"

    msg["From"] = EMAIL

    msg["To"] = receiver_email

    msg.set_content(
        f"""
Time to take your medication.

Medicine: {medicine}
Dosage: {dosage}

Stay healthy.
"""
    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            EMAIL,
            EMAIL_PASSWORD
        )

        smtp.send_message(msg)