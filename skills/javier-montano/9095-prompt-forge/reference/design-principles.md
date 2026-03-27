# Design Principles — Deep Dive

Seven principles govern every prompt produced by prompt-forge. Each principle exists because it solves a real failure mode observed across thousands of prompt iterations.

## Table of Contents

1. [Hybrid Role](#1-hybrid-role)
2. [Conversational Flow](#2-conversational-flow)
3. [Deliverable-Oriented](#3-deliverable-oriented)
4. [Dynamic Intelligence](#4-dynamic-intelligence)
5. [Executive Tone](#5-executive-tone)
6. [Complete Structure](#6-complete-structure)
7. [Iterative Co-Design](#7-iterative-co-design)

---

## 1. Hybrid Role

**Problem it solves:** Generic roles ("You are a helpful assistant") produce generic outputs. Single-domain roles ("You are a copywriter") miss cross-disciplinary opportunities.

**The pattern:** Combine three dimensions into one archetype:

```
Archetype = Domain Expertise + Methodology + Communication Style
```

**Example:**
```
You are a conversion-focused content strategist who applies behavioral psychology
frameworks (Cialdini, Kahneman) and communicates like a senior McKinsey consultant —
direct, evidence-driven, structured in recommendations.
```

**Dimensions to combine:**

| Dimension | Purpose | Examples |
|-----------|---------|----------|
| Domain expertise | What the AI *knows* | UX design, tax law, prompt engineering |
| Methodology | How the AI *thinks* | Design thinking, MECE, scientific method |
| Communication style | How the AI *speaks* | Executive briefing, coaching, academic |

**Validation checklist:**
- Does the archetype restrict the AI's scope? (It should)
- Could someone infer the output style from the role alone?
- Would a human with this profile exist in the real world?

**Antipatterns:**
- "You are an expert in everything" — too broad, no constraint value
- "You are a Python developer" — too narrow, misses architectural and communication dimensions
- Stacking 5+ roles without synthesis — confuses priority

---

## 2. Conversational Flow

**Problem it solves:** Flat prompts create unpredictable conversation trajectories. The AI doesn't know when to ask, when to execute, when to deliver.

**The pattern:** Structure interaction as a state machine with phases:

```
Discovery → Execution → Delivery → [Iteration]
```

Each phase has:
- **Entry condition** — What triggers this phase
- **Behavior** — What the AI does in this phase
- **Exit condition** — What moves to the next phase

**Example:**
```markdown
### Phase 1: Discovery (1-2 turns)
Entry: User initiates conversation
Behavior: Ask max 2 targeted questions to identify deliverable type and constraints
Exit: User confirms scope OR provides enough context to infer

### Phase 2: Execution
Entry: Scope confirmed
Behavior: Generate complete first draft using Playbook template
Exit: Draft delivered

### Phase 3: Iteration
Entry: User provides feedback
Behavior: Apply targeted modifications, re-evaluate affected sections
Exit: User approves OR 3 iterations reached
```

**Design rules:**
- Max 2 questions per turn (more causes user fatigue)
- Proactive inference over interrogation — guess intelligently, confirm quickly
- First-strike value: deliver something useful in the first substantial response

---

## 3. Deliverable-Oriented

**Problem it solves:** Prompts that say "help users with X" produce aimless conversations. Without a concrete output, neither the AI nor the user knows when they're done.

**The pattern:** Define the exact artifact the user walks away with.

**Good:**
```
Deliverable: A 500-word product description following the PAS framework,
formatted in markdown with H2 headings for Problem, Agitation, Solution,
and a call-to-action footer.
```

**Bad:**
```
Help the user write better product descriptions.
```

**Deliverable checklist:**
- Format specified (markdown, JSON, structured prose, etc.)
- Length bounded (approximate word count or section count)
- Structure defined (what sections, in what order)
- Success criteria clear (what makes it "done")

---

## 4. Dynamic Intelligence

**Problem it solves:** LLMs default to surface-level pattern matching. Without explicit reasoning directives, complex tasks get shallow treatment.

**The pattern:** Embed reasoning techniques directly in the prompt structure.

**Chain-of-thought integration:**
```markdown
Before generating the deliverable, analyze:
1. What is the user's actual goal (not just the stated request)?
2. What constraints limit the solution space?
3. What are 2-3 viable approaches?
4. Which approach best fits the constraints and why?
```

**Multi-perspective analysis:**
```markdown
Evaluate the problem from three lenses:
- Technical feasibility (can it be built?)
- User impact (will anyone use it?)
- Business viability (does it make money?)
```

**Tree-of-thought for complex decisions:**
```markdown
For non-obvious decisions:
- Generate 3 candidate solutions
- Evaluate each against the constraints
- Select the best and explain why the others were rejected
```

**When to use each:**
- Chain-of-thought → sequential reasoning, step-by-step problems
- Multi-perspective → evaluation, recommendation, strategy
- Tree-of-thought → design decisions with multiple valid paths

---

## 5. Executive Tone

**Problem it solves:** LLMs over-hedge by default. "I think maybe you could perhaps consider..." destroys confidence and wastes tokens.

**The pattern:** Write instructions that produce direct, confident, professional output.

**Tone directives:**
```markdown
Communication rules:
- Lead with the recommendation, then justify
- No hedging language ("might", "perhaps", "it seems like")
- Use concrete specifics over abstract descriptions
- If uncertain, state the uncertainty directly: "I don't have data on X"
  rather than softening everything with qualifiers
```

**The Minto Pyramid (inverted structure):**
```
1. Conclusion / Recommendation (what to do)
2. Justification (why this approach)
3. Evidence (supporting data and analysis)
4. Context (background needed to evaluate)
```

This mirrors how senior professionals communicate — answer first, details if needed.

---

## 6. Complete Structure

**Problem it solves:** Incomplete prompts create behavior gaps. The AI encounters situations the prompt didn't anticipate and improvises poorly.

**The pattern:** Use the Playbook template (see `playbook-template.md`) as a completeness checklist. Every section exists because omitting it causes a specific failure:

| Section | Failure When Missing |
|---------|---------------------|
| Role & Archetype | Generic, unfocused outputs |
| Objective | No success criteria, endless conversation |
| Parameters | Wrong model settings, token waste |
| Interaction Flow | Unpredictable conversation shape |
| Constraints | Scope creep, harmful outputs |
| Key Questions | Missing context, wrong assumptions |
| Output Template | Inconsistent deliverable format |
| Self-Correction | Errors compound without recovery |

**Completeness rule:** A prompt can omit sections intentionally (simple use cases don't need all sections), but never accidentally. If a section is missing, there should be a reason.

---

## 7. Iterative Co-Design

**Problem it solves:** Prompts aren't software — you can't "spec" them perfectly upfront. They improve through structured testing and feedback.

**The pattern:** Build feedback loops into both the prompt and the design process.

**In-prompt self-correction:**
```markdown
Self-correction triggers:
- If the user says "that's not what I meant" → re-enter Discovery phase
- If output exceeds 2x the expected length → compress and highlight key points
- If confidence on a claim is < 70% → flag it explicitly
- After 3 turns without progress → summarize state and offer reset
```

**In-process iteration (the Excellence Loop):**
1. Draft the prompt
2. Score against the 10-criterion rubric
3. Fix the lowest-scoring dimensions
4. Re-score. Target: all dimensions ≥ 8
5. Test with 3 real-world scenarios
6. Collect feedback, iterate

**Semantic versioning for prompts:**
- v0.X — Draft, still in design
- v1.0 — First stable version, tested and scored
- v1.X — Minor improvements (constraint tweaks, tone adjustments)
- v2.0 — Major restructure (new sections, changed flow)

Track versions in the prompt header so you know what changed and why.
