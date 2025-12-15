# Data Research Seed File

> **Purpose:** Provide initial input about your project's data requirements to guide AI research
> **Status:** Draft | Complete
> **Last Updated:** [YYYY-MM-DD]

---

## Instructions

This seed file helps you document your project's data needs before the AI generates comprehensive data research. Fill out as much as you can - incomplete sections are fine! The AI will ask clarifying questions during the `/speckit.research` phase.

**How to use:**
1. Copy this file to `.specify/research-seeds/technical/data-research.seed.md`
2. Fill out the sections below with what you know
3. Leave sections blank if uncertain - the AI will help
4. Run `/speckit.research` to generate full research document

---

## Data Entities

**What data does your system manage?**

List the main "things" your system tracks (e.g., Users, Products, Orders, Invoices, etc.):

```
Example:
- Users: People who use the system
- Products: Items for sale
- Orders: Purchase transactions

Your entities:
1.
2.
3.
```

---

## Entity Relationships

**How do these entities relate to each other?**

Describe the connections between entities:

```
Example:
- A User can place many Orders (1:many)
- An Order contains many Products (many:many)
- Each Product belongs to one Category (many:1)

Your relationships:
1.
2.
3.
```

---

## Key Attributes

**What information do you need to track for each entity?**

For each major entity, list important attributes/fields:

```
Example:
User:
- email (unique, required)
- name
- created_at
- subscription_type (free|premium|enterprise)

Your attributes:
Entity 1:
-
-

Entity 2:
-
-
```

---

## Storage Requirements

**Where and how should data be stored?**

Check all that apply:
- [ ] Relational database (PostgreSQL, MySQL, etc.)
- [ ] Document database (MongoDB, etc.)
- [ ] Key-value store (Redis, etc.)
- [ ] File storage (S3, local filesystem)
- [ ] Graph database
- [ ] Time-series database
- [ ] Other: ___________

**Constraints:**
```
Example:
- Must support ACID transactions
- Needs full-text search capability
- Should handle 10k+ records per entity

Your constraints:
-
-
```

---

## Data Flow

**How does data move through the system?**

Describe the main data flows:

```
Example:
1. User submits form → API validates → Database stores
2. External service sends webhook → Queue processes → Database updates
3. Batch job reads CSV → Transforms → Database imports

Your flows:
1.
2.
3.
```

---

## Data Volume & Growth

**How much data will you handle?**

```
Example:
- Initial: 1,000 users, 5,000 products
- Year 1: 10,000 users, 50,000 products
- Expected growth: 50% per year

Your estimates:
- Initial:
- Year 1:
- Growth rate:
```

---

## Data Migration

**Is there existing data to migrate?**

- [ ] No existing data (greenfield project)
- [ ] Yes, from existing system

If yes, provide details:
```
- Source system:
- Data format:
- Volume:
- Challenges:
```

---

## Data Retention & Archival

**How long should data be kept?**

```
Example:
- User data: 7 years (regulatory requirement)
- Logs: 90 days
- Deleted items: 30 days soft-delete before purge

Your policies:
-
-
```

---

## Data Privacy & Security

**What data requires special protection?**

```
Example:
- PII (Personally Identifiable Information): email, name, address
- Payment data: credit card numbers (PCI-DSS compliance)
- Health data: medical records (HIPAA compliance)

Your sensitive data:
-
-
-
```

---

## Special Considerations

**Any unique data requirements?**

```
Example:
- Multi-tenancy: Data must be isolated per organization
- Versioning: Need to track historical changes
- Soft deletes: Never permanently delete records
- Audit trail: Track who changed what and when

Your considerations:
-
-
```

---

## Questions & Uncertainties

**What are you unsure about?**

List questions you have about data design:

```
1.
2.
3.
```

---

## Additional Notes

Any other information about data that might be helpful:

```

```

---

**Next Steps:**
After filling out this seed file, run `/speckit.research` to generate a comprehensive data research document with AI analysis, recommendations, and technology suggestions.
