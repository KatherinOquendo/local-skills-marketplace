---
name: github-actions-ci
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Build CI/CD pipelines with GitHub Actions — test, lint, build, deploy
  workflows with matrix builds, caching, and environment management. [EXPLICIT]
  Trigger: "GitHub Actions", "CI/CD", "CI pipeline", "deploy workflow"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# GitHub Actions CI/CD

> "If it's not automated, it's not reliable." — Unknown

## TL;DR

Guides GitHub Actions CI/CD pipeline creation — building workflows for linting, testing, building, and deploying with matrix strategies, dependency caching, environment secrets, and deployment protection rules. Use when setting up or improving continuous integration and deployment for a project. [EXPLICIT]

## Procedure

### Step 1: Discover
- Check existing `.github/workflows/` directory for current workflows
- Identify pipeline stages needed (lint, test, build, deploy)
- Review required Node.js versions and environment variables
- Determine deployment targets (Firebase, Hostinger, Vercel, Netlify)

### Step 2: Analyze
- Design workflow triggers: push to main, pull request, manual dispatch
- Plan job dependencies: lint → test → build → deploy (sequential)
- Evaluate matrix strategy for multi-version testing
- Design secret management for API keys and deployment credentials

### Step 3: Execute
- Create `.github/workflows/ci.yml` with lint, test, and build jobs
- Configure dependency caching with `actions/cache` for `node_modules`
- Set up matrix strategy for Node.js version testing
- Add deployment job with environment protection rules
- Store secrets in GitHub repository settings (never in workflow files)
- Configure status checks as required for PR merging
- Add concurrency groups to cancel outdated workflow runs
- Set up Slack/email notifications for deployment status

### Step 4: Validate
- Verify workflow triggers on PR and push as expected
- Confirm caching reduces subsequent build times
- Check that deployment only runs on main branch, not PRs
- Verify status checks block PR merge when tests fail

## Quality Criteria

- [ ] CI runs lint, test, and build on every PR
- [ ] Dependency caching configured to reduce build times
- [ ] Secrets stored in GitHub settings, never in workflow YAML
- [ ] Deployment requires manual approval for production environment
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Hardcoding secrets in workflow files (use GitHub Secrets)
- Not caching dependencies (doubles build time unnecessarily)
- Running deployments on every push without environment protection

## Related Skills

- `firebase-deployment` — Firebase deploy steps in GitHub Actions
- `linting-formatting` — lint step in CI pipeline

## Usage

Example invocations:

- "/github-actions-ci" — Run the full github actions ci workflow
- "github actions ci on this project" — Apply to current context


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
