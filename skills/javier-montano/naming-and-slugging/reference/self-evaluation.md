# Naming & Slugging Self-Evaluation Rubric

Run through this checklist before shipping any named artifact (skill, workflow, rule, document, file). Every item should pass.

## Structure Check (4 items)

- [ ] **Kebab-case compliant**: Uses only lowercase letters, numbers, and hyphens (e.g., `audit-and-fix`, not `audit_and_fix`)
- [ ] **Descriptive name**: Name clearly indicates purpose/action without needing extra context
- [ ] **Appropriate length**: Name is 2-4 words (hyphenated), not 1 word (too vague) or 6+ words (too long)
- [ ] **No version/status markers**: Does not include version numbers (v1, v2) or status labels (beta, draft, wip)

## Findability Check (3 items)

- [ ] **Searchable**: Name contains no cryptic abbreviations; would be found with keyword search
- [ ] **Self-describing**: Reader knows the artifact type and purpose without opening it
- [ ] **Grep-friendly**: Name uses words that naturally appear in documentation and comments; easy to search

## Consistency Check (3 items)

- [ ] **Follows entity pattern**: Skill names match conventions (workflows are action phrases: audit-and-fix, create-and-validate)
- [ ] **Consistent with peers**: Follows same naming style as similar artifacts in the ecosystem
- [ ] **No undocumented exceptions**: If any deviation from the pattern, it is justified in context (root SKILL.md or reference doc)

## Red Flags (automatic fail)

If any of these are true, the name needs revision:

| Red Flag | Example | Action |
|---|---|---|
| Underscores instead of hyphens | `audit_and_fix` | Replace with hyphens |
| UPPERCASE or MixedCase | `AuditAndFix`, `AUDIT` | Convert to lowercase kebab-case |
| Version markers | `audit-v2`, `fix-beta` | Remove version/status suffix |
| Too cryptic | `a-f`, `audit-fix-opt` | Use full words |
| Too long | `comprehensive-audit-and-fix-workflow-master` | Limit to 4 words max |

## Grading

Count passing items from the three checks above (10 total):

| Score | Verdict |
|---|---|
| 10/10 | Ship it |
| 8-9/10 | Minor fixes needed — address 1-2 gaps and re-evaluate |
| 6-7/10 | Significant rework — likely a length or consistency problem |
| Below 6 | Reconsider — this name is too vague or doesn't follow conventions |

## Quick Self-Check Example

**Artifact**: Workflow for auditing and fixing naming violations

Bad names:
- `audit_fix_names` (underscores)
- `AuditAndFix` (MixedCase)
- `fix-naming-violations-v2` (version marker)
- `a-n-f` (too cryptic)

Good name: `audit-and-fix` (4 checks: kebab-case ✓, descriptive ✓, 3 words ✓, no markers ✓)

Score: 10/10 → Ship it
