from flask import Flask, jsonify, current_app, request, url_for
import sqlite3 as sql
from jsonschema import validate
import os
import bcrypt
import uuid
import pyotp
import qrcode
import io
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["DATABASE"] = "./data/register.db"


def create_user(username, email, password):
    if not os.path.exists(app.config["DATABASE"]):
        print("Error: Database does not exist.")
        return jsonify({"error": "Internal server error"}), 500

    if not username or not email or not password:
        print("Error: Username, email, or password not provided.")
        return jsonify({"error": "Username, email, or password not provided."}), 400

    con = sql.connect(app.config["DATABASE"])
    cur = con.cursor()
    cur.execute(
        "SELECT vX8hR_username, ajkSC_email FROM e50PMSBi_users WHERE vX8hR_username = ? OR ajkSC_email = ?",
        (username, email),
    )
    user = cur.fetchone()
    if user:
        print("Error: Username/email already in use.")
        return jsonify({"error": "Username/email already in use."}), 409

    salt = bcrypt.gensalt(rounds=14)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    while True:
        user_id = str(uuid.uuid4())  # Generate UUID v7
        cur.execute(
            "SELECT Wj89c_uuid FROM e50PMSBi_users WHERE Wj89c_uuid = ?", (user_id,)
        )
        user = cur.fetchone()
        if not user:
            break
        else:
            continue

    # Generate OTP secret
    otp_secret = pyotp.random_base32()
    cur.execute(
        "INSERT INTO e50PMSBi_users (Wj89c_uuid, vX8hR_username, ajkSC_email, D9K66_password, As7cn_otp_secret) VALUES (?, ?, ?, ?, ?)",
        (user_id, username, email, hashed_password.decode(), otp_secret),
    )
    con.commit()
    con.close()

    # Generate OTP URI
    otp_uri = pyotp.totp.TOTP(otp_secret).provisioning_uri(
        name=email, issuer_name="YourAppName"
    )

    # Generate QR code
    qr = qrcode.make(otp_uri)
    buffered = io.BytesIO()
    qr.save(buffered, format="PNG")
    qr_code_data = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return (
        jsonify(
            {
                "message": "User created successfully",
                "otp_secret": otp_secret,
                "qr_code_data": qr_code_data,
            }
        ),
        201,
    )


def verify_otp(username, otp):
    if not os.path.exists(app.config["DATABASE"]):
        print("Error: Database does not exist.")
        return jsonify({"error": "Internal server error"}), 500

    con = sql.connect(app.config["DATABASE"])
    cur = con.cursor()
    cur.execute(
        "SELECT otp_secret FROM e50PMSBi_users WHERE vX8hR_username = ?", (username,)
    )
    user = cur.fetchone()
    if not user:
        print("Error: User not found.")
        return jsonify({"error": "User not found."}), 404

    otp_secret = user[0]
    totp = pyotp.TOTP(otp_secret)
    if totp.verify(otp):
        return (
            jsonify({"message": "OTP verified successfully", "username": username}),
            200,
        )
    else:
        return jsonify({"error": "Invalid OTP"}), 401


def checkPW(username, password):
    if not os.path.exists(app.config["DATABASE"]):
        print("Error: Database does not exist.")
        return False

    con = sql.connect(app.config["DATABASE"])
    cur = con.cursor()

    cur.execute(
        "SELECT D9K66_password FROM e50PMSBi_users WHERE vX8hR_username = ?",
        (username,),
    )
    user = cur.fetchone()

    if not user:
        print("Error: User not found.")
        return False

    hashed_password = user[0]
    if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
        return True
    else:
        return False


def changePW(username, email, password):
    if not os.path.exists(app.config["DATABASE"]):
        print("Error: Database does not exist.")
        return jsonify({"error": "Internal server error"}), 500

    con = sql.connect(app.config["DATABASE"])
    cur = con.cursor()

    cur.execute(
        "SELECT * FROM e50PMSBi_users WHERE vX8hR_username = ? AND ajkSC_email = ?",
        (username, email),
    )
    user = cur.fetchone()
    if not user:
        print("Error: User not found.")
        return jsonify({"error": "User not found."}), 404

    salt = bcrypt.gensalt(rounds=14)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    cur.execute(
        "UPDATE e50PMSBi_users SET D9K66_password = ? WHERE vX8hR_username = ? AND ajkSC_email = ?",
        (hashed_password.decode(), username, email),
    )
    con.commit()

    con.close()
    return jsonify({"message": "Password changed successfully"}), 200


def get_uuid(username):
    if not os.path.exists(app.config["DATABASE"]):
        logger.error("Database does not exist.")
        return jsonify({"error": "Internal server error"}), 500

    con = sql.connect(app.config["DATABASE"])
    cur = con.cursor()

    logger.debug(f"Looking for uuid with username: {username}")
    cur.execute(
        "SELECT Wj89c_uuid FROM e50PMSBi_users WHERE vX8hR_username = ?",
        (username,),
    )
    user = cur.fetchone()
    if not user:
        logger.error("User not found.")
        return jsonify({"error": "User not found."}), 404

    logger.debug(f"Found user: {user}")
    return user[0], 200


if __name__ == "__main__":
    with app.app_context():

        def create_database():
            if not os.path.exists("./data"):
                os.makedirs("./data")

            con = sql.connect(app.config["DATABASE"])
            cur = con.cursor()

            cur.execute(
                """CREATE TABLE IF NOT EXISTS e50PMSBi_users (
                            Wj89c_uuid TEXT NOT NULL PRIMARY KEY,
                            vX8hR_username TEXT NOT NULL UNIQUE,
                            ajkSC_email TEXT NOT NULL UNIQUE,
                            D9K66_password TEXT NOT NULL,
                            As7cn_otp_secret TEXT NOT NULL
                        )"""
            )

            con.commit()
            con.close()

        create_database()
