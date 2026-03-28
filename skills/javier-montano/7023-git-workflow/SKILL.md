---
name: git-workflow
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Git workflow fundamentals: branching strategy, commit conventions, PR workflow, conflict resolution, release tagging. Foundation for parallel-workflow. [EXPLICIT]
  Trigger: "git workflow", "branching", "commit convention", "PR process", "merge conflict", "release"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Git Workflow

> "Method over hacks. Evidence over assumption."

## TL;DR

Establishes Git workflow fundamentals: branching strategy (trunk-based or feature branches), conventional commit messages, PR templates and review process, conflict resolution patterns, and release tagging with semantic versioning. Foundation that parallel-workflow builds on. [EXPLICIT]

## Procedure

### Step 1: Discover
- Read existing code and identify current patterns
- Check for existing documentation or configuration
- Identify gaps and improvement opportunities

### Step 2: Analyze
- Evaluate options and select the best approach for the project context
- Consider Constitution principles (XIII Think First, XIV Simple First)
- Map to quality gates

### Step 3: Execute
- Implement the solution following established patterns
- Apply evidence tags to all claims
- Generate output using brand template if HTML

### Step 4: Validate
- Verify implementation works correctly
- Check against quality criteria
- Evidence tags applied to all claims

## Quality Criteria

- [ ] Implementation follows established patterns
- [ ] Evidence tags applied to all claims
- [ ] Tested and verified
- [ ] Constitution-compliant

## Related Skills

- `parallel-workflow` — Advanced parallel Git patterns
- `github-actions-ci` — CI/CD integration
- `deployment-checklist` — Pre-deploy Git checks

## Usage

Example invocations:

- "/git-workflow" — Run the full git workflow workflow
- "git workflow on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
