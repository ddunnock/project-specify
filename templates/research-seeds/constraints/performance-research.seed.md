# Performance Research Seed File

> **Purpose:** Provide initial input about performance requirements to guide AI research
> **Status:** Draft | Complete
> **Last Updated:** [YYYY-MM-DD]

---

## Instructions

This seed file helps you document performance requirements before the AI generates comprehensive performance research.

**How to use:**
1. Copy this file to `.specify/research-seeds/constraints/performance-research.seed.md`
2. Fill out the sections below
3. Run `/speckit.research` to generate full research document

---

## Performance Targets

**What are your performance goals?**

```
Page Load Time:
- Target: _________ (e.g., < 2 seconds)
- Measured: [ ] Time to First Byte (TTFB)  [ ] Largest Contentful Paint (LCP)  [ ] Time to Interactive (TTI)

API Response Time:
- Target: _________ (e.g., < 200ms for 95th percentile)
- Critical endpoints: _________

Database Query Time:
- Target: _________ (e.g., < 100ms for 99th percentile)

Background Job Processing:
- Target: _________ (e.g., < 5 minutes per job)
```

---

## Scalability Requirements

**How much load must the system handle?**

```
Current Load:
- Concurrent users: _________
- Requests per second: _________
- Data volume: _________
- Transactions per day: _________

Expected Growth (Year 1):
- Concurrent users: _________
- Requests per second: _________
- Data volume: _________
- Transactions per day: _________

Expected Growth (Year 3):
- Concurrent users: _________
- Requests per second: _________
- Data volume: _________
```

---

## Throughput Requirements

**How much data/work must be processed?**

```
Typical workload:
- Reads per second: _________
- Writes per second: _________
- Data ingestion rate: _________ (e.g., GB/hour)
- Batch processing: _________ (e.g., records/hour)

Peak workload:
- Peak hours: _________ (e.g., 9am-5pm Mon-Fri)
- Peak multiplier: _________ (e.g., 3x typical)
- Seasonal peaks: _________ (e.g., Black Friday, tax season)

Processing requirements:
- Real-time processing: [ ] Yes [ ] No
- Batch processing: [ ] Yes [ ] No
- Event-driven processing: [ ] Yes [ ] No
```

---

## Latency Requirements

**How fast must the system respond?**

```
User-facing operations:
- Search results: _________ (e.g., < 500ms)
- Form submission: _________ (e.g., < 1s)
- Page navigation: _________ (e.g., < 1s)
- Data updates: _________ (e.g., < 2s)

Background operations:
- Email sending: _________ (e.g., < 5 minutes)
- Report generation: _________ (e.g., < 10 minutes)
- Data exports: _________ (e.g., < 1 hour)

Third-party integrations:
- Payment processing: _________ (e.g., < 3s)
- External API calls: _________ (e.g., < 2s)
- Webhook delivery: _________ (e.g., < 10s)
```

---

## Availability Requirements

**What uptime is required?**

```
Service Level Agreement (SLA):
- Target uptime: _________% (e.g., 99.9% = 43 min downtime/month)
- Allowed downtime: _________ per month

Maintenance windows:
- Frequency: _________ (e.g., monthly)
- Duration: _________ (e.g., 2 hours)
- Timing: _________ (e.g., Sunday 2am-4am)

Critical vs. non-critical components:
- Critical (must be 99.9%+): _________
- Important (99% OK): _________
- Nice-to-have (95% OK): _________
```

---

## Reliability Requirements

**How reliable must the system be?**

```
Error rates:
- Acceptable error rate: _________% (e.g., < 0.1%)
- Maximum failure rate: _________% (e.g., < 1%)

Data integrity:
- [ ] Zero data loss tolerance
- [ ] Minimal data loss acceptable (specify: _________)
- [ ] Can reconstruct from backups

Disaster recovery:
- RTO (Recovery Time Objective): _________ (e.g., 4 hours)
- RPO (Recovery Point Objective): _________ (e.g., 1 hour of data loss max)
```

---

## Capacity Planning

**What capacity is needed?**

```
Storage capacity:
- Current: _________
- Year 1: _________
- Year 3: _________
- Growth rate: _________% per year

Compute capacity:
- CPU: _________ cores
- Memory: _________ GB
- Scaling method: [ ] Vertical [ ] Horizontal [ ] Both

Network capacity:
- Bandwidth: _________ Mbps/Gbps
- Data transfer: _________ GB/month
```

---

## Performance Bottlenecks

**What could limit performance?**

