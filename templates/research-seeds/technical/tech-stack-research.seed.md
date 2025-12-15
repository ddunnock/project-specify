# Technology Stack Research Seed File

> **Purpose:** Provide initial input about your project's technology choices to guide AI research
> **Status:** Draft | Complete
> **Last Updated:** [YYYY-MM-DD]

---

## Instructions

This seed file helps you document your technology preferences and constraints before the AI generates comprehensive tech stack research.

**How to use:**
1. Copy this file to `.specify/research-seeds/technical/tech-stack-research.seed.md`
2. Fill out the sections below
3. Run `/speckit.research` to generate full research document

---

## Programming Languages

**What languages are you considering or required to use?**

```
Example:
- Backend: Python (Django/FastAPI) or Node.js (Express)
- Frontend: TypeScript with React
- Infrastructure: Terraform (HCL)

Your choices:
- Backend:
- Frontend:
- Infrastructure:
- Other:
```

**Why these languages?**
```
Example:
- Team expertise in Python
- React has large ecosystem
- Company standard is TypeScript

Your reasons:
-
-
```

---

## Frameworks & Libraries

**What frameworks are you planning to use?**

### Backend Framework
```
Options considered:
- [ ] Django
- [ ] FastAPI
- [ ] Express.js
- [ ] Spring Boot
- [ ] Ruby on Rails
- [ ] ASP.NET Core
- [ ] Other: ___________

Preferred:

Why:
```

### Frontend Framework
```
Options considered:
- [ ] React
- [ ] Vue.js
- [ ] Angular
- [ ] Svelte
- [ ] Next.js
- [ ] Nuxt
- [ ] Other: ___________

Preferred:

Why:
```

### Key Libraries
```
Example:
- Forms: React Hook Form
- State: Redux Toolkit
- Styling: Tailwind CSS
- HTTP: Axios
- Testing: Jest + React Testing Library

Your libraries:
-
-
-
```

---

## Database Technology

**What database(s) will you use?**

```
Primary Database:
- [ ] PostgreSQL
- [ ] MySQL/MariaDB
- [ ] MongoDB
- [ ] SQL Server
- [ ] Oracle
- [ ] SQLite
- [ ] Other: ___________

Rationale:


Additional Databases/Stores:
- Cache: _________ (Redis, Memcached, etc.)
- Search: _________ (Elasticsearch, Algolia, etc.)
- Queue: _________ (RabbitMQ, Redis, SQS, etc.)
```

---

## Infrastructure & Hosting

**Where will the application run?**

```
Hosting Platform:
- [ ] AWS
- [ ] Azure
- [ ] Google Cloud Platform
- [ ] DigitalOcean
- [ ] Vercel/Netlify
- [ ] Heroku
- [ ] On-premise
- [ ] Other: ___________

Deployment Method:
- [ ] Containers (Docker/Kubernetes)
- [ ] Serverless (Lambda, Cloud Functions)
- [ ] Traditional VMs
- [ ] Platform-as-a-Service
- [ ] Bare metal

Why this choice:
-
-
```

---

## DevOps & CI/CD

**What tools for development and deployment?**

```
Version Control:
- Git hosting: _________ (GitHub, GitLab, Bitbucket)

CI/CD Pipeline:
- [ ] GitHub Actions
- [ ] GitLab CI
- [ ] Jenkins
- [ ] CircleCI
- [ ] Azure DevOps
- [ ] Other: ___________

Infrastructure as Code:
- [ ] Terraform
- [ ] CloudFormation
- [ ] Pulumi
- [ ] Ansible
- [ ] Other: ___________

Container Orchestration:
- [ ] Kubernetes
- [ ] Docker Swarm
- [ ] ECS/Fargate
- [ ] Not using containers
- [ ] Other: ___________
```

---

## Development Tools

**What tools will developers use?**

```
Package Managers:
- Backend: _________ (pip, npm, yarn, maven, etc.)
- Frontend: _________ (npm, yarn, pnpm)

Build Tools:
- Frontend: _________ (Vite, Webpack, esbuild)
- Backend: _________ (Make, setuptools, etc.)

Code Quality:
- Linter: _________ (ESLint, Pylint, etc.)
- Formatter: _________ (Prettier, Black, etc.)
- Type checker: _________ (TypeScript, mypy, etc.)

Testing Frameworks:
- Unit tests: _________
- Integration tests: _________
- E2E tests: _________
```

