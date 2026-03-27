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

| Status | Criteria |
|--------|----------|
| DRAFT | New, not reviewed |
| CERTIFIED | Reviewed, gold standard structure (SKILL.md + refs + agents + prompts + evals) |
| MOAT | Fully tested with evals, references complete, production-quality |

Only CERTIFIED or MOAT skills in `main` branch.

## Scripts

| Script | Purpose | When to Run |
|--------|---------|-------------|
| `scripts/generate-registry.sh` | Full inventory scan | After bulk changes |
| `scripts/compare-duplicates.sh` | Duplicate analysis + recommendations | When duplicates suspected |
| `scripts/generate-manifests.sh` | Auto-generate plugin manifests | After registry changes |
| `scripts/consolidate-canonical.sh` | Copy best versions to canonical | After decisions approved |
| `scripts/skill-sync.sh` | Propagate canonical → plugins | After canonical edits |
| `scripts/validate-sync.sh` | Detect drift | Pre-commit or periodic |

## Drift Detection

Run `scripts/validate-sync.sh` to detect:
- Skills modified in plugins that should be edited in canonical
- Missing canonical versions
- Overlay incompatibilities

Integrate as pre-commit hook or run before pushing.
