---
name: subagent-monitor-deep
type: variation
version: 2.0.0
description: "Subagent Monitor — deep analysis mode. Exhaustive coverage."
---

# Subagent Monitor — Deep Mode

## When to Use

Use deep mode when thoroughness matters more than speed: architecture decisions, security audits, compliance reviews, critical deliverables.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | Yes | User + codebase scan |
| `{{depth}}` | No | Set to "deep" |

## Execution (Deep)

1. Load ALL knowledge: `knowledge/body-of-knowledge.md` + cross-referenced skills
2. Check guardrails: `references/guardrails/*.json`
3. Lead executes with exhaustive analysis:
   - Cover ALL edge cases, not just common path
   - Research: check standards, best practices, recent changes
   - Document every assumption with `[ASSUMPTION]` tag
4. Support reviews with expanded scope:
   - Security, accessibility, performance, business viability
   - Adversarial scenarios: what could go wrong?
5. Guardian validates with strict criteria:
   - Evidence tags 100% coverage (no untagged claims)
   - Quality gate fully met
   - Confidence >= 0.95 with evidence support

## Output

- Exhaustive deliverable with full evidence trail
- Edge cases documented
- Risk assessment included
- Recommendations with priority ranking
- Confidence score with justification
