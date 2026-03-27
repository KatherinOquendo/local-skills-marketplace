---
name: error-handling
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Error handling patterns: try/catch, error boundaries, fallback UI, user-friendly error messages, offline error states. Ensures graceful degradation.
  Trigger: "error handling", "try catch", "error boundary", "fallback", "graceful degradation"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Error Handling

> "Method over hacks. Evidence over assumption."

## TL;DR

Implements error handling patterns for web applications: try/catch with meaningful messages, error boundaries for component isolation, fallback UI for failed states, offline error handling, and user-friendly error messages. Every error state is a UX opportunity, not a dead end.

## Procedure

### Step 1: Discover
- Read existing code and identify current patterns
- Check for existing documentation or configuration
- Identify gaps and improvement opportunities

### Step 2: Analyze
- Evaluate options and select the best approach for the project context
- Consider Constitution principles (XIII Think First, XIV Simple First)
- Map to quality gates

### Step 3: Execute
- Implement the solution following established patterns
- Apply evidence tags to all claims
- Generate output using brand template if HTML

### Step 4: Validate
- Verify implementation works correctly
- Check against quality criteria
- Evidence tags applied to all claims

## Quality Criteria

- [ ] Implementation follows established patterns
- [ ] Evidence tags applied to all claims
- [ ] Tested and verified
- [ ] Constitution-compliant

## Related Skills

- `e2e-testing` — Test error states in E2E
- `firebase-setup` — Firebase error handling patterns
- `vanilla-javascript` — DOM error handling
