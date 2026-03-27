# Story Completion Checklist (Definition of Done)

**Purpose**: Verify a story is truly complete before marking it `done` in sprint-status.yaml.
**Gate owner**: Developer agent (Amelia), QA agent (Quinn), or human reviewer.
**Rule**: A story is not done until every item is checked. Partial completion is status `in-progress` or `review`, never `done`.

---

## Acceptance Criteria

- [ ] **Every acceptance criterion tested** — each Given/When/Then block from the story has a corresponding passing test (unit, integration, or e2e as appropriate)
- [ ] **Edge cases and error paths verified** — negative cases from the ACs are tested, not just happy paths

## Code Quality

- [ ] **Code reviewed** — at least one reviewer (human or agent) has approved the implementation; review comments are resolved, not deferred
- [ ] **All tests passing** — full test suite runs green, including pre-existing tests (no regressions)
- [ ] **No linting errors or warnings** — code passes the project's configured linter without suppressions added for this change
- [ ] **No open security findings** — no new vulnerabilities introduced; if a security scanner runs, it reports no new issues for the changed files

## Conventions

- [ ] **Code follows `project-context.md` conventions** — naming, file structure, branching, and commit message formats match documented standards
- [ ] **No hardcoded secrets or credentials** — API keys, passwords, and tokens use environment variables or secrets management

## Documentation

- [ ] **Inline documentation updated** — public functions/methods have doc comments if the project convention requires them; complex logic is commented
- [ ] **Architecture docs updated** if the implementation deviated from the planned approach (new ADR if deviation is significant)

## Sprint Tracking

- [ ] **`sprint-status.yaml` updated** — story status set to `done`, notes field reflects any deviations or learnings
- [ ] **Branch merged** to the target branch per the project's branching strategy
- [ ] **Story file frontmatter updated** — `status: done` in the story's YAML frontmatter

---

**Reference**: `references/phase-4-implementation.md`, `checklists/story-ready.md`
