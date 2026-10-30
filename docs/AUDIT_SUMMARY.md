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

Python source syntax compiled successfully during preparation. Direct runtime validation of Flask, bcrypt and PyOTP integration was **not possible in the preparation environment** because these dependencies were absent and package installation could not reach the package index. An independent regression suite is provided but its outcomes **must not be claimed as passing until run** in an environment with the dependencies installed. The original report documents **8/8 manual checks passed**, which remains separate from this package's verification status.

## Required before public release

- Confirm The Open University's rules for public sharing of assessed code, especially while final results are pending.
- Run application and regression suite in a clean local virtual environment; record actual results.
- Perform full secret scan on the proposed Git history as well as the working files.
- Review dependency versions and known vulnerabilities.
- Do not expose this educational app on the public internet.
