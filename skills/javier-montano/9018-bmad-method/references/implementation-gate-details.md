# Implementation Readiness Gate -- Detailed Specifications

The gate is a **mandatory checkpoint** before Phase 4. It validates that planning and solutioning artifacts are complete and aligned. [EXPLICIT]

**Run the gate**:
```bash
python scripts/validate_prd.py <project-root>
```

## The 13 Validation Steps

| # | Check | Validates |
|---|-------|-----------|
| 1 | PRD completeness | All required sections present |
| 2 | Architecture alignment | Arch addresses all PRD requirements |
| 3 | Story decomposition | All FRs covered by stories |
| 4 | Acceptance criteria | Every story has Given/When/Then |
| 5 | Dependency map | Story sequencing is valid |
| 6 | Risk register | Risks identified with mitigations |
| 7 | NFR coverage | Performance, security, scalability addressed |
| 8 | API contracts | Endpoints defined with schemas |
| 9 | Data model | Schema covers all entities |
| 10 | Security review | Auth, authz, encryption defined |
| 11 | Performance targets | SLAs/SLOs specified |
| 12 | Deployment strategy | CI/CD, environments, rollback |
| 13 | Rollback plan | Recovery procedures documented |

**Output**: `PASS` / `CONCERNS` / `FAIL` [EXPLICIT]

## Gate Result Actions

| Result | Criteria | Concrete Next Steps |
|--------|----------|-------------------|
| **PASS** | All 13 checks pass, <=2 WARNs | Proceed to Phase 4. Archive gate report in `architecture/gate-result.md`. |
| **CONCERNS** | No FAILs, 3+ WARNs | 1. Document each WARN as tracked risk. 2. Assign mitigation owner per WARN. 3. Proceed but review WARNed areas first in sprint 1. 4. Re-evaluate at retrospective. |
| **FAIL** | Any check is FAIL | 1. Identify responsible agent per failed check. 2. Return to Phase 3. 3. Re-run gate after remediation. 4. Max 3 attempts before escalating to user. |

## FAIL Remediation Routing

| Failed Check | Responsible Agent | Action |
|-------------|-------------------|--------|
| 1 (PRD completeness) | John/PM | Complete missing PRD sections |
| 2 (Architecture alignment) | Winston/Architect | Map unaddressed FRs to components |
| 3-5 (Stories, criteria, dependencies) | Bob/Scrum Master | Rewrite/add stories, fix sequencing |
| 6 (Risk register) | John/PM + Winston/Architect | Add risks with mitigations |
| 7-13 (NFRs, API, data, security, etc.) | Winston/Architect | Update architecture.md |

Use `templates/implementation-readiness.md.tmpl` as the gate checklist. [EXPLICIT]

## Agent Roster

| Agent | Role | Phase | File | Conflict Resolution |
|-------|------|-------|------|---------------------|
| Mary | Analyst | 1 | `agents/mary-analyst.md` | Defers to data; if data conflicts, escalates to user |
| John | Product Manager | 2 | `agents/john-pm.md` | Owns scope decisions; defers technical feasibility to Winston |
| Sally | UX Designer | 2 | `agents/sally-ux.md` | Advocates for user; defers to John on scope, Winston on feasibility |
| Winston | Architect | 3 | `agents/winston-architect.md` | Owns technical decisions; defers to John on requirements, creates ADR for disputes |
| Bob | Scrum Master | 3-4 | `agents/bob-scrum-master.md` | Owns process/decomposition; defers to Winston on technical sizing |
| Amelia | Developer | 4 | `agents/amelia-developer.md` | Follows story spec; escalates ambiguity to Bob, architectural gaps to Winston |
| Quinn | QA Engineer | 4 | `agents/quinn-qa.md` | Quality is non-negotiable; escalates unresolved findings to Bob/SM |
| Barry | Quick Flow Dev | Any | `agents/barry-quick-flow.md` | Self-contained; escalates to full BMAD flow if scope exceeds threshold |
| Orchestrator | Meta-router | Any | `agents/orchestrator.md` | Routes disputes to the agent who owns that artifact |
| Gate Reviewer | Gate evaluator | 3->4 | `agents/gate-reviewer.md` | Impartial; cannot be overridden by other agents |
| Retro Facilitator | Sprint retro | 4 | `agents/retrospective-facilitator.md` | Facilitates resolution; does not take sides |

[EXPLICIT]
