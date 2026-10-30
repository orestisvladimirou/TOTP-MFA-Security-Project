# Threat model (report-based summary)

## Scope and assets

A local Flask application with account credentials, password hashes, TOTP shared secrets, session state, an authenticated dashboard and authentication-event logs.

The original report considered password guessing, compromised/reused credentials, failed second-factor attempts and exposure of stored credentials/logs. Real-time phishing relay was reviewed conceptually, not tested against an external service. Production availability, distributed botnets, endpoint malware and large-scale network threats were outside scope.

## STRIDE-style considerations

| Category | Example | Control or residual risk |
| --- | --- | --- |
| Spoofing | Impersonation using a stolen password | Second TOTP stage protects against password-only compromise; real-time phishing relay remains possible |
| Tampering | Altering authentication/session state | Separate pending-MFA and authenticated states; session settings were not production-hardened |
| Repudiation | Denying a login or lockout event | `auth_logs` records basic outcomes; not tamper-evident |
| Information disclosure | Exposure of stored passwords or TOTP secrets | Passwords use bcrypt; recoverable TOTP secrets remain sensitive in SQLite |
| Denial of service | Maliciously triggering account lockout | Five-attempt lockout slows guessing but can lock out a legitimate user |
| Elevation of privilege | Accessing dashboard without completing TOTP | Authenticated session established only after successful second factor; no comprehensive penetration test |

## Security claims and boundaries

The project showed, within its controlled local tests, that a correct password alone did not grant an authenticated session and invalid OTPs were rejected. It did **not** establish resistance to real-time phishing, replay, account-lockout abuse, or every production threat. The report identified origin-bound public-key methods such as WebAuthn/passkeys as a stronger future direction for phishing resistance.
