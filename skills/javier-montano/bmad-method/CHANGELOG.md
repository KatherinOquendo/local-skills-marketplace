# BMAD Method Skill — Changelog

All notable changes to the `bmad-method` skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows [Semantic Versioning](https://semver.org/).

---

## [2.0.0] — 2026-03-25

### Summary
10x quality elevation with systemic expansion. Every file refined for density, precision, and traceability. New modules close structural gaps in troubleshooting, integration, metrics, conflict resolution, and simplified BMAD Lite variant.

### Added — New Systemic Modules
- `references/troubleshooting.md` — 40+ symptom→diagnosis→fix entries organized by phase
- `references/integration-patterns.md` — Git hooks, CI/CD, IDE, Jira/Linear/GitHub sync
- `references/metrics-framework.md` — 13 KPIs with formulas, targets, thresholds
- `references/conflict-resolution-protocol.md` — Ownership matrix, escalation hierarchy, resolution patterns
- `references/anti-patterns-catalog.md` — 27 anti-patterns across 5 categories with severity ratings
- `references/bmad-lite.md` — Simplified 3-stage BMAD for solo devs and small scope

### Added — Checklists Module (7 files)
- `checklists/phase-1-complete.md` — 14-item Phase 1 completion gate
- `checklists/phase-2-complete.md` — 20-item Phase 2 completion gate
- `checklists/phase-3-complete.md` — 20-item Phase 3 completion gate
- `checklists/sprint-ready.md` — 14-item sprint readiness verification
- `checklists/story-ready.md` — 11-item Definition of Ready
- `checklists/story-done.md` — 12-item Definition of Done
- `checklists/quick-flow-triage.md` — 8-item quick flow eligibility check

### Added — Diagnostic Scripts (2 files)
- `scripts/lint_artifacts.py` — Lint all BMAD artifacts: frontmatter, IDs, cross-refs, orphans, staleness
- `scripts/diagnose_project.py` — Project health diagnosis: phase detection, completeness, gate prediction

### Added — Example Artifact
- `examples/greenfield-saas/gate-result.md` — Realistic 13-step gate result (10 PASS, 2 WARN, 1 FAIL)

### Changed — SKILL.md
- Added `## Scope & Limits` section (BMAD is/is not)
- Added `## Decision Log` with 7 key design decisions (D1-D7) with rationale
- Added `## Assumptions` section (7 assumptions)
- Added `Failure Recovery` blocks to all 4 phases in Section 5
- Added `### Gate Result Actions` with CONCERNS/FAIL remediation routing table
- Added `Conflict Resolution` column to Agent Roster (Section 9)
- Tightened prose: removed filler, shortened descriptions, cleaned path prefixes

### Changed — All 11 Agent Files
- Added `## Failure Modes` (4-5 scenarios per agent with symptom + recovery)
- Added `## Conflict Resolution` (inter-agent dispute handling)
- Added `## Quality Metrics` (2-3 KPIs per agent with targets)
- Added `## Edge Cases` (2-3 unusual situations per agent)
- Added `See also:` cross-references
- Tightened persona descriptions: removed non-differentiating sentences

### Changed — All 16 Reference Files
- Added `## Assumptions`, `## Limits`, `## Acceptance Criteria` to every file
- Added 40 numbered assertions ([R1]-[R40]) for traceability
- Replaced "should" with "must"/"may" throughout
- Added concrete thresholds (numbers, percentages, time limits)
- Added `⚠️ Anti-pattern` callouts inline
- Added `See also:` cross-references between all reference files
- Key additions per file:
  - `methodology-overview.md`: Decision tree, comparison metrics, version compatibility
  - `phase-1-analysis.md`: Time-boxing rules, skip criteria, minimum viable brief
  - `phase-2-planning.md`: PRD quality rubric (1-5 scale), scope lock criteria
  - `phase-3-solutioning.md`: Architecture review checklist, story splitting heuristics
  - `phase-4-implementation.md`: Sprint failure recovery, velocity anomaly detection
  - `quick-flow.md`: Escalation decision tree, max consecutive QF chain rule
  - `agent-as-code.md`: Agent testing strategy, semver rules, deprecation process
  - `project-context-guide.md`: Staleness detection, mandatory review cadence
  - `artifact-flow-chain.md`: Impact analysis algorithm, versioning rules
  - `implementation-readiness-gate.md`: Override procedure, partial gate for MVPs, metrics history
  - `progressive-context.md`: Token budget calculator, context priority ranking
  - `brownfield-patterns.md`: Risk scoring matrix, minimum documentation threshold
  - `greenfield-patterns.md`: MVP scoping framework, technology selection matrix
  - `enterprise-governance.md`: RACI matrix, audit checklist, escalation hierarchy
  - `customization-guide.md`: Compatibility test suite, customization registry format
  - `schemas.md`: Validation rules per field, migration guide, backwards compatibility

### Changed — All 14 Templates
- Added `<!-- REQUIRED -->` and `<!-- OPTIONAL -->` markers on all fields
- Added `<!-- VALIDATION: [rule] -->` constraints (regex, ranges, enums)
- Added `<!-- ANTI-PATTERN: -->` warnings for common mistakes
- Added `## Completion Checklist` to each template
- Replaced generic placeholders with specific guidance

### Changed — All 10 Scripts
- Added `--dry-run` flag to all scripts that create/modify files
- Added `--verbose` flag for detailed output
- Improved error messages with `Fix:` suggestions
- Added input validation with clear messages
- Added `--help` epilog with usage examples
- Standardized exit codes: 0=success, 1=warning, 2=error

### Changed — All 18 Workflow Step Files
- Added `## Rollback Procedure` to each step
- Added `## Skip Conditions` with clear criteria
- Added `## Time Box` with maximum time before escalation
- Added concrete acceptance criteria (checkboxes) for step completion

### Changed — All 8 Prompt Fragments
- Added `## Pre-conditions` and `## Post-conditions`
- Added `## Failure Signals` (how to detect failed transitions)
- Tightened to pure actionable instructions

### Changed — All 12 Example Files
- Added `## Lessons Learned` and `## Decisions Made` sections
- Added inline `<!-- NOTE: -->` annotations

### Metrics
| Metric | v1.0.0 | v2.0.0 |
|--------|--------|--------|
| Total files | 89 | **105** |
| Directories | 11 | **12** (+ checklists/) |
| Numbered assertions | 0 | **40** ([R1]-[R40]) |
| Anti-patterns cataloged | ~7 (scattered) | **27** (consolidated) |
| KPIs defined | 0 | **13** (metrics framework) |
| Checklists | 0 | **7** |
| Diagnostic scripts | 0 | **2** |

---

## [1.0.0] — 2026-03-25

### Summary
Initial release of the BMAD method skill with comprehensive scaffolding exceeding the Anthropic skill-creator baseline.

### Added
- `SKILL.md` — Main skill file (381 lines) covering DECLARE/USE/APPLY dimensions
- `agents/` — 11 agent personas (Mary, John, Sally, Winston, Bob, Amelia, Quinn, Barry, Orchestrator, Gate Reviewer, Retro Facilitator)
- `scripts/` — 8 Python scripts (init, validate, scaffold, generate, check, export)
- `references/` — 16 knowledge documents covering all BMAD concepts
- `templates/` — 14 file templates for all BMAD artifacts
- `prompts/` — 8 phase-transition prompt fragments
- `workflows/` — 5 sharded workflows with 18 step files
- `examples/` — 4 example flows (greenfield SaaS with full artifacts, brownfield migration, quick-flow bugfix, enterprise multi-team)
- `assets/` — Interactive project dashboard (HTML)
- `LICENSE.txt` — MIT license

### Scaffolding Comparison (vs Anthropic skill-creator)
| Category | skill-creator | bmad-method |
|----------|:---:|:---:|
| Total files | ~20 | **89** |
| agents/ | 3 | **11** |
| references/ | 1 | **16** |
| templates/ | 0 | **14** |
| prompts/ | 0 | **8** |
| workflows/ | 0 | **18 steps** |
| examples/ | 0 | **11** |
