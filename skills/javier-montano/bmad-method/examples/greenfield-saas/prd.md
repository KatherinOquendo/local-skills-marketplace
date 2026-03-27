---
title: "TaskFlow — Product Requirements Document"
version: "0.1.0"
status: "Approved"
author: "John (PM Agent)"
date: "2025-03-14"
product-brief-ref: "product-brief.md"
stakeholders:
  - "Alex Chen (Tech Lead / PO)"
  - "Jordan Rivera (Frontend Dev)"
success-metrics:
  - "1,000 registered users in 6 months"
  - "40% week-2 retention"
  - "< 5 min time to first task"
---

# TaskFlow — Product Requirements Document

## 1. Executive Summary

TaskFlow is a lightweight project management tool designed for small startup teams (2-10 people) who need structured task tracking without the complexity of enterprise PM tools. The MVP delivers a kanban-based task management system with user authentication, project workspaces, task CRUD, drag-and-drop board, team assignments, real-time notifications, search, and a simple dashboard.

The product will be built as a Next.js web application with tRPC API layer, PostgreSQL database, and Clerk authentication. The 3-month MVP scope is tightly constrained to the core task management loop: create project, add tasks, assign work, track status.

## 2. Problem Statement

### Current State

Small teams adopt enterprise PM tools (Jira, Asana) or unstructured tools (Notion, spreadsheets) because no purpose-built option exists for their scale. Enterprise tools require 2-3 weeks of setup and ongoing administration. Unstructured tools lack the conventions needed for consistent sprint execution. Teams oscillate between tools, losing context and momentum.

### Desired State

A team of 5 signs up for TaskFlow, creates their first project, and has their kanban board populated with tasks in under 10 minutes. The tool enforces just enough structure (status columns, assignments, priorities) without requiring configuration. Teams stay organized without feeling managed.

## 3. User Personas

### Persona 1: Sam the Startup Founder

- **Role**: CEO/CTO of a 4-person startup, writes code and manages product
- **Goals**: Keep the team aligned on priorities, see what's blocked, ship faster
- **Pain Points**: Spent a week setting up Jira, team barely uses it. Notion boards go stale.
- **Tech Proficiency**: High — full-stack developer, comfortable with SaaS tools

### Persona 2: Priya the Team Lead

- **Role**: Engineering lead at a 8-person startup, manages 4 developers
- **Goals**: Assign work clearly, track sprint progress, unblock team quickly
- **Pain Points**: Needs visibility into who's working on what, without micromanaging
- **Tech Proficiency**: High — uses GitHub daily, prefers keyboard-driven tools

### Persona 3: Casey the Individual Contributor

- **Role**: Frontend developer, works on assigned tasks
- **Goals**: Know what to work on next, update task status quickly, minimize context switching
- **Pain Points**: Too many tools with overlapping functionality, notification fatigue
- **Tech Proficiency**: Medium-High — comfortable with dev tools, prefers simple UIs

## 4. Functional Requirements

| ID      | Requirement                           | Priority    | Persona       | Notes                     |
|---------|---------------------------------------|-------------|---------------|---------------------------|
| FR-001  | User authentication (email/password)  | Must Have   | All           | Clerk-based               |
| FR-002  | Social login (Google, GitHub)         | Must Have   | Sam, Priya    | Clerk social providers    |
| FR-003  | Project creation and management       | Must Have   | Sam, Priya    | Name, description, team   |
| FR-004  | Task CRUD operations                  | Must Have   | All           | Title, desc, status, etc. |
| FR-005  | Kanban board with drag-and-drop       | Must Have   | All           | Core interaction model    |
| FR-006  | Task assignment to team members       | Must Have   | Priya         | Single assignee per task  |
| FR-007  | In-app notification system            | Should Have | All           | Assignment, mentions      |
| FR-008  | Global search across tasks            | Should Have | Sam, Priya    | Full-text on title + desc |
| FR-009  | Project dashboard with metrics        | Should Have | Sam, Priya    | Task counts by status     |
| FR-010  | Team invitation via email             | Must Have   | Sam, Priya    | Clerk organization invite |

