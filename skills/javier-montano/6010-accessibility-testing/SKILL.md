---
name: accessibility-testing
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Test web accessibility with axe-core, screen reader testing, keyboard
  navigation, and color contrast validation for WCAG compliance. [EXPLICIT]
  Trigger: "accessibility", "a11y", "WCAG", "screen reader", "axe-core"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Accessibility Testing

> "The power of the web is in its universality. Access by everyone regardless of disability is an essential aspect." — Tim Berners-Lee

## TL;DR

Guides comprehensive accessibility testing — automated scanning with axe-core, manual keyboard navigation testing, screen reader verification, color contrast validation, and WCAG 2.1 AA compliance checking. Use when auditing, building, or maintaining accessible web applications. [EXPLICIT]

## Procedure

### Step 1: Discover
- Run axe-core scan on all key pages and interactive components
- Check current WCAG compliance level and known issues
- Identify dynamic content that needs ARIA live regions
- Review form error handling and label associations

### Step 2: Analyze
- Categorize findings by WCAG level (A, AA, AAA) and severity
- Prioritize fixes: critical (blocks usage) → high (major difficulty) → medium → low
- Identify patterns requiring manual testing (focus management, screen reader flow)
- Evaluate color contrast ratios for all text/background combinations

### Step 3: Execute
- Integrate axe-core into unit tests (jest-axe) and e2e tests (Playwright axe)
- Fix semantic HTML issues (headings hierarchy, landmark regions, list structure)
- Add ARIA attributes where native HTML semantics are insufficient
- Ensure all interactive elements are keyboard accessible (Tab, Enter, Space, Escape)
- Implement focus management for dynamic content (modals, route changes, notifications)
- Verify color contrast meets WCAG AA (4.5:1 normal text, 3:1 large text)
- Test with screen readers (VoiceOver on Mac, NVDA on Windows)

### Step 4: Validate
- axe-core reports zero violations on all pages
- Complete keyboard-only navigation test of all user flows
- Screen reader announces all content in logical order
- Reduced motion preference disables animations

## Quality Criteria

- [ ] axe-core integrated in CI — zero automated violations
- [ ] All interactive elements keyboard accessible with visible focus indicators
- [ ] Color contrast meets WCAG AA ratios for all text
- [ ] Screen reader testing completed for critical user flows
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Relying solely on automated tools (they catch only ~30% of a11y issues)
- Adding ARIA attributes to elements that already have native semantics
- Using `outline: none` without providing alternative focus indicators

## Related Skills

- `modal-dialog-patterns` — focus management is critical for modal accessibility
- `navigation-patterns` — navigation is the most common a11y failure area

## Usage

Example invocations:

- "/accessibility-testing" — Run the full accessibility testing workflow
- "accessibility testing on this project" — Apply to current context


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
