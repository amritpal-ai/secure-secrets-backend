# 🔐 Secure Secrets Backend

A **production-grade, multi-tenant backend system** for securely storing and managing sensitive secrets.  
Built with a **zero-knowledge security model**, ensuring that **stored secrets are never readable by the server or administrators**.

This system is designed as a **general-purpose secure backend**, with password management being one possible use case.

---

## 🌐 Live Deployment

🚀 **Live Service:**  
👉 https://password-manager-kopq.onrender.com

> Deployed on a Linux-based production environment with a managed PostgreSQL database.

---

## 🎯 System Capabilities

### 👤 Authentication & Identity
- User registration with **email-based OTP verification**
- Secure authentication using **bcrypt-hashed credentials**
- Password reset flow without loss of encrypted data
- Session-based access with secure validation

### 🗄️ Encrypted Secrets Storage
- Per-user encrypted secret vaults
- Secrets encrypted at rest using **strong symmetric cryptography**
- User-specific encryption keys protected by user credentials
- Secure secret creation, update, search, and deletion

### 🔐 Security Architecture
- **Zero-knowledge design** — server cannot read stored secrets
- Encryption keys never stored in plaintext
- Vault access preserved even after credential resets
- Protection against database leaks exposing sensitive data

---

## 🧱 Backend Architecture

- Clear separation of authentication, cryptography, and data layers
- Relational database design optimized for multi-user access
- Centralized error handling and request validation
- Environment-based configuration for secure deployments

---

## 🧰 Tech Stack

### Backend
- Python 3
- Flask
- SQLAlchemy
- bcrypt
- cryptography (Fernet)

### Database
- PostgreSQL (Neon – serverless cloud database)

### Frontend (minimal)
- HTML5
- CSS3
- Jinja2 templates

### Deployment
- Gunicorn
- Linux-based hosting (Render / Railway compatible)
- `.env`-based secrets management

---

## 🗂️ Project Structure

```text
secure-secrets-backend/
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

## 🔐 Security Model (High-Level)

- User credentials are **hashed**, never stored
- Encryption keys are:
  - Randomly generated
  - Encrypted using user credentials
- Secrets remain protected even after password resets
- Compromised database data does **not** reveal plaintext secrets

---

## 🛠️ Local Development

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run locally
```bash
python app.py
```

### Production server
```bash
gunicorn app:app
```

---

## 📄 License

MIT License

Built by **Amritpal Singh**  
Backend-focused secure systems project
