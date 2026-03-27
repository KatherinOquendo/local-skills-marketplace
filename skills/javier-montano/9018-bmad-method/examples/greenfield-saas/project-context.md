---
project-name: "TaskFlow"
version: "0.1.0"
team-size: 2
created: "2025-03-10"
last-updated: "2025-03-18"
---

# TaskFlow — Project Context

<!-- This is the project constitution. It defines the shared understanding
     that all team members and agents reference throughout the lifecycle. -->

## Vision

TaskFlow is a lightweight, opinionated project management tool built for small teams that find existing solutions (Jira, Asana, Monday) overly complex and expensive. Our north star is a PM tool that a 5-person startup can adopt in under 10 minutes with zero configuration. Success means teams spend more time building and less time managing their tools.

## Problem Statement

Small teams (2-10 people) at early-stage startups waste 3-5 hours per week wrestling with enterprise-grade PM tools. They need task tracking, not portfolio management. They need a kanban board, not a Gantt chart. Current tools are either too heavy (Jira), too unstructured (Notion), or too expensive per-seat (Linear). TaskFlow fills the gap: structured enough to keep work organized, simple enough to not require a PM certification.

## Tech Stack

| Layer        | Technology           | Version   | Rationale                                          |
|-------------|----------------------|-----------|---------------------------------------------------|
| Frontend    | Next.js (App Router) | 14.x      | SSR + RSC for fast initial loads, React ecosystem  |
| Backend     | tRPC                 | 11.x      | End-to-end type safety, no API schema maintenance  |
| Database    | PostgreSQL           | 16        | Relational integrity for project/task hierarchies  |
| ORM         | Prisma               | 5.x       | Type-safe queries, easy migrations, good DX        |
| Auth        | Clerk                | 5.x       | Drop-in auth with social login, minimal config     |
| Hosting     | Vercel               | —         | Zero-config Next.js deployment, preview deploys    |
| CI/CD       | GitHub Actions       | —         | Native GitHub integration, free for public repos   |
| Monitoring  | Vercel Analytics     | —         | Built-in, no additional setup required             |

## Constraints

- **Budget**: $0 infrastructure cost during MVP (Vercel free tier, Supabase free tier for Postgres, Clerk free tier up to 10k MAU)
- **Timeline**: 3-month MVP deadline (March 10 - June 10, 2025). Must be demoable by May 15.
- **Regulatory**: No specific compliance requirements for MVP. GDPR-aware data handling (EU users possible).
- **Technical**: Must work on modern browsers (Chrome 90+, Firefox 90+, Safari 15+). No native mobile app for MVP.
- **Staffing**: 2-person team. One fullstack lead (Alex), one junior frontend developer (Jordan). No dedicated designer — use component library.

## Conventions

### Code Style

- Language standard: TypeScript strict mode (`"strict": true` in tsconfig)
- Linter config: ESLint with `@next/eslint-config-next` + `eslint-config-prettier`
- Formatter: Prettier (2-space indent, single quotes, trailing commas)

### Git Workflow

- Branching model: Trunk-based development with short-lived feature branches
- Commit convention: Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`)
- PR review policy: All PRs require 1 approval. Self-merge allowed for solo work after CI passes.

### Naming Conventions

- Files: kebab-case (`create-task-form.tsx`)
- Components: PascalCase (`CreateTaskForm`)
- Database entities: snake_case (`task_assignments`)
- API endpoints: tRPC routers use camelCase (`task.create`, `project.getById`)

### Testing Strategy

- Unit test minimum coverage: 70%
- Integration tests: tRPC router tests with test database
- E2E tests: Playwright for critical paths (login, create project, create task, move task)

## Team

| Role              | Name               | Contact                | Responsibility                         |
|------------------|--------------------|------------------------|---------------------------------------|
| Tech Lead / PO   | Alex Chen          | alex@taskflow.dev      | Architecture, backend, prioritization  |
| Frontend Dev     | Jordan Rivera      | jordan@taskflow.dev    | UI components, pages, E2E tests        |

## Links

| Resource          | URL                                      |
|------------------|------------------------------------------|
| Repository       | https://github.com/taskflow-app/taskflow |
| Project Board    | https://github.com/orgs/taskflow-app/projects/1 |
| Design Files     | https://www.figma.com/file/taskflow-mvp  |
| CI/CD Dashboard  | https://github.com/taskflow-app/taskflow/actions |
| Staging          | https://staging.taskflow.dev             |
| Production       | https://taskflow.dev                     |
| Documentation    | https://docs.taskflow.dev                |

---

<!-- NOTE: This project-context.md is intentionally detailed because it demonstrates
     the level of specificity expected. Notice how every tech stack choice has a
     rationale, every constraint is measurable, and conventions document actual
     practices, not aspirational ones. -->

## Lessons Learned

- **What went right**: Filling out the Tech Stack rationale column early prevented decision debates during architecture. When Winston (Architect) asked "why tRPC?", the answer was already documented.
- **What was tricky**: The Constraints section required iteration. The first draft had vague constraints like "limited budget" — it took a second pass to quantify them ($0 infrastructure, free tiers only).
- **Edge case handled**: With only 2 team members, the Team table is small. Rather than adding fictional roles, we documented who covers multiple responsibilities (Alex = Tech Lead + PO).

## Decisions Made

- **2-person team strategy**: Chose to have Alex cover both Tech Lead and Product Owner roles rather than hiring. Trade-off: single point of failure for requirements AND architecture, but faster decision-making for an MVP.
- **Free-tier-only infrastructure**: Accepted Vercel/Supabase/Clerk free tiers as hard constraints. Trade-off: potential scaling limitations at ~1K users, but zero cost during validation phase.

<!-- Keep this file up to date. It is the single source of truth for project context. -->
