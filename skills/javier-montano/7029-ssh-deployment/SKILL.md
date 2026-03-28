---
name: ssh-deployment
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Deploy to Hostinger via SSH+Git with key management, post-receive hooks, and
  rollback strategy. Alternative to FTP/SFTP for automated deployments. [EXPLICIT]
  Trigger: "SSH deploy", "Hostinger SSH", "git push deploy", "remote deployment", "SFTP"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# SSH Deployment

> "Push to deploy. If it breaks, push to revert."

## TL;DR

Deploys to Hostinger shared hosting via SSH+Git as an alternative to FTP/SFTP. Sets up SSH key authentication, bare Git repository on the server with post-receive hook for automatic deployment, and rollback via `git revert`. Covers key management, connection security, and `.ssh/config` for convenience. Falls back to SFTP if SSH is unavailable on the Hostinger plan. [EXPLICIT]

## Procedure

### Step 1: Discover
- Verify Hostinger plan supports SSH access (Business plan and above)
- Check if SSH is enabled in Hostinger control panel (Advanced → SSH Access)
- Identify server hostname, port (typically 65002 for Hostinger), and username
- Check if Git is available on the remote server (`ssh user@host "git --version"`)
- If SSH unavailable, fall back to `hostinger-deployment` skill (FTP/SFTP)

### Step 2: Analyze
- Choose deployment strategy:
  - **Option A**: SSH + Git bare repo with post-receive hook (recommended for automated deploys)
  - **Option B**: SSH + rsync (for non-git projects)
  - **Option C**: SFTP upload (fallback if SSH unavailable)
- Plan SSH key management: generate Ed25519 key pair, add to Hostinger
- Design post-receive hook: pull, build (if needed), symlink to `public_html`
- Plan rollback: `git revert HEAD` + push triggers automatic rollback

### Step 3: Execute
- Generate SSH key pair (if not exists):
  ```bash
  ssh-keygen -t ed25519 -C "deploy@jm-adk" -f ~/.ssh/hostinger_deploy
  ```
- Add public key to Hostinger (SSH Access panel or `~/.ssh/authorized_keys`)
- Configure `~/.ssh/config`:
  ```
  Host hostinger
    HostName {server-ip}
    Port 65002
    User {username}
    IdentityFile ~/.ssh/hostinger_deploy
    StrictHostKeyChecking accept-new
  ```
- Test connection: `ssh hostinger "echo ok"`
- Set up bare Git repo on server:
  ```bash
  ssh hostinger "git init --bare ~/deploy.git"
  ```
- Create post-receive hook:
  ```bash
  ssh hostinger "cat > ~/deploy.git/hooks/post-receive << 'HOOK'
  #!/bin/bash
  GIT_WORK_TREE=~/public_html git checkout -f main
  echo \"Deployed at \$(date)\"
  HOOK
  chmod +x ~/deploy.git/hooks/post-receive"
  ```
- Add remote and push:
  ```bash
  git remote add deploy hostinger:~/deploy.git
  git push deploy main
  ```
- For projects with build step, extend the hook:
  ```bash
  GIT_WORK_TREE=~/public_html git checkout -f main
  cd ~/public_html && npm ci && npm run build
  ```

### Step 4: Validate
- `ssh hostinger "echo ok"` succeeds without password prompt
- `git push deploy main` triggers automatic deployment
- Site loads correctly at `https://yourdomain.com` after push
- Rollback works: `git revert HEAD && git push deploy main`
- SSH key has no passphrase (for CI automation) OR passphrase is managed by ssh-agent
- `.ssh/config` file permissions are correct (600)

## Quality Criteria

- [ ] SSH connection works without password (key-based auth)
- [ ] Post-receive hook deploys automatically on push
- [ ] Site loads correctly after deployment
- [ ] Rollback via `git revert` + push works
- [ ] SSH key permissions are secure (600 for private key)
- [ ] `.ssh/config` configured for convenience
- [ ] Falls back to SFTP if SSH unavailable
- [ ] No credentials stored in repository
- [ ] Evidence tags applied to all claims

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Password-based SSH login | Insecure, can't automate | Use Ed25519 key pair |
| Storing SSH key in repo | Credential exposure | Use `~/.ssh/` with proper permissions |
| No rollback plan | Broken deploys stay broken | Always test `git revert` + push |
| Ignoring port number | Hostinger uses non-standard SSH port | Check panel for correct port (often 65002) |
| Skip connection test | Discover errors at deploy time | Always `ssh host "echo ok"` first |

## Related Skills

- `hostinger-deployment` — FTP/SFTP deployment (fallback)
- `firebase-deployment` — Firebase Hosting deployment (alternative target)
- `github-actions-ci` — Automate SSH deployment in CI pipeline
- `deployment-checklist` — Pre-deploy quality gates

## Usage

Example invocations:

- "/ssh-deployment" — Run the full ssh deployment workflow
- "ssh deployment on this project" — Apply to current context


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
