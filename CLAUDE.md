# JM Labs — Repository Instructions

## What This Repo Contains

Canonical source for JM Labs skills, plugins, and orchestration. Not a code project — a knowledge engineering repository where the primary artifacts are markdown skill files.

## Conventions

- Skills follow the Anthropic gold standard: SKILL.md + references/ + scripts/ + evals/
- Skill quality is tracked per-skill in `skills/README.md`
- All skills in English, even when the operator works in Spanish
- Evidence tags on every claim: `[EXPLICIT]` `[INFERRED]` `[OPEN]`
- No Sofka-proprietary content in this repo

## Branching

- `main` — production-quality skills only (CERTIFIED or MOAT status)
- Feature branches for skill improvements: `improve/{skill-name}`

## Commit Messages

- `feat(skills): add {skill-name} to {category}` — new skill upload
- `improve(skills): {skill-name} → CERTIFIED` — moat upgrade completion
- `scaffold: add {directory} structure` — scaffolding additions
- `docs: update {file}` — README or documentation changes
