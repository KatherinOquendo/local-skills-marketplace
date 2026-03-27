# Ecosystem Integration Checklist

Run through this checklist after creating all artifacts in an ecosystem.

## Naming (4 items)

- [ ] All skill directories use kebab-case
- [ ] All rule files follow `R-kebab-case.md` pattern
- [ ] All workflow files follow `verb-noun.md` pattern
- [ ] No version markers, status prefixes, or underscores in any name

## Cross-References (4 items)

- [ ] Every skill referenced in a workflow actually exists
- [ ] Every rule referenced in a skill's documentation actually exists
- [ ] Workflow prerequisites list real, existing skills and tools
- [ ] No circular dependencies between artifacts (A needs B needs A)

## Rule Integrity (3 items)

- [ ] No two rules impose contradictory constraints on the same files
- [ ] Rule globs don't overlap ambiguously (if they do, priority is documented)
- [ ] Every rule has been validated with `rule_validator.py`

## Workflow Integrity (3 items)

- [ ] Every workflow has 10 or fewer steps
- [ ] Every workflow ends with a verification step
- [ ] Turbo annotations are only on safe, reversible actions

## Completeness (3 items)

- [ ] The ecosystem has at least one entry-point workflow (how do users start?)
- [ ] Critical failure modes are covered by rules
- [ ] No orphan artifacts (everything is referenced from somewhere)

## Scoring

| Score | Verdict |
|---|---|
| 17/17 | Ecosystem is production-ready |
| 14-16 | Minor gaps — address before shipping |
| 10-13 | Structural issues — likely missing cross-references or rules |
| Below 10 | Major rework needed — ecosystem isn't cohesive yet |
