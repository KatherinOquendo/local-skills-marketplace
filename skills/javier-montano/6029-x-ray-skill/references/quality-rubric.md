# Quality Rubric: 10 Criteria + 13-Point Gate

Shared reference for x-ray-skill and certify-skill. Defines every quality measurement with scoring guides, detection methods, and the certification formula.

## 10-Criterion Quality Rubric

Each criterion scored 1-10. Pass threshold: every dimension >= 7, average >= 8.

### 1. Foundation (Fundamento)

Every claim traces to a methodology, evidence type, or design decision.

| Score | Meaning | Example |
|-------|---------|---------|
| 10 | Every instruction has a traceable rationale. Trade-offs cited. | "Keep under 500 lines because progressive disclosure reduces cognitive load" |
| 7 | Most grounded. A few "do X" without why. | 2-3 rules without reasoning in a 200-line skill |
| 4 | Many rules without rationale. Feels arbitrary. | "Use tables" with no explanation of benefit |
| 1 | No reasoning anywhere. | Random list of commands |

**Detection:** Search for imperative statements. If a rule exists without a "because", trade-off, or reasoning sentence within 2 lines, it lacks foundation. Count: ungrounded rules / total rules = gap percentage.

### 2. Truthfulness (Veracidad)

No fabricated data, unsupported statistics, or over-promised capabilities.

| Score | Meaning | Example |
|-------|---------|---------|
| 10 | Every quantitative claim verifiable or marked as estimate. | "Typically 3-5 minutes" → acceptable estimate. "Saves 60% of time" → needs evidence. |
| 7 | Mostly accurate. 1-2 soft claims without evidence. | "Most users prefer..." without data |
| 4 | Multiple unsupported statistics. | "Reduces errors by 80%" with no source |
| 1 | Fabricated data or misleading capabilities. | Claims the skill can do things it structurally cannot |

**Detection:** Grep for percentages (`\d+%`), time estimates ("minutes", "hours"), and superlatives ("most", "best", "always"). Each hit: verifiable? If not, marked as estimate? If neither, truthfulness violation.

### 3. Quality (Calidad)

Professional writing, consistent formatting, all references resolve.

| Score | Meaning |
|-------|---------|
| 10 | Consistent heading hierarchy (h2→h3→h4, no jumps), table formatting, code blocks. All refs resolve. No typos. |
| 7 | Minor inconsistencies. One broken ref or mixed style. |
| 4 | Multiple broken refs. Mixed formatting. Orphan sections. |
| 1 | Unprofessional. Broken structure. |

**Detection:** (1) `Grep '^#{1,6} '` — check heading levels are sequential. (2) Grep file paths in SKILL.md → `ls` each. (3) Check table alignment consistency. (4) Spot-check for typos in headers and key terms.

### 4. Density (Densidad)

Every sentence carries unique value. Zero filler across files.

| Score | Meaning |
|-------|---------|
| 10 | Remove any sentence → information loss. No two sentences say the same thing. Zero cross-file duplication. |
| 7 | Occasional redundancy. Some compressible sentences. Minor cross-file overlap. |
| 4 | Significant filler. Multiple sections restating the same point. |
| 1 | Could be 50% shorter without losing content. |

**Detection:** (1) Per paragraph: "If deleted, does the reader lose anything?" (2) Cross-file: grep 10-word phrases from references/ in SKILL.md — matches indicate duplication. (3) Check for meta-commentary that describes what will happen instead of just doing it ("In this section we will explain how to...").

### 5. Simplicity (Simplicidad)

Simplest expression of each idea. No over-engineered prose.

| Score | Meaning |
|-------|---------|
| 10 | Fewest words preserving precision. Tables over paragraphs. One concern per section. |
| 7 | Generally clear. A few over-explained concepts. |
| 4 | Multiple frameworks for the same concept. Abstractions without payoff. |
| 1 | Simple ideas buried in jargon or process. |

**Detection:** (1) Sections explaining the same concept in multiple ways — pick the best, delete the rest. (2) Meta-commentary ratio: sentences about the process vs sentences that ARE the process. (3) Word count per concept — if you need 100 words where 30 would suffice, simplicity is low.

