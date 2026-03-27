---
name: rest-api-development-primary
type: execution
version: 2.0.0
description: "Execute the Rest Api Development workflow with triad orchestration."
triad:
  lead: "rest-api-development-lead"
  support: "rest-api-development-support"
  guardian: "rest-api-development-guardian"
---

# Rest Api Development — Execute

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
3. **Lead** (`rest-api-development-lead`): Execute SKILL.md Steps 1-4 for `{{task}}`
   - Discover → Analyze → Execute → Validate
   - Apply evidence tags on all claims
4. **Support** (`rest-api-development-support`): Review for cross-cutting concerns
   - Edge cases, security, accessibility, performance
5. **Guardian** (`rest-api-development-guardian`): Validate
   - Evidence tags complete
   - Quality gate met
   - Constitution XIII + XIV respected
   - Output exceeds expectations

## Output

- Primary deliverable for `{{task}}` in `{{output_format}}`
- Evidence tags on every claim
- Recommendations beyond the ask
- Confidence score (>= 0.95)