### FR-001: User Authentication (Email/Password)

Users must be able to create an account with email and password, and subsequently log in to access their projects. Authentication state persists across browser sessions.

**Acceptance Criteria:**
- [x] User can register with valid email and password (min 8 characters)
- [x] User can log in with correct credentials and is redirected to dashboard
- [x] Invalid credentials display a clear error message
- [x] Password reset flow via email is functional

### FR-002: Social Login (Google, GitHub)

Users must be able to authenticate using their Google or GitHub accounts for frictionless onboarding.

**Acceptance Criteria:**
- [ ] User can sign up / log in with Google OAuth
- [ ] User can sign up / log in with GitHub OAuth
- [ ] Social login creates a linked account if email matches an existing account

### FR-003: Project Creation and Management

Authenticated users can create project workspaces that contain tasks. Each project has a name, optional description, and a team of members.

**Acceptance Criteria:**
- [ ] User can create a new project with name (required) and description (optional)
- [ ] Project creator is automatically set as owner
- [ ] Owner can rename or archive a project
- [ ] Projects appear in the user's dashboard sidebar

### FR-004: Task CRUD Operations

Within a project, users can create, read, update, and delete tasks. Each task has: title, description, status, priority, and assignee.

**Acceptance Criteria:**
- [ ] User can create a task with title (required), description, priority, assignee
- [ ] User can edit any task field inline
- [ ] User can delete a task (soft delete with confirmation)
- [ ] Tasks display creation date and last-modified timestamp

### FR-005: Kanban Board with Drag-and-Drop

Each project displays a kanban board with configurable status columns. Users can drag tasks between columns to update status.

**Acceptance Criteria:**
- [ ] Board displays columns: To Do, In Progress, In Review, Done
- [ ] User can drag a task card between columns to change status
- [ ] Column task counts update in real-time
- [ ] Board state persists on page refresh

### FR-006: Task Assignment

Tasks can be assigned to any team member within the project. Assignment triggers a notification.

**Acceptance Criteria:**
- [ ] User can assign a task to any project member via dropdown
- [ ] User can reassign or unassign a task
- [ ] Assignee receives an in-app notification on assignment

### FR-007: In-App Notification System

Users receive real-time notifications for task assignments, status changes on their tasks, and @-mentions in task descriptions.

**Acceptance Criteria:**
- [ ] Notification bell icon shows unread count
- [ ] Clicking notification navigates to the relevant task
- [ ] User can mark notifications as read individually or all-at-once

### FR-008: Global Search

Users can search across all tasks in a project by title and description text.

**Acceptance Criteria:**
- [ ] Search input is accessible from the project header
- [ ] Results return matching tasks with highlighted keywords
- [ ] Search is debounced (300ms) for performance

### FR-009: Project Dashboard

Each project has a dashboard view showing high-level metrics: task counts by status, recent activity, and team workload.

**Acceptance Criteria:**
- [ ] Dashboard shows task distribution across statuses (bar chart or visual)
- [ ] Dashboard shows tasks assigned per team member
- [ ] Dashboard shows 5 most recently updated tasks

### FR-010: Team Invitation

Project owners can invite team members by email address. Invitees receive an email and join the project upon registration or login.

**Acceptance Criteria:**
- [ ] Owner can invite users by email from project settings
- [ ] Invited user receives email with join link
- [ ] Existing users are added immediately; new users join after signup

## 5. Non-Functional Requirements

| ID       | Category       | Requirement                                    | Target              |
|----------|---------------|-----------------------------------------------|---------------------|
| NFR-001  | Performance   | API response time (P95)                        | < 200ms             |
| NFR-002  | Performance   | Page load time (initial, 3G)                   | < 3 seconds         |
| NFR-003  | Availability  | Uptime SLA                                     | 99.9%               |
| NFR-004  | Accessibility | WCAG compliance level                          | AA                  |
| NFR-005  | Security      | Authentication tokens                          | Clerk JWT, httpOnly |

## 6. Success Metrics

