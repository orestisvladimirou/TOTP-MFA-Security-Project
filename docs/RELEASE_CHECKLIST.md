# Pre-publication checklist

This is a **private portfolio source snapshot** with reviewed Flask code and templates. It is not yet cleared for public release.

## Academic permission

- [ ] Confirm with the TM470 module team or university guidance whether the original submitted code/report may be made public.
- [ ] Prefer waiting for final module grading before publishing assessed work.
- [ ] Do not publish assignment questions, evaluation material or the submitted report verbatim without permission.

## Source recovery and audit

- [x] Retrieve the original Flask Python source, HTML templates and dependency manifest.
- [x] Review code for obvious embedded credentials, session secrets, tokens and personal identifiers. No hard-coded TOTP credentials found in application source.
- [x] Exclude the original SQLite database, journals, `.env`, caches, logs and virtual environments from this package.
- [ ] Search all files and commit history for leaked secrets before making the repository public.
- [ ] Replace screenshots with redacted synthetic-data examples; blur any OTP setup QR codes and shared secrets.
- [x] Source matches recovered `app.py` except disabling debug mode at startup; original behavior and remaining limitations are documented.

## Technical review

- [x] Record direct dependencies from imported modules; select supported version ranges (versions still need environment validation).
- [x] Document local setup and test execution commands; dependencies were installed and tests executed successfully on the owner's Windows PC.
- [ ] Open the application in a browser and manually verify registration, TOTP enrolment and login; regression tests already passed in a local virtual environment.
- [ ] Reproduce the original eight manual checks; record any differences from the report.
- [x] Add and locally run the separate regression suite: **8/8 passed on Windows / Python 3.13.5 on 30 October 2026** (3.360 seconds; owner-provided terminal output). These are not the original TM470 manual tests.
- [x] Clearly disclose educational/non-production limitations.

## Portfolio polish

- [x] Include a concise README, architecture, historical evaluation and security limitations.
- [ ] Add verified, redacted screenshots when available.
- [ ] Choose a licence consciously (do not assume the original coursework is automatically cleared for licensing).
- [ ] Publish the repository only after academic, privacy and secret-scanning checks pass.
- [ ] Add the verified GitHub link to the CV and LinkedIn profile.
