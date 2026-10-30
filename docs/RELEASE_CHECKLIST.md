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
- [x] Document expected local setup and execution commands (not yet runtime validated).
- [ ] Run the project in a clean virtual environment and verify basic flows.
- [ ] Reproduce the original eight manual checks; record any differences from the report.
- [x] Add a separate automated regression suite; **execution remains pending**, and tests are not original TM470 work.
- [x] Clearly disclose educational/non-production limitations.

## Portfolio polish

- [x] Include a concise README, architecture, historical evaluation and security limitations.
- [ ] Add verified, redacted screenshots when available.
- [ ] Choose a licence consciously (do not assume the original coursework is automatically cleared for licensing).
- [ ] Publish the repository only after academic, privacy and secret-scanning checks pass.
- [ ] Add the verified GitHub link to the CV and LinkedIn profile.
