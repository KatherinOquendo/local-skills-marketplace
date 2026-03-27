# Improvement Patterns: Prioritized by Impact

15 patterns across 3 layers. Apply top-down: infrastructure first, then content, then DX. Each pattern has: When (trigger condition), Fix (specific action), Risk (what can go wrong), and Verification (how to confirm success).

## Layer A: Structural Infrastructure (Highest Impact)

Fixes that unblock all other quality work. A skill with broken infrastructure can't be evaluated on content.

### A1. Frontmatter Repair

**When:** name not kebab-case, description lacks triggers, description is first-person, or description exceeds 1024 chars.

**Fix:** Rewrite description in third person with 3-5 trigger phrases. Add "even if they don't explicitly ask for..." clause.

**Before → After:**
```yaml
# Before
description: "Analyzes user input and reformulates prompts."

# After
description: >
  This skill should be used when the user asks to "analyze my input",
  "clean up my request", or "reformulate this prompt". Analyzes raw
  user input and reformulates into precise prompts. Use whenever
  input seems vague or ambiguous, even if not explicitly requested.
```

**Risk:** Over-stuffing triggers makes the skill fire on unrelated inputs. Limit to 3-5 specific phrases that users actually say.
**Verification:** Read the description aloud. Could a colleague tell when to use this skill from the description alone?

### A2. Directory Naming Alignment

**When:** Directories don't match ecosystem convention (reference/ vs references/, tools/ vs scripts/).

**Fix:** Rename directories. Update every path reference in every file. Verify with `grep -r 'old-name/' .` — result should be zero matches.

**Risk:** Broken references if any path is missed. Mitigation: grep all files for the old name BEFORE renaming to build a complete checklist.
**Verification:** `grep -r 'old-name/' .` returns zero matches after rename.

### A3. Progressive Disclosure Section

**When:** SKILL.md references files in references/ but doesn't tell Claude WHEN to load them.

**Fix:** Add a "Before {Action}" section mapping each reference to its loading condition AND skip condition.

```markdown
- **Step 1:** Read `references/X.md` when {condition}. Skip when {other condition}.
```

**Risk:** Loading conditions too broad = loads everything (defeats the purpose). Too narrow = misses context. Target: each reference loaded in ~30-50% of invocations.
**Verification:** For a clear, simple input, no references should load. For a complex, multi-gap input, 2-3 references should load.

### A4. Evals Infrastructure

**When:** No evals/ directory or evals.json.

**Fix:** Create evals/evals.json with minimum 5 test prompts. Requirements:
- Each eval targets a distinct capability
- 1+ false-positive test (input that should NOT trigger deep behavior)
- 1+ edge case test
- Assertions are discriminating (not "output is not empty")

**Risk:** Evals that pass trivially don't catch regressions. Each assertion should fail if the skill degrades — test by imagining a broken version of the skill.
**Verification:** For each assertion, ask: "Would this pass if the skill did nothing useful?" If yes, the assertion is too weak.

### A5. Glossary and Data Contracts

**When:** Multiple files use different words for the same concept, or inter-component input/output is implicit.

**Fix:** Add to SKILL.md:
1. **Glossary table** — term | definition | produced by
2. **Data contracts table** — component | receives | produces

**Risk:** Over-formalizing simple skills. A single-file skill with 3 sections doesn't need a glossary. Apply only when terminology confusion is detected (same concept, different words across files).
**Verification:** Grep 5 key terms from the glossary across all files. Zero variants found.

## Layer B: Instructional Quality (High Impact)

Improves how well the skill guides the model. Structure without good instructions produces structured garbage.

### B1. Good vs Bad Example

**When:** No concrete comparison showing correct vs incorrect behavior.

