# Security considerations

## Scope

This is an educational, locally tested authentication prototype. It is **not suitable for production authentication** without substantial redesign, security review and further testing. The original source was reviewed for this private portfolio preparation. The application is included, with debugging disabled at startup; the original SQLite database and academic submissions were excluded.

## Documented limitations

| Area | Limitation in the original project | Production-oriented improvement |
| --- | --- | --- |
| TOTP secrets | Recoverable TOTP secrets stored directly in SQLite | Encrypt at rest, protect encryption keys, use secrets management, design re-enrolment |
| TOTP replay | No tracking of already accepted time-step values | Prevent reuse of an accepted OTP within its valid interval |
| TOTP attempts | MFA verification route lacked an independent failure throttle | Add appropriate rate limiting and abuse monitoring |
| Password lockout | Five failures lead to 60-second per-account lockout, not distributed rate limiting | Add layered account/IP/request protections; evaluate lockout-based denial-of-service |
| Session handling | Flask secret regenerated at app startup | Stable protected application secret, HTTPS, secure cookie configuration |
| CSRF | No explicit CSRF protection on state-changing forms | Add CSRF protection and safe HTTP methods |
| Deployment | Original code used Flask debug mode; this portfolio copy disables it, but has no public TLS setup | Disable debugging, use HTTPS and a production-grade server |
| Audit logs | Basic auth event history only; no central monitoring or tamper-evident storage | Structured monitoring, access controls, retention and log integrity |
| MFA phishing | Manually entered TOTP codes can be relayed in real time | Consider origin-bound WebAuthn/passkeys for phishing-resistant authentication |

These are documented project limitations, not claims of independently verified vulnerabilities in any future revision.

## Before uploading code or screenshots

- Remove real credentials, access tokens, Flask secrets, authenticators' shared secrets and password-reset artifacts.
- Remove SQLite databases, WAL/journal files, local virtual environments, `.env` files and debug logs.
- Review screenshots for student identifiers, email addresses, usernames, passwords, TOTP seeds/QR codes and machine-specific information.
- Use synthetic demo accounts and fabricated-but-clearly-labelled sample data.
- Review the full Git history for secrets; deleting a file in a later commit does not erase earlier commits.
- Publish tested source code and dependency versions only after an actual code review.
- Check academic-conduct requirements before publicly releasing assessed material.

## Vulnerability disclosure

Because the project is not intended for deployment, do not connect it to real accounts or expose it on the public internet. If the repository is published, use GitHub's private vulnerability reporting feature or contact its maintainer before disclosing sensitive findings.
