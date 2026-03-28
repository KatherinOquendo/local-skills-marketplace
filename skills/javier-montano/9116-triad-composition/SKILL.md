---
name: triad-composition
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Select Lead + Support + Guardian from composition matrix based on domain classification. [EXPLICIT]
  Trigger: "triad composition"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Triad Composition

> "Method over hacks. Evidence over assumption."

## TL;DR

Select Lead + Support + Guardian from composition matrix based on domain classification. This is an orchestration-layer skill used internally by Pristino and the adk-orchestrator. Protocol details in PRISTINO.md. [EXPLICIT]

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

## Usage

Example invocations:

- "/triad-composition" — Run the full triad composition workflow
- "triad composition on this project" — Apply to current context


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
