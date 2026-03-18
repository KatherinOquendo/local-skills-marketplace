# Ecosystem Repair Playbook

Solutions for common ecosystem issues discovered by ecosystem-checker.py. Use this playbook when running verify-and-repair workflow.

## Broken References: SKILL.md Points to Missing File

**Symptom**: ecosystem-checker reports "Reference in SKILL.md:workflows points to missing workflow file"

**Root Cause**:
- Workflow file was renamed or deleted without updating SKILL.md
- Typo in workflow filename or path in frontmatter

**Fix Steps**:
1. Check if file exists: `ls -la /path/to/workflows/ | grep <referenced-name>`
2. If file exists with different name: update SKILL.md to correct name
3. If file doesn't exist: either create the missing workflow or remove the reference
4. Update SKILL.md frontmatter: `workflows: [workflow-one, workflow-two]` (no file extensions)
5. Verify: `grep -r "<old-name>" /path/to/skill/`; result should be 0 matches

**Verification**: ecosystem-checker.py reports 0 broken refs to this file

---

## Broken References: Workflow Step References Non-Existent Tool/File

**Symptom**: ecosystem-checker reports "Step 3 in workflow-X.md references undefined tool Y"

**Root Cause**:
- Tool name was renamed/removed from tools/ directory
- Typo in tool reference within workflow step
- Tool was deleted but workflow not updated

**Fix Steps**:
1. List available tools: `ls /path/to/tools/` or check tools manifest
2. Find the correct tool name; update workflow step to match
3. If tool no longer exists: either create it or rewrite step to use alternative tool
4. Update workflow file: find and replace `old-tool-name` with `correct-tool-name`
5. Verify: `grep -r "old-tool-name" /path/to/workflows/`; result should be 0 matches

**Verification**: ecosystem-checker.py reports 0 broken refs in this workflow

---

## Orphan Files: Artifact Exists But Not Referenced Anywhere

**Symptom**: ecosystem-checker reports "File /path/to/some-rule.md is orphaned (not referenced in any SKILL.md or workflow)"

**Root Cause**:
- File was created but not registered in a SKILL.md frontmatter
- File was moved/renamed but reference not updated
- Artifact was deprecated but not removed

**Fix Steps (Choose One)**:

**Option A: Document the orphan (keep it)**
1. Open the artifact (rule, workflow, document)
2. Check if it serves a purpose (referenced in comments, used manually, part of toolkit)
3. If yes: add frontmatter entry or register in a parent SKILL.md
4. Update appropriate SKILL.md: add to `rules:`, `workflows:`, or `reference:` list
5. Verify: ecosystem-checker now references this file

**Option B: Archive the orphan (keep but remove from active ecosystem)**
1. Create `/archive/` directory if it doesn't exist
2. Move file: `mv /path/to/orphan.md /archive/orphan.md`
3. Update any SKILL.md that referenced it: change path to point to archive or remove
4. Verify: ecosystem-checker reports file as archived

**Option C: Delete the orphan (remove it)**
1. Inspect file contents to confirm it's truly unused
2. Check git history or comments to understand why it exists
3. If truly obsolete: `rm /path/to/orphan.md`
4. Verify: ecosystem-checker reports 0 orphans for this path

**Verification**: `ecosystem-checker.py` reports this file as registered, archived, or 0 orphans remain

---

## Naming Violations: File Not Compliant with Kebab-Case

**Symptom**: ecosystem-checker reports "File my_workflow.md violates naming convention (underscores not allowed)"

**Root Cause**:
- File was created with non-compliant name (underscores, MixedCase, spaces, etc.)
- Historical files not updated when naming convention was formalized

**Fix Steps**:
1. Run naming-and-slugging/audit-and-fix workflow on the file's directory
2. Slugger.py will generate proposed kebab-case name
3. Review proposal: `python slugger.py --clean my_workflow.md` → proposes `my-workflow.md`
4. Apply rename: `mv my_workflow.md my-workflow.md`
5. Update all references: find files that reference old name and update paths
6. Verify: `grep -r "my_workflow" /path/to/project/`; result should be 0 matches

**Verification**: ecosystem-checker.py reports 0 naming violations in this directory

---

## Rule Conflicts: Two Rules Enforce Contradictory Constraints

