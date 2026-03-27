# Gold Standard Skill Anatomy

What a 10/10 skill looks like. Based on the Anthropic skill-creator plugin and the creator-moat-skill quality framework. Use this as the comparison baseline for every x-ray-skill diagnostic.

## Directory Structure

```
skill-name/
├── SKILL.md              (required — under 500 lines)
├── references/            (deep supporting content loaded on demand)
├── scripts/               (deterministic automation — must be chmod +x)
├── agents/                (sub-roles that operate independently, not sequentially)
├── evals/
│   └── evals.json         (test prompts + expectations + assertions)
└── assets/                (templates, viewers, static files used in output)
```

Only SKILL.md is required. Every other directory serves a specific purpose — its absence is a gap only if the skill's complexity warrants it.

### When Each Directory Is Warranted

| Directory | Create When | Skip When | Decision Signal |
|-----------|------------|-----------|-----------------|
| references/ | SKILL.md exceeds 300 lines, or domain knowledge requires examples/protocols beyond the core instructions | Skill is a simple utility (< 150 lines total) | Content that a reader might need 20% of the time belongs in references/ |
| scripts/ | A task repeats identically across invocations (validation, packaging, benchmarking) | All operations require judgment (no deterministic subset) | If you catch yourself writing the same Bash snippet across test runs, extract it |
| agents/ | Sub-roles operate independently on different inputs (grader, comparator, analyzer) | Roles are sequential phases of one pipeline | Ask: can this role run in parallel with another? If yes, agent. If no, it's a section in SKILL.md |
| evals/ | Skill will be iteratively improved or distributed to others | Personal one-off skill with known behavior | Without evals, improvement is guesswork |
| assets/ | Output includes files generated from templates (HTML viewers, report scaffolds) | Output is pure text/markdown | Templates that change per invocation belong here |

## Frontmatter Contract

```yaml
---
name: "{kebab-case, max 64 chars, lowercase letters/numbers/hyphens only}"
description: >
  This skill should be used when the user asks to "{phrase 1}",
  "{phrase 2}", "{phrase 3}", or mentions {keyword}.
  {One sentence: what it does.}
  Use this skill whenever {broader trigger context},
  even if they don't explicitly ask for "{skill name}".
argument-hint: "<required-arg> [optional-arg] [--flag]"
allowed-tools:
  - {minimum set — principle of least privilege}
model: opus          # only when complex reasoning required; omit for default
context: fork        # only when isolated subagent needed; omit otherwise
user-invocable: false  # only for background knowledge skills
disable-model-invocation: true  # only for skills with side effects (deploy, commit)
---
```

### Frontmatter Validation Rules

| Field | Rule | Failure Mode | Severity |
|-------|------|-------------|----------|
| name | kebab-case, 1-64 chars, no uppercase, no spaces, no angle brackets | Claude cannot route to the skill | BLOCKER |
| description | Third person, 3-5 trigger phrases in quotes, pushy broader context, <= 1024 chars | Skill under-triggers or never triggers | BLOCKER |
| argument-hint | Documents expected input format; present when skill takes arguments | User doesn't know what to pass | WARNING |
| allowed-tools | Minimum set for the skill's operations | Over-permissioning = security risk; under-permissioning = runtime failure | WARNING |
| model | Justified by skill complexity (opus for multi-step reasoning, sonnet for standard) | Unnecessary opus costs context; insufficient model degrades output | INFO |
| context | `fork` only when the skill must run in an isolated subagent | Unnecessary fork wastes resources | INFO |

**Trade-off for description length:** Longer descriptions trigger more accurately but consume context on every skill-list scan. Target 150-300 chars for the core trigger, up to 1024 for the full description with broader context.

**Trade-off for allowed-tools:** Too broad (all tools) = security risk, the skill can do anything. Too narrow (Read only) = the skill breaks when it needs to Glob for files. Start with Read + Glob + Grep, add Write/Edit/Bash only if the skill creates or modifies files.

## Body Structure

Sections in recommended order. Not every skill needs every section — but every missing section should be a conscious decision, not an oversight.

| Section | Required? | Purpose | What Breaks Without It | Acceptance Criteria |
|---------|-----------|---------|----------------------|---------------------|
| Title + value proposition | Yes | 1-2 sentences: WHY this skill exists | No motivation; user doesn't understand when to use it | Answers "what does this do and why should I care?" in <= 2 sentences |
| When to Activate / Usage | Yes | Invocation examples + scaling guidance | Over/under-triggering; no usage patterns | 2+ examples with arguments; scaling table if complexity varies |
| Before {Action} | Recommended | Progressive disclosure: which refs to load when | Loads all refs (wastes context) or none (misses knowledge) | Each ref file has a loading condition and a skip condition |
| Core Process | Yes | The actual instructions | No instructions = no skill | Tables > bullets; code blocks for templates; one concern per subsection |
| Assumptions & Limits | Yes | Where the skill breaks | Silent failures on edge inputs | Each limit is specific (not "may have limitations") with a handling strategy |
| Edge Cases (3+) | Yes | Non-obvious scenarios | Breaks on real-world input | Each case has: scenario, detection, handling. Minimum 3. |
| Good vs Bad Example (1+) | Yes | Calibration for the model | Model doesn't know what "good" looks like for this skill | Side-by-side comparison with reasoning for the difference |
| Antipatterns | Recommended | What NOT to do | Repeats common mistakes | Each antipattern: problem, bad pattern, fix, why it matters |
| Validation Gate (5+) | Yes | Quality assurance before output | No self-check; garbage passes through | Each criterion is testable (not "ensure quality") with a verification method |
| Reference Files | When refs exist | Tells Claude refs exist and when to load | Claude doesn't know about files it wasn't told about | Table: file, content summary, load-when condition |

