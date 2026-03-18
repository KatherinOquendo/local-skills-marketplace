# Verify and Repair Ecosystem

Workflow for scanning a project ecosystem for issues (broken references, orphans, naming violations, conflicts) and applying fixes in priority order.

## Frontmatter

description: Scan ecosystem for issues and apply repairs in priority order with verification

## Steps

1. **Run ecosystem-checker.py on target directory**
   - Execute: `python ecosystem-checker.py /path/to/project --report issues.json`
   - Capture all issues: broken refs, orphan files, naming violations, rule conflicts, workflow gaps
   - Parse results into categories by severity and type
   - Report summary: "Found 8 issues: 3 broken refs, 2 orphans, 2 naming violations, 1 conflict"
   - If FAIL → Report tool not found or permission errors; ask user to check paths

2. **Collect and prioritize all issues**
   - Extract each issue: type, file path, description, impact
   - Sort by priority: naming violations (highest), broken refs, orphans, conflicts (lowest)
   - Create issue list: "1. naming violation in skill-one/SKILL.md, 2. broken ref to non-existent workflow, ..."
   - Show user prioritized list; ask confirmation to proceed
   - If FAIL → Ask user which issues to skip or deprioritize

3. **For each issue: look up fix in repair-playbook.md**
   - Open reference/repair-playbook.md
   - Locate section matching issue type (Broken References, Orphan Files, Naming Violations, etc.)
   - Extract fix steps, commands, and verification checks
   - Apply repair steps in sequence
   - If FAIL → Report missing playbook entry; ask user for manual guidance

4. **Fix broken references (priority 1)**
   - Identify files and lines with broken references (files not found, undefined rules/workflows)
   - For each broken ref: check if file exists but path is wrong; if so, update reference
   - If file doesn't exist: check repair-playbook.md for create or delete guidance
   - Execute: update SKILL.md frontmatter, workflow steps, rule references
   - Verify: grep for old path and confirm 0 matches
   - If FAIL → Report which refs couldn't be fixed; ask user to resolve

5. **Fix naming violations (priority 2)** // turbo
   - Identify files with naming violations (underscores, MixedCase, version markers, etc.)
   - Run naming-and-slugging/audit-and-fix workflow on each violated file
   - Apply renames: `mv old_name.md new_name.md`
   - Update all references to renamed files
   - Verify: grep for old names and confirm 0 matches
   - If FAIL → Report which renames failed; ask user to resolve permissions

6. **Fix orphan files (priority 3)**
   - Identify files that exist but are not referenced anywhere (ecosystem-checker reports these)
   - For each orphan: decide document, move to archive, or delete
   - If documenting: add to project registry or SKILL.md
   - If deleting: ask user confirmation and remove file
   - Verify: ecosystem-checker reports 0 orphans
   - If FAIL → Ask user about remaining orphans; user decides disposition

7. **Resolve rule and workflow conflicts (priority 4)**
   - Identify rules that contradict each other or workflows that have duplicate logic
   - For each conflict: apply repair-playbook guidance (merge, scope-narrow, or deprecate)
   - If merging: combine rule logic into single file, update globs/references
   - If deprecating: mark as deprecated in frontmatter, keep for reference
   - Verify: no rule or workflow referenced twice with different logic
   - If FAIL → Ask user to manually resolve complex conflicts

8. **Re-run ecosystem-checker to verify repairs**
   - Execute: `python ecosystem-checker.py /path/to/project --report issues-after.json`
   - Compare issues-after.json with original issues.json
   - Expected: issues-after.json is empty or contains only informational notes
   - Count successful repairs: "Resolved 7 of 8 issues | 1 remaining (user-deferred)"
   - If FAIL → Review unresolved issues; iterate with user

9. **Generate ecosystem health report**
   - Create summary: issue counts (before/after), repairs applied, verification results
   - Format: "✓ 7 issues resolved | ✓ 0 broken refs remain | ✓ 0 orphans | ✓ All naming compliant"
   - Include: files modified, renames applied, conflicts resolved
   - Archive: save original and final ecosystem-checker reports for audit trail
   - If FAIL → Ask user to review report for accuracy

10. **Verification: ecosystem integrity confirmed**
    - Confirm: ecosystem-checker.py returns 0 issues (or info-level only)
    - Confirm: all cross-references valid (no broken paths in SKILL.md, workflows, rules)
    - Confirm: no orphan files in project
    - Confirm: no naming violations
    - Confirm: no conflicting rules or workflows
    - Expected: all checks pass
    - If FAIL → Flag remaining issues; provide guidance for manual review

## Verification Checklist

- [ ] ecosystem-checker.py reports 0 issues
- [ ] All broken references repaired or documented
- [ ] All orphan files handled (documented, moved, or deleted)
- [ ] All naming violations fixed
- [ ] All rule/workflow conflicts resolved
- [ ] Grep confirms: no references to old filenames remain
- [ ] Health report generated and archived
