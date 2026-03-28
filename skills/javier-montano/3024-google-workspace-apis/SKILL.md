---
name: google-workspace-apis
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Integrate Google Workspace APIs — Sheets, Docs, Drive, Calendar, and Gmail
  programmatic access for automation and data workflows. [EXPLICIT]
  Trigger: "google sheets API", "google docs API", "google drive", "workspace API"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Google Workspace APIs

> "Automate the boring parts so humans can do the interesting ones." — Unknown

## TL;DR

Guides integration with Google Workspace APIs — reading/writing Google Sheets, generating Google Docs, managing Drive files, creating Calendar events, and sending Gmail programmatically. Use when building automations, data pipelines, or integrations that interact with Google Workspace. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify which Workspace APIs are needed (Sheets, Docs, Drive, Calendar, Gmail)
- Check Google Cloud Console for existing API enablement and credentials
- Review authentication requirements (service account vs OAuth2 user consent)
- Determine data flow direction (read from, write to, or bidirectional)

### Step 2: Analyze
- Choose auth strategy: service account for server-to-server, OAuth2 for user data
- Plan API scope requirements (principle of least privilege)
- Design rate limiting and quota management (Sheets API: 300 requests/min)
- Evaluate batch request opportunities to reduce API calls

### Step 3: Execute
- Enable required APIs in Google Cloud Console
- Set up credentials (service account key or OAuth2 client ID)
- Use `googleapis` npm package or REST API directly
- Implement Sheets integration: read ranges, append rows, format cells
- Build Drive file management: upload, share, organize in folders
- Create Calendar event automation with attendees and reminders
- Add error handling for quota limits, auth expiration, and permission errors

### Step 4: Validate
- Test API calls with actual Workspace resources (use test account/folder)
- Verify service account has correct sharing permissions on target resources
- Confirm rate limiting handles burst scenarios gracefully
- Check that OAuth2 refresh tokens work for long-running automations

## Quality Criteria

- [ ] API scopes follow principle of least privilege
- [ ] Service account keys stored securely (not in source code)
- [ ] Rate limiting and retry logic implemented for API quota management
- [ ] Error responses handled with user-friendly messages
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Requesting broad OAuth scopes when narrow ones suffice
- Storing service account JSON keys in the repository
- Making individual API calls when batch requests are available

## Related Skills

- `cloud-functions` — Workspace API calls typically run in Cloud Functions
- `scheduled-functions` — automated Workspace workflows run on schedules

## Usage

Example invocations:

- "/google-workspace-apis" — Run the full google workspace apis workflow
- "google workspace apis on this project" — Apply to current context


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
