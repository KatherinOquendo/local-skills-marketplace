---
epic-id: "EPIC-001"
title: "User Authentication & Authorization"
status: "In Progress"
priority: "Critical"
prd-refs:
  - "FR-001"
  - "FR-002"
  - "FR-010"
story-count: 3
estimated-points: 11
dependencies: []
---

# EPIC-001: User Authentication & Authorization

## Description

Implement the complete authentication and authorization system for TaskFlow using Clerk. This epic covers user registration (email/password and social login), session management, and the foundation for project-level authorization. It is the first epic because every other feature depends on having authenticated users.

This epic delivers the auth infrastructure that all subsequent features build on: the Clerk integration, the local user sync mechanism, the tRPC auth middleware, and the initial onboarding flow that creates a user's first project.

## Business Value

Authentication is a zero-or-one feature — without it, the product cannot function. By using Clerk, we avoid 2-3 weeks of custom auth development and get production-grade security from day one. The onboarding flow (sign up + create first project) directly impacts our "time to first task" success metric.

### Key Results

- Users can register and log in within 30 seconds
- Social login (Google, GitHub) reduces signup friction by 40% vs email-only
- Team invitation flow enables multi-user projects (core product value)

## Acceptance Criteria

- [x] Users can register with email/password
- [x] Users can log in with Google or GitHub
- [ ] Clerk user data syncs to local PostgreSQL user table via webhook
- [ ] tRPC middleware validates Clerk JWT on every authenticated request
- [ ] New users are guided through a first-project creation flow
- [ ] Project owners can invite team members by email

## Story List

| Story ID   | Title                                     | Points | Priority | Status      |
|-----------|-------------------------------------------|--------|----------|-------------|
| STORY-001 | User login with email/password            | 3      | Critical | Done        |
| STORY-002 | User signup with onboarding flow          | 5      | Critical | In Progress |
| STORY-003 | Team invitation and member management     | 3      | High     | To Do       |

### Story Sequencing

1. STORY-001 — Login flow first; establishes Clerk integration and tRPC auth middleware
2. STORY-002 — Signup builds on login infrastructure; adds onboarding and first project creation
3. STORY-003 — Invitation requires both auth and project models to be in place

## Dependencies

### Internal Dependencies

| Dependency               | Type             | Status       | Impact if Delayed                |
|-------------------------|------------------|-------------|----------------------------------|
| Prisma schema + migrations | Technical     | Done        | Blocks all database operations   |
| tRPC base setup          | Technical        | Done        | Blocks all API procedures        |

### External Dependencies

| Dependency               | Owner            | Expected By  | Risk Level                       |
|-------------------------|------------------|-------------|----------------------------------|
| Clerk account setup      | Alex             | 2025-03-18  | Low — straightforward SaaS setup |
| Supabase project setup   | Alex             | 2025-03-18  | Low — free tier, instant setup   |

## Notes

- Clerk's `@clerk/nextjs` package provides `<SignIn>` and `<SignUp>` components that can be customized with Tailwind
- User sync uses Clerk webhooks (user.created, user.updated events) to keep local DB in sync
- The `clerkId` field on the User model is the foreign key linking Clerk's user to our data

### Open Questions

- [x] Should we support magic link login? Decision: No, not for MVP. Email/password + social is sufficient.
- [ ] Do we need email verification before allowing project creation? Leaning yes for spam prevention.

---

### Change Log

| Date         | Author               | Changes                    |
|-------------|----------------------|----------------------------|
| 2025-03-16  | Bob (Scrum Master)   | Epic created               |
| 2025-03-20  | Bob (Scrum Master)   | STORY-001 marked Done      |

<!-- NOTE: This epic demonstrates the correct structure:
     1. prd-refs maps to specific FRs (FR-001, FR-002, FR-010)
     2. story-count (3) matches the actual number of stories in the table
     3. estimated-points (11) equals the sum of individual story points (3+5+3)
     4. Story sequencing explains WHY each story comes in that order
     5. Open questions have resolution status ([x] resolved, [ ] pending) -->

## Lessons Learned

- **What went right**: Sequencing STORY-001 (login) before STORY-002 (signup) was correct — the Clerk integration and tRPC auth middleware from login became the foundation for signup.
- **What was tricky**: STORY-003 (team invitation) depends on both auth AND project models. It was tempting to start it in parallel, but the dependency on project creation (from STORY-002's onboarding) made it a true sequential dependency.
- **Key insight**: The estimated-points (11) for a first sprint was conservative. For a 2-person team learning BMAD, this allowed room for the learning curve without overcommitting.

## Decisions Made

- **3 stories for auth epic**: Could have been 2 (login+signup combined) or 5 (separating social login, password reset, etc.). Three stories balanced granularity with overhead. Each story is independently deliverable and testable.
- **No magic link login**: Resolved in Open Questions. Email/password + social login covers the target personas without adding complexity.
