# helper_files/email_helper.py

import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

import random

def generate_otp(length=6):
    """Generate a numeric OTP of given length (default 6 digits)."""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def send_otp(to_email, otp):
    msg = EmailMessage()
    msg["Subject"] = "Your OTP for Password Manager"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg.set_content(f"Hello,\n\nYour OTP is: {otp}\nIt is valid for 10 minutes.\n\n- Password Manager")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("❌ Email sending failed:", e)
        return False
