# Workflow Research Seed File

> **Purpose:** Provide initial input about your project's business workflows to guide AI research
> **Status:** Draft | Complete
> **Last Updated:** [YYYY-MM-DD]

---

## Instructions

This seed file helps you document business processes and workflows before the AI generates comprehensive workflow research.

**How to use:**
1. Copy this file to `.specify/research-seeds/domain/workflow-research.seed.md`
2. Fill out the sections below
3. Run `/speckit.research` to generate full research document

---

## Primary Workflows

**What are the main business processes?**

List the key workflows that drive your business:

```
Example:
1. Customer Onboarding
2. Order Processing
3. Payment Collection
4. Fulfillment & Shipping
5. Returns & Refunds
6. Customer Support

Your workflows:
1.
2.
3.
4.
5.
```

---

## Workflow 1: [Name]

**Describe your first major workflow:**

```
Workflow Name:


Purpose:


Trigger: (What starts this workflow?)


Actors: (Who is involved?)
-
-

Steps:
1.
2.
3.
4.
5.

End State: (How does it conclude?)


Success Criteria:
-
-

Failure Scenarios:
-
-
```

---

## Workflow 2: [Name]

**Describe your second major workflow:**

```
Workflow Name:


Purpose:


Trigger:


Actors:
-
-

Steps:
1.
2.
3.
4.
5.

End State:


Success Criteria:
-
-

Failure Scenarios:
-
-
```

---

## Workflow 3: [Name]

**Describe your third major workflow:**

```
Workflow Name:


Purpose:


Trigger:


Actors:
-
-

Steps:
1.
2.
3.

End State:


Success Criteria:
-
-

Failure Scenarios:
-
-
```

---

## Decision Points

**What decisions are made in workflows?**

```
Example:
Workflow: Order Processing
Decision Point: Payment authorization result
- IF authorized → Proceed to fulfillment
- IF declined → Notify customer, hold order
- IF pending → Wait for manual review

Your decision points:
Workflow:
Decision:
Options:
-
-
```

---

## Parallel Activities

**What activities can happen simultaneously?**

```
Example:
In Order Fulfillment:
- Parallel: Pick items from warehouse + Generate shipping label
- Parallel: Send confirmation email + Update inventory

Your parallel activities:
-
-
```

---

## Handoffs Between Actors

**Who hands off work to whom?**

```
Example:
Customer → Sales Rep (places order)
Sales Rep → Warehouse (fulfillment request)
Warehouse → Shipping (ready to ship)
Shipping → Customer (delivery)

Your handoffs:
-
-
-
```

---

## Waiting States

**Where does work wait for external input?**

```
Example:
- Waiting for customer payment confirmation
- Waiting for supervisor approval
- Waiting for third-party API response
- Waiting for scheduled batch job

Your waiting states:
-
-
-
```

---

## Exception Handling

**What happens when things go wrong?**

```
Example:
Exception: Payment fails during checkout
Handling:
1. Retry payment once automatically
2. If fails again, notify customer
3. Hold order for 24 hours
4. Cancel if not resolved

Your exception handling:
Exception:
Handling:
-
-
```

---

## Workflow Dependencies

**What workflows depend on others?**

```
Example:
- Fulfillment cannot start until Order is Paid
- Refund cannot process until Return is Received
- Shipping cannot occur until Inventory is Reserved

Your dependencies:
-
-
-
```

---

## Workflow Duration

**How long do workflows typically take?**

```
Example:
- Customer Onboarding: 5-10 minutes
- Order Processing: 1-2 hours
- Shipping: 3-5 business days
- Refund Processing: 5-7 business days

Your durations:
-
-
-
```

---

## Automation Opportunities

**What steps could be automated?**

```
Example:
- Automated inventory check before order confirmation
- Automated shipping label generation
- Automated customer notifications
- Automated refund approval for amounts under $50

Your automation opportunities:
-
-
-
```

---

## Manual Interventions

**When is human judgment required?**

```
Example:
- Manual review for orders over $5000
- Manual approval for refunds outside policy
- Manual resolution of payment disputes
- Manual handling of hazardous materials

Your manual steps:
-
-
-
```

---

## Workflow Monitoring

**How are workflows tracked?**

```
What needs to be monitored:
- Average workflow completion time
- Number of workflows in each state
- Failure/exception rates
- Bottlenecks and delays

Metrics to track:
-
-
-
```

---

## Workflow Variations

**Are there different paths through the workflow?**

```
Example:
Standard Order:
Customer → Payment → Fulfillment → Shipping → Delivery

Expedited Order:
Customer → Payment → Priority Fulfillment → Express Shipping → Delivery

Your variations:
-
-
```

---

## Integration Points

**Where do workflows touch external systems?**

```
Example:
- Payment gateway for authorization
- Shipping carrier API for tracking
- Email service for notifications
- Inventory management system

Your integrations:
-
-
-
```

---

## SLA Requirements

**What service level agreements apply?**

```
Example:
- Orders must be processed within 24 hours
- Support tickets responded to within 2 hours
- Refunds issued within 5 business days

Your SLAs:
-
-
-
```

---

## Questions & Uncertainties

**What workflow questions do you have?**

```
1.
2.
3.
```

---

## Additional Notes

Any other workflow considerations:

```

```

---

**Next Steps:**
After filling out this seed file, run `/speckit.research` to generate a comprehensive workflow research document with AI analysis, process diagrams, and optimization recommendations.
