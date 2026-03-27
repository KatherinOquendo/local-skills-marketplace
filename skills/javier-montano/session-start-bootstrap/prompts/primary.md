---
name: session-start-bootstrap-primary
type: execution
version: 2.0.0
description: "Execute the Session Start Bootstrap workflow with triad orchestration."
triad:
  lead: "session-start-bootstrap-lead"
  support: "session-start-bootstrap-support"
  guardian: "session-start-bootstrap-guardian"
---

# Session Start Bootstrap — Execute

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
3. **Lead** (`session-start-bootstrap-lead`): Execute SKILL.md Steps 1-4 for `{{task}}`
   - Discover → Analyze → Execute → Validate
   - Apply evidence tags on all claims
4. **Support** (`session-start-bootstrap-support`): Review for cross-cutting concerns
   - Edge cases, security, accessibility, performance
5. **Guardian** (`session-start-bootstrap-guardian`): Validate
   - Evidence tags complete
   - Quality gate met
   - Constitution XIII + XIV respected
   - Output exceeds expectations

## Output

- Primary deliverable for `{{task}}` in `{{output_format}}`
- Evidence tags on every claim
- Recommendations beyond the ask
- Confidence score (>= 0.95)
