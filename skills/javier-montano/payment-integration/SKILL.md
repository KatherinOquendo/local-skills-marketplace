---
name: payment-integration
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Integrate payment processing with Stripe Checkout, PayPal, subscription billing,
  webhook handling, and PCI compliance considerations.
  Trigger: "payment", "Stripe", "PayPal", "checkout", "subscription billing"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Payment Integration

> "Payment flows must be the most tested, most reliable, most boring code in your system." — Unknown

## TL;DR

Guides payment integration with Stripe and PayPal — Checkout sessions, subscription management, webhook-driven fulfillment, refund handling, and PCI compliance. Use when adding payment processing, subscription billing, or one-time purchases to your application.

## Procedure

### Step 1: Discover
- Identify payment types needed (one-time, recurring subscription, usage-based)
- Check Stripe/PayPal account setup and API key configuration
- Review product/price catalog requirements
- Determine tax, currency, and regional payment method requirements

### Step 2: Analyze
- Choose integration approach: Stripe Checkout (hosted) vs Stripe Elements (embedded)
- Plan subscription lifecycle: trial → active → past_due → canceled
- Design webhook-driven fulfillment (never trust client-side payment confirmation)
- Evaluate SCA (Strong Customer Authentication) requirements for EU

### Step 3: Execute
- Create Stripe products and prices via API or Dashboard
- Implement Checkout Session creation in Cloud Functions
- Set up webhook endpoint for payment events (`checkout.session.completed`, `invoice.paid`)
- Build subscription management: upgrade, downgrade, cancel, resume
- Handle payment failures with dunning (retry logic, customer notification)
- Implement refund processing via admin interface
- Store customer/subscription IDs in Firestore linked to user documents
- Use Stripe test mode and test card numbers for development

### Step 4: Validate
- Test complete purchase flow with Stripe test cards (success, decline, 3DS)
- Verify webhook processes all payment events correctly
- Confirm subscription lifecycle transitions work (trial end, payment failure, cancellation)
- Check that no raw card data touches your servers (PCI compliance)

## Quality Criteria

- [ ] Payment confirmation driven by webhooks, not client-side callbacks
- [ ] Stripe secret keys stored as Firebase secrets, never in client code
- [ ] Subscription status synced between Stripe and Firestore via webhooks
- [ ] All Stripe test scenarios covered (success, decline, 3D Secure, disputes)
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Confirming payment on the client side without webhook verification (users can skip payment)
- Exposing Stripe secret key in frontend code
- Building custom card input forms instead of using Stripe Elements (PCI scope increase)

## Related Skills

- `webhook-handling` — Stripe webhooks drive the payment fulfillment flow
- `ecommerce-frontend` — checkout UI that triggers payment processing
