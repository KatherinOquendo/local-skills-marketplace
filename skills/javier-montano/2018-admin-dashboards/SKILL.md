---
name: admin-dashboards
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Build admin dashboard interfaces with data tables, filters, charts, CRUD
  operations, and real-time data updates. Covers layout patterns and state management. [EXPLICIT]
  Trigger: "admin panel", "dashboard", "data table", "CRUD interface"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Admin Dashboards

> "A dashboard should answer questions before they're asked." — Stephen Few

## TL;DR

Guides the architecture and implementation of admin dashboard interfaces featuring sortable/filterable data tables, CRUD operations, charts/metrics, real-time updates, and role-based access control. Use when building back-office tools, content management systems, or operational dashboards. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify data entities and their relationships (users, orders, content, settings)
- Review user roles and permission levels (admin, editor, viewer)
- Check existing API endpoints and data schemas
- Determine real-time requirements (WebSocket, polling, SSE)

### Step 2: Analyze
- Plan navigation structure (sidebar, breadcrumbs, nested routes)
- Design data table features (sort, filter, search, pagination, bulk actions)
- Choose chart library (Chart.js, Recharts, D3, Apache ECharts)
- Evaluate state management for complex filter/table interactions

### Step 3: Execute
- Build sidebar layout with collapsible navigation and role-based menu items
- Implement data tables with server-side pagination, sorting, and column configuration
- Add CRUD forms with validation, optimistic updates, and confirmation dialogs
- Create metric cards and charts for KPI overview section
- Wire real-time updates via Firestore listeners or WebSocket connections
- Add export functionality (CSV, PDF) for table data

### Step 4: Validate
- Test with large datasets (1000+ rows) — no UI freezing
- Verify CRUD operations handle errors gracefully (network failures, conflicts)
- Confirm role-based access hides unauthorized actions, not just routes
- Check keyboard navigation for data tables and forms

## Quality Criteria

- [ ] Data tables handle sorting, filtering, and pagination without full page reload
- [ ] CRUD operations show loading states, success feedback, and error recovery
- [ ] Dashboard loads key metrics within 1 second
- [ ] Role-based access enforced on both UI and API levels
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Loading all records client-side instead of server-side pagination
- Building custom data tables from scratch when libraries like TanStack Table exist
- Hiding menu items but not protecting API routes for unauthorized roles

## Related Skills

- `firestore-queries` — efficient data fetching for dashboard tables
- `cloud-functions` — API endpoints backing CRUD operations

## Usage

Example invocations:

- "/admin-dashboards" — Run the full admin dashboards workflow
- "admin dashboards on this project" — Apply to current context


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
