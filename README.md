# TOTP Multi-Factor Authentication — Security Design & Evaluation

**Python / Flask / SQLite / bcrypt / PyOTP**  
**University capstone (TM470), The Open University · 2026**  
**Status:** Completed local educational prototype, prepared for a *private* technical portfolio. **Not production-ready.**

A small web application built to examine how adding Time-Based One-Time Password (TOTP) verification changes the security of a password-based login. It demonstrates password hashing, a second authentication stage, temporary account lockout, and authentication-event logging, alongside analysis of residual security risks.

## What the application does

- Creates a local account with an **8-character minimum** password rule and a **bcrypt** password hash.
- Generates a unique TOTP secret and displays it for manual enrollment in an authenticator app.
- Requires successful password verification and a six-digit TOTP code (30-second interval, ±1-step tolerance) **before** accessing the dashboard.
- Applies a **60-second per-account lockout** after **five failed password attempts**.
- Records registration, password, lockout and MFA outcomes in a local `auth_logs` table **without writing submitted passwords or OTPs to those event records**.

### Workflow

```text
Register --> bcrypt password hash + TOTP secret --> enroll authenticator

Log in --> verify password --> pending MFA --> verify TOTP --> dashboard
             |                                 |
             +-- failed/locked                +-- invalid code: access denied
```

## Run locally

This code is for demonstration on **localhost only**. Do **not** deploy it to the public internet or use real account credentials.

Prerequisites: Python 3.10+ and a local authenticator app that supports TOTP.

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`, select **Register**, choose a synthetic username and password, and enter the displayed TOTP secret in your authenticator. Select **Login** and complete both steps. All data is local and stored in a generated `auth.db` SQLite file; it is excluded by `.gitignore` and should never be committed.

**Important:** This code is a minimally modified copy of the original TM470 Flask prototype. The sole application-source change for this portfolio preparation was to disable Flask's `debug=True` startup setting. The remaining original authentication logic and templates have been preserved. The original secret-key generation remains process-local and resets sessions on restart. No production hardening is implied.

## Evaluation and reproducibility

The **original capstone evaluation** completed eight controlled *manual* functional/security checks using synthetic accounts, UI screenshots, database inspection and event logs. All eight produced the expected behavior. The evaluation did **not** include a separate deployed password-only implementation, an automated attack campaign, a penetration test or a quantitative usability study.

A new `unittest` regression suite and GitHub Actions workflow accompany this portfolio copy. **These tests were added after the university evaluation and must not be represented as original capstone results.** To run the regression suite when the dependencies are installed:

```bash
python -m unittest discover -s tests -v
```

**Local regression verification (30 October 2026):** all **8/8** tests passed on Windows with Python **3.13.5**, in **3.360 seconds**, with zero failures or errors. This result was observed from the user's PowerShell output, not from GitHub Actions. GitHub Actions is temporarily configured for manual triggering only because available Actions usage is exhausted.

The original assessment findings are documented in [Evaluation](docs/EVALUATION.md). The regression suite uses its own temporary SQLite database rather than the original test database.

## Security limitations

**This application is intentionally not production-hardened.** Key known limitations include recoverable TOTP secrets stored in SQLite, no same-window OTP replay tracking, no independent MFA-attempt throttling, lack of CSRF protection, basic account-level lockout only, non-persistent Flask session secret, and no HTTPS or operational monitoring setup. Manually entered TOTP codes are **not phishing-resistant** against real-time relay. See [Security](SECURITY.md) and [Threat model](docs/THREAT_MODEL.md).

## Documentation

- [Architecture and flow](docs/ARCHITECTURE.md)
- [Original eight-test evaluation](docs/EVALUATION.md)
- [STRIDE-style threat model](docs/THREAT_MODEL.md)
- [Security and disclosure notes](SECURITY.md)
- [Publication checklist](docs/RELEASE_CHECKLIST.md)

## Publication and academic-integrity note

This project originated as assessed university coursework. The private portfolio snapshot **does not include** the assessment submission, student identifier, original SQLite database, or unredacted screenshots. **Do not make the repository public or license the assessed code for reuse until university rules and any applicable permissions have been confirmed.**

This repository presents educational project work, **not** an awarded industry security certification, production MFA service, or independently audited security product.
