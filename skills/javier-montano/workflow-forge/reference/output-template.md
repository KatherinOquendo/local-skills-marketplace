# Workflow Output Template

Use this template when creating new automation workflows.

```markdown
---
description: [Action-oriented summary: what this workflow accomplishes]
---
# [workflow-name]

## Prerequisites
- [What must be true before running this workflow?]
- [Required tools, skills, or project configurations]

## Steps

### 1. Load context  // turbo
Read any required configuration or reference files.
- Read `[relevant config or reference file]`
- Confirm prerequisites are met

### 2. [Action verb] [target]  // turbo (if safe)
[Clear instruction with specific tool/command]
```bash
[exact command to run, if applicable]
```

### 3. [Action verb] [target]
[Clear instruction]
- Expected output: [what should happen]
- If this fails: [remediation step]

### [N]. Verify results
- [ ] [Specific check: file exists, test passes, output matches]
- [ ] [Specific check]
- If FAIL → [What to do: retry step X, check logs, escalate]

## Skills Used
- [skill-name]: [what it's used for in this workflow]
```

## Complete Example

```markdown
---
description: Deploys the staging environment with database migrations
---
# deploy-staging

## Prerequisites
- Git repository with clean working tree
- SSH access to staging server
- Database credentials in `.env.staging`

## Steps

### 1. Verify clean state  // turbo
```bash
git status --porcelain
```
If output is not empty, abort: "Commit or stash changes before deploying."

### 2. Run tests  // turbo
```bash
npm test
```
All tests must pass. If any fail, stop deployment.

### 3. Build production bundle  // turbo
```bash
npm run build
```
Expected output: `dist/` directory with compiled assets.

### 4. Run database migrations
```bash
npm run migrate:staging
```
This modifies the staging database. Review the migration list before confirming.
If FAIL → Check migration logs in `logs/migrate.log`, rollback with `npm run migrate:rollback`.

### 5. Deploy to staging server
```bash
rsync -avz dist/ staging:/var/www/app/
```
Transfers built assets to the staging server.
If FAIL → Check SSH connection and server disk space.

### 6. Verify deployment  // turbo
```bash
curl -s https://staging.example.com/health | jq .status
```
- [ ] Health endpoint returns "ok"
- [ ] No new errors in staging logs (check last 5 minutes)
- If FAIL → Rollback: `ssh staging 'cd /var/www/app && git checkout HEAD~1'`

## Skills Used
- None (standalone workflow)
```

## Template Rules

**Step naming**: Always start with a verb. "Create", "Run", "Verify", "Read", "Check" — not "The creation step" or "Database handling."

**Turbo annotation**: Add `// turbo` on the same line as the step header. Only for safe, reversible actions.

**Remediation**: Every step that can fail should say what to do on failure. At minimum, the verification step needs a remediation path.

**Prerequisites**: Be specific. "Node.js installed" is vague. "Node.js >= 18 with npm" is clear.
