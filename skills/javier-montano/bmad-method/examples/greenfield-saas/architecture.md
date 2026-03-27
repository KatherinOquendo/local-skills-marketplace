---
title: "TaskFlow — Architecture Document"
version: "0.1.0"
status: "Approved"
prd-ref: "prd.md"
architect: "Winston (Architect Agent)"
date: "2025-03-16"
tech-stack:
  frontend: "Next.js 14 (App Router)"
  backend: "tRPC 11"
  database: "PostgreSQL 16 (Supabase)"
  infrastructure: "Vercel"
adrs:
  - "ADR-001: tRPC over REST"
  - "ADR-002: Clerk over NextAuth"
  - "ADR-003: Prisma over Drizzle"
---

# TaskFlow — Architecture Document

## 1. System Overview

TaskFlow is a monolithic Next.js application deployed on Vercel that serves both the frontend UI and the tRPC API layer. The application uses PostgreSQL (hosted on Supabase) as its primary data store and Clerk for authentication. The architecture optimizes for developer velocity on a 2-person team — minimal operational overhead, maximum type safety, and zero infrastructure management.

### Key Design Goals

- **Developer velocity**: End-to-end TypeScript with tRPC eliminates API contract maintenance
- **Operational simplicity**: Serverless deployment on Vercel removes infrastructure management
- **Type safety**: Prisma + tRPC + TypeScript create a fully typed data path from DB to UI

### Architecture Style

Modular monolith deployed as a serverless Next.js application. All components live in a single repository and deploy as a single unit. Separation is achieved through tRPC router boundaries, not service boundaries.

## 2. Component Diagram (C4 Level 2)

```
┌──────────────────────────────────────────────────────────────────┐
│                         TaskFlow System                          │
│                                                                  │
│  ┌─────────────────┐    ┌──────────────────┐    ┌────────────┐  │
│  │   Web Client    │───▶│  Next.js App     │───▶│ PostgreSQL │  │
│  │   (Browser)     │    │  (App Router +   │    │ (Supabase) │  │
│  │   React RSC     │    │   tRPC Server)   │    │            │  │
│  └─────────────────┘    └──────────────────┘    └────────────┘  │
│         │                       │                                │
│         │                       ▼                                │
│         │               ┌──────────────────┐                     │
│         └──────────────▶│   Clerk Auth     │                     │
│          (JWT tokens)   │   (External)     │                     │
│                         └──────────────────┘                     │
└──────────────────────────────────────────────────────────────────┘
```

### Component Descriptions

| Component        | Technology              | Responsibility                               | Interfaces              |
|-----------------|-------------------------|----------------------------------------------|------------------------|
| Web Client      | React (RSC + Client)    | UI rendering, user interaction, local state   | HTTPS to Next.js app   |
| Next.js App     | Next.js 14, tRPC 11     | SSR, API routes, business logic, data access  | Prisma to DB, Clerk SDK|
| PostgreSQL      | PostgreSQL 16 (Supabase)| Persistent data storage, relational integrity | TCP/5432 via Prisma    |
| Clerk Auth      | Clerk SaaS              | User authentication, session management       | REST API, JWT tokens   |

## 3. Technology Stack

| Layer            | Technology              | Version    | Purpose                               |
|-----------------|-------------------------|------------|---------------------------------------|
| Frontend        | Next.js (App Router)    | 14.x       | Server-rendered React application     |
| UI Components   | shadcn/ui + Tailwind    | latest     | Accessible component library          |
| API Layer       | tRPC                    | 11.x       | Type-safe RPC between client/server   |
| ORM             | Prisma                  | 5.x        | Type-safe database access, migrations |
| Database        | PostgreSQL              | 16         | Primary data store                    |
| Auth            | Clerk                   | 5.x        | Authentication and user management    |
| Drag & Drop     | dnd-kit                 | 6.x        | Accessible kanban board interactions  |
| Hosting         | Vercel                  | —          | Serverless deployment                 |
| Monitoring      | Vercel Analytics        | —          | Web vitals and usage metrics          |

## 4. Data Model

### Entity Relationship Overview

| Entity            | Key Fields                                             | Relationships                           |
|------------------|--------------------------------------------------------|-----------------------------------------|
| User             | id (uuid), clerkId, email, name, avatarUrl             | Has many ProjectMemberships, TaskAssignments |
| Project          | id (uuid), name, description, ownerId, archived        | Has many Tasks, ProjectMemberships      |
| ProjectMembership| id, projectId, userId, role (OWNER/MEMBER)             | Belongs to Project, User                |
| Task             | id (uuid), title, description, status, priority, order | Belongs to Project, has optional Assignee|
| Notification     | id, userId, type, taskId, read, createdAt              | Belongs to User, references Task        |

### Prisma Schema (Core Models)

