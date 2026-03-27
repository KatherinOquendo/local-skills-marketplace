---
name: accessibility-design
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Implements WCAG 2.1 AA accessibility patterns including ARIA roles, keyboard
  navigation, screen reader support, color contrast, and inclusive design
  principles for web applications.
  Trigger: "accessibility", "WCAG", "ARIA", "a11y", "screen reader", "inclusive design"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Accessibility Design

> "The power of the Web is in its universality. Access by everyone regardless of disability is an essential aspect." — Tim Berners-Lee

## TL;DR

Implements WCAG 2.1 AA compliance with proper ARIA roles, keyboard navigation, screen reader support, and inclusive design patterns to ensure web applications are usable by everyone. Use this skill when building new features, auditing existing applications, or establishing accessibility standards for a team.

## Procedure

### Step 1: Discover
- Audit current accessibility state using automated tools (axe, Lighthouse)
- Test with keyboard-only navigation (Tab, Enter, Escape, Arrow keys)
- Test with screen readers (VoiceOver, NVDA) for content comprehension
- Review color contrast ratios against WCAG AA requirements (4.5:1 text, 3:1 large text)

### Step 2: Analyze
- Categorize issues by WCAG principle: Perceivable, Operable, Understandable, Robust
- Prioritize by impact: how many users affected and severity of barrier
- Identify patterns that need ARIA vs. patterns where semantic HTML suffices
- Map interactive components to required keyboard interaction patterns (WAI-ARIA APG)

### Step 3: Execute
- Use semantic HTML elements before reaching for ARIA (button, nav, main, aside)
- Implement ARIA roles, states, and properties for custom interactive widgets
- Design focus management: visible focus indicators, focus trapping in modals, skip links
- Ensure form inputs have associated labels, error messages, and descriptions
- Implement live regions (aria-live) for dynamic content updates
- Add prefers-reduced-motion and prefers-color-scheme media query support

### Step 4: Validate
- Run automated tests (axe-core) in CI pipeline
- Perform manual keyboard navigation testing for all interactive flows
- Test with at least one screen reader on critical user journeys
- Verify focus order matches visual reading order

## Quality Criteria

- [ ] All interactive elements are keyboard accessible
- [ ] Color contrast meets WCAG AA ratios (4.5:1 text, 3:1 large)
- [ ] Images have meaningful alt text or are decorative (alt="")
- [ ] Forms have proper labels, error messages, and descriptions
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- ARIA overuse: adding roles to elements that are already semantic (role="button" on a button)
- Visible focus removal (`outline: none`) without replacement
- Color as the only means of conveying information

## Related Skills

- `html-semantic` — semantic HTML is the foundation of accessibility
- `form-engineering` — accessible form patterns and validation
- `responsive-design` — responsive and accessible design overlap significantly
