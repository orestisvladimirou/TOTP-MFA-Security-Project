# Evaluation results

**Source:** TM470 final project report, September 2026, Section 5 and its evidence appendix. These results reflect the original author's controlled local, manual tests; they are **not** a fresh test run of source files in this repository.

| # | Functional/security check | Reported result |
| --- | --- | --- |
| 1 | Registration and generation of a TOTP enrolment secret | Passed |
| 2 | Rejection of a registration password shorter than eight characters | Passed |
| 3 | Storage of a bcrypt password hash instead of the plaintext password | Passed |
| 4 | Dashboard access after a correct password **and** valid TOTP | Passed |
| 5 | Rejection of an incorrect password before MFA | Passed |
| 6 | Account lockout for 60 seconds after five incorrect passwords | Passed |
| 7 | Denial of dashboard access after a valid password but incorrect TOTP | Passed |
| 8 | Authentication logging of relevant events without submitted password/OTP values | Passed |

**Original evaluation result: 8/8 checks produced expected outcomes.**

## Evidence types

The report used synthetic accounts, browser screenshots, SQLite database inspection and the `auth_logs` table to corroborate the intended branches of the authentication flow.

## What these tests do not establish

- No independently deployed password-only comparison system was benchmarked.
- No automated attack campaign, public penetration test or real-user study was performed.
- No quantitative login-time or usability measurement was completed.
- Basic lockout did not establish protection against distributed attempts or all denial-of-service scenarios.
- TOTP tests did not establish phishing resistance or absence of same-window code replay.
- A passing local functional check does not establish production security or scalability.

## Re-running tests

A separate regression suite is included under `tests/`. Run `python -m unittest discover -s tests -v` after installing the dependencies. These are **new portfolio tests**, not part of the original capstone evaluation. The original 8/8 result above remains a historical manual-testing finding, and any fresh test execution should be reported separately.
