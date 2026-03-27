# Skill Architecture Standard — Canonical Pattern

## The Sub-Repo Pattern

A production-grade skill is a modular system designed for Progressive Disclosure. The architecture protects the agent's context window and enforces structured reasoning.

## File Topology

```text
{skill-name}/
├── SKILL.md                # Entry point, orchestrator
└── references/             # Domain knowledge (PLURAL, always)
    ├── {domain}-{aspect-1}.md
    ├── {domain}-{aspect-2}.md
    └── {domain}-{aspect-3}.md
```

## SKILL.md Canonical Sections (17 total)

| # | Section | Purpose |
|---|---------|---------|
| 1 | Frontmatter YAML | Contract: name, description, model, context, allowed-tools |
| 2 | Title + Description | What the skill does in 1-3 sentences |
| 3 | Principio Rector | 2-3 philosophical rules that guide all decisions |
| 4 | Inputs | Parameters, auto-detection, reference loading |
| 5 | When to Use | Activation triggers |
| 6 | When NOT to Use | Redirects to correct skill |
| 7 | Delivery Structure (S1-S6) | The 6 sections the skill produces |
| 8 | Trade-off Matrix | Decision trade-offs with enables/constrains |
| 9 | Assumptions | What must be true for the skill to work |
| 10 | Limits | What the skill explicitly does NOT do |
| 11 | Edge Cases | 3-5 scenarios with handling guidance |
| 12 | Manejo de Inputs Ambiguos | How to handle missing or vague inputs |
| 13 | Validation Gate | Checklist with executor note |
| 14 | Cross-References | Links to related skills |
| 15 | Output Format Protocol | Format selection logic |
| 16 | Output Artifact | Template of the deliverable |
| 17 | Fuente | Citations and references |

## Frontmatter Standard

```yaml
---
name: metodologia-{nombre}
description: >
  {functional description with activation triggers}
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
```

## Parameter Taxonomy

| Parameter | Purpose | Values |
|-----------|---------|--------|
| MODO | Agent autonomy level | piloto-auto, desatendido, supervisado, paso-a-paso |
| PROFUNDIDAD | Audit depth (audits only) | express, standard, deep |
| FORMATO | Output format | markdown, html, dual |
| ALCANCE | Output scope | ejecutiva, tecnica (or domain-specific) |

## Reference File Naming

- Use descriptive domain-specific names (YES: `aws-service-catalog.md`, NO: `knowledge_graph.md`)
- Kebab-case
- Domain prefix for grouping
- Minimum 3 files per skill

## Reference Loading Syntax

```
Load references:
  Read ${CLAUDE_SKILL_DIR}/references/{file-name}.md
```

## Validation Gate Format

Always include executor note before checklist:

```
*El agente que ejecuta este skill debe verificar cada item antes de entregar el output al usuario.*
```
