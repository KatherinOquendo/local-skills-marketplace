# Skills Catalog

Canonical library of Claude Code skills. Each skill follows the Anthropic gold standard structure (SKILL.md + references/ + optional scripts/agents/evals).

## Quality Status Key

| Status | Meaning |
|--------|---------|
| MOAT | CERTIFIED + elevated via excellence loop + systemic coherence verified |
| CERTIFIED | Passes 10-criterion rubric (avg >= 8, all >= 7) + 13-point gate (13/13) |
| PENDING | Uploaded, not yet audited. Functional but may lack edge cases, examples, or evals. |

## Catalog

| Category | Skill | Status | Description |
|----------|-------|--------|-------------|
| quality-suite | x-ray-skill | MOAT | Diagnostic scan — 10-criterion scorecard |
| quality-suite | surgeon-skill | MOAT | Precision improvements with content preservation |
| quality-suite | certify-skill | MOAT | Final quality gate — CERTIFIED/CONDITIONAL/BLOCKED |
| quality-suite | trigger-skill | MOAT | Description optimization — trigger accuracy metrics |
| quality-suite | benchmark-skill | MOAT | Before/after comparison — dimension-by-dimension delta |
| quality-suite | assembly-skill | MOAT | One-command full pipeline — configurable depth |
| core | input-analyst | MOAT | 5-pass input pre-processing — surface, root cause, calibration, intent, reformulation |
| forge | creator-moat-skill | MOAT | Skill creation + quality architecture |

*Remaining skills will be added as they are uploaded and certified.*

## Naming Conventions

- Kebab-case: `api-architecture`, not `APIArchitecture`
- Suffix `-skill` for quality/meta skills: `x-ray-skill`, `surgeon-skill`
- No brand prefix in this repo (Sofka skills are in separate repos)
- MetodologIA mirror uses `metodologia-` prefix in `skills/metodologia/`

## Category Guide

| Category | What Goes Here |
|----------|---------------|
| `core/` | Skills that other skills depend on (input-analyst, task-engine, excellence-loop) |
| `quality-suite/` | The 6-skill quality engineering pipeline |
| `forge/` | Skills that create other skills or meta-artifacts (prompts, workflows, rules) |
| `architecture/` | Software/cloud/infrastructure/security architecture domain skills |
| `discovery/` | PreSales discovery and AS-IS assessment skills |
| `data/` | Data engineering, governance, quality, analytics, ML/AI architecture |
| `output/` | Format and brand output skills (DOCX, HTML, XLSX, design system) |
| `agents/` | Agent creation and constitution skills |
| `orchestration-skills/` | Orchestration and governance skills (discovery orchestrator, PMO, risk) |
| `governance-skills/` | Testing strategy, quality engineering, DevSecOps, observability |
| `metodologia/` | MetodologIA-branded skills (GPL-3.0, mirrored from MAO plugin) |
