# 🔐 Password Manager

A secure, self-hosted password manager built with Flask and SQLAlchemy. Passwords are encrypted in the database using per-user Fernet keys derived from your master password — the server never sees your plaintext passwords.

---

## Features

- Register / Login with OTP email verification
- Per-user AES encryption (Fernet) for stored passwords
- Add, edit, delete vault entries
- Password generator
- Forgot password flow via OTP
- Search your vault
- Works with SQLite (local) or PostgreSQL (Neon / any provider)

---

## Local Setup

### Prerequisites

- Python 3.10+
- pip

### 1. Clone / unzip the project

```bash
cd password_manager
```

### 2. Create a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```


Fill in your `.env`:

```env
FLASK_SECRET_KEY=any-random-secret-string
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
EMAIL_USER=you@gmail.com
EMAIL_PASS=xxxx xxxx xxxx xxxx
```

### 4. Run the app

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

---

## Email — Gmail SMTP

OTPs are sent via **Gmail SMTP** using a Google App Password.

`EMAIL_PASS` must be a **Gmail App Password**, not your regular Gmail password.

**How to generate a Gmail App Password:**
1. Go to [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Sign in and select **"Mail"** + your device
3. Copy the 16-character password (spaces included) into `EMAIL_PASS`

> If `EMAIL_USER` or `EMAIL_PASS` are missing, the app falls back to **dev mode**: OTPs print to the terminal instead of being emailed.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `FLASK_SECRET_KEY` | Yes | Random string used to sign sessions |
| `DATABASE_URL` | Yes | PostgreSQL or SQLite connection string |
| `EMAIL_USER` | Yes | Gmail address used to send OTPs |
| `EMAIL_PASS` | Yes | Gmail App Password (16 chars, spaces OK) |

---

## Database Options

### PostgreSQL / Neon (recommended)

```env
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
```

Tables are created automatically on first run — no manual migration needed.

### SQLite (quick local testing)

```env
DATABASE_URL=sqlite:///passwords.db
```

The `passwords.db` file is created in the project root automatically.

---

## Project Structure

```
password_manager/
├── app.py                  # Flask routes and application entry point
├── init_db.py              # One-time DB initialisation script (optional)
├── requirements.txt        # Python dependencies
├── .env                    # Your local config (do not commit to git)
├── .env.example            # Template for environment variables
├── Procfile                # Production deployment (Heroku / Railway)
├── helper_files/
│   ├── db.py               # SQLAlchemy models and DB helper functions
│   ├── email_helper.py     # OTP generation and Gmail SMTP sending
│   ├── passgenerator.py    # Random password generator
│   ├── secure_helper.py    # Hashing, Fernet encryption/decryption
│   └── strength_checker.py # Password strength scoring
├── templates/
│   └── *.html
└── static/
    └── style.css
```

---

## Security Notes

- Master passwords are hashed with bcrypt — never stored in plaintext
- Each user has a unique Fernet encryption key stored encrypted in the database
- The encryption key is derived from the master password — resetting your password generates a new key and **existing vault entries become inaccessible**
- Session data is signed with `FLASK_SECRET_KEY` — use a strong random value
- `EMAIL_PASS` is a Google App Password, not your Gmail password — it can be revoked at any time from your Google account

---
