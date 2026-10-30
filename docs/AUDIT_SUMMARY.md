# Private portfolio source audit — 30 October 2026

## Input

The user provided `mfa_project.zip` containing two identical copies of the Flask application, two identical SQLite databases, HTML templates, original academic material, and screenshots. The source copies and databases were compared using SHA-256; their respective pairs matched.

## Included

- A single copy of the Flask `app.py` and five original templates
- A concise dependency manifest
- Historical project documentation and a separate new regression test suite
- One application change: Flask startup `debug=True` changed to `debug=False`

## Deliberately excluded

- `auth.db` (contains account information, bcrypt hashes and a recoverable TOTP shared secret)
- Original assessment files and student identification details
- Duplicate TMA03 code, database and other unnecessary folders
- Screenshot evidence pending independent inspection/redaction; no unredacted screenshots are bundled

## Verification status

Python source syntax compiled successfully during preparation, although direct runtime validation in the preparation environment was unavailable due to missing dependencies. On **30 October 2026**, the owner ran the independent portfolio regression suite locally on **Windows / Python 3.13.5** and provided the terminal result: **8 tests run in 3.360 seconds — OK (zero failures/errors)**. This provides evidence that the tested application behaviors work in that environment, but is not an independent security audit or a complete manual browser review. GitHub Actions has not provided a successful CI result due to exhausted Actions usage; automatic workflow triggers are temporarily disabled. The original capstone report separately documents **8/8 historical manual checks passed**. Do not combine these two sets of results.

## Required before public release

- Confirm The Open University's rules for public sharing of assessed code, especially while final results are pending.
- Manually run the application in a browser and validate enrolment and login flow; local regression suite has already passed (8/8, 30 October 2026).
- Perform full secret scan on the proposed Git history as well as the working files.
- Review dependency versions and known vulnerabilities.
- Do not expose this educational app on the public internet.
