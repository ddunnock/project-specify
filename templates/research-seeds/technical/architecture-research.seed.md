# Architecture Research Seed File

> **Purpose:** Provide initial input about your project's system architecture to guide AI research
> **Status:** Draft | Complete
> **Last Updated:** [YYYY-MM-DD]

---

## Instructions

This seed file helps you document your system architecture vision before the AI generates comprehensive architecture research. Fill out what you know - incomplete is fine!

**How to use:**
1. Copy this file to `.specify/research-seeds/technical/architecture-research.seed.md`
2. Fill out the sections below
3. Leave sections blank if uncertain
4. Run `/speckit.research` to generate full research document

---

## System Architecture Type

**What type of architecture are you considering?**

Check all that apply:
- [ ] Monolithic (single deployable application)
- [ ] Microservices (multiple independent services)
- [ ] Serverless (functions-as-a-service)
- [ ] Modular monolith (single deployment, modular code)
- [ ] Event-driven architecture
- [ ] Layered architecture (n-tier)
- [ ] Hexagonal/Clean architecture
- [ ] Other: ___________

**Why this approach?**
```

```

---

## Major System Components

**What are the main building blocks of your system?**

List the major components and their responsibilities:

```
Example:
1. Web Application (Frontend)
   - User interface
   - Client-side validation
   - State management

2. API Server (Backend)
   - Business logic
   - Data access
   - Authentication/authorization

3. Background Workers
   - Email sending
   - Report generation
   - Data imports

Your components:
1.

2.

3.
```

---

## Component Communication

**How do components talk to each other?**

```
Example:
- Frontend → API: REST over HTTPS
- API → Database: SQL queries
- API → Workers: Message queue (RabbitMQ)
- Workers → External Services: HTTP webhooks

Your communication:
-
-
-
```

---

## Integration Points

**What external systems does your project integrate with?**

```
Example:
- Stripe API (payments)
- SendGrid API (email)
- S3 (file storage)
- Google Maps API (geocoding)

Your integrations:
-
-
-
```

---

## Deployment Architecture

**How will the system be deployed?**

- [ ] Cloud (AWS, Azure, GCP)
- [ ] On-premise
- [ ] Hybrid
- [ ] Containers (Docker/Kubernetes)
- [ ] Traditional VMs
- [ ] Platform-as-a-Service (Heroku, Vercel, etc.)

**Deployment details:**
```
Example:
- Platform: AWS
- Frontend: CloudFront + S3
- Backend: ECS with Fargate
- Database: RDS PostgreSQL
- Cache: ElastiCache Redis

Your deployment:
- Platform:
- Components:
-
-
```

---

## Scalability Requirements

**How should the system scale?**

```
Example:
- Must handle 10,000 concurrent users
- Horizontal scaling for API servers
- Read replicas for database
- CDN for static assets
- Load balancer for high availability

Your requirements:
-
-
-
```

---

## High Availability & Resilience

**What are your uptime requirements?**

```
Target uptime: ___% (e.g., 99.9% = ~43 minutes downtime/month)

Resilience strategies:
- [ ] Multiple availability zones
- [ ] Automated failover
- [ ] Circuit breakers
- [ ] Graceful degradation
- [ ] Health checks & auto-recovery
- [ ] Backup & disaster recovery

Details:
-
-
```

---

## Security Architecture

**What security measures are needed?**

```
- [ ] API authentication (JWT, OAuth, etc.)
- [ ] API authorization (RBAC, ABAC)
- [ ] Encryption at rest
- [ ] Encryption in transit (TLS)
- [ ] WAF (Web Application Firewall)
- [ ] DDoS protection
- [ ] Security scanning & monitoring
- [ ] Secrets management (Vault, AWS Secrets Manager)

Details:
-
-
```

---

## Data Flow Architecture

**How does data flow through the system?**

Describe the main data paths:

```
Example:
Write Path:
User → Frontend → API Gateway → Service → Database → Cache invalidation

Read Path:
User → Frontend → CDN (cache hit) OR API → Cache (hit) OR Database (miss)

Your flows:
-
-
```

---

## State Management

**Where is application state stored?**

```
- [ ] Database (persistent state)
- [ ] Cache (temporary state)
- [ ] Client-side (browser/mobile app)
- [ ] Session store
- [ ] Distributed cache
- [ ] In-memory (application state)

Details:
-
-
```

---

## Component Diagram

**Can you sketch the architecture?**

If you have a rough diagram or ASCII art, include it here:

```
Example:

┌─────────┐        ┌─────────┐
│ Browser │───────▶│   CDN   │
└─────────┘        └─────────┘
                        │
                        ▼
                   ┌─────────┐
                   │   API   │
                   └─────────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
        ┌──────────┐        ┌──────────┐
        │ Database │        │  Cache   │
        └──────────┘        └──────────┘

Your diagram:


```

---

## Technology Constraints

**Are there any architectural constraints?**

```
Example:
- Must use existing Azure infrastructure
- Cannot use serverless (compliance requirement)
- Must support air-gapped deployment
- Limited to open-source technologies

Your constraints:
-
-
```

---

## Patterns & Practices

**What architectural patterns are you considering?**

```
Example:
- CQRS (Command Query Responsibility Segregation)
- Event sourcing
- API Gateway pattern
- Backend-for-Frontend (BFF)
- Strangler Fig (gradual migration)

Your patterns:
-
-
```

---

## Cross-Cutting Concerns

**How will you handle these across the system?**

```
Logging:
-

Monitoring:
-

Error handling:
-

Caching:
-

Configuration:
-
```

---

## Questions & Uncertainties

**What architectural questions do you have?**

```
1.
2.
3.
```

---

## Additional Notes

Any other architectural considerations:

```

```

---

**Next Steps:**
After filling out this seed file, run `/speckit.research` to generate a comprehensive architecture research document with AI analysis, technology recommendations, and architectural patterns.
