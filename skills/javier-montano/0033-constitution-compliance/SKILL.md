---
name: constitution-compliance
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Validate outputs against Constitution v5.2.0 (18 principles). Flag violations before delivery.
  Trigger: "constitution compliance"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Constitution Compliance

> "Method over hacks. Evidence over assumption."

## TL;DR

Validate outputs against Constitution v5.2.0 (18 principles). Flag violations before delivery. This is an orchestration-layer skill used internally by Pristino and the adk-orchestrator. Protocol details in PRISTINO.md.

## Procedure

### Step 1: Discover
- Gather input and context
- Load relevant indexes and configuration

### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV
- Score candidates by relevance and confidence

### Step 3: Execute
- Apply the selected approach
- Tag all outputs with evidence markers

### Step 4: Validate
- Verify quality criteria met
- Confirm confidence >= 0.95

## Quality Criteria

- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Confidence >= 0.95
- [ ] Actionable output

## Related Skills

- See PRISTINO.md for full orchestration protocol
