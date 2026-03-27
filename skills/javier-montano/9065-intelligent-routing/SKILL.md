---
name: intelligent-routing
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Match user intent to the best domain for Lead agent selection using BM25 + semantic similarity.
  Trigger: "intelligent routing"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Intelligent Routing

> "Method over hacks. Evidence over assumption."

## TL;DR

Match user intent to the best domain for Lead agent selection using BM25 + semantic similarity. This is an orchestration-layer skill used internally by Pristino and the adk-orchestrator. Protocol details in PRISTINO.md.

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