```prisma
model User {
  id          String   @id @default(uuid())
  clerkId     String   @unique
  email       String   @unique
  name        String
  avatarUrl   String?
  createdAt   DateTime @default(now())

  memberships  ProjectMembership[]
  assignments  Task[]              @relation("TaskAssignee")
  notifications Notification[]
}

model Project {
  id          String   @id @default(uuid())
  name        String
  description String?
  archived    Boolean  @default(false)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  tasks       Task[]
  memberships ProjectMembership[]
}

model ProjectMembership {
  id        String @id @default(uuid())
  role      Role   @default(MEMBER)

  project   Project @relation(fields: [projectId], references: [id])
  projectId String
  user      User    @relation(fields: [userId], references: [id])
  userId    String

  @@unique([projectId, userId])
}

model Task {
  id          String     @id @default(uuid())
  title       String
  description String?
  status      TaskStatus @default(TODO)
  priority    Priority   @default(MEDIUM)
  order       Int        @default(0)
  createdAt   DateTime   @default(now())
  updatedAt   DateTime   @updatedAt

  project     Project  @relation(fields: [projectId], references: [id])
  projectId   String
  assignee    User?    @relation("TaskAssignee", fields: [assigneeId], references: [id])
  assigneeId  String?

  notifications Notification[]
}

enum Role     { OWNER MEMBER }
enum TaskStatus { TODO IN_PROGRESS IN_REVIEW DONE }
enum Priority   { LOW MEDIUM HIGH URGENT }
```

### Data Flow

1. User authenticates via Clerk, receives JWT
2. Client sends tRPC request with Clerk session token
3. tRPC middleware validates token, attaches userId to context
4. tRPC procedure calls Prisma to query/mutate PostgreSQL
5. Response flows back through tRPC to client with full type inference

### Data Storage Strategy

- **Primary store**: PostgreSQL on Supabase (managed, auto-backups)
- **Caching layer**: None for MVP — Prisma query caching + Next.js route cache sufficient
- **Backup policy**: Supabase daily automatic backups, 7-day retention
- **Data retention**: Soft-delete for tasks and projects; hard-delete user data on account deletion (GDPR)

## 5. API Design

### API Style

tRPC (type-safe RPC) — no REST endpoints, no OpenAPI spec. Client and server share TypeScript types at build time. API is consumed exclusively by the TaskFlow web client.

### Key tRPC Routers

| Router      | Procedure            | Type     | Description                    | Auth Required |
|-------------|---------------------|----------|--------------------------------|---------------|
| auth        | auth.syncUser       | mutation | Sync Clerk user to local DB    | Yes           |
| project     | project.create      | mutation | Create a new project           | Yes           |
| project     | project.list        | query    | List user's projects           | Yes           |
| project     | project.getById     | query    | Get project with tasks         | Yes           |
| project     | project.update      | mutation | Update project name/desc       | Yes (owner)   |
| project     | project.invite      | mutation | Invite member by email         | Yes (owner)   |
| task        | task.create         | mutation | Create task in project         | Yes (member)  |
| task        | task.update         | mutation | Update task fields             | Yes (member)  |
| task        | task.delete         | mutation | Soft-delete a task             | Yes (member)  |
| task        | task.reorder        | mutation | Update task order/status       | Yes (member)  |
| task        | task.search         | query    | Full-text search within project| Yes (member)  |
| notification| notification.list   | query    | Get user's notifications       | Yes           |
| notification| notification.markRead| mutation| Mark notification(s) as read   | Yes           |
| dashboard   | dashboard.summary   | query    | Project metrics summary        | Yes (member)  |

### Error Handling

tRPC errors use standard error codes (`NOT_FOUND`, `UNAUTHORIZED`, `FORBIDDEN`, `BAD_REQUEST`). All procedures validate input with Zod schemas. Client displays user-friendly error messages from the `message` field.

## 6. Security Architecture

### Authentication

Clerk handles all authentication flows (email/password, Google OAuth, GitHub OAuth). The Next.js app receives a signed JWT from Clerk on each request. The tRPC middleware validates the JWT and resolves the local user record.

### Authorization

Project-level authorization: tRPC procedures check `ProjectMembership` before allowing access. Two roles:
- **OWNER**: Full access including project settings, invitations, and archive
- **MEMBER**: CRUD on tasks, view project, update own assignments

### Data Protection

- **Encryption at rest**: Supabase encrypts all data at rest (AES-256)
- **Encryption in transit**: All connections use TLS 1.3 (Vercel enforces HTTPS)
- **PII handling**: User email and name stored; minimal PII footprint. Delete on account removal.
- **Secrets management**: Environment variables in Vercel dashboard. `CLERK_SECRET_KEY` and `DATABASE_URL` never committed to Git.

### Security Controls

| Control               | Implementation                           | Status     |
|----------------------|------------------------------------------|------------|
| JWT validation       | Clerk middleware on every tRPC call       | Planned    |
| Input validation     | Zod schemas on all tRPC inputs           | Planned    |
| SQL injection prev.  | Prisma parameterized queries             | By default |
| CSRF protection      | SameSite cookies via Clerk               | By default |
| Rate limiting        | Vercel Edge middleware (100 req/min/IP)  | Planned    |

