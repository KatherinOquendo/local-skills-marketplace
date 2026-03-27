---
name: input-tolerance
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Normalize imperfect input: typos, voice, dyslexia, multilingual, multimodal. Extract intent from noise.
  Trigger: "input tolerance"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Input Tolerance

> "Method over hacks. Evidence over assumption."

## TL;DR

Normalize imperfect input: typos, voice, dyslexia, multilingual, multimodal. Extract intent from noise. This is an orchestration-layer skill used internally by Pristino and the adk-orchestrator. Protocol details in PRISTINO.md.

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
