"""
init_db.py — Run this once to create the database tables.
The tables are also auto-created on each app.py startup, so this
script is only needed if you want to pre-populate test data.

Usage:
    python init_db.py
"""
from helper_files.db import init_db, add_user
from helper_files.secure_helper import hash_password, generate_encryption_key, encrypt_key_with_password
from dotenv import load_dotenv

load_dotenv()

# ========== INIT TABLES ==========
init_db()
print("Tables created successfully.")

# ========== OPTIONAL: ADD TEST USER ==========
# Uncomment the lines below to seed a test account.
# email = "test@example.com"
# master_password = "Test1234!"
# hashed_pw = hash_password(master_password)
# vault_key = generate_encryption_key()
# encrypted_key = encrypt_key_with_password(vault_key, master_password)
# add_user(email, hashed_pw, encrypted_key)
# print(f"Test user '{email}' added.")
