# JM Labs

Private monorepo for Javier Montano's skill engineering, plugin frameworks, orchestration systems, and professional tooling.

## Brand Map

| Brand | Scope | License | Where |
|-------|-------|---------|-------|
| **JM Labs** | Personal innovation, core tools, experiments | MIT | This repo (`skills/`, `plugins/`, `software/`) |
| **MetodologIA** | Open methodology, community skills | GPL-3.0 | Mirrored in `skills/metodologia/`; upstream in MAO plugin |
| **Sofka** | Enterprise discovery, client delivery | All Rights Reserved | Separate repos (`sofka-discovery-framework`, `sofka-presales-skills`) |

## Repository Structure

| Directory | Content | Status |
|-----------|---------|--------|
| `skills/` | Canonical skill library across 10 categories | Active |
| `plugins/` | Plugin frameworks (MAO, PM, Sovereign Architect, Scriba) | Active |
| `orchestration/` | Meta-orchestrator network (14 files) | Active |
| `governance/` | Policies, standards, frameworks, templates | Scaffolding |
| `deliverables/` | Discovery outputs, architecture docs, proposals | Scaffolding |
| `software/` | Code projects, tools, experiments | Scaffolding |

## Skills Overview

| Category | Count | Description |
|----------|-------|-------------|
| `core/` | ~5 | Foundational skills: input-analyst, task-engine, excellence-loop |
| `quality-suite/` | 6 | Skill engineering pipeline: x-ray, surgeon, certify, trigger, benchmark, assembly |
| `forge/` | 5 | Meta-creation: prompt-forge, workflow-forge, rule-forge, ecosystem-forge, creator-moat |
| `architecture/` | 12+ | API, software, enterprise, cloud, security, mobile, infrastructure, etc. |
| `discovery/` | 10+ | AS-IS analysis, flow mapping, scenario analysis, roadmap, feasibility, etc. |
| `data/` | 5+ | Data engineering, governance, quality, analytics, data science architecture |
| `output/` | 5+ | Brand output formats: DOCX, HTML, XLSX, design system, UX writing |
| `agents/` | 3+ | Agent creator, agent constitution, open-claw-builder |
| `orchestration-skills/` | 3+ | Discovery orchestrator, project management, risk controlling |
| `metodologia/` | 52 | MetodologIA mirror (GPL-3.0) |

## Quick Start

```bash
# Browse skills
cat skills/README.md

# Use the quality pipeline on any skill
# /x-ray-skill skills/core/input-analyst
# /surgeon-skill skills/core/input-analyst
# /certify-skill skills/core/input-analyst

# Or run the full pipeline in one command
# /assembly-skill skills/core/input-analyst
```

## Quality Standards

Every skill in this repo targets CERTIFIED status (10-criterion rubric, 13-point gate). Quality is tracked in `skills/README.md` per skill.

| Status | Meaning |
|--------|---------|
| CERTIFIED | Passes all quality checks, production-ready |
| MOAT | CERTIFIED + elevated to 10x density and systemic coherence |
| PENDING | Uploaded but not yet audited/improved |

## Related Repositories

| Repo | Brand | Visibility |
|------|-------|------------|
| `sofka-discovery-framework` | Sofka | Private |
| `sofka-presales-skills` | Sofka | Public |
| `sofka-discovery-framework-public` | Sofka | Public mirror |