### 6. Clarity (Claridad)

Unambiguous. Two readers interpret identically.

| Score | Meaning |
|-------|---------|
| 10 | Zero ambiguity. Every instruction has one interpretation. Pronouns have antecedents. Terms defined. |
| 7 | Mostly clear. A few dual-interpretation statements. |
| 4 | Multiple ambiguous instructions. Undefined terms. |
| 1 | Contradictory instructions. Reader cannot determine what to do. |

**Detection:** (1) Grep for pronouns without antecedents: "it", "this", "that" not preceded by a noun in the same sentence. (2) Undefined terms: concepts used as if common knowledge but never defined. (3) Grep for "appropriate", "relevant", "as needed" without qualifying criteria.

### 7. Precision (Precisión)

Specific numbers, names, thresholds — not vague qualifiers.

| Score | Meaning |
|-------|---------|
| 10 | All thresholds numeric ("under 500 lines", "3+ edge cases"). All deliverables named. All criteria testable. |
| 7 | Mostly specific. A few "some", "many", "appropriate" without bounds. |
| 4 | Vague throughout. "Good quality", "reasonable effort". |
| 1 | No measurable criteria anywhere. |

**Detection:** Grep for vague qualifiers: "appropriate", "reasonable", "good", "some", "many", "various", "several", "enough". Each unqualified hit = precision deduction. Count: vague terms / total qualifying terms.

### 8. Depth (Profundidad)

Covers edge cases, trade-offs, failure modes. Anticipates what goes wrong.

| Score | Meaning |
|-------|---------|
| 10 | 5+ edge cases with handling. Failure mode table with recovery. Trade-offs with reasoning. Antipatterns listed. |
| 7 | 3+ edge cases. Some failure handling. Trade-offs mentioned. |
| 4 | Edge cases mentioned but not handled. No failure modes. |
| 1 | Happy path only. |

**Detection:** Count: edge cases (with handling instructions, not just mentions), failure modes (with recovery, not just listing), trade-offs (with reasoning, not just "there are trade-offs"). Each needs a specific handling instruction — "handle appropriately" doesn't count.

### 9. Coherence (Coherencia)

Consistent terminology cross-file. No contradictions.

| Score | Meaning |
|-------|---------|
| 10 | Same concept = same word everywhere. Glossary defined. All cross-refs resolve. Zero contradictions. |
| 7 | Mostly consistent. 1-2 terminology variants. |
| 4 | Multiple terms for same concept. Cross-file contradictions. |
| 1 | Files contradict each other. |

**Detection:** (1) Pick 5 key terms from SKILL.md. Grep each across all files. Flag variants (same concept, different words). (2) Compare instructions in SKILL.md vs references — do they ever contradict? (3) Check all file paths reference real files and all files are referenced.

**Single-file skills:** Automatic 10 or N/A (no cross-file to contradict). Don't penalize for having one file.

### 10. Value (Valor)

Every section justifies its existence.

| Score | Meaning |
|-------|---------|
| 10 | Delete any section → skill breaks or measurably degrades. Every component serves the user's need. |
| 7 | Most sections essential. 1-2 nice-to-have but not load-bearing. |
| 4 | Multiple sections that don't affect behavior. Template-driven structure. |
| 1 | Mostly boilerplate. Structure without substance. |

**Detection:** For each section: "If this didn't exist, would the skill produce worse output?" Sections that exist only because a template required them (empty edge cases, template validation) are zero-value. Sections whose content appears elsewhere are negative-value (duplication cost > information value).

## 13-Point Meta-Validation Gate

Binary pass/fail. All 13 must pass for CERTIFIED.

