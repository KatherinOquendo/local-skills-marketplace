---
story-id: "STORY-002"
epic-ref: "EPIC-001"
title: "User signup with onboarding flow"
status: "In Progress"
points: 5
priority: "Critical"
assigned-to: "Jordan Rivera"
sprint: "1"
dependencies:
  - "STORY-001"
acceptance-criteria-count: 4
---

# STORY-002: User signup with onboarding flow

## User Story

**As a** new user,
**I want** to sign up and create my first project,
**So that** I can start managing my team's tasks immediately.

## Acceptance Criteria

### AC-1: Successful email/password signup

- **Given** a visitor on the TaskFlow signup page
- **When** they enter a valid email, a password meeting requirements (min 8 characters, 1 uppercase, 1 number), and click "Create Account"
- **Then** a new account is created, the user is authenticated, and they are redirected to the `/onboarding` page

### AC-2: Duplicate email rejection

- **Given** a visitor using an email that is already registered ("alex@taskflow.dev")
- **When** they attempt to create an account with that email
- **Then** they see an error message "An account with this email already exists" and are offered a link to the sign-in page

### AC-3: Weak password rejection

- **Given** a visitor on the signup page
- **When** they enter a password shorter than 8 characters or missing required complexity
- **Then** they see inline validation feedback indicating the specific requirement not met (length, uppercase, number) before form submission

### AC-4: Onboarding flow — first project creation

- **Given** a newly registered user on the `/onboarding` page
- **When** they enter a project name (e.g., "My First Project") and click "Get Started"
- **Then** a new project is created with them as OWNER, and they are redirected to the project's kanban board at `/project/{id}/board` with a welcome toast message

## Technical Notes

- Use Clerk's `<SignUp>` component with custom appearance matching TaskFlow brand colors
- Clerk handles password validation rules — configure in Clerk dashboard (min 8 chars, mixed case, numbers)
- The `/onboarding` page is a simple form: project name input + "Get Started" button
- On submit, call `project.create` tRPC procedure, then redirect to the new project's board
- Track the "time to first task" metric by recording a timestamp event at onboarding completion
- The onboarding page should check if user already has projects — if yes, redirect to dashboard (handles page refresh edge case)

### Affected Components

| Component                     | Change Type | Notes                                       |
|------------------------------|-------------|---------------------------------------------|
| `app/(auth)/sign-up/`         | New         | Sign-up page using Clerk component          |
| `app/(app)/onboarding/`       | New         | First-project creation page                 |
| `server/routers/project.ts`   | New         | project.create tRPC procedure               |
| `prisma/schema.prisma`        | Modify      | Ensure Project + ProjectMembership models   |
| `components/ui/toast.tsx`     | New         | Toast notification component (shadcn/ui)    |

### API Changes

New tRPC procedures:
- `project.create` (mutation): Input `{ name: string, description?: string }`. Creates project, creates OWNER membership for current user. Returns project with ID.
- `project.list` (query): Returns all projects where user has a membership. Used by dashboard and onboarding redirect check.

### Database Changes

Seeds required tables (already in schema):
- Inserts into `Project` table (name, description)
- Inserts into `ProjectMembership` table (projectId, userId, role: OWNER)

## Dependencies

| Dependency           | Type             | Status       | Blocking?   |
|---------------------|------------------|-------------|-------------|
| STORY-001 (Login)   | Story dependency | Done        | No          |
| Clerk signup config | External service | Done        | No          |
| Project Prisma model| Database schema  | Done        | No          |

## Definition of Done

- [ ] All acceptance criteria pass
- [ ] Code reviewed and approved
- [ ] Unit tests written and passing (>= 70% coverage)
- [ ] Integration tests passing
- [ ] No new linter warnings or errors
- [ ] Documentation updated (if applicable)
- [ ] Deployed to staging and verified
- [ ] Product owner sign-off

## Tasks

| Task                                          | Estimate | Assigned To | Status      |
|----------------------------------------------|----------|-------------|-------------|
| Create sign-up page with Clerk component      | 2h       | Jordan      | Done        |
| Build onboarding page UI                      | 3h       | Jordan      | In Progress |
| Implement project.create tRPC procedure       | 2h       | Alex        | Done        |
| Implement project.list tRPC procedure         | 1h       | Alex        | Done        |
| Add onboarding redirect logic                 | 1h       | Jordan      | To Do       |
| Add welcome toast notification                | 1h       | Jordan      | To Do       |
| Write unit + integration tests                | 3h       | Jordan      | To Do       |
| E2E test: full signup-to-board flow           | 2h       | Jordan      | To Do       |

---

### Notes

In progress during Sprint 1. The Clerk `<SignUp>` component is working. Currently building the onboarding page. Alex has completed the backend procedures. Jordan is handling the frontend flow and will write tests once the UI is connected.

<!-- NOTE: This story demonstrates an in-progress state:
     1. Definition of Done checkboxes are still unchecked ([ ])
     2. Tasks table shows mixed statuses (Done, In Progress, To Do)
     3. The story depends on STORY-001 and that dependency is marked Done
     4. AC-4 (onboarding flow) is the most complex AC — it creates both a
        project AND a membership in a single user action -->

## Lessons Learned

- **What went right**: Splitting backend (Alex) and frontend (Jordan) tasks allowed parallel work. The tRPC procedures were ready before the UI, enabling Jordan to connect immediately.
- **What was tricky**: AC-4's redirect logic ("if user already has projects, redirect to dashboard") is an edge case that only surfaces on page refresh. This was not in the initial ACs and was added during implementation.
- **Key insight**: A 5-point story is at the upper end of comfortable for a single sprint. The work is split across two developers, which adds coordination overhead. For future sprints, prefer 3-point stories.

## Decisions Made

- **Onboarding as a separate page**: Could have been a modal after signup. Chose a dedicated `/onboarding` page for cleaner URL routing and the ability to handle the "already has projects" redirect edge case.
- **shadcn/ui Sonner for toasts**: Selected the Sonner toast component from shadcn/ui for the welcome message. Trade-off: adds a dependency, but consistent with the design system choice and provides accessible notifications by default.
