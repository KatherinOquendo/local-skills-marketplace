# Best Practices & Immutable Laws

## 1. Structural Markdown Linting (Phase G Standards)

Every markdown file you generate for the new skill MUST pass strict structural machine linting. If you generate a `.md` file, obey these rules unconditionally:

- **MD022/MD032 (The Blank Line Purge)**: ALWAYS surround lists, headings, and code fences with a single blank line. Never attach a bullet point directly under a paragraph or heading without a blank line separating them.
- **MD031 (Code Block Blank Lines)**: Fenced code blocks (` ``` `) must be surrounded by blank lines on the outside.
- **MD060 (Table Alignment)**: Tables must be visually and literally character-aligned. 
  - Do NOT use unicode ellipsis (`…`); use three ascii periods (`...`).
  - Avoid escaped quotes (`\"`) inside markdown tables if possible, as they break literal character counts for pipes `|`.

## 2. Progressive Disclosure Doctrine

The main orchestrator (`SKILL.md`) must ONLY contain:
- YAML frontmatter.
- The persona definition.
- The strict **Instruction Loading Sequence** (instructing the agent to read the `reference/` files).
- The high-level execution steps.

**CRITICAL**: Do NOT put the heavy business logic, laws, or templates inside `SKILL.md`. Defer them to the `reference/` files.

## 3. High-Density Directives

- Avoid generic platitudes like "Be helpful and concise." 
- Use highly specific, actionable constraints (e.g., "Enforce functional purity and use immutable types").
- Cut conversational fluff out of your templates.
