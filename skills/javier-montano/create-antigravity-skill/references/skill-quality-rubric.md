# Skill Quality Rubric — Validation Criteria

## Structural Validation (Pass/Fail)

| Check | Criterion | Severity |
|-------|-----------|----------|
| S-01 | SKILL.md exists as entry point | CRITICAL |
| S-02 | YAML frontmatter complete (name, description, model, context, allowed-tools) | CRITICAL |
| S-03 | `references/` directory exists (plural) | CRITICAL |
| S-04 | Minimum 3 reference files | HIGH |
| S-05 | Reference file names are domain-specific (not generic) | HIGH |
| S-06 | All 17 canonical sections present | HIGH |
| S-07 | `${CLAUDE_SKILL_DIR}/references/` syntax for loading | HIGH |
| S-08 | Parameter taxonomy follows standard (MODO, FORMATO, ALCANCE) | MEDIUM |
| S-09 | Executor note in Validation Gate | MEDIUM |
| S-10 | Fuente section with citations | LOW |

## Content Quality (1-10 Scale)

| Dimension | 1-3 (Poor) | 4-6 (Acceptable) | 7-9 (Good) | 10 (Excellent) |
|-----------|------------|-------------------|------------|----------------|
| **Clarity** | Ambiguous instructions | Mostly clear | Clear and actionable | Crystal-clear, no interpretation needed |
| **Precision** | Generic platitudes | Some specific guidance | Specific and measurable | Every instruction changes agent behavior |
| **Consistency** | Mixed terminology | Mostly consistent | Consistent within skill | Consistent with entire ecosystem |
| **Edge Cases** | None documented | 1-2 obvious cases | 3-5 with handling | Comprehensive with decision trees |
| **Modularity** | Monolithic SKILL.md | Some separation | Clear separation | Perfect progressive disclosure |
| **Density** | Filler-heavy | Some filler | Lean | Every line earns its place |
| **Readability** | Wall of text | Structured but dense | Well-organized | Scannable, navigable, hierarchical |
| **Completeness** | Missing critical sections | Most sections present | All sections present | All sections with domain depth |

## Markdown Linting (Strict)

- Blank line before and after ALL headings
- Blank line before and after ALL lists
- Blank line before and after ALL code fences
- Tables visually aligned (no unicode ellipsis, no escaped quotes in tables)
- No trailing whitespace

## Anti-Patterns to Detect

| Anti-Pattern | Description | Fix |
|-------------|-------------|-----|
| **Monolith SKILL.md** | All logic in one file | Split to references/ |
| **Generic ref names** | knowledge_graph.md, best_practices.md | Domain-specific names |
| **Platitude padding** | "Be helpful", "Write good code" | Specific constraints |
| **Missing redirects** | When NOT to Use without alternatives | Name the correct skill |
| **Orphan references** | Ref files not loaded in Inputs | Add Load references block |
| **Implicit decisions** | Architecture choices without justification | Add to Trade-off Matrix |
| **Untestable gates** | Validation items that can't be verified | Make measurable |
