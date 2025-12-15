# Compliance Research Seed File

> **Purpose:** Provide initial input about regulatory and compliance requirements to guide AI research
> **Status:** Draft | Complete
> **Last Updated:** [YYYY-MM-DD]

---

## Instructions

This seed file helps you document compliance requirements before the AI generates comprehensive compliance research.

**How to use:**
1. Copy this file to `.specify/research-seeds/constraints/compliance-research.seed.md`
2. Fill out the sections below
3. Run `/speckit.research` to generate full research document

---

## Applicable Regulations

**What laws and regulations apply to your project?**

```
Check all that apply:
- [ ] GDPR (General Data Protection Regulation - EU)
- [ ] CCPA (California Consumer Privacy Act)
- [ ] HIPAA (Health Insurance Portability and Accountability Act)
- [ ] PCI-DSS (Payment Card Industry Data Security Standard)
- [ ] SOC 2 (System and Organization Controls 2)
- [ ] COPPA (Children's Online Privacy Protection Act)
- [ ] FERPA (Family Educational Rights and Privacy Act)
- [ ] SOX (Sarbanes-Oxley Act)
- [ ] FISMA (Federal Information Security Management Act)
- [ ] FedRAMP (Federal Risk and Authorization Management Program)
- [ ] ISO 27001 (Information Security Management)
- [ ] WCAG (Web Content Accessibility Guidelines)
- [ ] ADA (Americans with Disabilities Act)
- [ ] Other: ___________

Details:
-
-
-
```

---

## Industry-Specific Compliance

**What industry standards must be followed?**

```
Industry:


Relevant standards:
-
-
-

Regulatory bodies:
-
-
```

---

## Data Privacy Requirements

**What data privacy laws apply?**

```
GDPR Requirements (if applicable):
- [ ] Right to access
- [ ] Right to deletion (Right to be forgotten)
- [ ] Right to data portability
- [ ] Right to rectification
- [ ] Consent management
- [ ] Data breach notification (72 hours)
- [ ] Privacy by design
- [ ] Data Protection Impact Assessment (DPIA)

CCPA Requirements (if applicable):
- [ ] Right to know what data is collected
- [ ] Right to delete personal information
- [ ] Right to opt-out of data sales
- [ ] Non-discrimination for exercising rights

Other privacy requirements:
-
-
```

---

## Data Residency Requirements

**Where must data be stored?**

```
Geographic restrictions:
- [ ] Data must stay in specific country/region: ___________
- [ ] No data transfer outside jurisdiction
- [ ] Data localization required
- [ ] Cloud region restrictions

Rationale:


```

---

## Healthcare Compliance (HIPAA)

**If healthcare data is involved:**

```
- [ ] Handles Protected Health Information (PHI)
- [ ] Requires Business Associate Agreement (BAA)
- [ ] Needs HIPAA-compliant hosting
- [ ] Audit logging required
- [ ] Access controls required
- [ ] Encryption at rest and in transit
- [ ] Breach notification procedures

PHI data types:
-
-
```

---

## Payment Compliance (PCI-DSS)

**If processing payments:**

```
PCI-DSS Level:
- [ ] Level 1 (6M+ transactions/year)
- [ ] Level 2 (1-6M transactions/year)
- [ ] Level 3 (20K-1M e-commerce transactions/year)
- [ ] Level 4 (<20K e-commerce transactions/year)

Requirements:
- [ ] Cardholder data must not be stored
- [ ] Use approved payment gateway
- [ ] Annual compliance validation
- [ ] Quarterly vulnerability scans
- [ ] Secure network architecture

Payment processor:

```

---

## Accessibility Compliance

**What accessibility standards must be met?**

```
Standards:
- [ ] WCAG 2.1 Level A
- [ ] WCAG 2.1 Level AA
- [ ] WCAG 2.1 Level AAA
- [ ] Section 508 compliance
- [ ] ADA Title III compliance
- [ ] EN 301 549 (European standard)

Requirements:
- [ ] Screen reader compatibility
- [ ] Keyboard navigation
- [ ] Color contrast ratios
- [ ] Text alternatives for images
- [ ] Captions for video content
- [ ] Accessible forms

User groups requiring accommodation:
-
-
```

