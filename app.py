from flask import Flask, render_template, request, redirect, url_for, session, flash
from helper_files.db import *
from helper_files.secure_helper import (
    hash_password, check_password,
    encrypt_data, decrypt_data,
    generate_encryption_key, encrypt_key_with_password, decrypt_key_with_password
)
from helper_files.email_helper import *
from helper_files.passgenerator import *
from cryptography.fernet import Fernet

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# === EMAIL SETTINGS ===
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")

@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response



# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if get_user_by_username(username):
            flash("User already exists", "danger")
            return redirect("/register")

        otp = generate_otp()
        session["otp_code"] = otp
        session["otp_type"] = "register"
        session["otp_user"] = username
        session["otp_password"] = password

        if send_otp(username, otp):
            flash("OTP sent to your email", "info")
            return redirect(url_for("verify_otp"))
        else:
            flash("Failed to send OTP", "danger")
            return redirect("/register")

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = get_user_by_username(username)
        if not user or not check_password(password, user.hashed_password):
            flash("Invalid credentials")
            return redirect(url_for("login"))

        session["username"] = username

        encrypted_key = get_encryption_key(username)
        vault_key = decrypt_key_with_password(encrypted_key, password)

        session["vault_key"] = vault_key  # ✅ bytes

        return redirect(url_for("dashboard"))

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for("login"))


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "username" not in session or "vault_key" not in session:
        return redirect(url_for("login"))

    email = session["username"]
    vault_key = session["vault_key"]        # ✅ NO encode
    fernet = Fernet(vault_key)

    query = request.args.get("q", "").lower()
    vault_entries = []

    for entry in get_vault_by_user(email):
        decrypted_password = decrypt_data(entry.password, fernet)

        if not query or query in entry.site.lower():
            vault_entries.append({
                "id": entry.id,
                "site": entry.site,
                "username": entry.username,
                "password": decrypted_password
            })

    return render_template("dashboard.html", vault=vault_entries)


# ---------------- ADD PASSWORD ----------------
@app.route("/add_pass", methods=["GET", "POST"])
def add_pass():
    if "username" not in session or "vault_key" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        site = request.form["site"]
        username = request.form["username"]
        password = request.form["password"]

        vault_key = session["vault_key"]
        fernet = Fernet(vault_key)

        encrypted_password = encrypt_data(password, fernet)

        add_vault_entry(
            site,
            username,
            encrypted_password,
            session["username"]
        )

        return redirect(url_for("dashboard"))

    return render_template("add_pass.html")


# ---------------- EDIT PASSWORD / USERNAME ----------------
@app.route("/edit_pass/<entry_id>/<field>", methods=["GET", "POST"])
def edit_pass(entry_id, field):
    if "username" not in session or "vault_key" not in session:
        return redirect(url_for("login"))

    if field not in ["username", "password"]:
        flash("Invalid field.", "danger")
        return redirect(url_for("dashboard"))

    email = session["username"]
    vault_key = session["vault_key"]
    fernet = Fernet(vault_key)

    entry = get_vault_entry_by_id(entry_id)
    if not entry or entry.owner_email != email:
        flash("Entry not found.", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        new_value = request.form.get("new_value")
        if not new_value:
            flash("Value cannot be empty.", "danger")
            return redirect(request.url)

        if field == "password":
            new_value = encrypt_data(new_value, fernet)

        update_vault_field_by_id(entry_id, field, new_value)
        flash(f"{field.capitalize()} updated successfully.", "success")
        return redirect(url_for("dashboard"))

    generated_value = None
    if request.args.get("gen") == "1" and field == "password":
        generated_value = generate_password()

    return render_template(
        "edit_pass.html",
        field=field,
        entry=entry,
        entry_id=entry.id,
        generated_value=generated_value
    )


# ---------------- DELETE PASSWORD ----------------
@app.route("/delete_pass/<entry_id>", methods=["POST"])
def delete_pass(entry_id):
    if "username" not in session:
        return redirect(url_for("login"))

    entry = get_vault_entry_by_id(entry_id)
    if not entry or entry.owner_email != session["username"]:
        flash("Entry not found.")
        return redirect(url_for("dashboard"))

    confirm_site = request.form.get("confirm_site", "").strip()
    if confirm_site != entry.site:
        flash("Site name does not match. Deletion cancelled.")
        return redirect(url_for("dashboard"))

    delete_vault_entry_by_id(entry_id)
    flash("Entry deleted successfully.")
    return redirect(url_for("dashboard"))


# ---------------- FORGOT PASSWORD ----------------
@app.route("/forgot_pass", methods=["GET", "POST"])
def forgot_pass():
    if request.method == "POST":
        username = request.form["username"]
        user = get_user_by_username(username)

        if not user:
            flash("User not found", "danger")
            return redirect("/forgot_pass")

        otp = generate_otp()
        session["otp_code"] = otp
        session["otp_type"] = "forgot_pass"
        session["otp_user"] = username

        if send_otp(username, otp):
            flash("OTP sent to your email", "info")
            return redirect("/verify_otp")
        else:
            flash("Failed to send OTP", "danger")

    return render_template("forgot_pass.html")


# ---------------- VERIFY OTP ----------------
@app.route("/verify_otp", methods=["GET", "POST"])
def verify_otp():
    if request.method == "POST":
        entered_otp = request.form.get("otp")
        flow = session.get("otp_type")
        actual_otp = session.get("otp_code")
        email = session.get("otp_user")

        # Basic validation
        if not entered_otp or not actual_otp or not flow or not email:
            flash("Session expired. Please try again.", "danger")
            return redirect("/login")

        if entered_otp != actual_otp:
            flash("Invalid OTP.", "danger")
            return render_template("verify_otp.html")

        # ---------- FLOW HANDLING ----------
        if flow == "register":
            password = session.get("otp_password")
            if not password:
                flash("Session expired. Please register again.", "danger")
                return redirect("/register")

            hashed = hash_password(password)
            key = generate_encryption_key()
            encrypted_key = encrypt_key_with_password(key, password)

            add_user(email, hashed, encrypted_key)

            # Clear everything for register
            session.clear()
            return redirect("/login")

        elif flow == "forgot_pass":
            # IMPORTANT: keep reset_username
            session["reset_username"] = email

            # Remove only OTP-related session data
            session.pop("otp_code", None)
            session.pop("otp_type", None)
            session.pop("otp_user", None)

            return redirect("/newpass")

        else:
            flash("Invalid flow.", "danger")
            session.clear()
            return redirect("/login")

    return render_template("verify_otp.html")



# ---------------- NEW PASSWORD ----------------
@app.route("/newpass", methods=["GET", "POST"])
def newpass():
    if "reset_username" not in session:
        flash("Unauthorized access.", "danger")
        return redirect("/login")

    if request.method == "POST":
        email = session.pop("reset_username")
        new_password = request.form["password"]

        hashed = hash_password(new_password)
        new_key = generate_encryption_key()
        encrypted_key = encrypt_key_with_password(new_key, new_password)

        update_user_password(email, hashed, encrypted_key)

        flash("Password changed. Please login.")
        return redirect("/login")

    return render_template("newpass.html")


if __name__ == "__main__":
    app.run()
