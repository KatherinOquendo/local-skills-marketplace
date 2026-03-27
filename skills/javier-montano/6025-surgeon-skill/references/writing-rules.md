# Writing Rules for Skill Prose

Apply when rewriting or adding content to a skill. Each rule includes the reasoning — not as justification theater, but because understanding the WHY lets you handle edge cases the rule doesn't cover.

## Voice and Form

| Rule | Correct | Incorrect | Why |
|------|---------|-----------|-----|
| Imperative form | "Read the file" | "You should read the file" | Removes ambiguity (who?), shorter, consistent across sections |
| Third person in description | "This skill should be used when..." | "I analyze inputs when..." | Anthropic routing: the model reads descriptions in third person to decide which skill to invoke |
| Active voice | "Parse the input" | "The input should be parsed" | Clearer actor, shorter, easier to follow |
| Present tense | "Each pass produces..." | "Each pass will produce..." | Instructions describe behavior, not future predictions |

**When to break the rules:** Direct quotes from users ("the user says 'help me'") use the user's voice, not imperative. Example output blocks show what the skill produces, not instructions — they follow the output's natural voice.

## Emphasis and Conviction

| Rule | Correct | Incorrect | Why |
|------|---------|-----------|-----|
| Explain WHY | "Keep under 500 lines because progressive disclosure reduces cognitive load" | "SKILL.md MUST be under 500 lines" | Models respond better to reasoning than to commands — reasoning builds judgment |
| No ALL CAPS | "preserve intent when correcting" | "ALWAYS preserve intent" | LLMs don't weight ALL CAPS as emphasis. Humans interpret it as shouting. Neither benefits. |
| Reasoning over rules | "If a correction could alter meaning, skip it — wrong corrections erode trust" | "NEVER change meaning" | Rigid rules invite loophole-finding. Reasoning produces correct behavior in novel situations. |
| Specifics over generics | "Score 7+ on every dimension" | "Score well on quality" | Vague criteria produce vague compliance. Numeric thresholds are testable. |

**The CAPS test:** If you catch yourself writing MUST, ALWAYS, NEVER, or IMPORTANT in caps — pause. Rewrite the sentence to explain the consequence of violation. If you can't articulate a consequence, the rule may not be needed.

## Structure and Format

| Rule | When | Why | Anti-Pattern |
|------|------|-----|-------------|
| Tables over bullet lists | Data has 2+ dimensions | Faster to scan, enforces parallel structure | Bullet list of (term, definition, example) triples |
| Code blocks for templates | Output formats, schemas, CLI examples | Shows exact format, no ambiguity | Describing a JSON structure in prose |
| One concern per section | Always | Prevents bloat, enables progressive disclosure | A section covering process + edge cases + examples |
| Headings follow hierarchy | h2 → h3 → h4, never skip | Predictable navigation, valid document outline, accessible | h2 followed by h4 (skipping h3) |
| Consistent heading style | Either all sentence-case or all title-case | Mixed casing signals carelessness | "## The Process" followed by "## edge cases" |

## Content Principles

| Principle | Application | Detection |
|-----------|------------|-----------|
| Every sentence earns its place | Delete any sentence; if the reader loses nothing, it was filler | "If I remove this, does the skill produce worse output?" |
| Define before use | First occurrence of a term = definition. Later = usage. | Grep for key terms — first occurrence should include a definition |
| Examples are instructions | A concrete example teaches more than 3 paragraphs of prose | Sections with long explanations and no examples → add example, trim explanation |
| Edge cases before happy path | Edge cases reveal design decisions; happy path is obvious | If edge cases are an afterthought appendix, promote them |
| Trade-offs over absolutes | "Aggressive correction catches more but risks meaning changes" > "Be conservative" | Sentences with "always" or "never" without trade-off reasoning |
| Show, don't describe | Before→After comparisons communicate changes better than descriptions | "Changed the description" vs showing the actual before and after text |

## Anti-Patterns to Eliminate

| Pattern | Detection | Fix | Severity |
|---------|-----------|-----|----------|
| Keyword stuffing in description | Description reads like SEO text with 10+ unrelated terms | 3-5 specific trigger phrases the user would actually say | HIGH — causes false triggers |
| Unreferenced resources | File exists in references/ but SKILL.md never mentions it | Add reference pointer with WHEN and SKIP conditions | HIGH — Claude won't know the file exists |
| Second person | "You should...", "You can...", "You need to..." | Rewrite in imperative: "Parse...", "Read...", "Check..." | MEDIUM — inconsistent voice |
| Orphan sections | Section exists but nothing references or depends on it | Integrate into a related section, or remove if zero value | MEDIUM — wasted context |
| Template without content | "## Edge Cases\n\nTBD" or empty section | Write the content or remove the header entirely | HIGH — placeholder headers set false expectations |
| Broken examples | Code blocks or templates that don't match the actual output format | Test every example against the skill's real output schema | HIGH — misleading examples degrade output quality |
| Meta-commentary | "In this section we will explain how to..." | Delete the commentary, keep the explanation | LOW — filler but not harmful |

## Cross-File Consistency

For multi-file skills. Applies during Step 4 of the surgeon-skill process.

| Rule | How to Check | Fix |
|------|-------------|-----|
| **Same term = same word** | Grep 5 key terms across all files. Flag variants. | Standardize on SKILL.md's terminology in all references. |
| **SKILL.md is authority** | If SKILL.md and a reference contradict, SKILL.md wins. | Fix the reference to align with SKILL.md. |
| **References extend, not repeat** | Grep 10-word phrases from references in SKILL.md. | Delete the reference copy, keep the SKILL.md copy, add a cross-reference. |
| **Integration sections are lean** | Reference files should have 3-5 line pipeline pointers. | Replace full re-explanations with "See SKILL.md [section] for details." |
| **Formatting matches across files** | Table style, heading hierarchy, code block language. | Pick SKILL.md's style as the standard, apply to all references. |

**When NOT to enforce consistency:** If a reference file serves a different audience (e.g., a script's docstring vs SKILL.md's instructions), different voice is acceptable. Consistency matters for files the model reads together, not for human-only documentation.

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
