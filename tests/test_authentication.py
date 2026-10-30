"""Independent regression tests added for the portfolio (not part of original TM470 evaluation)."""

import sqlite3
import tempfile
import time
import unittest
from contextlib import closing
from pathlib import Path

import bcrypt
import pyotp

import app as prototype

USERNAME = "synthetic_tester"
PASSWORD = "Example-Test-Passphrase-123!"


class AuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.original_database = prototype.DATABASE
        prototype.DATABASE = str(Path(self.temp.name) / "synthetic_auth.db")
        prototype.app.config["TESTING"] = True
        prototype.init_db()
        self.client = prototype.app.test_client()

    def tearDown(self):
        prototype.DATABASE = self.original_database
        self.temp.cleanup()

    def register(self, password=PASSWORD):
        return self.client.post("/register", data={"username": USERNAME, "password": password})

    def login(self, password=PASSWORD):
        return self.client.post("/login", data={"username": USERNAME, "password": password})

    def get_secret(self):
        with closing(sqlite3.connect(prototype.DATABASE)) as conn:
            row = conn.execute("SELECT totp_secret FROM users WHERE username = ?", (USERNAME,)).fetchone()
        return row[0] if row else None

    def test_01_registration_creates_account_and_secret(self):
        response = self.register()
        self.assertEqual(response.status_code, 302)
        self.assertIn("/setup-mfa", response.location)
        self.assertIsNotNone(self.get_secret())

    def test_02_short_password_rejected(self):
        response = self.register("short")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"at least 8 characters", response.data)
        self.assertIsNone(self.get_secret())

    def test_03_bcrypt_hash_stored_not_plaintext(self):
        self.register()
        with closing(sqlite3.connect(prototype.DATABASE)) as conn:
            stored = conn.execute("SELECT password_hash FROM users WHERE username = ?", (USERNAME,)).fetchone()[0]
        self.assertNotEqual(stored, PASSWORD.encode())
        self.assertTrue(bcrypt.checkpw(PASSWORD.encode(), stored))

    def test_04_password_and_totp_required_for_access(self):
        self.register()
        self.assertEqual(self.client.get("/dashboard").status_code, 302)
        self.assertEqual(self.login().status_code, 302)
        self.assertEqual(self.client.get("/dashboard").status_code, 302)
        code = pyotp.TOTP(self.get_secret()).now()
        response = self.client.post("/verify-mfa", data={"code": code})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard", response.location)
        self.assertIn(b"successfully authenticated", self.client.get("/dashboard").data)

    def test_05_bad_password_prevents_mfa(self):
        self.register()
        response = self.login("incorrect-password")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid username or password", response.data)
        self.assertEqual(self.client.get("/verify-mfa").status_code, 302)

    def test_06_five_failures_trigger_lockout(self):
        self.register()
        for _ in range(5):
            self.login("incorrect-password")
        with closing(sqlite3.connect(prototype.DATABASE)) as conn:
            failures, until = conn.execute("SELECT failed_attempts, lockout_until FROM users WHERE username = ?", (USERNAME,)).fetchone()
        self.assertEqual(failures, 5)
        self.assertGreater(until, int(time.time()))
        response = self.login()
        self.assertIn(b"temporarily locked", response.data)

    def test_07_invalid_totp_prevents_dashboard(self):
        self.register()
        self.login()
        totp = pyotp.TOTP(self.get_secret())
        invalid_code = next(c for c in ("000000", "111111", "222222", "333333") if not totp.verify(c, valid_window=1))
        response = self.client.post("/verify-mfa", data={"code": invalid_code})
        self.assertIn(b"Invalid MFA code", response.data)
        self.assertEqual(self.client.get("/dashboard").status_code, 302)

    def test_08_authentication_events_without_submitted_secrets(self):
        self.register()
        self.login("incorrect-password")
        self.login()
        code = pyotp.TOTP(self.get_secret()).now()
        self.client.post("/verify-mfa", data={"code": code})
        with closing(sqlite3.connect(prototype.DATABASE)) as conn:
            rows = conn.execute("SELECT username, event, timestamp FROM auth_logs").fetchall()
        self.assertTrue(any(event == "user_registered" for _, event, _ in rows))
        self.assertTrue(any(event == "failed_password_attempt" for _, event, _ in rows))
        self.assertTrue(any(event == "mfa_success" for _, event, _ in rows))
        log_text = repr([(username, event) for username, event, _ in rows])
        self.assertNotIn(PASSWORD, log_text)
        self.assertNotIn(code, log_text)


if __name__ == "__main__":
    unittest.main()