```
Known bottlenecks:
- [ ] Database queries
- [ ] External API calls
- [ ] File uploads/downloads
- [ ] Image/video processing
- [ ] Search operations
- [ ] Report generation
- [ ] Data imports/exports
- [ ] Other: ___________

Details:
-
-
```

---

## Optimization Priorities

**What must be optimized first?**

```
Priority 1 (Critical):
Operation:
Current performance:
Target performance:
Impact:

Priority 2 (High):
Operation:
Current performance:
Target performance:
Impact:

Priority 3 (Medium):
Operation:
Current performance:
Target performance:
Impact:
```

---

## Caching Strategy

**What should be cached?**

```
Cache layers:
- [ ] CDN (static assets)
- [ ] Application cache (API responses)
- [ ] Database query cache
- [ ] Session cache
- [ ] Full-page cache

Cache duration:
- Static assets: _________
- API responses: _________
- Database queries: _________
- Session data: _________

Cache invalidation:
Strategy: _________ (TTL, event-driven, manual)
```

---

## Database Performance

**What database performance is needed?**

```
Query performance:
- Read latency: _________ (e.g., < 50ms)
- Write latency: _________ (e.g., < 100ms)
- Complex query latency: _________ (e.g., < 500ms)

Database scaling:
- [ ] Read replicas
- [ ] Sharding
- [ ] Partitioning
- [ ] Connection pooling

Indexing strategy:
-
-
```

---

## Frontend Performance

**What frontend performance is needed?**

```
Core Web Vitals targets:
- LCP (Largest Contentful Paint): _________ (< 2.5s good)
- FID (First Input Delay): _________ (< 100ms good)
- CLS (Cumulative Layout Shift): _________ (< 0.1 good)

Bundle size:
- JavaScript: _________ KB (target)
- CSS: _________ KB (target)
- Images: _________ KB per page (target)

Optimization techniques:
- [ ] Code splitting
- [ ] Lazy loading
- [ ] Image optimization (WebP, AVIF)
- [ ] Tree shaking
- [ ] Minification
- [ ] Compression (Gzip, Brotli)
```

---

## Mobile Performance

**What mobile-specific performance is needed?**

```
Mobile network conditions:
- [ ] Must work on 3G
- [ ] Optimized for 4G
- [ ] Designed for 5G

Mobile considerations:
- [ ] Reduced bundle sizes
- [ ] Offline capabilities
- [ ] Progressive Web App (PWA)
- [ ] Adaptive loading based on connection

Mobile targets:
- Page load on 3G: _________
- App startup time: _________
```

---

## Load Testing

**How will performance be validated?**

```
Load test scenarios:
1. Normal load: _________ concurrent users
2. Peak load: _________ concurrent users
3. Stress test: _________ concurrent users (find breaking point)
4. Endurance test: _________ hours at _________ load

Testing tools:
- [ ] JMeter
- [ ] Gatling
- [ ] k6
- [ ] Artillery
- [ ] Locust
- [ ] Other: ___________

Test frequency:
- [ ] Before each release
- [ ] Monthly
- [ ] Quarterly
- [ ] After major changes
```

---

## Monitoring & Metrics

**What performance metrics will be tracked?**

```
Application metrics:
- [ ] Request/response times
- [ ] Error rates
- [ ] Throughput (req/sec)
- [ ] Active users
- [ ] Queue depths
- [ ] Job processing times

Infrastructure metrics:
- [ ] CPU utilization
- [ ] Memory usage
- [ ] Disk I/O
- [ ] Network I/O
- [ ] Database connections

Business metrics:
- [ ] Conversion rate
- [ ] Cart abandonment
- [ ] Search success rate
- [ ] Time to complete workflows

Alerting thresholds:
- CPU > _________% for _________ minutes
- Response time > _________ for _________ minutes
- Error rate > _________% for _________ minutes
```

---

## Performance Budget

**What are the performance limits?**

```
Time budget:
- Initial page load: _________ seconds
- Route transitions: _________ seconds
- API calls: _________ milliseconds

Size budget:
- Total page size: _________ MB
- JavaScript bundle: _________ KB
- CSS bundle: _________ KB
- Images per page: _________ KB

Request budget:
- HTTP requests per page: _________
- Third-party requests: _________
```

---

## Constraints

**What performance constraints exist?**

```
Technical constraints:
-
-

Budget constraints:
-
-

Infrastructure constraints:
-
-
```

---

## Questions & Uncertainties

**What performance questions do you have?**

```
1.
2.
3.
```

---

## Additional Notes

Any other performance considerations:

```

```

---

**Next Steps:**
After filling out this seed file, run `/speckit.research` to generate a comprehensive performance research document with AI analysis, performance optimization strategies, and monitoring recommendations.