## Progressive Disclosure (3 Levels)

| Level | Content | Loaded When | Size Constraint |
|-------|---------|-------------|-----------------|
| 1. Metadata | name + description | Always — used for skill routing | ~100-300 chars for name, ~150-1024 chars for description |
| 2. Body | SKILL.md instructions | When skill triggers | Under 500 lines because progressive disclosure reduces cognitive load for the model |
| 3. Resources | references/, scripts/, agents/ | On demand via "Before {Action}" section | Unlimited, but each file should have a clear loading condition |

**Why 500 lines?** Beyond ~500 lines, the model's attention to specific instructions degrades. Content that's needed only 20% of the time should be in references/ — loaded by condition, not by default.

## Writing Style Rules

| Rule | Correct | Incorrect | Why It Matters |
|------|---------|-----------|----------------|
| Imperative form | "Read the file" | "You should read the file" | Removes ambiguity (who?), shorter, consistent across sections |
| Third person in description | "This skill should be used when..." | "I analyze inputs when..." | Anthropic routing standard — the model reads descriptions to decide which skill to invoke |
| Explain WHY | "Keep under 500 lines because progressive disclosure reduces cognitive load" | "SKILL.md MUST be under 500 lines" | Models respond better to reasoning than to commands — they build judgment, not just compliance |
| Tables for structured data | Gap types table | Bullet list of gap types | Tables enforce parallel structure and are faster to scan than prose |
| No CAPS emphasis | "preserve intent when correcting" | "ALWAYS preserve intent" | LLMs don't process ALL CAPS as emphasis; it reads as shouting to humans and as noise to models |
| Reference files explicitly | "Read references/X.md when Y condition" | (file exists but never mentioned) | Claude doesn't know a file exists unless SKILL.md mentions it with a loading condition |
| One concern per section | Each section covers one topic | A section that covers process + edge cases + examples | Bloated sections are harder to navigate and harder to update without side effects |

## Systemic Coherence Requirements

For multi-file skills. Single-file skills are automatically coherent.

| Check | What It Means | Detection Method | Severity if Violated |
|-------|--------------|-----------------|---------------------|
| Unified terminology | Same concept = same word everywhere. "root need" in SKILL.md = "root need" in references (not "root cause" in one and "underlying problem" in another) | Grep 5 key terms across all files | HIGH — inconsistency confuses the model |
| Data contracts | Each component's input/output is explicit in SKILL.md, not just narrative | Look for a table showing what each pass/step receives and produces | MEDIUM — implicit contracts drift over time |
| Evidence taxonomy | One system for tagging claims, used consistently | Check if references use the same tags as SKILL.md (explicit/inferred/open or equivalent) | MEDIUM — mixed systems make traceability impossible |
| Cross-reference integrity | Every file path in SKILL.md resolves to an actual file. Every file in the directory is mentioned in SKILL.md. | Grep paths → ls each; ls directory → grep each filename in SKILL.md | HIGH — orphan files waste space; broken refs break loading |
| Schema alignment | Output templates in SKILL.md match JSON schemas in workflows and match eval expectations | Compare field names across all three | HIGH — misalignment means evals test the wrong thing |

## Evals Structure

```json
{
  "skill_name": "skill-name",
  "description": "what the eval suite tests",
  "evals": [
    {
      "id": 1,
      "name": "descriptive-kebab-case-name",
      "prompt": "exact user input to test with",
      "expected_output": "what success looks like (1-2 sentences)",
      "files": [],
      "expectations": [
        "specific, verifiable assertion about the output",
        "another specific assertion — each tests one thing"
      ]
    }
  ]
}
```

### Eval Quality Requirements

| Requirement | Meaning | Anti-Pattern |
|------------|---------|-------------|
| Minimum 5 evals | Cover the skill's core capabilities + at least 1 edge case | 3 happy-path tests that all pass trivially |
| Each targets a distinct capability | No two evals test the same thing | 5 variations of the same input |
| 1+ false-positive test | Input that should NOT trigger deep behavior | All tests expect maximum output — no scaling test |
| Discriminating assertions | An assertion should fail if the skill degrades | "Output is not empty" — passes for any non-blank response |
| Named evals | `name` field describes what's being tested | `id: 1` without a name — unclear what failed |

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
