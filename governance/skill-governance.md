# Skill Governance Process — JM Labs

## Canonical Skill Architecture

```
skills/                          ← CANONICAL SOURCE OF TRUTH
├── javier-montano/              ← 95 canonical skills (MIT)
│   ├── REGISTRY.json            ← Machine-readable registry
│   ├── REGISTRY-REPORT.md       ← Human-readable inventory
│   └── {skill-name}/SKILL.md   ← Each canonical skill
├── metodologia/                 ← 54 canonical skills (GPL-3.0)
│   └── {skill-name}/SKILL.md
│
plugins/                         ← CONSUMERS (inherit from canonical)
├── javier-montano/
│   ├── sovereign-architect/     ← 127 skills (49 inherited, 78 plugin-only)
│   ├── pm-project-framework/    ← 109 skills (21 inherited, 88 plugin-only)
│   └── scriba/                  ← 24 skills (0 inherited, 24 plugin-only)
└── metodologia/
    └── metodologia-discovery-framework/ ← 111 skills (73 inherited, 38 plugin-only)
```

## Workflow: New Skill

1. **Generic skill** → create in `skills/{entity}/{name}/` as canonical
2. **Plugin-specific** → create in `plugins/.../skills/{name}/`, add to `plugin_only_skills` in manifest
3. Run `scripts/skill-sync.sh` to propagate

## Workflow: Update Canonical Skill

1. Edit `skills/{entity}/{name}/SKILL.md`
2. Run `scripts/skill-sync.sh --plugin=all`
3. Check overlay compatibility
4. Commit canonical + synced changes together

## Workflow: Promote Plugin-Only to Canonical

1. Copy from plugin to `skills/{entity}/{name}/`
2. Extract domain-specific content into overlay
3. Update plugin manifest: move from `plugin_only_skills` to `inherited_skills`
4. Run `scripts/skill-sync.sh`

## Quality Gates

| Status | Criteria | Formula |
|--------|----------|---------|
| DRAFT | New, not reviewed | No formula — any skill starts here |
| CERTIFIED | Reviewed, gold standard structure | All rubric dims >= 7, avg >= 8, all S1-S9 structural checks pass |
| MOAT | Production-quality with evals and evidence | CERTIFIED + M1-M5 (see below) |

**Only MOAT skills in `main` branch.** CERTIFIED is the minimum for feature branches.

### MOAT Formula (extends CERTIFIED)

```
MOAT = CERTIFIED (all dims >= 7, avg >= 8, S1-S9 pass)
  + M1: evals/evals.json exists with >= 5 test prompts covering distinct capabilities
  + M2: At least 1 false-positive eval + 1 edge-case eval in evals.json
  + M3: All files in references/ have substantive content (>= 20 lines each, no TBD/placeholder)
  + M4: SKILL.md uses Template A (Modern) — Template B (Physics/Protocol) is DEPRECATED
  + M5: Evidence tags [EXPLICIT]/[INFERRED]/[OPEN] on >= 80% of factual claims
```

### Complexity Tiers (required assets per tier)

Not all skills need the same asset set. Tier is determined by inherent complexity, not current state.

| Tier | Criteria | Required Assets | Recommended Assets |
|------|----------|----------------|-------------------|
| **Utility** (< 150 lines, single concern) | Simple transformation, lookup, formatting | SKILL.md, evals/ | references/ |
| **Standard** (150-400 lines, multi-step process) | Analysis, design, multi-phase workflow | SKILL.md, evals/, references/, prompts/ | agents/, examples/ |
| **Orchestrator** (400+ lines, delegates to sub-skills) | Pipeline coordination, multi-agent | SKILL.md, evals/, references/, agents/, prompts/, examples/ | scripts/, knowledge/ |

### Template A (Only Accepted Template)

Template B (Physics/Protocol/TL;DR) is **DEPRECATED**. All skills must use Template A:

1. YAML Frontmatter (name, description 3rd person with 3-5 triggers, allowed-tools)
2. Title + Value Proposition (1-2 sentences)
3. Usage (2+ invocation examples)
4. Before {Action} / Progressive Disclosure (if references/ exists)
5. Core Process (tables > bullets, code blocks for templates)
6. Assumptions & Limits (3+ specific limits)
7. Edge Cases (3+ with handling)
8. Good vs Bad Example (1+ side-by-side)
9. Validation Gate (5+ testable checkboxes)
10. Reference Files table (if references/ exists)

### Evidence Tags

All skills must use the English evidence taxonomy on factual claims:
- `[EXPLICIT]` — Direct fact/specification
- `[INFERRED]` — Derived conclusion
- `[OPEN]` — Unknown/to-be-validated

Target: >= 80% coverage on factual claims in SKILL.md.

## Scripts

| Script | Purpose | When to Run |
|--------|---------|-------------|
| `scripts/generate-registry.sh` | Full inventory scan | After bulk changes |
| `scripts/compare-duplicates.sh` | Duplicate analysis + recommendations | When duplicates suspected |
| `scripts/generate-manifests.sh` | Auto-generate plugin manifests | After registry changes |
| `scripts/consolidate-canonical.sh` | Copy best versions to canonical | After decisions approved |
| `scripts/skill-sync.sh` | Propagate canonical → plugins | After canonical edits |
| `scripts/validate-sync.sh` | Detect drift | Pre-commit or periodic |
| `scripts/moat-audit.sh` | Full MOAT compliance audit | Monthly or before release |
| `scripts/batch-evals-scaffold.sh` | Scaffold evals for skills missing them | During consolidation waves |
| `scripts/batch-template-migrate.sh` | Migrate Template B to Template A | During consolidation waves |
| `scripts/new-skill.sh` | Scaffold new skill with Template A + empty evals | When creating a new skill |

## Drift Detection

Run `scripts/validate-sync.sh` to detect:
- Skills modified in plugins that should be edited in canonical
- Missing canonical versions
- Overlay incompatibilities

Integrate as pre-commit hook or run before pushing.