**Fix:** Add "Example: Good vs Bad" section with:
- Specific input
- Bad approach (with specific failure mode: over-analysis, projection, scope invention)
- Good approach (with reasoning for why it's correct)

**Risk:** Example too specific to one scenario → model over-fits. Example too generic → no calibration value. Target: an example that illustrates the skill's most important decision (e.g., when to go deep vs when to pass through).
**Verification:** A reader unfamiliar with the skill can articulate the core quality difference from the example alone.

### B2. Caps Emphasis → Reasoning

**When:** Instructions use ALL CAPS, MUST, ALWAYS, NEVER as emphasis.

**Fix:** Replace each with reasoning. Pattern: "[rule] because [consequence if violated]."

```markdown
# Before: "ALWAYS preserve intent. NEVER change meaning."
# After: "Preserve intent when correcting — a wrong correction is worse than leaving the typo."
```

**Risk:** Removing emphasis without adding reasoning leaves the instruction weaker. Every CAPS removal must be accompanied by a "because" clause.
**Verification:** Grep for ALL CAPS words (excluding acronyms). Count should be zero.

### B3. Reference Pointers with WHEN Context

**When:** Reference files mentioned without loading conditions.

**Fix:** Each pointer gets: "Read X when {condition}. Skip when {other condition}."

**Risk:** Missing the skip condition. Without it, Claude defaults to loading everything.
**Verification:** Each reference pointer has both a load-when AND a skip-when.

### B4. Failure Modes Table

**When:** Assumptions & Limits exists but doesn't prescribe recovery behavior.

**Fix:** Add table: failure | signal | recovery. Include at minimum:
- Insufficient input (too short, too vague)
- Tool failure (script error, permission denied)
- Conflicting signals (multiple interpretations)
- Output too large/small for context

**Risk:** Generic recovery ("handle appropriately") is worse than no table — it gives false confidence. Every recovery must be a specific action.
**Verification:** Each recovery row answers: "If I encounter this, what exactly do I do next?"

### B5. Evidence Tagging

**When:** Claims and inferences aren't distinguished from user statements.

**Fix:** Define taxonomy (explicit / inferred / open) and require all passes/steps to tag their outputs.

**Risk:** Over-tagging creates noise. Apply evidence tagging only to skills that make inferences about user intent — not to utility skills that process deterministic input.
**Verification:** In the skill's output template, each claim-bearing field has an evidence type.

## Layer C: Developer Experience (Medium Impact)

Improves maintainability and iteration. Not critical for first deployment but compounds over time.

### C1. Cross-File Deduplication

**When:** Content appears in both SKILL.md and a reference file, or in multiple reference files.

**Fix:** Keep content in the most specific file. Replace duplicates with cross-references. SKILL.md has the overview; references have the depth.

**When NOT to apply:** Short duplications (1-2 sentences) that serve as self-contained context. Forcing a reader to jump to another file for a 1-sentence concept is worse than minor duplication.
**Verification:** Grep 10-word phrases from references/ in SKILL.md. Matches beyond single-sentence context pointers indicate duplication.

### C2. Confidence Aggregation

**When:** Multiple passes produce separate confidence levels but no aggregation rule.

**Fix:** Define: overall confidence = min(per-pass confidences). Document per-pass criteria.

**When NOT to apply:** Skills with a single step or no confidence concept. Don't add confidence mechanics where the domain doesn't warrant them.
**Verification:** The output schema includes an overall confidence field with documented aggregation logic.

### C3. Backtrack Protocol

**When:** Multi-pass pipeline with no guidance for when a later pass invalidates an earlier result.

**Fix:** Add backtrack table: discovery → which pass to re-run → what downstream changes.

**When NOT to apply:** Single-pass skills or skills where passes don't feed each other.
**Verification:** For each pass that produces output used by a later pass, the backtrack table has an entry for "what if this output turns out to be wrong?"

### C4. Multi-Turn Handling

**When:** Skill assumes single-shot input but users send follow-up messages.

**Fix:** Add guidance: accumulate context (don't restart), resolve open questions, detect intent drift, expect confidence to increase across turns.

**When NOT to apply:** Skills invoked once per session (packaging, validation). Multi-turn matters for analysis and creation skills.
**Verification:** The skill has explicit instructions for how a second message modifies the first analysis.

### C5. Output Schema Alignment

**When:** Output template in SKILL.md doesn't match JSON schema in workflow/evals.

**Fix:** Make them identical in field names and structure. Human-readable template and JSON schema are views of the same contract.

**Verification:** List field names from SKILL.md template and from JSON schema side by side. Zero mismatches.

## Intervention Protocol

For every fix, regardless of layer:

```
1. SNAPSHOT   → Read the target file. Note key domain concepts.
2. APPLY      → Make the specific change. Prefer Edit over Write (smaller diff).
3. VERIFY     → Re-read. Confirm every domain concept from the snapshot is present.
4. DOCUMENT   → Record: what changed, why, which file:lines, what was preserved.
```

**Content preservation is the surgeon-skill's hippocratic oath.** Domain knowledge is the reason the skill exists. Structural improvements serve the knowledge — never the reverse. If an intervention requires removing domain content, stop and ask the user.

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
