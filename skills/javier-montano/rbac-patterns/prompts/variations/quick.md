---
name: rbac-patterns-quick
type: variation
version: 2.0.0
description: "Rbac Patterns in quick mode."
---

# Rbac Patterns — quick Mode

## When to Use

Use quick mode when you need adjusted depth for the Rbac Patterns workflow.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | No | Auto-detected |
| `{{depth}}` | No | Set to "quick" |

## Execution

1. Load skill: `skills/rbac-patterns/knowledge/body-of-knowledge.md`
2. Check guardrails: `references/guardrails/*.json`
3. Execute at quick depth with evidence tags
4. Lead → Support → Guardian validation
5. Confidence >= 0.95

## Output

- Deliverable calibrated to quick depth
- Evidence-tagged, Constitution-compliant
- Recommendations beyond the ask
