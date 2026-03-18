# Evaluation Rubric — Complete Scoring Guide

## Table of Contents

1. [Scoring Parameters](#scoring-parameters)
2. [Criterion Details](#criterion-details)
3. [Failure Taxonomy](#failure-taxonomy)
4. [Adversarial Vectors](#adversarial-vectors)
5. [The Excellence Loop](#the-excellence-loop)

---

## Scoring Parameters

Each criterion is scored 1-10:

| Score Range | Label | Meaning |
|-------------|-------|---------|
| 9-10 | Excellent | Production-ready, no improvements needed |
| 7-8 | Good | Functional, minor improvements possible |
| 5-6 | Acceptable | Works but has clear weaknesses |
| 3-4 | Weak | Significant issues affecting performance |
| 1-2 | Failed | Fundamentally broken, needs redesign |

**Production threshold:** All criteria ≥ 8 for deployment. Any criterion below 6 blocks release.

---

## Criterion Details

### 1. Foundation (Fundamento)

**What it measures:** Structural completeness — archetype, objective, constraints, and flow are present and well-defined.

**Scoring guide:**
- 10: Every Playbook section present, archetype is a true hybrid (domain + methodology + style), objective is measurable
- 8: All sections present, archetype clear but could be more specific
- 6: Missing 1-2 sections, archetype is single-dimensional
- 4: Missing critical sections (constraints or output template), generic role
- 2: No discernible structure, vague intent

**Repair protocol:** Apply the Playbook template. Fill missing sections. Upgrade the archetype to hybrid.

---

### 2. Accuracy (Veracidad)

**What it measures:** Factual correctness of all claims, frameworks, and techniques referenced in the prompt.

**Scoring guide:**
- 10: Every framework, technique, and claim is verifiable and correctly applied
- 8: All major claims correct, minor terminology imprecisions
- 6: Generally correct but includes unsourced or unverifiable claims
- 4: Contains factual errors that would affect output quality
- 2: Major factual errors or hallucinated frameworks

**Repair protocol:** Verify every named framework (AIDA, MECE, etc.). Remove or correct anything unverifiable. Replace proprietary/made-up terminology with standard terms unless the prompt is building a deliberate vocabulary.

---

### 3. Quality (Calidad)

**What it measures:** Writing quality — professional, precise, free of filler, grammatically correct.

**Scoring guide:**
- 10: Every sentence carries meaning, zero filler, professional register throughout
- 8: Mostly clean, 1-2 instances of filler or imprecise wording
- 6: Functional but contains redundancy or inconsistent register
- 4: Noticeable filler, passive voice overuse, unclear passages
- 2: Poorly written, difficult to follow, unprofessional

**Repair protocol:** Remove filler words ("basically", "essentially", "in order to"). Convert passive to active voice. Eliminate redundant sentences. Ensure consistent register throughout.

---

### 4. Density (Densidad)

**What it measures:** Information-to-token ratio. Maximum value per word.

**Scoring guide:**
- 10: Cannot remove a single sentence without losing meaning. Every word earns its place.
- 8: Tight writing, minor compression opportunities
- 6: Some sections could be compressed 20-30%
- 4: Significant redundancy, same ideas stated multiple times
- 2: Could be cut in half without losing content

**Repair protocol:** Apply the 2x constraint — if two sentences say the same thing, merge. Eliminate introductory padding ("In this section we will..."). Convert verbose patterns to concise equivalents.

**Token economics:** Every unnecessary token in a system prompt is paid for on every single interaction. A 500-token prompt used 10,000 times costs 5M tokens of redundancy. Density directly reduces operating cost.

---

### 5. Simplicity (Simplicidad)

**What it measures:** Structural accessibility — could someone unfamiliar with prompt engineering understand how it works?

**Scoring guide:**
- 10: A non-technical user could read and understand the structure
- 8: Clear to anyone with basic AI familiarity
- 6: Requires prompt engineering knowledge to parse
- 4: Over-engineered with unnecessary abstraction layers
- 2: Incomprehensible without deep technical background

**Repair protocol:** Remove jargon that doesn't serve the prompt's function. Flatten unnecessary hierarchy. Replace formal structures with plain language where possible.

---

### 6. Clarity (Claridad)

**What it measures:** Unambiguity. Each instruction has exactly one interpretation.

**Scoring guide:**
- 10: Every instruction is unambiguous. A pedantic reader would interpret it identically to a casual one.
- 8: Mostly clear, 1-2 instructions could be read two ways
- 6: Several ambiguous instructions that could produce different behaviors
- 4: Key sections are open to interpretation
- 2: Contradictory or systematically ambiguous

**Repair protocol:** For each instruction, ask: "Could a literal-minded AI interpret this differently than intended?" If yes, rewrite with specifics. Replace "appropriate" with exact criteria. Replace "sometimes" with explicit trigger conditions.

---

### 7. Precision (Precisión)

**What it measures:** Constraint specificity. Are boundaries enforceable or just aspirational?

**Scoring guide:**
- 10: Every constraint is testable (you could write an assertion for it)
- 8: Most constraints are specific and enforceable
- 6: Mix of specific and vague constraints
- 4: Constraints are mostly aspirational ("be professional", "keep it concise")
- 2: No enforceable constraints

**Repair protocol:** Convert aspirational constraints to specific ones. "Be concise" → "Maximum 300 words per response". "Be professional" → "Use third-person, no contractions, cite sources with inline references".

---

### 8. Depth (Profundidad)

**What it measures:** Edge case handling, failure modes, and advanced scenarios.

**Scoring guide:**
- 10: Handles ambiguous input, conflicting requirements, missing context, and failure states gracefully
- 8: Covers main edge cases, has fallback behavior defined
- 6: Handles the happy path well but doesn't address edge cases
- 4: Only works for ideal inputs
- 2: Breaks on any non-trivial variation

**Repair protocol:** Identify the top 5 ways a user could "break" the prompt. Add handling for each: ambiguous requests, missing information, contradictory constraints, scope-exceeding requests, and multi-turn context loss.

---

### 9. Coherence (Coherencia)

**What it measures:** Internal consistency. All sections reinforce each other. No contradictions.

**Scoring guide:**
- 10: Every section references and supports the others. Reading any section in isolation gives a consistent picture.
- 8: Mostly coherent, minor tensions between sections
- 6: Some sections feel disconnected or repetitive
- 4: Contradictions between constraints, role, and output format
- 2: Sections actively conflict with each other

**Repair protocol:** Map dependencies between sections. Check: Does the output template match what the interaction flow produces? Do constraints align with the stated role? Does the tone directive match the archetype?

---

### 10. Value (Valor)

**What it measures:** The delta between using this prompt and not using it. Would a user get meaningfully better results?

**Scoring guide:**
- 10: Transformative improvement — the AI behaves as a genuinely different, specialized tool
- 8: Clear improvement in consistency, quality, and relevance of outputs
- 6: Modest improvement, mostly in formatting consistency
- 4: Marginal improvement over a vanilla conversation
- 2: No discernible benefit over talking to the base model directly

**Repair protocol:** Identify what the prompt adds that the base model wouldn't do on its own. If the answer is "formatting only", add domain-specific reasoning, constraints, and methodology. The prompt should embed expertise, not just cosmetics.

---

## Failure Taxonomy

Common failure patterns and their root causes:

| Failure Pattern | Symptom | Root Cause | Fix |
|----------------|---------|------------|-----|
| Lazy drift | AI gives shorter, less detailed responses over turns | No depth maintenance directive | Add self-correction trigger for response length |
| Scope creep | AI answers questions outside its domain | Weak constraints, no refusal protocol | Add explicit out-of-scope handling |
| Context amnesia | AI forgets earlier conversation details | No conversation state management | Add state summary between phases |
| Format decay | Output format degrades after a few turns | Output template not reinforced | Add format reminder in iteration phase |
| Hedging inflation | Responses get increasingly tentative | Executive tone not reinforced | Add anti-hedging directive in constraints |
| Hallucination cascade | AI invents facts that build on each other | No uncertainty signaling | Add "flag when uncertain" protocol |

---

## Adversarial Vectors

Five vectors to test prompts against:

1. **Lazy LLM** — The model tries to minimize effort. Test: give a complex request and check if the response is thorough.
2. **Recency Override** — Recent conversation overrides system prompt behavior. Test: after 10 turns, check if the role is still active.
3. **Context Overflow** — Too much information in the conversation causes the model to lose system prompt instructions. Test: flood with data, check behavior.
4. **Format Hallucination** — The model invents a format different from the one specified. Test: check if output matches the template exactly.
5. **Scope Escape** — The model answers off-topic questions it should refuse. Test: ask something outside the defined domain.

---

## The Excellence Loop

Structured iteration to reach production quality:

```
┌─ Score the prompt against all 10 criteria
│
├─ Identify the 3 lowest-scoring dimensions
│
├─ Apply the repair protocol for each
│
├─ Re-score (verify improvement, check for regressions)
│
├─ If all ≥ 8 → DONE
│
└─ If not → repeat (max 3 iterations)
```

**Iteration discipline:**
- Fix no more than 3 dimensions per iteration (more causes regressions)
- After each fix, verify that other dimensions didn't decrease
- If a dimension stubbornly stays below 8 after 2 attempts, reconsider whether the prompt's architecture needs restructuring rather than patching
