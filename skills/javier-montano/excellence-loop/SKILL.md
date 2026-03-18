---
name: excellence-loop
description: >
  This skill should be used when the user asks to "polish this output",
  "evaluate quality", "refine this document", "run a quality gate",
  or mentions excellence loop, rubric scoring, or iterative refinement.
  It evaluates output against a 10-criterion rubric, refines until criteria are met, detects diminishing returns, and delivers only the final polished version.
  Use this skill whenever the user needs document-level quality assurance on a deliverable, even if they don't explicitly ask for "excellence loop".
argument-hint: "<content-path or inline content> [--strict] [--show-history] [--max-iterations 3]"
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - Glob
---

# Excellence Loop

No response ships until it earns its score. Evaluate, refine, repeat — then deliver only the final version.

## Scope

This skill runs ONLY on final document outputs: HTML, Markdown, DOCX, PDF, XLSX, or substantial text responses. It does NOT run on intermediate work products, code commits, or conversational replies.

## The Mandate

The loop is invisible. The user receives only the final, polished version. No meta-discourse about iterations, no "I refined this 3 times", no process traces.

**Exception:** User explicitly asks for iteration history. Then deliver final version PLUS a separate version history artifact.

## The 10-Criterion Rubric

Each criterion scored 1-10. Target: all criteria at 10 before delivery.

| # | Criterion | Measures | Quick Test |
|---|-----------|----------|------------|
| 1 | **Foundation** | Structural completeness — all necessary components present? | Remove any section. Does it break? |
| 2 | **Truthfulness** | Factual accuracy — all claims verifiable? | Can you cite a source for every claim? |
| 3 | **Quality** | Writing quality — professional, precise, zero filler? | Read aloud. Does every sentence carry meaning? |
| 4 | **Density** | Information per word — maximum value per token? | Cut 20%. Did you lose anything important? |
| 5 | **Simplicity** | Accessibility — could a non-expert follow the structure? | Show to outsider. Do they get it? |
| 6 | **Clarity** | Unambiguity — one interpretation only? | Could a pedantic reader misinterpret anything? |
| 7 | **Precision** | Specificity — constraints and claims specific enough? | Replace vague words with specifics. Does meaning change? |
| 8 | **Depth** | Edge case coverage — handles the non-obvious? | What happens with weird input? Missing data? |
| 9 | **Coherence** | Internal consistency — no contradictions? | Do all sections reinforce each other? |
| 10 | **Value** | User impact — meaningful improvement over not having this? | Would the user pay for this quality? |

For detailed scoring parameters and repair protocols, read `reference/rubric-criteria.md`.

## The Loop

```
Draft → EVALUATE (score 10 criteria)
              ↓
         All 10/10? → YES → DELIVER
              ↓ NO
         IDENTIFY (3 lowest criteria)
              ↓
         REFINE (targeted fixes)
              ↓
         RE-EVALUATE → All 10/10? → DELIVER
              ↓ NO
         Max iterations? → YES → DELIVER best version
              ↓ NO
         Loop back to IDENTIFY
```

## Iteration Limits

| Signal | Action |
|--------|--------|
| All criteria = 10 | Deliver immediately |
| All criteria >= 8 after iteration 1 | Deliver (good enough for most contexts) |
| Score delta < 0.5 between iterations | Diminishing returns — deliver current best |
| Same criterion fails after 2 fix attempts | Architecture problem — note it, deliver best |
| Total iterations = 3 | Hard stop — deliver current best |

## Refinement Tactics

Fix lowest-scoring criteria first (highest impact).

