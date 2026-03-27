# Skill Output Templates

## Template 1: SKILL.md Skeleton

```markdown
---
name: metodologia-{skill-name}
description: >
  {Functional description. Include activation triggers: "use when the user asks to...",
  "activated when...", or "trigger on..."}
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# {Skill Title}: {Subtitle}

{1-3 sentence description of what the skill does and why it matters.}

---

## Principio Rector

1. **{Rule 1 name}.** {Explanation — why this rule exists and what it prevents.}
2. **{Rule 2 name}.** {Explanation.}
3. **{Rule 3 name (optional)}.** {Explanation.}

---

## Inputs

\```
Parametros:
  MODO:     [piloto-auto | desatendido | supervisado | paso-a-paso]
  FORMATO:  [markdown | html | dual]
  ALCANCE:  [ejecutiva | tecnica]
  {DOMAIN_PARAM}: [{domain-specific values}]

Deteccion automatica:
  - {Auto-detection rule 1}
  - {Auto-detection rule 2}
  - Default: MODO=piloto-auto, FORMATO=markdown, ALCANCE=tecnica
\```

Load references:

\```
Read ${CLAUDE_SKILL_DIR}/references/{domain}-{aspect-1}.md
Read ${CLAUDE_SKILL_DIR}/references/{domain}-{aspect-2}.md
Read ${CLAUDE_SKILL_DIR}/references/{domain}-{aspect-3}.md
\```

---

## When to Use

- {Trigger 1}
- {Trigger 2}
- {Trigger N}

## When NOT to Use

- {Anti-trigger 1} → **metodologia-{correct-skill}**
- {Anti-trigger 2} → **metodologia-{correct-skill}**

---

## Delivery Structure: 6 Sections

### S1: {Section Name}
{Description and deliverables}

### S2: {Section Name}
{Description and deliverables}

### S3: {Section Name}
{Description and deliverables}

### S4: {Section Name}
{Description and deliverables}

### S5: {Section Name}
{Description and deliverables}

### S6: {Section Name}
{Description and deliverables}

---

## Trade-off Matrix

| Decision | Habilita | Restringe | Cuando Usar |
|----------|----------|-----------|-------------|
| {Decision 1} | {Benefit} | {Cost} | {Context} |

---

## Assumptions
{Numbered list}

## Limits
{Numbered list}

---

## Edge Cases
{3-5 numbered scenarios with handling}

---

## Manejo de Inputs Ambiguos
{Bulleted list of ambiguous input scenarios and how to handle}

---

## Validation Gate

*El agente que ejecuta este skill debe verificar cada item antes de entregar el output al usuario.*

- [ ] {Check 1}
- [ ] {Check N}

---

## Cross-References

| Skill | Relacion |
|-------|----------|
| {skill-name} | {relationship} |

---

## Output Format Protocol
{Format selection logic}

## Output Artifact
{Template of the deliverable}

---
**Fuente**: {Citations}
```

## Template 2: Reference File Skeleton

```markdown
# {Domain} — {Aspect}

## {Major Section 1}

{Content: tables, lists, decision trees, diagrams}

## {Major Section 2}

{Content}

---

## {Summary or Quick Reference}

{Condensed reference for rapid lookup}
```