| # | Checkpoint | Verification Command/Method | Common Failure |
|---|-----------|---------------------------|----------------|
| 1 | One SKILL.md at skill root | `ls {path}/SKILL.md` | Nested deeper in plugin structure |
| 2 | Frontmatter has name + description | Parse YAML between `---` markers | Missing description or malformed YAML |
| 3 | Description: 3rd person, 3-5 triggers, pushy | Count quoted phrases in description | First person, 1-2 triggers, no broader context |
| 4 | Body uses imperative form | `grep -c 'you should\|you can\|you need' SKILL.md` → 0 | "You should read the file" instead of "Read the file" |
| 5 | SKILL.md under 500 lines | `wc -l SKILL.md` <= 500 | Monolithic 800-line SKILL.md without references/ |
| 6 | 1+ Good vs Bad example | Grep for "Good" and "Bad" near each other | Missing — most common single failure |
| 7 | Validation gate with 5+ criteria | Count `- [ ]` checkboxes | 3 vague checkboxes or missing entirely |
| 8 | Assumptions & Limits section, specific | Section exists + has >3 specific limits | Section header with "pending" or boilerplate |
| 9 | Edge Cases with 3+ scenarios | Count bold items in Edge Cases section | 1-2 edge cases or none |
| 10 | All referenced files exist | Grep paths → `ls` each | Broken reference to renamed/deleted file |
| 11 | Progressive disclosure mechanism | "Before" section or ref-loading instructions | References/ exists but SKILL.md never says when to load |
| 12 | No security-compromising content | Content review for exploit code, key exposure | `disable-model-invocation` missing on side-effect skill |
| 13 | Intent wouldn't surprise user | Semantic: does description match actual behavior? | Description says "analyze" but skill actually modifies files |

## Certification Formula

```
CERTIFIED:   All dimensions >= 7/10 AND average >= 8/10 AND 13/13 gate pass
CONDITIONAL: Average >= 8/10 BUT 1-2 dimensions at 6/10 OR 11-12/13 gate
BLOCKED:     Any dimension < 6/10 OR 3+ gate failures OR no SKILL.md
```

**Edge case in scoring:** A skill with one dimension at 6 and average at 8.5 is CONDITIONAL — the single weak dimension needs attention but doesn't block usage. A skill with average 7.9 but all dimensions >= 7 is also CONDITIONAL — close but the aggregate quality isn't there yet.

## MOAT Extension Checks (M1-M5)

Beyond the 10-criterion rubric and 13-point gate, MOAT certification adds 5 deterministic checks. These extend CERTIFIED — a skill must pass CERTIFIED before MOAT checks apply.

| # | Check | Detection | Pass | Fail Severity |
|---|-------|-----------|------|---------------|
| M1 | Evals exist with >= 5 tests | `ls evals/evals.json` + count entries | File exists, >= 5 entries | BLOCKER |
| M2 | False-positive + edge-case evals | Grep eval names/tags | >= 1 false-positive, >= 1 edge-case | WARNING |
| M3 | References substantive | `wc -l` each file in references/, grep pending/Todo | All >= 20 lines, zero templates | BLOCKER |
| M4 | Template A compliance | Grep for "## Usage" or "## When to Activate" + "## Validation Gate" | Both present, no "## The Physics"/"## The Protocol" | BLOCKER |
| M5 | Evidence tag coverage | Count [EXPLICIT]/[INFERRED]/[OPEN] vs factual sentences | >= 80% (Standard/Orchestrator), >= 50% (Utility) | WARNING |

### MOAT Formula

```
MOAT = CERTIFIED (all dims >= 7, avg >= 8, 13/13 gate, S1-S9 pass)
     + M1 pass + M2 pass + M3 pass + M4 pass + M5 pass
     + zero BLOCKER failures in M-checks
```

### Complexity Tier Determination

The required asset set depends on the skill's inherent complexity:

| Tier | Signal | Required for MOAT | Evidence Tag Threshold |
|------|--------|------------------|----------------------|
| Utility (< 150 lines, single concern) | Simple lookup, formatting, translation | SKILL.md + evals/ | >= 50% |
| Standard (150-400 lines, multi-step) | Analysis, design, workflow | SKILL.md + evals/ + references/ + prompts/ | >= 80% |
| Orchestrator (400+ lines, delegates) | Pipeline, multi-agent coordination | SKILL.md + evals/ + references/ + agents/ + prompts/ + examples/ | >= 80% |

---
**Author:** Javier Montano | **Last updated:** March 27, 2026
