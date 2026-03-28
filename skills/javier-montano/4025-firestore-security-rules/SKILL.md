---
name: firestore-security-rules
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Write Firestore security rules with auth-based access control, custom claims,
  data validation, rate limiting, and rule testing strategies. [EXPLICIT]
  Trigger: "firestore rules", "security rules", "firestore permissions", "custom claims"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Firestore Security Rules

> "The database is only as secure as its weakest rule — and 'allow read, write: if true' is pretty weak." — Unknown

## TL;DR

Guides Firestore security rule implementation — from basic auth checks to advanced patterns with custom claims, field-level validation, rate limiting, and comprehensive rule testing using the emulator. Use when securing Firestore data access beyond simple authenticated/unauthenticated checks. [EXPLICIT]

## Procedure

### Step 1: Discover
- Map all collections and their access requirements by user role
- Identify existing rules in `firestore.rules` and test coverage
- Check custom claims usage in Firebase Auth for role-based access
- Review client queries that rules must permit (rules + queries must align)

### Step 2: Analyze
- Design access control matrix: collection × role × operation (read/write/create/update/delete)
- Plan field-level validation rules (required fields, types, value ranges)
- Determine rate limiting needs (prevent spam creation, abuse)
- Evaluate helper function extraction for reusable rule logic

### Step 3: Execute
- Write rules with granular operations: `get`, `list`, `create`, `update`, `delete`
- Add auth checks: `request.auth != null`, `request.auth.uid == resource.data.userId`
- Implement custom claims for roles: `request.auth.token.role == 'admin'`
- Validate data on write: field existence, types, string lengths, enum values
- Add rate limiting: `request.time > resource.data.lastWrite + duration.value(1, 's')`
- Create helper functions: `isOwner()`, `isAdmin()`, `isValidPost()`
- Write rule unit tests using `@firebase/rules-unit-testing`

### Step 4: Validate
- Run rule tests against emulator covering all access patterns
- Test denied access paths (unauthorized users, wrong roles, invalid data)
- Verify rules don't block legitimate client queries
- Deploy rules to staging first and test with real client code

## Quality Criteria

- [ ] No collection accessible without explicit auth checks
- [ ] Write operations validate required fields and data types
- [ ] Custom claims used for role-based access (not client-set fields)
- [ ] Rule unit tests cover allow AND deny scenarios for each collection
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Using `allow read, write: if true` in production (completely open database)
- Checking roles via a user document field instead of custom claims (client can modify)
- Writing rules without tests (rules are code — they need tests)

## Related Skills

- `firebase-auth` — authentication provides the identity rules check against
- `firestore-modeling` — document structure must support the security model

## Usage

Example invocations:

- "/firestore-security-rules" — Run the full firestore security rules workflow
- "firestore security rules on this project" — Apply to current context


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
