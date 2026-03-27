# Sprint Readiness Checklist

**Purpose**: Verify all preconditions are met before a sprint begins.
**Gate owner**: Scrum Master agent (Bob) or human scrum master.
**Rule**: Do not start development until every item is checked or has a documented exception.

---

## Planning

- [ ] **Sprint goal defined** — a single sentence stating what this sprint achieves; not a list of stories
- [ ] **Sprint number and dates set** in `sprint-status.yaml` with status `planning`
- [ ] **Velocity baseline established** — average of last 3 sprints, or team capacity estimate for Sprint 1
- [ ] **Capacity calculated** — velocity minus risk buffer (10-20%), adjusted for known absences or holidays
- [ ] **Stories selected** — total points of selected stories fit within calculated capacity

## Story Readiness

- [ ] **All selected stories pass Definition of Ready** — see `checklists/story-ready.md`
- [ ] **No unresolved blockers** on any selected story — `blocked-by` dependencies are all `done`
- [ ] **Stories assigned** — each story has a primary implementer in the `assigned-to` field
- [ ] **Story priority order clear** — team knows which stories to start first based on dependencies and priority

## Infrastructure

- [ ] **`project-context.md` is current** — tech stack, conventions, and constraints reflect the actual state of the codebase
- [ ] **Test infrastructure working** — test runner executes, existing tests pass, test database or mocks are available
- [ ] **CI/CD pipeline functional** — commits trigger lint, test, and build stages; failures are reported
- [ ] **Development environment reproducible** — any developer (human or AI agent) can set up and run the project from documented instructions

## Communication

- [ ] **Sprint status file initialized** — `sprint-status.yaml` updated with selected stories, assignees, and `todo` status

---

**Next**: Story development (`workflows/sprint-cycle/step-02-develop.md`)
**Reference**: `references/phase-4-implementation.md`, `checklists/story-ready.md`