| Criterion | Typical Fix |
|-----------|-------------|
| Foundation | Add missing sections, strengthen structure |
| Truthfulness | Verify claims, remove unverifiable statements, add sources |
| Quality | Remove filler, fix passive voice, sharpen wording |
| Density | If 2 sentences say the same thing, merge. Compress without losing meaning |
| Simplicity | Flatten hierarchy, replace jargon, simplify |
| Clarity | Replace vague qualifiers with specifics ("appropriate" becomes exact criteria) |
| Precision | Convert aspirational statements to testable claims ("be concise" becomes "max 300 words") |
| Depth | Add edge case handling, failure modes, fallbacks |
| Coherence | Map cross-section dependencies, resolve contradictions |
| Value | Add domain expertise, methodology, reasoning that goes beyond generic |

For detailed tactics with examples, read `reference/refinement-tactics.md`.

## Fast Path

If initial evaluation shows all criteria >= 8:
1. One quick refinement pass targeting any criterion below 10.
2. Re-evaluate.
3. Deliver.

## Confidence-Calibrated Depth

When receiving input from task-engine with confidence metadata:

| Task-engine confidence | Loop depth |
|------------------------|------------|
| >= 0.95 | Fast path (1 iteration max) |
| 0.85 - 0.94 | Standard loop (2 iterations max) |
| < 0.85 | Full loop (3 iterations, aggressive refinement) |

## Version History Format

When requested:
```
## Version History — [Content Name]

### Iteration 1 (initial draft)
- Scores: F:9 V:8 Q:10 D:7 S:9 Cl:8 P:9 Dp:10 Co:9 Va:8
- Average: 8.7/10
- Weaknesses: Density (7), Clarity (8), Value (8)

### Iteration 2 (final)
- Changes: [specific changes made]
- Scores: F:10 V:10 Q:10 D:10 S:10 Cl:10 P:10 Dp:10 Co:10 Va:10
- Average: 10.0/10 — DELIVERED
```

## Pipeline Integration

```
[input-analyst] → [task-engine] → Response → [excellence-loop] → User
```

This is the final stage. Output goes directly to the user.

## Assumptions & Limits

- Scoring is self-assessed. The rubric provides structure, but scores are judgment calls, not measurements.
- "10/10" is an aspiration, not a guarantee. Some content domains resist perfection (creative writing, opinion pieces).
- The loop adds latency proportional to iteration count. For time-sensitive responses, reduce max iterations.
- This skill evaluates document-level quality. It does not validate code correctness, data accuracy, or domain-specific compliance.
- Diminishing returns are real. The third iteration rarely improves scores by more than 0.5 points average.

## Edge Cases

- **Very short content (< 100 words):** Density and Foundation may be hard to score meaningfully. Use judgment — not every criterion applies equally to a 2-sentence answer.
- **Creative content:** Simplicity and Precision may conflict with artistic intent. Score these relative to the content's purpose, not absolute standards.
- **User requests "quick and dirty":** Skip the loop entirely. The user has explicitly opted out of quality iteration.
- **Content in non-English languages:** Apply the same rubric. Criterion names are universal concepts.
- **Scores oscillate between iterations:** A criterion improves then regresses. This indicates a structural tension. Stop, note the trade-off, deliver the best balanced version.
- **User provides their own rubric:** Honor it. Map their criteria to the 10-criterion framework where possible, add any new dimensions.

## Validation Gate

Before delivering the final version, confirm:

- [ ] All 10 criteria have been scored
- [ ] No criterion is below 6 (or the deficit is documented as architectural)
- [ ] At least one refinement pass was attempted (no first-draft delivery for substantial content)
- [ ] The delivered version contains zero meta-commentary about the loop process
- [ ] If iteration history was not requested, no scoring artifacts leak into the output
- [ ] Diminishing returns logic was applied (did not iterate pointlessly)

## Reference Files

- `reference/rubric-criteria.md` — Detailed scoring guide per criterion with examples and repair protocols
- `reference/refinement-tactics.md` — Specific tactics for improving each criterion
- `reference/diminishing-returns.md` — When to stop iterating, signal detection, cost-benefit
- `reference/version-history-template.md` — Archive format for tracking iterations

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
