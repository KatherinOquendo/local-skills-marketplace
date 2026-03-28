---
name: visual-regression
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Detect visual changes with screenshot comparison testing using Chromatic,
  Percy, or Playwright visual comparisons for UI regression prevention. [EXPLICIT]
  Trigger: "visual regression", "screenshot testing", "Chromatic", "Percy"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Visual Regression Testing

> "A pixel out of place today is a design system breakdown tomorrow." — Unknown

## TL;DR

Guides visual regression testing setup — screenshot-based comparison using Chromatic (Storybook), Percy, or Playwright's built-in visual comparison to detect unintended UI changes before deployment. Use when maintaining design consistency across code changes and preventing visual regressions. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify components and pages most susceptible to visual regressions
- Check existing Storybook setup (Chromatic integrates directly)
- Review current visual QA process (manual vs automated)
- Determine viewport sizes and themes to capture (mobile, desktop, dark mode)

### Step 2: Analyze
- Choose tool: Chromatic (Storybook), Percy (any framework), Playwright (free, built-in)
- Plan snapshot scope: component-level (Storybook stories) vs page-level (URLs)
- Define threshold for acceptable pixel differences (anti-aliasing tolerance)
- Design review workflow for approving intentional visual changes

### Step 3: Execute
- Set up visual testing tool with CI integration
- Create baseline snapshots for all critical components/pages
- Configure viewport sizes: mobile (375px), tablet (768px), desktop (1280px)
- Capture snapshots in multiple states (default, hover, focus, error, loading)
- Add dark mode snapshots if supported
- Integrate approval workflow in PR process (approve/reject visual diffs)
- Set up Playwright visual comparison with `toHaveScreenshot()` for free option

### Step 4: Validate
- CI reports visual differences on every PR with comparison images
- Intentional changes are explicitly approved (not auto-accepted)
- False positives from anti-aliasing or animation timing are minimized
- Baseline snapshots are updated when design changes are intentional

## Quality Criteria

- [ ] Visual regression tests run on every PR in CI
- [ ] Multiple viewports and themes captured in snapshots
- [ ] Review workflow requires explicit approval for visual changes
- [ ] False positive rate is manageable (not causing alert fatigue)
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Auto-approving all visual diffs (defeats the purpose of visual testing)
- Capturing screenshots of animated elements without stable state
- Testing only one viewport size (misses responsive layout issues)

## Related Skills

- `e2e-testing` — Playwright can serve both functional and visual testing
- `dark-mode` — visual regression testing should cover both themes

## Usage

Example invocations:

- "/visual-regression" — Run the full visual regression workflow
- "visual regression on this project" — Apply to current context


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
