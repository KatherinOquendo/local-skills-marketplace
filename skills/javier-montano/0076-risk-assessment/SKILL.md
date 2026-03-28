---
name: risk-assessment
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Identifies, quantifies, and mitigates project and technical risks using
  risk registers, probability/impact matrices, and mitigation strategies. [EXPLICIT]
  Produces actionable risk management plans. [EXPLICIT]
  Trigger: "risk register", "risk matrix", "mitigation", "risk assessment"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Risk Assessment

> "Risk comes from not knowing what you are doing." — Warren Buffett

## TL;DR

Systematically identifies, quantifies, and plans mitigations for project and technical risks using risk registers and probability/impact matrices. Use this skill at project inception, before major milestones, or when uncertainty threatens delivery commitments. [EXPLICIT]

## Procedure

### Step 1: Discover
- Brainstorm risks across categories: technical, schedule, resource, external, organizational
- Review lessons learned from similar projects
- Examine assumptions — each assumption is a potential risk if wrong
- Check dependencies on third parties, APIs, and external systems

### Step 2: Analyze
- Score each risk on Probability (1-5) and Impact (1-5)
- Calculate risk exposure: Probability × Impact
- Classify risks: Critical (>15), High (10-15), Medium (5-9), Low (<5)
- Identify risk triggers — early warning signs that a risk is materializing

### Step 3: Execute
- Create a risk register with: ID, description, category, probability, impact, exposure, owner, trigger, mitigation, contingency
- Build a probability/impact heat map for visual communication
- Define mitigation strategies: Avoid, Transfer, Mitigate, Accept
- Establish risk review cadence and escalation thresholds

### Step 4: Validate
- Verify every high/critical risk has a named owner and active mitigation
- Confirm mitigation strategies are actionable (budget, timeline, responsible party)
- Check that risk triggers are observable and measurable
- Review risk register completeness with cross-functional team

## Quality Criteria

- [ ] Risk register covers technical, schedule, resource, and external categories
- [ ] Every risk has probability, impact, owner, and mitigation strategy
- [ ] Critical risks have both mitigation and contingency plans
- [ ] Risk triggers are defined for top 10 risks
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Risk theater: maintaining a register nobody reads or updates
- Mitigations that are just "monitor the risk" without concrete actions
- Ignoring organizational and political risks

## Related Skills

- `feasibility-validation` — risk assessment informs feasibility scoring
- `cost-estimation` — risk contingency feeds into effort estimates
- `security-architecture` — technical security risks via STRIDE

## Usage

Example invocations:

- "/risk-assessment" — Run the full risk assessment workflow
- "risk assessment on this project" — Apply to current context


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
