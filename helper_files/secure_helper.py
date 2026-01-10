import bcrypt
from cryptography.fernet import Fernet
import base64
import hashlib

# --- 1. Hashing for master password ---

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

# --- 2. Password-derived key for encrypting the user's encryption key ---

def derive_key_from_password(password):
    if isinstance(password, str):
        password = password.encode()   # convert ONLY if needed

    digest = hashlib.sha256(password).digest()
    return base64.urlsafe_b64encode(digest)


def get_fernet_from_password(password):
    key = derive_key_from_password(password)
    return Fernet(key)

# --- 3. Core encryption/decryption for vault data ---

def encrypt_data(plain_text, fernet):
    return fernet.encrypt(plain_text.encode()).decode()

def decrypt_data(encrypted_text, fernet):
    if isinstance(encrypted_text, str):
        encrypted_text = encrypted_text.encode()
    return fernet.decrypt(encrypted_text).decode()


# --- 4. New additions: Fernet key management ---

def generate_encryption_key():
    """Generate a random Fernet key to encrypt/decrypt vault data."""
    return Fernet.generate_key().decode()  # Store as str in DB

def encrypt_key_with_password(encryption_key, password):
    """Encrypt the user-specific Fernet key using the password-derived Fernet."""
    fernet = get_fernet_from_password(password)
    return fernet.encrypt(encryption_key.encode()).decode()

def decrypt_key_with_password(encrypted_key, password):
    """Decrypt the stored Fernet key using the password-derived Fernet."""
    fernet = get_fernet_from_password(password)
    return fernet.decrypt(encrypted_key.encode()).decode()

def get_fernet(password):
    key = derive_key_from_password(password)
    return Fernet(key)
