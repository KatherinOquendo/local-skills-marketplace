---
name: code-review
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Conduct effective code reviews with PR checklists, anti-pattern detection,
  best practice enforcement, and constructive feedback techniques. [EXPLICIT]
  Trigger: "code review", "PR review", "pull request", "review checklist"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Code Review

> "Code reviews are not about finding bugs — they're about sharing knowledge and raising the bar." — Unknown

## TL;DR

Guides effective code review practices — PR review checklists, common anti-pattern detection, constructive feedback techniques, and automated review tooling. Use when establishing code review standards, reviewing pull requests, or improving team code quality practices. [EXPLICIT]

## Procedure

### Step 1: Discover
- Read the PR description and linked issue/ticket for context
- Check the scope of changes (files modified, lines added/removed)
- Review CI status (tests passing, linting clean, build succeeding)
- Understand the architectural context of the changed code

### Step 2: Analyze
- Review logic correctness: does the code do what it claims?
- Check for common anti-patterns: code duplication, god objects, magic numbers
- Evaluate error handling: are edge cases and failures handled?
- Assess test coverage: are new behaviors tested, including error paths?
- Verify security: input validation, auth checks, no exposed secrets
- Evaluate code sustainability (Constitution XII): Is the code understandable
  without the original author? Are variable/function names business-readable?
  Is the abstraction level appropriate (not over-engineered per XIV)?
  Are dependencies minimal and justified?

### Step 3: Execute
- Use a structured review checklist (correctness, security, performance, maintainability)
- Leave specific, actionable comments with suggested code when possible
- Distinguish between blocking issues, suggestions, and nitpicks (prefix labels)
- Highlight positive patterns worth reinforcing (not just problems)
- Request changes only for blocking issues, approve with suggestions for non-blocking
- Check for consistent naming, formatting, and code style adherence

### Step 4: Validate
- Confirm all blocking comments are addressed before approval
- Verify the final implementation matches the PR's stated intent
- Check that test coverage increased or maintained (not decreased)
- Ensure CI passes on the final commit

## Quality Criteria

- [ ] PR reviewed within agreed SLA (typically 24 hours)
- [ ] Comments are specific, actionable, and labeled by severity
- [ ] Security implications evaluated for all changes
- [ ] Both positive patterns and improvement areas noted
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Rubber-stamping PRs without thorough review (approval without reading)
- Blocking PRs for style preferences when linting tools should enforce style
- Leaving vague comments like "this is wrong" without explanation or suggestion

## Related Skills

- `linting-formatting` — Automated enforcement of style reduces review burden
- `test-strategy` — Reviewing test quality alongside code quality
- `integrity-chain-validation` — Verify code traces back to requirements

## Usage

Example invocations:

- "/code-review" — Run the full code review workflow
- "code review on this project" — Apply to current context


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
