# Audit and Fix Naming Violations

Workflow for identifying, analyzing, and correcting naming convention violations in a directory.

## Frontmatter

description: Audit a directory for naming violations and apply fixes with user approval

## Steps

1. **Receive target directory path**
   - User provides the directory to audit (e.g., `/path/to/project/skills`)
   - Verify the directory exists and contains artifacts (skills, workflows, rules, docs)
   - If FAIL → Report directory not found and ask for correct path

2. **Run registry-linter.py on the directory**
   - Execute: `python registry-linter.py /path/to/target --report violations.json`
   - Collect all violations (errors + warnings) into a list
   - Capture: filenames, specific violations (underscores, MixedCase, version markers, etc.)
   - If FAIL → Check that registry-linter.py exists; report missing tool

3. **Collect violations summary**
   - Parse violations.json into categories: structure, findability, consistency
   - Count total violations by type (underscores: 3, MixedCase: 2, too-long: 1, etc.)
   - Display summary to user: "Found 12 violations across 8 files"

4. **Generate fix suggestions for each violation**
   - For each violation, run: `python slugger.py --clean <filename>` or `--validate <filename>`
   - Slugger outputs proposed new name in kebab-case
   - Build before→after mapping (old_name.md → new_name.md)
   - If FAIL → Report slugger.py errors; ask user to check tool configuration

5. **Present proposed renames to user**
   - Create before/after table with columns: Current Name | Proposed Name | Reason
   - Example: `fix_bugs.md | fix-bugs | Underscores not allowed`
   - Ask user: "Apply these 12 renames? (yes/no)"
   - If FAIL or "no" → Stop and ask user which renames to apply or skip

6. **Apply approved renames** // turbo
   - For each approved rename: `mv /path/to/old_name.md /path/to/new_name.md`
   - Update references in SKILL.md frontmatter (if any)
   - Update internal links in .md files that reference renamed artifacts
   - Track: success count and any failures (permission denied, file exists)
   - If FAIL → Report which renames failed; stop and ask user to resolve

7. **Re-run linter to verify zero violations**
   - Execute: `python registry-linter.py /path/to/target --report violations-after.json`
   - Compare violations-after.json with original
   - Expected result: violations-after.json is empty or warnings only
   - If FAIL → Review remaining violations; user decides next steps

8. **Self-evaluate naming quality using rubric**
   - Run self-evaluation.md rubric on each renamed artifact
   - Score each: Structure, Findability, Consistency checks
   - Report: "12 artifacts audited | 11 score 10/10 | 1 scores 8/10"
   - If FAIL → Identify lower-scoring names; suggest additional fixes

9. **Verify cross-references updated**
   - Grep for old filenames in project: `grep -r "old_name" /path/to/target`
   - Check SKILL.md files, workflow steps, rule references
   - Expected: 0 matches (all references updated)
   - If FAIL → Report broken references; ask user to fix manually

10. **Deliver audit report and confirm completion**
    - Summary: "✓ Fixed 12 naming violations | ✓ 0 linter violations remain | ✓ All cross-refs valid"
    - Document: original violations, fixes applied, artifacts rescored
    - Verification: ecosystem-checker passes (if available)
    - User can now ship updated directory with confidence

## Verification Checklist

- [ ] Target directory exists and contains expected artifacts
- [ ] registry-linter.py found 0 violations (or only warnings)
- [ ] All approved renames were applied successfully
- [ ] No broken cross-references remain
- [ ] Self-evaluation scores: no artifact below 8/10
