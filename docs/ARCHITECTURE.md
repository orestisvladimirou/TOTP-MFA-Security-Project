# Architecture and authentication workflow

This document summarizes the TM470 report and has been cross-checked against the recovered original `app.py` and templates.

## Components

- **Flask**: local web routes and authenticated session state
- **SQLite `users` table**: account details, bcrypt password hashes, TOTP shared secrets and failed-attempt/lockout fields
- **SQLite `auth_logs` table**: username, event type and timestamp for security-relevant outcomes
- **bcrypt**: salted password hashing and password verification
- **PyOTP**: generation/verification of time-based one-time passwords
- **Software authenticator**: generates a current TOTP code for local test accounts

## Registration

1. Reject passwords shorter than eight characters.
2. Hash accepted passwords with bcrypt and generate a per-user TOTP secret.
3. Store account information locally in SQLite.

## Authentication

1. Check account lockout state and verify the submitted password.
2. A correct password sets **pending MFA**, not a fully authenticated session.
3. Request the six-digit TOTP value.
4. Only successful TOTP verification allows authenticated dashboard access.
5. Failed password attempts, lockout events and MFA outcomes are recorded in the event log, without submitted secrets.

## Deliberate limits

The report describes local, single-user-style prototype testing. It did not deploy a separate password-only application or a production identity provider. Session protection, secret storage and verification windows would require security review before any public deployment.
