---
name: hostinger-deployment
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Deploy websites to Hostinger with cPanel, FTP, .htaccess configuration,
  DNS setup, SSL certificates, and PHP configuration.
  Trigger: "Hostinger", "cPanel", "FTP deploy", ".htaccess", "shared hosting"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Hostinger Deployment

> "Not everything needs Kubernetes — sometimes cPanel and FTP get the job done." — Unknown

## TL;DR

Guides website deployment to Hostinger shared hosting — cPanel file management, FTP/SFTP upload, .htaccess configuration for SPAs and redirects, DNS setup, SSL certificate provisioning, and PHP configuration. Use when deploying static sites, WordPress, or PHP applications to Hostinger.

## Procedure

### Step 1: Discover
- Log into Hostinger hPanel and identify the hosting plan and features
- Check domain registration and DNS configuration status
- Review PHP version and available extensions
- Identify deployment method: hPanel file manager, FTP/SFTP, or Git

### Step 2: Analyze
- Determine deployment strategy: manual upload vs automated (GitHub Actions + FTP)
- Plan .htaccess rules for SPA routing, HTTPS redirect, and caching
- Evaluate SSL setup: Hostinger free SSL or Let's Encrypt
- Design directory structure under `public_html`

### Step 3: Execute
- Build production assets locally (`npm run build`)
- Upload `dist/` contents to `public_html/` via SFTP or hPanel file manager
- Configure `.htaccess` for SPA routing: `RewriteRule . /index.html [L]`
- Set up HTTPS redirect in `.htaccess`: `RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]`
- Configure caching headers for static assets in `.htaccess`
- Enable SSL certificate in Hostinger dashboard
- Set up email accounts if needed (MX records)
- Configure automated deployment via GitHub Actions with FTP action

### Step 4: Validate
- Verify site loads correctly at the domain with HTTPS
- Test SPA routing — all routes return the app (not 404)
- Check SSL certificate is valid and auto-renewing
- Confirm cache headers are set correctly for static assets
- Test email delivery if MX records were configured

## Quality Criteria

- [ ] Site accessible via HTTPS with valid SSL certificate
- [ ] .htaccess configured for SPA routing and HTTPS redirect
- [ ] Static assets cached with appropriate Cache-Control headers
- [ ] Automated deployment pipeline set up (not manual FTP uploads)
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Uploading files manually via FTP every time (automate with CI/CD)
- Forgetting .htaccess SPA rewrite (causes 404 on direct URL access)
- Not enabling HTTPS (SEO penalty and security risk)

## Related Skills

- `domain-management` — DNS configuration for Hostinger-hosted sites
- `github-actions-ci` — automated deployment to Hostinger via FTP
