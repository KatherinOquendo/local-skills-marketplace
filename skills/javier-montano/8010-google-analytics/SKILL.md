---
name: google-analytics
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Implement Google Analytics 4 with custom events, conversion tracking, GTM
  integration, and data-driven insights for web applications. [EXPLICIT]
  Trigger: "google analytics", "GA4", "event tracking", "GTM", "conversions"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Google Analytics

> "Without data, you're just another person with an opinion." — W. Edwards Deming

## TL;DR

Guides Google Analytics 4 implementation — from initial setup through custom event tracking, conversion configuration, Google Tag Manager integration, and actionable reporting. Use when adding analytics to a web application or migrating from Universal Analytics to GA4. [EXPLICIT]

## Procedure

### Step 1: Discover
- Check existing analytics implementation (GA4, UA, other tools)
- Identify key user actions to track (sign-ups, purchases, feature usage)
- Review consent management requirements (GDPR, CCPA)
- Determine GTM vs direct gtag.js implementation preference

### Step 2: Analyze
- Define measurement plan: business goals → KPIs → metrics → events
- Design event taxonomy with consistent naming (snake_case, verb_noun)
- Plan custom dimensions and metrics for business-specific data
- Evaluate enhanced measurement events vs custom events needs

### Step 3: Execute
- Install GA4 via GTM or direct `gtag.js` snippet
- Configure enhanced measurement (scroll, outbound clicks, site search)
- Implement custom events: `gtag('event', 'sign_up', { method: 'google' })`
- Set up conversion events in GA4 admin
- Add user properties for segmentation (plan_type, account_age)
- Implement consent mode for GDPR compliance (`gtag('consent', 'update', {...})`)
- Configure GTM triggers and tags for complex tracking scenarios

### Step 4: Validate
- Use GA4 DebugView to verify events fire correctly with expected parameters
- Check GTM Preview mode for tag firing sequence
- Confirm conversions appear in GA4 reports within 24-48 hours
- Verify consent mode blocks tracking when consent is denied

## Quality Criteria

- [ ] Measurement plan documents all tracked events and their parameters
- [ ] Event naming follows consistent convention (snake_case recommended by GA4)
- [ ] Consent mode implemented for GDPR/CCPA compliance
- [ ] Conversion events configured for key business actions
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Tracking everything without a measurement plan (data overload, no insights)
- Using event names with spaces or mixed case (inconsistent reporting)
- Loading analytics scripts without consent management in regulated regions

## Related Skills

- `landing-pages` — conversion tracking is essential for landing page optimization
- `recaptcha-integration` — bot traffic skews analytics data

## Usage

Example invocations:

- "/google-analytics" — Run the full google analytics workflow
- "google analytics on this project" — Apply to current context


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
