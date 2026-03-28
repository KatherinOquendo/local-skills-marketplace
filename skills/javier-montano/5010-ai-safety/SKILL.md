---
name: ai-safety
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Content filters, output guardrails, jailbreak prevention, safety evaluation. [EXPLICIT]
  Trigger: "ai safety"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# Ai Safety
> "Method over hacks."
## TL;DR
Content filters, output guardrails, jailbreak prevention, safety evaluation. [EXPLICIT]
## Procedure
### Step 1: Discover
- Gather context and requirements
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV
### Step 3: Execute
- Implement with evidence tags
### Step 4: Validate
- Verify quality criteria met
## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output

## Usage

Example invocations:

- "/ai-safety" — Run the full ai safety workflow
- "ai safety on this project" — Apply to current context


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