## 7. Deployment Architecture

### Environment Strategy

| Environment  | Purpose              | URL                          | Auto-deploy |
|-------------|----------------------|------------------------------|-------------|
| Development | Local dev            | http://localhost:3000         | N/A         |
| Preview     | PR preview deploys   | *.vercel.app (per-PR)        | Yes         |
| Staging     | Pre-prod validation  | https://staging.taskflow.dev | Yes (main)  |
| Production  | Live                 | https://taskflow.dev         | Manual      |

### CI/CD Pipeline

1. Developer pushes to feature branch
2. GitHub Actions runs: lint, type-check, unit tests, build
3. Vercel creates preview deployment automatically
4. PR merged to `main` triggers staging deploy
5. Manual promotion from staging to production via Vercel dashboard

## 8. Performance Strategy

### Performance Targets

| Metric               | Target              | Measurement               |
|---------------------|---------------------|--------------------------|
| Page load (P95)     | < 3 seconds (3G)    | Vercel Web Vitals        |
| API response (P95)  | < 200ms             | Vercel function logs     |
| LCP                 | < 2.5 seconds       | Vercel Web Vitals        |
| CLS                 | < 0.1               | Vercel Web Vitals        |

### Optimization Strategies

- React Server Components for initial page loads (zero client JS for static content)
- tRPC batching for multiple concurrent queries
- Prisma query optimization with `select` and `include` (no over-fetching)
- Next.js Image component for avatar optimization

### Scaling Strategy

Vercel serverless functions auto-scale horizontally. Supabase PostgreSQL supports connection pooling via PgBouncer. For MVP scale (< 1,000 users), no manual scaling is required.

## 9. ADR Index

### ADR-001: tRPC over REST

- **Context**: Need an API layer between Next.js frontend and PostgreSQL backend. Options: REST, GraphQL, tRPC.
- **Decision**: Use tRPC. It provides end-to-end type safety without code generation or schema files. Since the API is consumed only by our own frontend, we don't need REST's universality or GraphQL's flexibility.
- **Consequences**: No public API for third-party integrations (acceptable for MVP). Tighter coupling between client and server (acceptable for monorepo). Excellent DX with autocomplete and type inference.

### ADR-002: Clerk over NextAuth

- **Context**: Need authentication with email/password and social login. Options: NextAuth.js, Clerk, Auth0, custom.
- **Decision**: Use Clerk. It provides a complete auth UI, user management dashboard, and organization features out of the box. Saves 2-3 weeks of auth implementation.
- **Consequences**: Third-party dependency for critical path. Free tier is generous (10K MAU). Vendor lock-in mitigated by abstracting auth behind a thin service layer.

### ADR-003: Prisma over Drizzle

- **Context**: Need a TypeScript ORM for PostgreSQL. Options: Prisma, Drizzle, Kysely, raw SQL.
- **Decision**: Use Prisma. Best-in-class migration system, intuitive schema DSL, strong community. Drizzle is faster at runtime but Prisma's DX advantage matters more for a 2-person team.
- **Consequences**: Slightly higher cold-start times on serverless (Prisma client initialization). Mitigated by Vercel's function warming. Schema-first approach aligns with BMAD's documentation-first philosophy.

---

### Change Log

| Date         | Version | Author               | Changes                        |
|-------------|---------|----------------------|--------------------------------|
| 2025-03-16  | 0.1.0   | Winston (Architect)  | Initial architecture document  |

<!-- NOTE: This architecture document demonstrates several key BMAD patterns:
     1. The Prisma schema is included directly — architecture docs should be concrete
     2. ADRs are embedded for a small project (separate files for larger ones)
     3. Security section addresses OWASP top concerns, not just "we use HTTPS"
     4. Performance targets have specific numbers with measurement tools
     5. The modular monolith decision is explicitly documented as an ADR -->

## Lessons Learned

- **What went right**: Including the full Prisma schema in the architecture doc eliminated ambiguity during implementation. Amelia (Developer) could copy-paste the schema directly rather than interpreting vague ER descriptions.
- **What was tricky**: The tRPC vs REST decision (ADR-001) required acknowledging the trade-off of no public API. This was acceptable for MVP but needed to be documented for future reference when integrations become a priority.
- **Key insight**: Keeping the component diagram as ASCII art rather than requiring a diagramming tool lowered the barrier to keeping it updated. The diagram is version-controlled alongside the code.

## Decisions Made

- **Modular monolith over microservices**: For a 2-person team, microservices would add operational overhead without proportional benefit. The tRPC router boundaries provide logical separation without deployment complexity.
- **Clerk over NextAuth**: Saved 2-3 weeks of auth implementation. Vendor lock-in risk is mitigated by the thin service layer abstraction documented in the security section.
- **No caching layer for MVP**: Prisma query caching + Next.js route cache is sufficient for <1K users. Adding Redis would increase infrastructure complexity for minimal benefit at MVP scale.
