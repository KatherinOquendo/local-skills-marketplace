---
name: post-tool-use-validator
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Validate tool outputs: lint check, evidence tags, quality gates. [EXPLICIT]
  Trigger: "post tool use validator"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# Post Tool Use Validator
> "Method over hacks."
## TL;DR
Validate tool outputs: lint check, evidence tags, quality gates. [EXPLICIT]
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

- "/post-tool-use-validator" — Run the full post tool use validator workflow
- "post tool use validator on this project" — Apply to current context


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
