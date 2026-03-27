# Create and Validate Rule

Workflow for drafting a new rule, validating structure, and ensuring it meets quality standards before shipping.

## Frontmatter

description: Create a rule from scratch, validate it against quality standards, and ship or iterate

## Steps

1. **Capture domain and scope for the rule**
   - Ask user: "What code or artifact pattern should this rule enforce?"
   - Ask: "What is the bad outcome the rule prevents?" (concrete impact, not "best practice")
   - Ask: "What file types/directories does this apply to?" (globs for scope)
   - Document: domain (e.g., Python/JavaScript), scope (e.g., `src/**/*.py`), and "why"
   - If FAIL → Ask user to clarify the problem the rule solves

2. **Draft rule using output-template.md format**
   - Open reference/output-template.md for structure
   - Create rule file: `R-<kebab-case-rule-name>.md`
   - Include: frontmatter (description, globs), Why section, Bad Example, Good Example
   - Ensure bad/good examples are minimal diff (same code, one violation fixed)
   - If FAIL → Report template errors; ask user to review examples

3. **Run rule-validator.py on the draft**
   - Execute: `python rule-validator.py R-<rule-name>.md --strict`
   - Capture: structural errors (missing fields, bad regex, empty examples)
   - Report: pass/fail on frontmatter, examples, glob patterns
   - If FAIL → Show validation errors; ask user to fix

4. **Check against self-evaluation.md rubric**
   - Run through 10-item checklist: Structure (4), Enforceability (3), Reasoning (3)
   - Score the draft rule (e.g., 8/10)
   - Identify failing items: missing "Why", vague examples, too-broad glob, etc.
   - If FAIL → Report score and list specific gaps

5. **If score < 8/10: apply fixes from best-practices.md**
   - Open reference/best-practices.md for guidance on common issues
   - Rewrite failing sections: tighten glob scope, clarify "Why", refine examples
   - Re-check against self-evaluation.md items
   - Document changes made (e.g., "Narrowed glob from `**/*` to `src/**/*.py`")
   - If FAIL → Ask user to manually adjust before retry

6. **Re-validate the updated rule**
   - Run rule-validator.py again: `python rule-validator.py R-<rule-name>.md --strict`
   - Verify: all structural checks pass, examples are valid
   - Run self-evaluation.md rubric again
   - Expected: score ≥ 8/10, no red flags
   - If FAIL → Review validation output; iterate with user

7. **Deliver validated rule file** // turbo
   - Copy finalized rule to destination: `cp R-<rule-name>.md /path/to/rules/`
   - Update ecosystem index (if rules registry exists)
   - Output: rule file path and final self-evaluation score
   - If FAIL → Report copy/index errors; verify permissions

8. **Verification: rule is binary, detectable, scoped**
   - Check: Rule describes violation as Pass/Fail, not "sometimes"
   - Check: Examples show how a linter/script could detect the violation
   - Check: Glob patterns are specific (not `*` or `**/*`; target actual directories)
   - Expected: All three checks pass
   - If FAIL → Rule needs rework; return to step 5

## Verification Checklist

- [ ] Rule file created with R- prefix and kebab-case name
- [ ] rule-validator.py passes with no structural errors
- [ ] Self-evaluation.md score ≥ 8/10
- [ ] No red flags (vague examples, weak "Why", overly broad scope)
- [ ] Examples use minimal diff (only the violation differs)
- [ ] Rule is binary (Pass/Fail), detectable (machine-checkable), and scoped