| Metric                  | Current Baseline | Target       | Measurement Method          |
|------------------------|------------------|--------------|----------------------------|
| Registered users       | 0                | 1,000 (6mo)  | Clerk dashboard            |
| Week-2 retention       | N/A              | 40%          | Cohort analysis            |
| Time to first task     | N/A              | < 5 min      | Onboarding funnel tracking |
| Tasks created/user/wk  | N/A              | 12           | Database aggregate query   |

## 7. Dependencies

| Dependency              | Type          | Owner              | Status       | Risk Level  |
|------------------------|---------------|--------------------|-------------|-------------|
| Clerk Auth Service     | Third Party   | Clerk              | Available   | Low         |
| Vercel Hosting         | Third Party   | Vercel             | Available   | Low         |
| PostgreSQL (Supabase)  | Third Party   | Supabase           | Available   | Low         |
| Figma Design Mockups   | Internal      | Alex (ad-hoc)      | In Progress | Medium      |

## 8. Risks

| ID     | Risk                                | Probability | Impact | Mitigation                                  |
|--------|-------------------------------------|-------------|--------|---------------------------------------------|
| R-001  | Scope creep delays MVP              | High        | High   | Strict MoSCoW, weekly scope review          |
| R-002  | Drag-and-drop performance on mobile | Medium      | Medium | Use proven library (dnd-kit), test early     |
| R-003  | Clerk free tier rate limits          | Low         | High   | Cache auth state, monitor usage              |
| R-004  | 2-person team capacity bottleneck   | Medium      | High   | Prioritize ruthlessly, cut Could Haves early |

## 9. Out of Scope

- Mobile native apps (iOS, Android)
- Time tracking features
- Gantt charts, timeline, or calendar views
- Custom task fields or templates
- Third-party integrations (GitHub, Slack, etc.)
- Advanced role-based permissions (beyond owner/member)
- Billing, subscriptions, or payment processing
- Offline mode
- Data export / import

## 10. Appendices

### A. Glossary

| Term           | Definition                                                    |
|---------------|---------------------------------------------------------------|
| Task          | A unit of work with title, description, status, priority      |
| Project       | A workspace containing tasks and team members                 |
| Kanban board  | Visual board with columns representing task statuses          |
| Sprint        | A time-boxed development iteration (1-2 weeks)                |

### B. References

- Product Brief: `product-brief.md`
- Project Context: `project-context.md`
- BMAD Method: Phase 2 Planning output

### C. Change Log

| Date         | Version | Author          | Changes                    |
|-------------|---------|-----------------|----------------------------|
| 2025-03-14  | 0.1.0   | John (PM Agent) | Initial PRD                |

<!-- NOTE: This PRD demonstrates several key patterns:
     1. FR IDs are sequential (FR-001 through FR-010) with no gaps
     2. Every FR has both a summary row in the table AND a detailed section with ACs
     3. Three personas are defined with different tech proficiency levels
     4. The "Out of Scope" section is explicit and comprehensive
     5. Dependencies table includes risk levels, not just status -->

## Lessons Learned

- **What went right**: Using the MoSCoW framework forced prioritization early. FR-007 (notifications) and FR-009 (dashboard) were marked "Should Have" instead of "Must Have", which created natural scope for deferral if the timeline slipped.
- **What was tricky**: Writing acceptance criteria for FR-005 (drag-and-drop kanban). The first draft said "user can drag tasks" — the revised version specifies column names, count updates, and persistence. The lesson: interaction-heavy features need more detailed ACs.
- **Edge case handled**: Three personas with different needs were covered without overcomplicating the FR table. The Persona column links each FR to who benefits, preventing "build it for everyone" thinking.

## Decisions Made

- **Single assignee per task**: FR-006 limits tasks to one assignee (not multiple). Trade-off: simpler data model and UI, but some users may want shared ownership. Deferring multi-assignee to post-MVP.
- **Soft delete for tasks**: FR-004 specifies soft delete with confirmation rather than hard delete. Trade-off: data never truly lost (GDPR implications addressed in architecture), but database grows larger over time.
