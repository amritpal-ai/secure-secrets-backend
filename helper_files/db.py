import os
import uuid
from sqlalchemy import create_engine, Column, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from dotenv import load_dotenv

load_dotenv()

# ---------------- DATABASE SETUP ----------------
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

# ---------------- MODELS ----------------
class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    hashed_password = Column(Text, nullable=False)
    encrypted_key = Column(Text, nullable=False)

    vault = relationship(
        "VaultEntry",
        back_populates="owner",
        cascade="all, delete-orphan"
    )


class VaultEntry(Base):
    __tablename__ = "vault"

    # ✅ AUTO-GENERATED UUID (CRITICAL FIX)
    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    site = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(Text, nullable=False)

    owner_email = Column(String, ForeignKey("users.email"), nullable=False)
    owner = relationship("User", back_populates="vault")

    __table_args__ = (
        UniqueConstraint(
            "site",
            "username",
            "owner_email",
            name="unique_site_user_owner"
        ),
    )

# ---------------- USER FUNCTIONS ----------------
def get_user_by_username(username):
    with SessionLocal() as session:
        return session.query(User).filter(User.email == username).first()


def add_user(username, hashed_password, encrypted_key):
    with SessionLocal() as session:
        user = User(
            email=username,
            hashed_password=hashed_password,
            encrypted_key=encrypted_key
        )
        session.add(user)
        session.commit()


def update_user_password(username, new_hashed_password, new_encrypted_key):
    with SessionLocal() as session:
        user = session.query(User).filter(User.email == username).first()
        if user:
            user.hashed_password = new_hashed_password
            user.encrypted_key = new_encrypted_key
            session.commit()


def get_encryption_key(username):
    with SessionLocal() as session:
        user = session.query(User).filter(User.email == username).first()
        return user.encrypted_key if user else None


def store_encryption_key(username, encrypted_key):
    with SessionLocal() as session:
        user = session.query(User).filter(User.email == username).first()
        if user:
            user.encrypted_key = encrypted_key
            session.commit()

# ---------------- VAULT FUNCTIONS ----------------
def get_vault_by_user(username):
    with SessionLocal() as session:
        user = session.query(User).filter(User.email == username).first()
        return user.vault if user else []


def add_vault_entry(site, username, password, owner_username):
    with SessionLocal() as session:
        existing = session.query(VaultEntry).filter(
            VaultEntry.site == site,
            VaultEntry.username == username,
            VaultEntry.owner_email == owner_username
        ).first()

        if existing:
            return False

        entry = VaultEntry(
            site=site,
            username=username,
            password=password,
            owner_email=owner_username
        )

        session.add(entry)
        session.commit()
        return True


def update_vault_entry(entry_id, new_username, new_password):
    with SessionLocal() as session:
        entry = session.query(VaultEntry).filter(VaultEntry.id == entry_id).first()
        if entry:
            entry.username = new_username
            entry.password = new_password
            session.commit()


def update_vault_field_by_id(entry_id, field, new_encrypted_value):
    with SessionLocal() as session:
        entry = session.query(VaultEntry).filter(VaultEntry.id == entry_id).first()
        if entry:
            if field == "username":
                entry.username = new_encrypted_value
            elif field == "password":
                entry.password = new_encrypted_value
            session.commit()


def get_vault_entry_by_id(entry_id):
    with SessionLocal() as session:
        return session.query(VaultEntry).filter(VaultEntry.id == entry_id).first()


def delete_vault_entry_by_id(entry_id):
    with SessionLocal() as session:
        entry = session.query(VaultEntry).filter(VaultEntry.id == entry_id).first()
        if entry:
            session.delete(entry)
            session.commit()
