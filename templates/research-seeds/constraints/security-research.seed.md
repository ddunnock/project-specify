# Security Research Seed File

> **Purpose:** Provide initial input about security requirements to guide AI research
> **Status:** Draft | Complete
> **Last Updated:** [YYYY-MM-DD]

---

## Instructions

This seed file helps you document security requirements before the AI generates comprehensive security research.

**How to use:**
1. Copy this file to `.specify/research-seeds/constraints/security-research.seed.md`
2. Fill out the sections below
3. Run `/speckit.research` to generate full research document

---

## Security Threat Model

**What security threats are you concerned about?**

```
Check all that apply:
- [ ] Data breaches
- [ ] SQL injection
- [ ] Cross-site scripting (XSS)
- [ ] Cross-site request forgery (CSRF)
- [ ] DDoS attacks
- [ ] Man-in-the-middle attacks
- [ ] Phishing attacks
- [ ] Insider threats
- [ ] Ransomware
- [ ] API abuse
- [ ] Account takeover
- [ ] Other: ___________

Highest priority threats:
1.
2.
3.
```

---

## Authentication Requirements

**How will users authenticate?**

```
Authentication methods:
- [ ] Username/password
- [ ] Email/password
- [ ] Social login (Google, Facebook, etc.)
- [ ] SSO (Single Sign-On)
- [ ] SAML
- [ ] OAuth 2.0 / OpenID Connect
- [ ] Magic links (passwordless)
- [ ] Biometric
- [ ] Certificate-based
- [ ] Other: ___________

Multi-factor authentication (MFA):
- [ ] Required for all users
- [ ] Required for admin/privileged users
- [ ] Optional
- [ ] Not needed

MFA methods:
- [ ] SMS codes
- [ ] Authenticator app (TOTP)
- [ ] Email codes
- [ ] Hardware security keys (FIDO2/WebAuthn)
- [ ] Biometric
```

---

## Authorization Requirements

**How will access be controlled?**

```
Access control model:
- [ ] Role-Based Access Control (RBAC)
- [ ] Attribute-Based Access Control (ABAC)
- [ ] Mandatory Access Control (MAC)
- [ ] Discretionary Access Control (DAC)
- [ ] Rule-Based Access Control

Roles needed:
- [ ] Admin/Superuser
- [ ] Manager/Supervisor
- [ ] Standard user
- [ ] Read-only user
- [ ] Guest/anonymous
- [ ] Other: ___________

Permission granularity:
- [ ] Resource-level (e.g., per document)
- [ ] Feature-level (e.g., can export data)
- [ ] Action-level (e.g., create/read/update/delete)
- [ ] Field-level (e.g., hide sensitive fields)
```

---

## Data Protection

**What data needs protection?**

```
Sensitive data types:
- [ ] Personally Identifiable Information (PII)
- [ ] Payment card data
- [ ] Health information (PHI)
- [ ] Financial data
- [ ] Intellectual property
- [ ] Trade secrets
- [ ] Authentication credentials
- [ ] API keys/secrets
- [ ] Other: ___________

Protection methods:
- [ ] Encryption at rest
- [ ] Encryption in transit (TLS 1.3)
- [ ] Database encryption
- [ ] Field-level encryption
- [ ] Tokenization
- [ ] Data masking
- [ ] Hashing (passwords)
- [ ] Key management service

Encryption standards:
- Algorithm: _________ (AES-256, RSA, etc.)
- Key rotation: _________ (e.g., every 90 days)
- Key storage: _________ (AWS KMS, Vault, etc.)
```

---

## Network Security

**How will network traffic be secured?**

```
- [ ] HTTPS/TLS for all connections
- [ ] VPN for admin access
- [ ] Firewall rules
- [ ] Network segmentation
- [ ] DMZ for public-facing services
- [ ] API gateway
- [ ] Rate limiting
- [ ] IP whitelisting
- [ ] DDoS protection (CloudFlare, AWS Shield)

Network architecture:
-
-
```

---

## Application Security

**What application-level security is needed?**

```
Input validation:
- [ ] Server-side validation (all inputs)
- [ ] Client-side validation (UX only)
- [ ] Parameterized queries (SQL injection prevention)
- [ ] Output encoding (XSS prevention)
- [ ] File upload restrictions

Session management:
- [ ] Secure session cookies (HttpOnly, Secure, SameSite)
- [ ] Session timeout: _________ minutes
- [ ] Re-authentication for sensitive actions
- [ ] CSRF tokens

Security headers:
- [ ] Content-Security-Policy (CSP)
- [ ] X-Frame-Options (clickjacking prevention)
- [ ] X-Content-Type-Options
- [ ] Strict-Transport-Security (HSTS)
- [ ] Referrer-Policy
```

---

## API Security

**How will APIs be secured?**

