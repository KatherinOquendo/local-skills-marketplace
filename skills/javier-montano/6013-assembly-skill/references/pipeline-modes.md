# Pipeline Modes: Configuration & Dependency Map

Detailed configuration for each assembly-skill mode. Includes phase dependencies, timing estimates, and decision points.

## Mode Specifications

### Quick Mode

```
Phase A (X-Ray) → Phase D (Report)
```

| Attribute | Value |
|-----------|-------|
| Phases | A (diagnostic) + D (report) |
| Modifies files | No |
| Requires confirmation | No |
| Time estimate | 3-5 minutes |
| Context usage | ~20% of window |
| Output | X-Ray scorecard + recommendation |

**Use when:** You need a quality snapshot without changes. Good for: triaging multiple skills, pre-meeting quality checks, monitoring skill health over time.

### Standard Mode (default)

```
Phase A (X-Ray) → Gate A → Phase B (Surgeon) → Gate B → Phase C (Certify) → Phase D (Report)
```

| Attribute | Value |
|-----------|-------|
| Phases | A + B + C + D |
| Modifies files | Yes (after Gate B confirmation) |
| Requires confirmation | Yes (Gate B: intervention plan) |
| Time estimate | 10-20 minutes |
| Context usage | ~60% of window |
| Output | Assembly report with before/after delta + certification |

**Use when:** You want the skill improved and certified in one session. The workhorse mode.

### Deep Mode

```
Phase A → Gate A → Phase B → Gate B → Phase C → Phase C+ (Trigger) → Re-certify → Phase D
```

| Attribute | Value |
|-----------|-------|
| Phases | A + B + C + C+ + re-certify + D |
| Modifies files | Yes (after Gate B) |
| Requires confirmation | Yes (Gate B + trigger optimization preview) |
| Time estimate | 20-40 minutes |
| Context usage | ~85% of window |
| Output | Full assembly report + trigger optimization metrics |

**Use when:** The skill's structure is solid (score 7+) and trigger accuracy is the highest-leverage improvement. Also: before publishing a skill to a marketplace or distributing to a team.

## Phase Dependency Map

```
Phase A ──→ Gate A decision:
  │           ├── score >= 8 + gate 13/13 → skip to Phase D
  │           └── otherwise → Phase B
  │
  ├── Phase B ──→ Gate B (user confirms plan) ──→ Execute interventions
  │                                                      │
  │                                              Phase C (certify)
  │                                                      │
  │                                    ┌── CERTIFIED ──→ Phase C+ (deep only)
  │                                    │                      │
  │                                    │               Re-certify
  │                                    │                      │
  │                                    └── CONDITIONAL/BLOCKED → Phase D (report remaining)
  │
  └── Phase D (report) ← always runs last
```

## Auto-Selection Logic

When mode is not specified, assess the skill's current state and select:

```
Read SKILL.md → estimate score:
  - No frontmatter or broken YAML → score ~2 → standard
  - Frontmatter OK, missing sections → score ~4-5 → standard
  - All sections present, some weak → score ~6-7 → standard
  - Most sections strong, description weak → score ~7-8 → deep (trigger is the lever)
  - All strong → score ~8+ → quick (already good)
```

**Decision factors beyond score:**
- If the user said "make it great" or "excellent" → bias toward deep
- If the user said "quick check" or "is it ready" → bias toward quick
- If time was mentioned ("I have 10 minutes") → match mode to time budget

## Gate Decision Trees

### Gate A: Should we intervene?

```
if score >= 8 AND gate == 13/13:
    report: "Skill meets production standards. Score: {N}/10."
    if mode == quick: → Phase D
    if mode != quick AND user didn't request changes: → Phase D
    if user explicitly requested changes: → Phase B (override)
else:
    → Phase B
```

### Gate B: Approve intervention plan?

```
present plan to user
if user confirms: → execute
if user removes items: → execute trimmed plan
if user rejects entirely: → Phase D (report diagnostic without changes)
```

### Gate C: Did certification pass?

```
if CERTIFIED:
    if mode == deep: → Phase C+ (trigger optimization)
    else: → Phase D (success)
if CONDITIONAL:
    report remaining blockers
    → Phase D (with "fix these N items" recommendation)
if BLOCKED:
    report foundational issues
    → Phase D (with "re-run surgeon-skill focusing on Layer A" recommendation)
```

## Timing Estimates by Skill Size

| Skill Size | Quick | Standard | Deep |
|-----------|-------|----------|------|
| Single file (< 200 lines) | 2 min | 8 min | 15 min |
| Small (3-5 files, < 500 lines) | 4 min | 12 min | 25 min |
| Medium (5-10 files, 500-2000 lines) | 6 min | 18 min | 35 min |
| Large (10+ files, 2000+ lines) | 10 min | 25 min | 45 min (may hit context limit) |

**Context window risk:** Large skills in deep mode may exhaust context. The pipeline monitors usage and falls back to standard mode if approaching limits, reporting: "Fell back to standard mode due to context constraints. Run trigger-skill separately."

## Cross-Skill Delegation

The assembly-skill doesn't contain diagnostic, improvement, or certification logic. It delegates to the other skills in the suite:

| Phase | Delegates To | What It Passes | What It Receives |
|-------|-------------|---------------|-----------------|
| A | x-ray-skill (internal) | Skill directory path | Scorecard, top 5 issues, component classification |
| B | surgeon-skill (internal) | Path + scorecard + top issues | Changelog, modified files list |
| C | certify-skill (internal) | Path (post-intervention) | Certification report, verdict |
| C+ | trigger-skill (internal) | Path + current description | Optimized description, trigger metrics |

"Internal" means the assembly-skill applies the logic from those skills directly — it doesn't spawn separate skill invocations (which would lose context). It reads the other skills' instructions and follows them.

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
