# Bootstrap Governed Project

Cross-skill cascade workflow for establishing complete governance structure (naming, rules, workflows, verification) for a new domain or project.

## Frontmatter

description: Create a complete governed project with naming conventions, rules, workflows, and verified ecosystem health

## Steps

1. **Receive domain/project specification from user**
   - Capture: project name, domain (Python/JavaScript/DevOps/etc.), scope (files, teams, deliverables)
   - Capture: initial governance priorities (what matters most: security, quality, performance, style)
   - Capture: existing artifacts or files to incorporate (old code, legacy rules, etc.)
   - Document: project specification for reference
   - If FAIL → Ask user to clarify project scope before proceeding

2. **Run naming-and-slugging to establish naming conventions**
   - Execute naming-and-slugging/workflows/audit-and-fix workflow on project directory
   - Establish standard patterns: skill names, workflow names, rule names, document names
   - Output: naming convention document summarizing project patterns
   - Example: "All workflows use action verbs (audit-and-fix, create-and-validate); all rules use R- prefix"
   - If FAIL → Review naming violations with user; apply fixes before proceeding

3. **Run rule-forge to create 3-5 governance rules**
   - Determine key rules for domain: 2-3 high-priority (enforce critical patterns), 1-2 supporting
   - Execute rule-forge/workflows/create-and-validate for each rule
   - Example rules: no console.log in production, SQL queries must use parameterized statements, config must be versioned
   - Collect validated rules into rules/ directory
   - Verify: each rule scores 8/10+ on self-evaluation.md
   - If FAIL → Ask user which rules are highest priority; create those first

4. **Run workflow-forge to create automation workflows**
   - Design 2-4 automation workflows that reference and enforce the rules
   - Example workflows: validate-pull-request (checks all rules), deploy-production (enforces security rules)
   - Execute workflow-forge/workflows/optimize-workflow for each workflow
   - Link workflows to rules: each workflow step should reference applicable rule by name
   - Collect validated workflows into workflows/ directory
   - Verify: each workflow scores 8/10+ on self-evaluation.md
   - If FAIL → Ask which workflows are most critical; prioritize and iterate

5. **Run ecosystem-forge to assemble all artifacts**
   - Create project SKILL.md that references all rules, workflows, reference docs
   - Organize directory structure: /rules, /workflows, /reference, /tools, /archive
   - Populate SKILL.md frontmatter with complete inventory of artifacts
   - Create README.md explaining governance model and how to use rules/workflows
   - If FAIL → Ask user to review directory structure; adjust if needed

6. **Run naming-and-slugging audit on everything**
   - Execute naming-and-slugging/workflows/audit-and-fix on entire project directory
   - Verify: 0 naming violations (all files kebab-case, no versions/status markers)
   - Update any newly discovered violations
   - Generate final naming compliance report
   - Expected: "All 27 artifacts compliant with naming convention"
   - If FAIL → Show remaining violations; iterate with user

7. **Run ecosystem-checker to verify integrity** // turbo
   - Execute: `python ecosystem-checker.py /path/to/project --report final-health.json`
   - Verify: 0 broken references, 0 orphans, 0 conflicts, 0 naming violations
   - Generate ecosystem health report: "✓ 47 artifacts | ✓ 0 issues | ✓ All cross-refs valid"
   - Document: project is now governed and ready for enforcement
   - If FAIL → Report issues found; review with user; apply repairs

8. **Deliver complete governed project**
   - Package: project SKILL.md, all rules, all workflows, reference docs, README, health report
   - Output: project summary (domain, 5 rules, 4 workflows, 47 total artifacts)
   - Provide: guide for team on how to use rules and workflows
   - Archive: baseline governance artifacts for version control
   - Expected: team can now use this project as template for similar domains
   - If FAIL → Ask user what's missing or needs adjustment

9. **Verification: ecosystem-checker passes, registry-linter passes**
   - Confirm: ecosystem-checker.py reports 0 issues
   - Confirm: all cross-references valid (no broken paths)
   - Confirm: all naming violations resolved
   - Confirm: no orphan files
   - Confirm: no rule/workflow conflicts
   - Expected: all checks pass
   - If FAIL → Flag remaining issues; provide repair guidance

10. **Optional: Create templates and documentation for future projects**
    - Document the governance approach for this domain
    - Create templates: template SKILL.md, template rule structure, template workflow structure
    - Save to /templates directory for reuse on similar projects
    - Provide: decision tree for when to create new rules vs. when to reuse existing
    - Output: project can now serve as reference for governance best practices
    - If FAIL → Ask user which templates would be most useful

## Verification Checklist

- [ ] Project directory contains: SKILL.md, /rules, /workflows, /reference, README.md
- [ ] All 3-5 rules created and scored 8/10+
- [ ] All 2-4 workflows created and scored 8/10+
- [ ] All artifacts have kebab-case names with no version/status markers
- [ ] ecosystem-checker.py reports 0 issues
- [ ] All cross-references valid (no broken paths)
- [ ] No orphan files or conflicting rules/workflows
- [ ] Team documentation complete and artifacts ready for use