**Symptom**: ecosystem-checker reports "Rule R-no-console-log and R-log-everything contradict on file handling"

**Root Cause**:
- Two rules were created for overlapping domains without coordination
- Rule scope (glob) overlaps; both apply to same files with contradictory requirements
- Rules evolved separately; drift introduced conflict

**Fix Steps (Choose One)**:

**Option A: Merge the rules**
1. Compare both rules: understand what each enforces
2. Create new rule that unifies both constraints without contradiction
3. Name new rule: `R-unified-rule-name` (e.g., `R-conditional-logging`)
4. Delete old rules or mark them as deprecated
5. Update SKILL.md and workflow references: point to unified rule
6. Verify: no other rules contradict the new rule

**Option B: Narrow scope to eliminate overlap**
1. Adjust glob patterns so rules apply to different file types
2. Example: `R-no-console-log` applies to `**/*.js` (not test files); `R-log-everything` applies to `**/*.test.js`
3. Update both rule files: change `globs:` to exclude overlap
4. Verify: files matching both rules no longer exist
5. Verify: ecosystem-checker reports no conflicts

**Option C: Deprecate one rule**
1. Determine which rule is more important or current
2. Mark deprecated rule: add `deprecated: true` to frontmatter
3. Document why in a comment: "Superseded by R-X-Y-Z"
4. Keep file for reference; update SKILL.md to note deprecation
5. Remove deprecated rule from active enforcement
6. Verify: ecosystem-checker reports 0 conflicts

**Verification**: ecosystem-checker.py reports no conflicting rules

---

## Workflow Gaps: Missing Verification or Error Recovery

**Symptom**: ecosystem-checker reports "Step 5 in workflow-X.md can fail but has no recovery instructions"

**Root Cause**:
- Workflow step executes a command that might fail (network call, file operation)
- No `If FAIL →` recovery instructions documented
- Unbounded loops or steps without exit conditions

**Fix Steps**:
1. Open workflow file and locate the flagged step
2. Identify what can go wrong: network timeout, file not found, permission denied, etc.
3. Add recovery instruction: `If FAIL → [what to do next]`
4. Example: "If FAIL → report error and ask user for correct path"
5. For unbounded operations: add explicit exit condition or maximum iterations
6. Re-run workflow-linter.py to verify improvement
7. Verify: all steps with potential failures have recovery paths

**Verification**: workflow-linter.py reports 0 gaps; self-evaluation.md score ≥ 8/10

---

## Cross-Skill Mismatches: Skill References Non-Existent Rule/Workflow

**Symptom**: ecosystem-checker reports "prompt-forge SKILL.md references non-existent rule R-clear-requirements"

**Root Cause**:
- Rule was renamed or deleted but SKILL.md not updated
- Typo in rule filename in SKILL.md frontmatter
- Rule hasn't been created yet; reference is aspirational

**Fix Steps**:
1. Check if rule exists: `ls /path/to/rules/ | grep -i "clear-requirements"`
2. If rule exists with different name: update SKILL.md to correct name
3. If rule doesn't exist: either create it or remove the reference from SKILL.md
4. Update SKILL.md frontmatter: verify all referenced rules, workflows, and documents exist
5. Test: run ecosystem-checker on updated SKILL.md
6. Verify: ecosystem-checker reports 0 mismatches for this skill

**Verification**: ecosystem-checker.py confirms all referenced artifacts exist

---

## Quick Reference: Issue Priority and Playbook Section

| Priority | Issue Type | Playbook Section |
|---|---|---|
| 1 | Naming Violations | Naming Violations: File Not Compliant |
| 2 | Broken References | Broken References (both sections) |
| 3 | Orphan Files | Orphan Files: Artifact Exists But Not Referenced |
| 4 | Cross-Skill Mismatches | Cross-Skill Mismatches |
| 5 | Rule Conflicts | Rule Conflicts: Contradictory Constraints |
| 6 | Workflow Gaps | Workflow Gaps: Missing Verification |

---

## How to Use This Playbook

1. Run ecosystem-checker.py to identify all issues
2. Sort issues by priority (use Quick Reference table above)
3. For each issue: locate the matching section in this playbook
4. Follow the Fix Steps; apply Verification checks
5. Document: which playbook sections were used, what changed, and outcomes
6. Re-run ecosystem-checker.py to confirm repairs
