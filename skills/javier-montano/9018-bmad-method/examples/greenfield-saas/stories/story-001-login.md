---
story-id: "STORY-001"
epic-ref: "EPIC-001"
title: "User login with email/password"
status: "Done"
points: 3
priority: "Critical"
assigned-to: "Alex Chen"
sprint: "1"
dependencies: []
acceptance-criteria-count: 3
---

# STORY-001: User login with email/password

## User Story

**As a** team member,
**I want** to log in with my email and password,
**So that** I can access my projects and tasks securely.

## Acceptance Criteria

### AC-1: Successful login

- **Given** a registered user with email "alex@taskflow.dev" and a valid password
- **When** they enter their credentials on the login page and click "Sign In"
- **Then** they are authenticated and redirected to the `/dashboard` page with their projects visible

### AC-2: Invalid password

- **Given** a registered user with email "alex@taskflow.dev"
- **When** they enter an incorrect password and click "Sign In"
- **Then** they see an error message "Invalid email or password" and remain on the login page without revealing which field was incorrect

### AC-3: Unregistered email

- **Given** a visitor using an email that is not registered ("unknown@example.com")
- **When** they attempt to log in with any password
- **Then** they see the same generic error message "Invalid email or password" (no user enumeration) and are offered a link to the signup page

## Technical Notes

- Use Clerk's `<SignIn>` component with appearance customization to match TaskFlow branding
- Configure Clerk redirect URLs: `afterSignInUrl: "/dashboard"`, `afterSignUpUrl: "/onboarding"`
- tRPC auth middleware reads `auth()` from `@clerk/nextjs/server` to extract userId
- First login triggers a `user.created` webhook that creates the local User record via `auth.syncUser`

### Affected Components

| Component                | Change Type | Notes                                    |
|-------------------------|-------------|------------------------------------------|
| `app/(auth)/sign-in/`    | New         | Sign-in page using Clerk component       |
| `middleware.ts`           | New         | Clerk auth middleware for route protection|
| `server/trpc/context.ts` | Modify      | Add userId from Clerk to tRPC context    |
| `server/routers/auth.ts` | New         | syncUser procedure for Clerk webhook     |

### API Changes

New tRPC procedure:
- `auth.syncUser` (mutation): Receives Clerk webhook payload, upserts User record in PostgreSQL

### Database Changes

No schema changes — User model already defined in Prisma schema from project scaffolding.

## Dependencies

| Dependency           | Type             | Status       | Blocking?   |
|---------------------|------------------|-------------|-------------|
| Clerk account setup | External service | Done        | No          |
| Prisma User model   | Database schema  | Done        | No          |

## Definition of Done

- [x] All acceptance criteria pass
- [x] Code reviewed and approved
- [x] Unit tests written and passing (>= 70% coverage)
- [x] Integration tests passing (tRPC auth middleware test)
- [x] No new linter warnings or errors
- [x] Documentation updated (project-context.md links verified)
- [x] Deployed to staging and verified
- [x] Product owner sign-off

## Tasks

| Task                                    | Estimate | Assigned To  | Status |
|----------------------------------------|----------|-------------|--------|
| Set up Clerk project and environment vars | 1h     | Alex        | Done   |
| Create sign-in page with Clerk component  | 2h     | Alex        | Done   |
| Implement Next.js middleware for auth     | 1h      | Alex        | Done   |
| Add Clerk userId to tRPC context          | 1h      | Alex        | Done   |
| Create auth.syncUser tRPC procedure       | 2h      | Alex        | Done   |
| Write integration tests                   | 2h      | Alex        | Done   |

---

### Notes

Completed in Sprint 1. Clerk integration was straightforward. The `<SignIn>` component accepted Tailwind classes via the `appearance` prop without issues. Webhook setup required a Clerk dashboard configuration step that should be documented in the project README.

<!-- NOTE: This story demonstrates several BMAD best practices:
     1. Given/When/Then format makes each AC independently testable
     2. AC-2 and AC-3 cover error paths, not just the happy path
     3. AC-3 explicitly prevents user enumeration (security by design)
     4. Technical Notes reference specific Clerk APIs and config values
     5. All Definition of Done checkboxes are marked [x] for a completed story
     6. The Tasks table shows actual hours and all have "Done" status -->

## Lessons Learned

- **What went right**: Writing the acceptance criteria before implementation (AC-3's "same generic error message") caught a security issue early. Without this AC, the initial implementation would have shown "email not found" — a user enumeration vulnerability.
- **What was tricky**: The `auth.syncUser` webhook procedure required testing with Clerk's test mode. The integration test needed a mock webhook payload, which was not documented in Clerk's examples.
- **Key insight**: A 3-point story was right-sized for this work. The Clerk components did most of the heavy lifting, but the tRPC middleware and webhook integration added enough complexity to justify more than a 1-point estimate.

## Decisions Made

- **Clerk hosted components over custom UI**: Used Clerk's `<SignIn>` component with Tailwind styling instead of building a custom login form. Trade-off: less visual control, but saved 1-2 days and inherits Clerk's security hardening.
- **Webhook-based user sync**: Chose to sync users via Clerk webhooks (user.created event) rather than on-demand sync during first API call. Trade-off: slight delay in local user creation, but cleaner separation of concerns.
