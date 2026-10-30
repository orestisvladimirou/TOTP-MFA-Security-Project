from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import bcrypt
import pyotp
import time
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(32)

DATABASE = "auth.db"
MAX_ATTEMPTS = 5
LOCKOUT_SECONDS = 60


def get_db():
    return sqlite3.connect(DATABASE, timeout=10)


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL,
            totp_secret TEXT,
            failed_attempts INTEGER DEFAULT 0,
            lockout_until INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            event TEXT,
            timestamp INTEGER
        )
    """)

    conn.commit()
    conn.close()


def log_event(username, event):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO auth_logs (username, event, timestamp) VALUES (?, ?, ?)",
        (username, event, int(time.time()))
    )
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password_text = request.form["password"]

        if len(password_text) < 8:
            return "Password must be at least 8 characters long."

        password = password_text.encode("utf-8")
        password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
        totp_secret = pyotp.random_base32()

        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash, totp_secret) VALUES (?, ?, ?)",
                (username, password_hash, totp_secret)
            )
            conn.commit()
            conn.close()

            log_event(username, "user_registered")
            session["username"] = username
            return redirect(url_for("setup_mfa"))

        except sqlite3.IntegrityError:
            return "Username already exists."

    return render_template("register.html")


@app.route("/setup-mfa")
def setup_mfa():
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT totp_secret FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        return redirect(url_for("login"))

    secret = result[0]
    return render_template("setup_mfa.html", secret=secret)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].encode("utf-8")
        current_time = int(time.time())

        event_to_log = None

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password_hash, failed_attempts, lockout_until FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()

        if not user:
            conn.close()
            log_event(username, "failed_login_unknown_user")
            return "Invalid username or password."

        password_hash, failed_attempts, lockout_until = user

        if lockout_until > current_time:
            conn.close()
            log_event(username, "login_blocked_lockout")
            return "Account temporarily locked. Try again later."

        if bcrypt.checkpw(password, password_hash):
            cursor.execute(
                "UPDATE users SET failed_attempts = 0, lockout_until = 0 WHERE username = ?",
                (username,)
            )
            conn.commit()
            conn.close()

            session["pending_mfa_user"] = username
            log_event(username, "password_success")
            return redirect(url_for("verify_mfa"))

        failed_attempts += 1

        if failed_attempts >= MAX_ATTEMPTS:
            lockout_until = current_time + LOCKOUT_SECONDS
            cursor.execute(
                "UPDATE users SET failed_attempts = ?, lockout_until = ? WHERE username = ?",
                (failed_attempts, lockout_until, username)
            )
            event_to_log = "account_locked"
        else:
            cursor.execute(
                "UPDATE users SET failed_attempts = ? WHERE username = ?",
                (failed_attempts, username)
            )
            event_to_log = "failed_password_attempt"

        conn.commit()
        conn.close()

        log_event(username, event_to_log)
        return "Invalid username or password."

    return render_template("login.html")


@app.route("/verify-mfa", methods=["GET", "POST"])
def verify_mfa():
    username = session.get("pending_mfa_user")
    if not username:
        return redirect(url_for("login"))

    if request.method == "POST":
        code = request.form["code"].strip()

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT totp_secret FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            return redirect(url_for("login"))

        secret = result[0]

        totp = pyotp.TOTP(secret, interval=30, digits=6, digest="sha1")

        if totp.verify(code, valid_window=1):
            session["authenticated_user"] = username
            session.pop("pending_mfa_user", None)
            log_event(username, "mfa_success")
            return redirect(url_for("dashboard"))

        log_event(username, "mfa_failed")
        return "Invalid MFA code."

    return render_template("verify_mfa.html")


@app.route("/dashboard")
def dashboard():
    username = session.get("authenticated_user")
    if not username:
        return redirect(url_for("login"))

    return render_template("dashboard.html", username=username)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(debug=False)
