# Trigger Patterns: Common Failures & Phrase Templates

Reference for trigger-skill. Organized by failure type, then by skill category.

## Common Trigger Failures

### Failure Type 1: Under-Triggering (skill never fires)

| Cause | Example | Fix |
|-------|---------|-----|
| First-person description | "I analyze skills for quality" | Third person: "This skill should be used when..." |
| No trigger phrases | "Analyzes and improves skill quality" | Add 3-5 quoted phrases: "audit a skill", "review quality" |
| Too technical | "Performs structural validation against gold-standard anatomy" | Use user language: "check if this skill is good" |
| Missing broader context | Description only covers exact matches | Add: "even if they don't explicitly ask for..." |
| Description too short | "Skill quality tool." (under 50 chars) | Expand to 150-300 chars with triggers + context |

### Failure Type 2: Over-Triggering (skill fires on unrelated requests)

| Cause | Example | Fix |
|-------|---------|-----|
| Vague keywords | "quality" triggers on any quality-related request | Scope: "skill quality" not just "quality" |
| Missing scope boundary | "Analyzes code" triggers on any code analysis | Add: "for Claude Code skills" (not generic code) |
| Keyword stuffing | 15 trigger phrases covering too much ground | Trim to 3-5 most specific phrases |
| No "what it IS" clause | Only trigger phrases, no functional description | Add: "{what it does}" after the trigger phrases |

### Failure Type 3: Cross-Triggering (wrong sibling skill fires)

| Cause | Example | Fix |
|-------|---------|-----|
| Identical domain keywords | x-ray-skill and certify-skill both mention "quality check" | Differentiate: x-ray = "diagnose/audit", certify = "validate/certify/gate" |
| Overlapping trigger phrases | Two skills both claim "improve this skill" | Assign ownership: surgeon-skill owns "improve", x-ray-skill owns "diagnose" |
| Vague functional description | Both say "evaluates skill quality" | Specify the distinct output: "produces scorecard" vs "produces certification verdict" |

## Phrase Templates by Skill Category

### Analysis/Diagnostic Skills

```
This skill should be used when the user asks to "{action verb} {domain object}",
"{question form}", "{colloquial phrase}", or mentions {domain keyword}.
{One sentence: reads/analyzes X and produces Y.}
Use this skill whenever {broader trigger}, even if they don't explicitly ask for "{skill name}".
```

**Effective trigger verbs:** audit, diagnose, assess, scan, review, inspect, check, analyze
**Effective question forms:** "how good is...", "what's the state of...", "is this ready..."

### Creation/Generation Skills

```
This skill should be used when the user asks to "{create verb} {artifact}",
"{build/make/generate} {artifact}", or needs {artifact type}.
{One sentence: generates X from Y with Z quality standards.}
Use this skill whenever {creation trigger}, even if they describe the need without naming the artifact.
```

**Effective trigger verbs:** create, build, generate, scaffold, draft, design, write
**Effective need-based triggers:** "I need a...", "help me make...", "can you build..."

### Improvement/Fix Skills

```
This skill should be used when the user asks to "{improve verb} {target}",
"{fix/upgrade/elevate} {target}", or says "{target} needs work".
{One sentence: reads X, identifies improvements, applies them preserving Y.}
Use this skill whenever {improvement trigger}, even if they just say "make it better".
```

**Effective trigger verbs:** improve, fix, upgrade, elevate, polish, refine, enhance
**Effective implicit triggers:** "make it better", "this needs work", "not good enough"

### Validation/Gate Skills

```
This skill should be used when the user asks to "{validate verb} {target}",
"{gate question}", or needs a quality verdict.
{One sentence: runs N checks and produces {PASS/FAIL/verdict}.}
Use this skill whenever {validation trigger}, even if they just ask "is this ready to ship".
```

**Effective trigger verbs:** certify, validate, verify, approve, gate, sign-off
**Effective gate questions:** "is this ready?", "can I ship this?", "does this pass?"

## Adjacency Conflict Resolution

When two skills have similar descriptions, differentiate on these dimensions (in priority order):

| Dimension | How to Differentiate | Example |
|-----------|---------------------|---------|
| **Action verb** | Each skill owns distinct verbs | x-ray owns "diagnose/audit", surgeon owns "improve/fix" |
| **Output type** | Each skill produces a distinct artifact | x-ray → scorecard, certify → certification verdict |
| **Lifecycle stage** | Each skill operates at a different point | x-ray = before improvement, certify = after improvement |
| **Scope** | Each skill covers different scope | x-ray covers "one skill", some other skill covers "all skills in a plugin" |

**Resolution process:**
1. List the conflicting skills' descriptions side by side
2. Identify which triggers overlap
3. Assign each overlapping trigger to the skill where it's most semantically natural
4. Rewrite both descriptions to emphasize their distinct action verbs and outputs
5. Re-test both with the same query set to verify differentiation

## Query Generation Heuristics

### For Should-Trigger Queries

| Category | How to Generate | Count |
|----------|----------------|-------|
| Exact match | Copy trigger phrases from the description | 3-4 |
| Paraphrase | Rewrite each trigger phrase in 2 different ways | 3-4 |
| Implicit | Describe the need without naming the skill or its verbs | 2-3 |
| Edge/borderline | Use adjacent domain language that probably belongs to this skill | 1-2 |

### For Should-NOT-Trigger Queries

| Category | How to Generate | Count |
|----------|----------------|-------|
| Adjacent domain | Use trigger phrases from sibling skills | 2-3 |
| Unrelated | Completely different domain (coding, writing, math) | 2-3 |
| Adversarial | Contains trigger keywords in wrong context | 1-2 |

**Quality check for test queries:** Each query should be something a real user would actually type. "Please execute the skill quality diagnostic assessment framework" is not a real user query. "Check this skill for me" is.

## Iteration Strategy

### Iteration 1: Fix False Negatives

False negatives (should trigger, doesn't) usually indicate missing trigger phrases or overly narrow description. Add the most common paraphrases that users actually say.

### Iteration 2: Fix False Positives

False positives (shouldn't trigger, does) usually indicate overly broad keywords or missing scope qualifiers. Narrow by adding domain context or functional specificity.

### Iteration 3: Balance and Polish

Verify the previous changes didn't introduce new problems. Tighten language for character efficiency (every char in the 1024 budget should earn its place).

**Diminishing returns beyond 3 iterations:** Each iteration has less room to improve. If accuracy plateaus, accept the best version and stop. Spending 2 more iterations for 1% improvement is a poor use of context.

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
