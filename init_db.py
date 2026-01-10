from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

from helper_files.secure_helper import (
    hash_password,
    generate_encryption_key,
    encrypt_key_with_password
)

load_dotenv()

# ========== DATABASE SETUP ==========
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True)
    hashed_password = Column(String, nullable=False)
    encrypted_key = Column(String, nullable=False)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# ========== FUNCTION TO ADD USER ==========
def add_user(email, hashed_pw, encrypted_key):
    session = Session()
    user = User(
        email=email,
        hashed_password=hashed_pw,
        encrypted_key=encrypted_key.decode()
    )
    session.add(user)
    session.commit()
    session.close()

# ========== INIT DB ==========
Base.metadata.create_all(engine)
print("✅ Tables created successfully.")

# ========== ADD TEST USER ==========
email = "test@example.com"
master_password = "test123"

hashed_pw = hash_password(master_password)

# ✅ Correct vault key workflow
vault_key = generate_encryption_key()
encrypted_key = encrypt_key_with_password(vault_key, master_password)

add_user(email, hashed_pw, encrypted_key)

print("✅ Test user added successfully.")
  