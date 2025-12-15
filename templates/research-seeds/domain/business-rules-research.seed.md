# Business Rules Research Seed File

> **Purpose:** Provide initial input about your project's business rules to guide AI research
> **Status:** Draft | Complete
> **Last Updated:** [YYYY-MM-DD]

---

## Instructions

This seed file helps you document business rules and logic before the AI generates comprehensive business rules research.

**How to use:**
1. Copy this file to `.specify/research-seeds/domain/business-rules-research.seed.md`
2. Fill out the sections below
3. Run `/speckit.research` to generate full research document

---

## Core Business Rules

**What are the fundamental business rules?**

List the key rules that govern how the business operates:

```
Example (E-commerce):
1. A customer must be logged in to place an order
2. Products cannot be sold if inventory is 0
3. Discount codes can only be used once per customer
4. Free shipping applies for orders over $50
5. Refunds must be requested within 30 days

Your rules:
1.
2.
3.
4.
5.
```

---

## Validation Rules

**What data validation rules are required?**

```
Example:
- Email addresses must be valid format
- Phone numbers must be 10 digits (US)
- Passwords must be 8+ characters with uppercase, lowercase, number
- Credit card expiry must be future date
- Order total must be greater than $0

Your validation rules:
-
-
-
```

---

## Calculation Rules

**How are calculated values determined?**

```
Example:
Order Total Calculation:
- Subtotal = sum(item price × quantity)
- Tax = subtotal × tax rate (by state)
- Shipping = calculated by weight and distance
- Discount = apply percentage off subtotal
- Total = subtotal + tax + shipping - discount

Your calculations:
1.


2.


3.

```

---

## Workflow Rules

**What rules govern process flows?**

```
Example:
Order Processing Rules:
- Order cannot be shipped until payment is confirmed
- Order cannot be cancelled after shipping
- Returns require original packaging
- Exchanges must be same or higher value

Your workflow rules:
-
-
-
```

---

## Authorization Rules

**Who can do what?**

```
Example:
- Admin: Full access to all functions
- Manager: Can approve refunds up to $500
- Customer Service: Can view orders, update status
- Customer: Can view own orders only

Your authorization rules:
Role 1:
-
-

Role 2:
-
-
```

---

## Business Logic Rules

**What complex logic governs the system?**

```
Example:
Pricing Rules:
- VIP customers get 10% off all orders
- Buy 2 get 1 free on selected items
- Flash sales override all other discounts
- Student discount cannot combine with other offers

Your business logic:
-
-
-
```

---

## Conditional Rules

**What if-then rules apply?**

```
Example:
IF customer is first-time buyer THEN apply 15% welcome discount
IF order total > $100 THEN free shipping
IF payment fails THEN hold order for 24 hours before cancelling
IF product is hazmat THEN only ground shipping allowed

Your conditional rules:
IF _________ THEN _________
IF _________ THEN _________
IF _________ THEN _________
```

---

## Constraints & Limits

**What limits or boundaries exist?**

```
Example:
- Maximum 10 items per order line
- Minimum order amount: $5
- Maximum discount: 50% off
- Account creation: 3 failed attempts = 15 min lockout
- Session timeout: 30 minutes of inactivity

Your constraints:
-
-
-
```

---

## Time-Based Rules

**What rules depend on time or date?**

```
Example:
- Orders placed before 2pm ship same day
- Sale prices valid for 48 hours
- Subscription renewal 7 days before expiry
- Invoice payment due within 30 days
- Data retention: delete after 7 years

Your time-based rules:
-
-
-
```

---

## State Transition Rules

**What are valid state changes?**

```
Example (Order States):
Draft → Submitted → Paid → Processing → Shipped → Delivered
                 → Cancelled (only if not Processing yet)

Invalid transitions:
- Cannot go from Shipped to Cancelled
- Cannot go from Delivered back to Processing

Your state machines:
Entity:
States:
Allowed transitions:
-
-
```

---

## Exception Rules

**When can rules be overridden?**

```
Example:
- Manager can approve refund past 30-day window (with reason)
- Admin can manually adjust inventory (audit logged)
- Customer service can waive shipping fee (supervisor approval)

Your exceptions:
-
-
-
```

---

## Compliance Rules

**What regulatory rules must be followed?**

```
Example:
- Age verification required for alcohol sales (21+)
- PCI-DSS: Cannot store CVV numbers
- GDPR: Must allow data export and deletion
- COPPA: Parental consent for users under 13

Your compliance rules:
-
-
-
```

---

## Business Rule Conflicts

**Are there any conflicting rules to resolve?**

```
Example:
Conflict: VIP discount (10%) vs Flash Sale (20%)
Resolution: Flash sale takes precedence

Your conflicts:
-
-
```

---

## Rule Precedence

**What order are rules evaluated?**

```
Example:
1. Check payment fraud rules (highest priority)
2. Apply flash sale pricing
3. Apply customer-specific discounts
4. Apply promotional codes
5. Calculate taxes (lowest priority)

Your precedence:
1.
2.
3.
```

---

## Dynamic Rules

**What rules can change at runtime?**

```
Example:
- Tax rates change based on customer location (lookup)
- Shipping costs vary by carrier availability
- Product prices adjust based on demand (surge pricing)
- Inventory allocated on first-come-first-served

Your dynamic rules:
-
-
-
```

---

## Questions & Uncertainties

**What business rule questions do you have?**

```
1.
2.
3.
```

---

## Additional Notes

Any other business rule considerations:

```

```

---

**Next Steps:**
After filling out this seed file, run `/speckit.research` to generate a comprehensive business rules document with AI analysis, rule formalization, and implementation recommendations.
