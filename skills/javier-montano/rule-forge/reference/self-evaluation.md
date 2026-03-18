# Rule Self-Evaluation Rubric

After creating a rule, run through this checklist. Every item should pass before the rule ships.

## Structure Check (4 items)

- [ ] **Frontmatter complete**: Has `description` (one-line) and `globs` (file patterns)
- [ ] **Named correctly**: Follows `R-kebab-case` format (e.g., `R-no-console-log`)
- [ ] **Bad example present**: Shows a concrete code violation
- [ ] **Good example present**: Shows the corrected version of the same code

## Enforceability Check (3 items)

- [ ] **Binary**: Rule can be evaluated as Pass or Fail — no "sometimes" or "it depends"
- [ ] **Detectable**: A script, regex, or AST analysis could find violations automatically
- [ ] **Scope is precise**: Glob patterns target specific directories/file types, not `*` or `**/*`

## Reasoning Check (3 items)

- [ ] **"Why" is concrete**: Explains what bad outcome the rule prevents (not "best practice")
- [ ] **No jargon without context**: Technical terms are explained or obvious from examples
- [ ] **Examples are minimal diff**: Bad and Good examples differ only in the violation itself

## Red Flags (automatic fail)

If any of these are true, the rule needs rework:

| Red Flag | Action |
|---|---|
| Rule uses "try to", "consider", or "prefer" | Convert to guideline, not rule |
| Glob is `*` or `**/*` | Narrow the scope |
| Bad and Good examples are unrelated code | Rewrite to show minimal difference |
| No "Why" section | Add reasoning — arbitrary rules get ignored |
| Two ways to comply with the constraint | Make it more specific |

## Grading

Count passing items from the three checks above (10 total):

| Score | Verdict |
|---|---|
| 10/10 | Ship it |
| 8-9/10 | Minor fixes needed — address gaps and re-evaluate |
| 6-7/10 | Significant rework — likely a scope or enforceability problem |
| Below 6 | Reconsider — this might be a guideline, not a rule |
