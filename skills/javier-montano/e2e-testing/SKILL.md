---
name: e2e-testing
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Write end-to-end tests with Playwright or Cypress — covering user flow testing,
  page objects, network mocking, and CI integration.
  Trigger: "e2e test", "Playwright", "Cypress", "user flow test"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# End-to-End Testing

> "If a user can break it, an e2e test should find it first." — Unknown

## TL;DR

Guides end-to-end test implementation with Playwright or Cypress — covering critical user flow testing, page object patterns, network request mocking, visual assertions, and CI integration. Use when you need to verify complete user journeys across your application.

## Procedure

### Step 1: Discover
- Identify critical user flows to test (sign-up, purchase, core features)
- Check existing e2e test infrastructure and framework
- Review CI pipeline for e2e test execution capacity
- Determine test environment requirements (staging, local, emulators)

### Step 2: Analyze
- Choose framework: Playwright (multi-browser, fast) vs Cypress (developer experience)
- Plan test scope: focus on critical paths, not exhaustive coverage
- Design page object or component model for reusable selectors
- Evaluate network mocking vs real API testing tradeoffs

### Step 3: Execute
- Set up Playwright/Cypress with TypeScript and project configuration
- Create page objects encapsulating selectors and actions
- Write tests for critical user flows using `data-testid` attributes
- Implement network mocking for external API dependencies
- Add visual assertions with screenshot comparison where appropriate
- Configure parallel test execution for faster CI runs
- Set up parallel browser matrix: Chromium + Firefox + WebKit for cross-browser coverage
- Set up test retries for handling transient failures (not masking real bugs)
- Configure post-deploy verification: run critical-path e2e suite against production URL
  using environment variable for target URL (`BASE_URL=https://yourdomain.com`)

### Step 4: Validate
- Run e2e suite against staging environment before production deploys
- Check test execution time — target under 10 minutes for full suite
- Verify tests are stable (no flaky failures over 10 consecutive runs)
- Confirm tests fail when application behavior regresses

## Quality Criteria

- [ ] Critical user flows covered (sign-up, login, core feature, payment)
- [ ] Page objects used for selector management and reusability
- [ ] Tests use `data-testid` attributes, not CSS selectors or text content
- [ ] E2e suite completes within CI time budget (typically under 15 minutes)
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Testing every feature with e2e (should be unit/integration tests instead)
- Using CSS selectors or XPath that break with styling changes
- Ignoring flaky tests instead of fixing root causes

## Related Skills

- `test-strategy` — E2e tests are the top of the test pyramid
- `accessibility-testing` — E2e tests can include a11y checks with axe integration
- `dual-layer-verification` — E2e infrastructure reused for runtime security verification
- `lighthouse-ci` — Performance verification in the same CI pipeline
- `bdd-full-spectrum` — Gherkin scenarios drive e2e test generation