```
API authentication:
- [ ] API keys
- [ ] JWT (JSON Web Tokens)
- [ ] OAuth 2.0
- [ ] mTLS (mutual TLS)
- [ ] HMAC signatures
- [ ] Other: ___________

API protection:
- [ ] Rate limiting (__ requests per minute)
- [ ] IP whitelisting
- [ ] Request signing
- [ ] Input validation
- [ ] Output filtering
- [ ] API versioning

API documentation security:
- [ ] Swagger/OpenAPI with authentication
- [ ] Internal-only documentation
- [ ] Redact sensitive endpoints
```

---

## Secrets Management

**How will secrets be managed?**

```
Secret types:
- [ ] Database credentials
- [ ] API keys
- [ ] Encryption keys
- [ ] OAuth client secrets
- [ ] Certificates
- [ ] Other: ___________

Storage method:
- [ ] Dedicated secrets manager (Vault, AWS Secrets Manager)
- [ ] Environment variables
- [ ] Encrypted configuration files
- [ ] Hardware Security Module (HSM)

Secret rotation:
- Frequency: _________
- Automated: [ ] Yes [ ] No
```

---

## Security Monitoring & Logging

**What security events need to be logged?**

```
Events to log:
- [ ] Failed login attempts
- [ ] Successful logins
- [ ] Authorization failures
- [ ] Data access (read/write/delete)
- [ ] Configuration changes
- [ ] Privilege escalation
- [ ] API calls
- [ ] Security setting changes

Log retention:
- Duration: _________
- Storage: _________
- Access controls: _________

Security monitoring:
- [ ] SIEM (Security Information and Event Management)
- [ ] Intrusion Detection System (IDS)
- [ ] Intrusion Prevention System (IPS)
- [ ] File Integrity Monitoring (FIM)
- [ ] Anomaly detection
- [ ] Real-time alerting

Tools:
-
-
```

---

## Vulnerability Management

**How will vulnerabilities be managed?**

```
Scanning:
- [ ] Dependency scanning (npm audit, Snyk, etc.)
- [ ] Static Application Security Testing (SAST)
- [ ] Dynamic Application Security Testing (DAST)
- [ ] Container scanning
- [ ] Infrastructure scanning
- [ ] Penetration testing

Scan frequency:
- [ ] Continuous (CI/CD)
- [ ] Weekly
- [ ] Monthly
- [ ] Quarterly

Remediation SLA:
- Critical: _________ (e.g., 24 hours)
- High: _________
- Medium: _________
- Low: _________
```

---

## Incident Response

**What's the plan for security incidents?**

```
Incident response team:
-
-

Incident severity levels:
- [ ] Critical (data breach, system compromise)
- [ ] High (attempted breach, significant vulnerability)
- [ ] Medium (suspicious activity)
- [ ] Low (minor security event)

Response procedures:
1.
2.
3.
4.

Escalation path:
-
-

Communication plan:
-
-
```

---

## Third-Party Security

**What security is required for integrations?**

```
Third-party services:
Service: _________
Security requirements: _________
Audit status: _________

Service: _________
Security requirements: _________
Audit status: _________

Vendor security assessment:
- [ ] SOC 2 Type II required
- [ ] ISO 27001 certification required
- [ ] Security questionnaire
- [ ] Penetration test results
- [ ] SLA for security incidents
```

---

## Backup & Recovery

**How is data backed up securely?**

```
Backup strategy:
- Frequency: _________
- Retention: _________
- Location: _________
- Encryption: [ ] Yes [ ] No

Recovery testing:
- [ ] Quarterly disaster recovery drills
- [ ] Annual recovery testing
- [ ] RTO (Recovery Time Objective): _________
- [ ] RPO (Recovery Point Objective): _________
```

---

## Security Training

**What security training is needed?**

```
Training for:
- [ ] Developers (secure coding)
- [ ] Operations (secure deployment)
- [ ] All staff (security awareness)
- [ ] Executives (risk management)

Training frequency:
- [ ] During onboarding
- [ ] Annual refresher
- [ ] After incidents
- [ ] Continuous

Topics:
-
-
```

---

## Compliance Alignment

**What security standards must be met?**

```
Standards:
- [ ] OWASP Top 10
- [ ] CIS Controls
- [ ] NIST Cybersecurity Framework
- [ ] ISO 27001
- [ ] PCI-DSS
- [ ] SOC 2
- [ ] FedRAMP
- [ ] Other: ___________
```

---

## Questions & Uncertainties

**What security questions do you have?**

```
1.
2.
3.
```

---

## Additional Notes

Any other security considerations:

```

```

---

**Next Steps:**
After filling out this seed file, run `/speckit.research` to generate a comprehensive security research document with AI analysis, threat modeling, and security architecture recommendations.
