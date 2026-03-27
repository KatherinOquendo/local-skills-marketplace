---
name: microcopy-writing-primary
type: execution
version: 2.0.0
description: "Execute the Microcopy Writing workflow with triad orchestration."
triad:
  lead: "microcopy-writing-lead"
  support: "microcopy-writing-support"
  guardian: "microcopy-writing-guardian"
---

# Microcopy Writing — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | What to accomplish | Yes | User input |
| `{{context}}` | Background and constraints | Yes | User or codebase |
| `{{constraints}}` | Additional rules | No | Guardrails JSON |
| `{{depth}}` | quick / standard / deep | No | Auto |
| `{{output_format}}` | html / docx / xlsx / md | No | Auto |

## Execution

1. **Load knowledge**: Read `knowledge/body-of-knowledge.md`
2. **Check guardrails**: Read `references/guardrails/*.json`
3. **Lead** (`microcopy-writing-lead`): Execute SKILL.md Steps 1-4 for `{{task}}`
   - Discover → Analyze → Execute → Validate
   - Apply evidence tags on all claims
4. **Support** (`microcopy-writing-support`): Review for cross-cutting concerns
   - Edge cases, security, accessibility, performance
5. **Guardian** (`microcopy-writing-guardian`): Validate
   - Evidence tags complete
   - Quality gate met
   - Constitution XIII + XIV respected
   - Output exceeds expectations

## Output

- Primary deliverable for `{{task}}` in `{{output_format}}`
- Evidence tags on every claim
- Recommendations beyond the ask
- Confidence score (>= 0.95)