---

## Third-Party Services

**What external services will you integrate?**

```
Example:
- Authentication: Auth0
- Payments: Stripe
- Email: SendGrid
- File storage: AWS S3
- CDN: CloudFlare
- Analytics: Google Analytics
- Error tracking: Sentry
- Logging: Datadog

Your services:
-
-
-
```

---

## API & Communication

**How will services communicate?**

```
API Style:
- [ ] REST
- [ ] GraphQL
- [ ] gRPC
- [ ] WebSockets
- [ ] Server-Sent Events
- [ ] Other: ___________

API Documentation:
- [ ] OpenAPI/Swagger
- [ ] GraphQL Schema
- [ ] API Blueprint
- [ ] Other: ___________

Message Queue (if needed):
- [ ] RabbitMQ
- [ ] Apache Kafka
- [ ] Redis Pub/Sub
- [ ] AWS SQS
- [ ] Not needed
```

---

## Security Tools

**What security tools are required?**

```
- [ ] SSL/TLS certificates (Let's Encrypt, etc.)
- [ ] Secrets management (Vault, AWS Secrets Manager)
- [ ] WAF (Web Application Firewall)
- [ ] DDoS protection
- [ ] Security scanning (Snyk, SonarQube)
- [ ] Vulnerability monitoring

Specific tools:
-
-
```

---

## Monitoring & Observability

**How will you monitor the system?**

```
Application Monitoring:
- [ ] Datadog
- [ ] New Relic
- [ ] AppDynamics
- [ ] Custom solution
- [ ] Other: ___________

Logging:
- [ ] ELK Stack (Elasticsearch, Logstash, Kibana)
- [ ] CloudWatch Logs
- [ ] Splunk
- [ ] Grafana Loki
- [ ] Other: ___________

Error Tracking:
- [ ] Sentry
- [ ] Rollbar
- [ ] Bugsnag
- [ ] Other: ___________

Metrics & Dashboards:
- [ ] Grafana
- [ ] Prometheus
- [ ] CloudWatch
- [ ] Datadog
- [ ] Other: ___________
```

---

## Technology Constraints

**Are there any limitations or requirements?**

```
Example:
- Must use company-approved vendor list
- Open-source only (licensing restrictions)
- Must run in air-gapped environment
- Legacy system integration requires .NET
- Team only knows Python and JavaScript

Your constraints:
-
-
-
```

---

## Version Requirements

**Any specific version requirements?**

```
Example:
- Python 3.11+ (for latest features)
- Node.js 18 LTS (company standard)
- PostgreSQL 15+ (for JSON improvements)

Your requirements:
-
-
```

---

## Performance Requirements

**What performance characteristics matter?**

```
- [ ] Low latency (real-time)
- [ ] High throughput (batch processing)
- [ ] Scalability (handle growth)
- [ ] Memory efficiency
- [ ] Small bundle size (frontend)
- [ ] Fast startup time

Details:
-
-
```

---

## Compatibility Requirements

**What must the stack be compatible with?**

```
Browser Support:
- [ ] Latest 2 versions of major browsers
- [ ] IE11 support required
- [ ] Mobile browsers
- [ ] Progressive Web App support

Operating Systems:
- [ ] Linux
- [ ] Windows
- [ ] macOS
- [ ] Mobile (iOS/Android)

Other:
-
-
```

---

## License Considerations

**Are there licensing restrictions?**

```
- [ ] Open source only
- [ ] Permissive licenses only (MIT, Apache)
- [ ] Commercial licenses OK
- [ ] GPL-compatible required

Notes:
-
```

---

## Questions & Uncertainties

**What technology questions do you have?**

```
1.
2.
3.
```

---

## Additional Notes

Any other technology considerations:

```

```

---

**Next Steps:**
After filling out this seed file, run `/speckit.research` to generate a comprehensive tech stack research document with AI analysis, technology comparisons, and recommendations.
