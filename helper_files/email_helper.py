
import os
import random
import requests
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")


# ---------------- OTP GENERATOR ----------------
def generate_otp(length=6):
    """Generate a numeric OTP"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


# ---------------- SEND OTP (RESEND) ----------------
def send_otp(to_email, otp):
    try:
        url = "https://api.resend.com/emails"

        headers = {
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "from": "onboarding@resend.dev",  # default test sender (no setup needed)
            "to": [to_email],
            "subject": "Your OTP for Password Manager",
            "html": f"""
                <h2>Your OTP is: {otp}</h2>
                <p>This OTP is valid for 10 minutes.</p>
                <br>
                <p>- Secure Password Manager</p>
            """
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return True
        else:
            print("❌ Resend Error:", response.text)
            return False

    except Exception as e:
        print("❌ Email sending failed:", e)
        return False