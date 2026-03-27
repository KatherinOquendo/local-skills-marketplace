---
name: requirements-engineering
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Elicits, structures, and validates software requirements using user stories,
  acceptance criteria in Given/When/Then format, and traceability matrices.
  Transforms vague stakeholder needs into precise, testable specifications.
  Trigger: "user stories", "acceptance criteria", "requirements"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Requirements Engineering

> "A requirement that is not testable is not a requirement — it is a wish." — Alan Davis

## TL;DR

Transforms stakeholder needs into structured, testable requirements using user stories with acceptance criteria in Given/When/Then (Gherkin) format. Use this skill when starting a new feature, capturing business rules, or when requirements are ambiguous and need formalization.

## Procedure

### Step 1: Discover
- Identify existing requirements documents, user stories, or feature descriptions in the codebase
- Search for `.feature` files, `README.md`, issue trackers, or specification docs
- Interview context: gather stakeholder roles, business goals, and constraints

### Step 2: Analyze
- Decompose high-level needs into INVEST-compliant user stories (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- Identify implicit requirements, edge cases, and non-functional requirements
- Map dependencies between stories and identify story splitting opportunities

### Step 3: Execute
- Write user stories in "As a [role], I want [goal], so that [benefit]" format
- Define acceptance criteria using Given/When/Then syntax for each story
- Create a traceability matrix linking requirements to business objectives
- Document assumptions, constraints, and out-of-scope items explicitly

### Step 4: Validate
- Verify each story meets INVEST criteria
- Confirm acceptance criteria are atomic, deterministic, and testable
- Cross-check coverage: every business rule has at least one acceptance criterion
- Review with stakeholders for completeness and correctness

## Quality Criteria

- [ ] Every user story follows "As a / I want / So that" format
- [ ] Acceptance criteria use Given/When/Then with concrete examples
- [ ] Non-functional requirements (performance, security, accessibility) are captured
- [ ] Stories are INVEST-compliant and appropriately sized
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Gold plating: adding requirements nobody asked for
- Ambiguous acceptance criteria that cannot be automated
- Missing negative scenarios and error paths in Given/When/Then

## Related Skills

- `stakeholder-mapping` — identifies who provides and validates requirements
- `domain-driven-design` — provides ubiquitous language for precise requirements
- `scenario-analysis` — evaluates alternative requirement approaches
