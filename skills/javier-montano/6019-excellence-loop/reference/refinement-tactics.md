# Refinement Tactics: Criterion-Specific Improvement Strategies

This document provides concrete, actionable tactics for improving each criterion. Use these when `refinement-suggester.py` identifies weak areas.

---

## Densidad (Information Density)

**Goal:** Maximize value per word. Eliminate redundancy and convert prose to structured formats.

### Tactic 1: 2x Constraint (Deduplication)

**Rule:** If two consecutive sentences say the same thing, they must merge into one.

**Process:**
1. Read each pair of consecutive sentences
2. If they express the same core idea, merge them
3. Keep the more specific or precise version
4. Delete the weaker phrasing

**Before:**
```
Machine learning models require large amounts of training data.
The quality of these models depends on having access to substantial datasets.
Without adequate data, the model will not perform well.
```

**After:**
```
Machine learning models require large amounts of high-quality training data;
without it, performance suffers.
```

**Token savings:** 25 → 18 words (28% reduction)

---

### Tactic 2: Table Conversion (Structure Over Prose)

**Rule:** If you list 3+ related items in prose, convert to a table or list.

**Conditions:**
- Items share 2+ common attributes
- Comparison across items is useful
- Items take up 3+ sentences to describe

**Before:**
```
There are three scheduling approaches.
Fixed intervals run tasks at set times and are simple but inflexible.
Event-driven triggers on specific conditions and provides responsiveness but requires setup.
Adaptive scheduling adjusts based on load and offers optimization but adds complexity.
```

**After:**
```
| Approach | Trigger | Pros | Cons |
|----------|---------|------|------|
| Fixed | Set times | Simple | Inflexible |
| Event-driven | Conditions | Responsive | Setup overhead |
| Adaptive | Load-based | Optimized | Complex |
```

**Token savings:** 60 → 30 words (50% reduction)

---

### Tactic 3: Filler Removal (Sentence-by-Sentence Audit)

**Phrases that add no meaning:**
- "It is important to note that..."
- "In this day and age..."
- "It goes without saying..."
- "As mentioned above..."
- "Rather interestingly..."
- "At the end of the day..."

**Before:**
```
It is important to note that modern software development, in this day and age,
requires automation. As a matter of fact, teams that implement CI/CD pipelines
see significant improvements.
```

**After:**
```
Modern software development requires automation. Teams implementing CI/CD
pipelines see significant improvements.
```

**Token savings:** 35 → 16 words (54% reduction)

---

## Calidad (Writing Quality)

**Goal:** Professional, precise writing with zero filler. Every sentence carries meaning.

### Tactic 1: Passive→Active Voice Conversion

**Pattern:** [subject] + [to be] + [past participle] → [agent] + [active verb] + [object]

**Examples:**

| Passive | Active | Improvement |
|---------|--------|-------------|
| "It is believed that performance should be optimized" | "Optimize performance" | -70% words |
| "The system was designed by engineers to handle load" | "Engineers designed the system to handle load" | Direct agent |
| "Testing should be performed after deployment" | "Test after deployment" | Imperative; clear action |
| "Errors were encountered when running the script" | "The script encountered errors" | Concrete subject |

**Before:**
```
The database was optimized by the team in order to improve query performance.
This optimization was accomplished through indexing, which was implemented carefully.
```

**After:**
```
The team optimized the database by carefully implementing indexes, improving query performance.
```

**Passive ratio:** 100% → 0% (3 passives → 0)

---

### Tactic 2: Filler Word Removal

**High-value filler to remove:**
- "rather" ("rather important" → "critical")
- "quite" ("quite good" → "effective")
- "very" (amplifier without precision)
- "really" (emphasis without meaning)
- "basically" (hedge)
- "essentially" (unnecessary)

**Before:**
```
The approach is quite effective and really helps with basically improving clarity.
```

**After:**
```
The approach improves clarity.
```

**Word count:** 13 → 5 (62% reduction)

---

### Tactic 3: Register Consistency Check

**Definition:** Tone and formality level should match throughout.

**Consistency violations:**
- Technical section: "So, like, you need to initialize the cache, ya know?"
- Formal section: "Lol we pretty much just loop over the array"
- Casual intro, formal body with no transition

**Process:**
1. Skim introduction — note the register (casual, professional, academic)
2. Sample each section — does it match?
3. If shift occurs, mark the transition point
4. Rewrite shifted sections to match the dominant register

**Before:**
```
## Advanced Optimization Techniques

Basically, we're gonna use memoization, which is pretty much storing results so you don't
have to compute them again. It's kind of important for performance, IMO.
```

**After:**
```
## Advanced Optimization Techniques

Memoization stores computed results, eliminating redundant calculations and improving performance.
```

---

## Claridad (Clarity/Unambiguity)

