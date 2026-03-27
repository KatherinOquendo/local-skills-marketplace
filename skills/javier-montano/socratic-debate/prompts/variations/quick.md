---
name: socratic-debate-quick
type: variation
version: 2.0.0
description: "Socratic Debate in quick mode."
---

# Socratic Debate — quick Mode

## When to Use

Use quick mode when you need adjusted depth for the Socratic Debate workflow.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | No | Auto-detected |
| `{{depth}}` | No | Set to "quick" |

## Execution

1. Load skill: `skills/socratic-debate/knowledge/body-of-knowledge.md`
2. Check guardrails: `references/guardrails/*.json`
3. Execute at quick depth with evidence tags
4. Lead → Support → Guardian validation
5. Confidence >= 0.95

## Output

- Deliverable calibrated to quick depth
- Evidence-tagged, Constitution-compliant
- Recommendations beyond the ask
