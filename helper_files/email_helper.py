import os
import sys
import random
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER", "").strip()
EMAIL_PASS = os.getenv("EMAIL_PASS", "").strip()
DEV_MODE   = not (EMAIL_USER and EMAIL_PASS)


# ---------------- OTP GENERATOR ----------------
def generate_otp(length=6):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


# ---------------- TERMINAL PRINT ----------------
def _print_otp(to_email, otp):
    """Always-visible terminal output, flushed immediately."""
    msg = (
        f"\n{'='*55}\n"
        f"  OTP for {to_email}  →  {otp}\n"
        f"{'='*55}\n"
    )
    print(msg, flush=True)
    sys.stdout.flush()


# ---------------- SEND OTP ----------------
def send_otp(to_email, otp):
    """
    Try Gmail SMTP first. If that fails (wrong creds, network block, etc.),
    always fall through to printing the OTP in the terminal so the app
    never gets stuck.
    """
    # ── Dev mode: no credentials configured ──────────────────────────────────
    if DEV_MODE:
        _print_otp(to_email, otp)
        return True

    # ── Try Gmail SMTP SSL (port 465) ─────────────────────────────────────────
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Your OTP – Password Manager"
        msg["From"]    = EMAIL_USER
        msg["To"]      = to_email

        html_body = f"""
        <html><body>
          <h2>Your One-Time Password</h2>
          <p style="font-size:32px;font-weight:bold;letter-spacing:6px">{otp}</p>
          <p>Valid for 10 minutes. Do not share it with anyone.</p>
          <p>— Secure Password Manager</p>
        </body></html>
        """
        msg.attach(MIMEText(html_body, "html"))

        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx, timeout=10) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())

        print(f"[EMAIL] OTP sent to {to_email}", flush=True)
        return True

    except smtplib.SMTPAuthenticationError:
        print(
            "\n[EMAIL ERROR] Gmail authentication failed.\n"
            "  Make sure EMAIL_PASS is a Gmail App Password, not your account password.\n"
            "  Generate one at: https://myaccount.google.com/apppasswords\n",
            flush=True
        )

    except smtplib.SMTPException as e:
        print(f"\n[EMAIL ERROR] SMTP error: {e}\n", flush=True)

    except OSError as e:
        print(f"\n[EMAIL ERROR] Network unreachable (port 465 blocked?): {e}\n", flush=True)

    except Exception as e:
        print(f"\n[EMAIL ERROR] Unexpected error: {e}\n", flush=True)

    # ── Fallback: always print to terminal so user can proceed ────────────────
    print("[EMAIL] Falling back to terminal output.", flush=True)
    _print_otp(to_email, otp)
    return False