**Goal:** One interpretation only. Replace vague qualifiers with specific criteria.

### Tactic: Vague Qualifier Replacement Table

**Replacement strategy:** Every vague word must be replaced with a specific criterion or condition.

| Vague Qualifier | Ambiguous Use | Specific Replacement | Reasoning |
|---|---|---|---|
| "appropriate" | "Choose appropriate tools" | "Choose tools matching [criteria: budget, team skill, integration needs]" | Criteria clarified |
| "sometimes" | "Sometimes you need X" | "When [condition], you need X" | Condition explicit |
| "significant" | "Significant improvement" | "Performance improved 40%" or "Resolves the top 3 user complaints" | Measurable |
| "often" | "Often causes issues" | "Causes issues in [X% of cases] or [when Y happens]" | Frequency explicit |
| "reasonable" | "A reasonable approach" | "An approach that [meets criteria: cost < $X, timeline < Y days]" | Criteria clear |
| "typically" | "Typically takes time" | "Takes 2-3 days with this method" | Specific |
| "usually" | "Usually works well" | "Works well in [conditions]; fails when [conditions]" | Bounded |
| "somewhat" | "Somewhat inefficient" | "Wastes 30% of cycles" or "Slower than alternative by X%" | Quantified |
| "roughly" | "Roughly 100 users" | "102 users" or "90-110 users" | Precise or bounded |
| "perhaps" | "Perhaps this is important" | "[If true, why it matters]. [If false, what doesn't.]" | Remove hedging |

**Before:**
```
You should optimize performance when it seems reasonable and appropriate.
This often helps, though sometimes it may not be necessary.
```

**After:**
```
When response time exceeds 200ms or resource utilization tops 85%, optimize performance.
This typically improves latency by 30-50% and reduces infrastructure costs by 20%.
```

---

## Precisión (Precision/Specificity)

**Goal:** All constraints are testable. No aspirational statements without specifics.

### Tactic: Aspirational→Testable Conversion

**Pattern:** Vague imperative + specific success criterion

| Aspirational | Problem | Testable Version | Success Metric |
|---|---|---|---|
| "Be concise" | How concise? | "Maximum 300 words per section" | Word count |
| "Write clearly" | What's clear? | "Maximum 2 vague qualifiers per paragraph" | Clarity audit |
| "Improve performance" | By how much? | "Reduce latency to < 100ms" | Latency measurement |
| "Make it better" | Better how? | "Increase from [current] to [target]" | Before/after metric |
| "High quality" | What's high? | "Pass code review with 0 objections" or "Score 9/10 on rubric" | Objective measure |
| "Effective communication" | How measured? | "Reader can summarize in <15 seconds" | Comprehension test |
| "Strong argument" | Convince whom? | "Addresses all 5 counterarguments" | Completeness check |

**Before:**
```
The API should be designed well and perform efficiently.
Focus on making it easy to use and reliable.
```

**After:**
```
The API must:
- Support 10,000 requests/sec with <50ms latency
- Require <5 minutes for a developer to integrate
- Return 99.95% uptime
- Provide type-safe responses (TypeScript/Go)
```

---

## Profundidad (Depth/Edge Case Coverage)

**Goal:** Anticipate failures. Handle incomplete, contradictory, and extreme data.

### Tactic: Edge Case Discovery Protocol

Ask these 5 questions for each major component:

#### Question 1: Missing Data
**Ask:** What if required data is missing?
**Example:** "If the user ID is missing, the system crashes"
**Fix:** Add validation with graceful fallback

#### Question 2: Contradictory Data
**Ask:** What if two constraints conflict?
**Example:** "If priority is 'urgent' but deadline is 'end of month', which wins?"
**Fix:** Define resolution rule or escalation path

#### Question 3: Extreme Values
**Ask:** What if this is much larger or smaller than expected?
**Example:** "Works for 100 items; what about 1M items?"
**Fix:** Document limits and provide overflow strategy

#### Question 4: Wrong Path
**Ask:** What if the user doesn't follow the recommended path?
**Example:** "If user skips the setup step, can recovery happen?"
**Fix:** Add detection and recovery mechanism

#### Question 5: Simultaneous Conditions
**Ask:** What if multiple conditions apply at once?
**Example:** "If both timeout AND connection lost, which error surfaces?"
**Fix:** Define priority and composition rules

**Before:**
```
To migrate data:
1. Export from source system
2. Transform to new format
3. Import to target system

Migration is complete when all rows are imported.
```

