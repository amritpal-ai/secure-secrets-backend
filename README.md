# 🔐 Secure Web-Based Password Manager

A **production-ready, secure, multi-user Password Manager Web Application** built using **Flask** and modern cryptography practices.  
Designed so that **even the admin cannot view user passwords**, following **zero-knowledge security principles**.

---

## 🌐 Live Deployment

🚀 **Live Website:**  
👉 https://password-manager-kopq.onrender.com

> A fully deployed, production-ready version of this password manager hosted on Render and backed by a Neon PostgreSQL database.

---


## ✨ Key Features

### 👤 User & Authentication
- ✅ User registration with **email OTP verification**
- 🔐 Secure login with **bcrypt-hashed master password**
- 🔁 **Forgot password** flow with OTP verification
- 🔄 Secure **master password change**

### 🗄️ Password Vault
- 🔐 Vault-level encryption using **Fernet**
- 🧠 Per-user encryption key protected by master password
- ➕ Add new credentials (manual or generated)
- 🔍 Search credentials by site name
- ✏️ Update saved passwords or usernames
- 🗑️ Delete vault entries
- 📋 One-click password copy

### 🔐 Security Architecture
- ❌ Admin **cannot** read stored passwords
- 🔑 Random vault key encrypted using master password
- 🔄 Vault remains accessible even after password reset
- 🧂 Password hashing using **bcrypt**
- 🔒 All sensitive data encrypted at rest

---

## 🧰 Tech Stack

### Backend
- Python 3
- Flask
- SQLAlchemy
- bcrypt
- cryptography (Fernet)

### Database
- PostgreSQL (Neon – serverless cloud DB)

### Frontend
- HTML5  
- CSS3  
- Jinja2 Templates  

### Deployment
- Gunicorn
- Render / Railway compatible
- `.env` based secrets management

---

## 🗂️ Project Structure

```text
password-manager/
├── app.py
├── helper_files/
│   ├── db.py
│   ├── secure_helper.py
│   └── otp_helper.py
├── templates/
├── static/
├── requirements.txt
├── Procfile
└── .env
```

---

## 🔐 Security Design (Zero-Knowledge)

- Master passwords are **hashed**, never stored
- Vault encryption keys are:
  - Randomly generated
  - Encrypted using the master password
- Even after a password reset:
  - Vault remains accessible
  - Encryption key stays intact
- Database leaks **do not expose plaintext passwords**

---

## 🛠️ Local Development Setup


### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Locally
```bash
python app.py
```

### Run in Production
```bash
gunicorn app:app
```

---

## 📄 License

**MIT License**

Built by **Amritpal Singh**  
Security-focused full-stack project 🚀