---

## Audit Requirements

**What auditing is required?**

```
Audit types needed:
- [ ] SOC 2 Type I (point-in-time)
- [ ] SOC 2 Type II (6-12 month period)
- [ ] ISO 27001 certification
- [ ] PCI-DSS compliance scan
- [ ] HIPAA compliance audit
- [ ] Internal security audit
- [ ] Other: ___________

Audit frequency:
- Annual: ___________
- Quarterly: ___________
- Continuous: ___________

Audit evidence requirements:
-
-
```

---

## Record Retention

**How long must records be kept?**

```
Example:
- Financial records: 7 years (SOX/IRS)
- Medical records: 6 years (HIPAA)
- Employee records: 3 years post-termination
- Audit logs: 1 year minimum

Your retention requirements:
Data type: ___________ | Retention period: ___________
Data type: ___________ | Retention period: ___________
Data type: ___________ | Retention period: ___________
```

---

## Consent Management

**What consent is required?**

```
Consent types:
- [ ] Marketing communications opt-in
- [ ] Cookie consent
- [ ] Data processing consent
- [ ] Terms of service acceptance
- [ ] Privacy policy acceptance
- [ ] Age verification (COPPA: 13+, GDPR: 16+)
- [ ] Parental consent for minors

Consent requirements:
- [ ] Must be freely given
- [ ] Must be specific and informed
- [ ] Must be unambiguous
- [ ] Must be withdrawable
- [ ] Must be documented

Opt-out requirements:
-
-
```

---

## Data Breach Requirements

**What must happen if data is breached?**

```
Notification timeline:
- [ ] 72 hours (GDPR)
- [ ] "Without unreasonable delay" (CCPA)
- [ ] 60 days (HIPAA)
- [ ] Other: ___________

Who must be notified:
- [ ] Affected individuals
- [ ] Regulatory authority
- [ ] Law enforcement
- [ ] Media (if large breach)
- [ ] Business partners

Breach response plan:
-
-
```

---

## Cross-Border Data Transfer

**Can data be transferred internationally?**

```
Transfer mechanisms:
- [ ] Standard Contractual Clauses (SCCs)
- [ ] Privacy Shield (US-EU) - invalidated, use SCCs
- [ ] Binding Corporate Rules (BCRs)
- [ ] Adequacy decisions
- [ ] Other: ___________

Restricted countries:
-
-
```

---

## Age Restrictions

**Are there age-related requirements?**

```
- [ ] COPPA (US): Must get parental consent for users under 13
- [ ] GDPR (EU): Age of consent is 16 (or lower as set by member state)
- [ ] Age verification required for: ___________

Age gate implementation:
-
```

---

## Compliance Documentation

**What documentation is required?**

```
Required documents:
- [ ] Privacy Policy
- [ ] Terms of Service
- [ ] Cookie Policy
- [ ] Data Processing Agreement (DPA)
- [ ] Business Associate Agreement (BAA)
- [ ] Security Policy
- [ ] Incident Response Plan
- [ ] Data Retention Policy

Review/update frequency:
-
```

---

## Penalties for Non-Compliance

**What are the consequences?**

```
GDPR: Up to €20M or 4% of global revenue
HIPAA: $100-$50,000 per violation, up to $1.5M annually
PCI-DSS: Fines from payment processors, loss of processing ability
CCPA: $2,500-$7,500 per violation

Your specific risks:
-
-
```

---

## Compliance Certifications Needed

**What certifications are required or beneficial?**

```
- [ ] SOC 2 Type II
- [ ] ISO 27001
- [ ] HITRUST (healthcare)
- [ ] FedRAMP (US government)
- [ ] CSA STAR (cloud security)
- [ ] Other: ___________

Business rationale:
-
-
```

---

## Questions & Uncertainties

**What compliance questions do you have?**

```
1.
2.
3.
```

---

## Additional Notes

Any other compliance considerations:

```

```

---

**Next Steps:**
After filling out this seed file, run `/speckit.research` to generate a comprehensive compliance research document with AI analysis, requirement mapping, and implementation guidance.