**After:**
```
To migrate data:
1. Export from source system
   - If export fails: retry 3x, then alert operator
   - If partial export: mark rows as retry candidates

2. Transform to new format
   - If format incompatibility detected: log and skip row
   - If duplicate key found: keep newest, log warning

3. Import to target system
   - If import fails: rollback transaction, retry once
   - If timeout occurs: save checkpoint, resume from last ID

4. Verify
   - Count rows: source export = target import (within ±1 for system deletes)
   - Spot-check 10 random rows
   - Monitor for discrepancies in first 24 hours

Success criteria:
- 100% row count match or documented exceptions
- Zero data corruption
- Rollback available for 48 hours post-migration
- Migration time < [X hours]
```

---

## Coherencia (Coherence/Internal Consistency)

**Goal:** All sections reinforce each other. Zero contradictions.

### Tactic: Cross-Section Dependency Mapping

**Process:**

1. **List all sections**
2. **For each section, identify:**
   - What must be established first (dependencies)?
   - What claims does this section make?
   - What other sections depend on this?
3. **Check ordering:** Can dependencies come after?
4. **Check contradictions:** Do any two sections contradict?

**Example Map:**

```
Intro (dependencies: none)
  ↓ establishes: problem statement, scope
  ↓ required by: all other sections

Architecture (dependencies: problem statement)
  ↓ establishes: system design, component relationships
  ↓ required by: implementation, edge cases

Implementation (dependencies: architecture)
  ↓ establishes: specific code patterns, choices
  ↓ required by: testing, performance tuning

Performance Tuning (dependencies: implementation, edge cases)
  ↓ conflict check: does this contradict simplicity goal? Reconcile

Testing (dependencies: implementation, architecture)
  ↓ cross-check: does test strategy match architecture description?
```

**Contradiction Resolution:**

| Conflict | Resolution |
|----------|-----------|
| Section A: "Always validate input" vs. Section B: "Skip validation for trusted sources" | Clarify: "Validate all external input. For trusted internal services, [specific exception]" |
| Section A: "Use async everywhere" vs. Section B: "Synchronous patterns are simpler" | Clarify: "Use async for I/O; synchronous for CPU-bound work" |
| Section A: "Minimize dependencies" vs. Section B: "Add this library" | Clarify: "Only add dependencies that [criteria]. This library meets [criteria]" |

---

## Valor (Value/User Impact)

**Goal:** Leverage domain expertise. Provide methodology, not just facts.

### Tactic 1: Expertise Injection Patterns

**Pattern 1: Domain-Specific Framework**
```
Before: "Use a database for persistence."
After: "Choose persistence based on [domain framework]:
  - If reads >> writes: optimize for read performance (indexing, caching)
  - If writes >> reads: optimize for write throughput (batching, async)
  - If strong consistency required: SQL + transactions
  - If eventual consistency acceptable: NoSQL + conflict resolution
For this use case [your case], I recommend [choice] because [reasoning]."
```

**Pattern 2: Common Pitfalls**
```
Before: "Document your code."
After: "Document code patterns that experts commonly get wrong:
  - [Pitfall 1]: Why it happens, how to avoid it
  - [Pitfall 2]: Why it happens, how to avoid it
  - [Pitfall 3]: Why it happens, how to avoid it
In your context, watch especially for [Pitfall specific to user's domain]."
```

**Pattern 3: Reasoning Directives**
```
Before: "Choose the right tool."
After: "To choose the right tool, follow this reasoning:
  1. First, map your constraints: [performance, cost, team skill, integration]
  2. Then, rank by importance: [in your domain, usually cost < performance]
  3. Finally, evaluate candidates: [tool A meets [criteria], tool B meets [criteria]]
  For YOUR constraints [user-specific], I recommend [choice]."
```

**Pattern 4: Shortcuts from Experience**
```
Before: "This is a common problem."
After: "This is a common problem. Experts solve it by [shortcut]:
  - What novices do: [long, inefficient path]
  - What experts do: [short, efficient path]
  - Why: [principle underlying the shortcut]
  [Specific code/example of shortcut]"
```

---

## Summary Table: Impact vs. Effort

| Criterion | Typical Effort | Token Savings | Complexity |
|-----------|---|---|---|
| Densidad | Low | 20-40% | Straightforward dedup |
| Claridad | Low | 10-20% | Simple replacement |
| Precisión | Low | 5-15% | Add constraints |
| Calidad | Medium | 15-30% | Requires rewriting |
| Simplicidad | Medium | 10-25% | Flatten hierarchy |
| Profundidad | Medium | 10-30% | Add edge cases |
| Coherencia | Medium | 5-15% | Verify consistency |
| Veracidad | High | Variable | Research & source |
| Fundamento | High | Variable | Restructure |
| Valor | High | Variable | Deep domain work |

**Quick refinement strategy:**
1. Start with low-effort, high-impact (Densidad, Claridad, Precisión)
2. Move to medium-effort (Calidad, Simplicidad, Profundidad)
3. Save high-effort for final passes (Fundamento, Valor, Veracidad)
