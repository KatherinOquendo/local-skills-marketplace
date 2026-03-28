---
name: firebase-extensions
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Install and configure Firebase Extensions for common tasks — Stripe payments,
  Algolia search, image resizing, and translation services. [EXPLICIT]
  Trigger: "firebase extension", "stripe extension", "algolia extension", "resize images"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Firebase Extensions

> "Don't build what's already been built — extend it." — Unknown

## TL;DR

Guides the selection, installation, and configuration of Firebase Extensions — pre-built solutions for common tasks like Stripe payments, Algolia search indexing, image resizing, email sending, and text translation. Use when a well-maintained extension can replace custom Cloud Function code. [EXPLICIT]

## Procedure

### Step 1: Discover
- Browse Firebase Extensions marketplace for available solutions
- Identify project needs that match existing extensions
- Check extension requirements (Blaze plan, specific Firebase services)
- Review extension source code and update frequency on GitHub

### Step 2: Analyze
- Evaluate extension vs custom implementation (maintenance burden, flexibility)
- Check configuration parameters and their impact on billing
- Plan integration points (Firestore collections, Storage paths, Auth events)
- Assess extension limitations and whether they meet edge case requirements

### Step 3: Execute
- Install extension via Firebase CLI: `firebase ext:install firebase/firestore-stripe-payments`
- Configure parameters (collection paths, API keys, feature toggles)
- Set up required secrets (Stripe API key, Algolia credentials)
- Test extension behavior in emulator or staging environment
- Integrate extension output with existing application logic
- Document extension configuration for team reference

### Step 4: Validate
- Verify extension triggers fire and produce expected results
- Check billing impact in Firebase Console (extensions use Cloud Functions quota)
- Confirm extension doesn't conflict with existing Cloud Functions
- Test extension behavior with edge cases (large files, concurrent writes)

## Quality Criteria

- [ ] Extension configured with appropriate collection paths and parameters
- [ ] Secrets stored via Firebase extension secret management
- [ ] Extension behavior tested in staging before production deployment
- [ ] Billing impact assessed and monitored
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Installing extensions without understanding their Cloud Functions quota usage
- Customizing extension code directly (fork instead; updates will overwrite changes)
- Using extensions for critical paths without understanding their failure modes

## Related Skills

- `payment-integration` — Stripe extension handles subscription lifecycle
- `image-optimization` — Resize Images extension for automatic thumbnails

## Usage

Example invocations:

- "/firebase-extensions" — Run the full firebase extensions workflow
- "firebase extensions on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
