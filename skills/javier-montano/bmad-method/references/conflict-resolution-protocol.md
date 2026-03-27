# BMAD Conflict Resolution Protocol

## Table of Contents
- [Purpose](#purpose)
- [Ownership Matrix](#ownership-matrix)
- [Escalation Hierarchy](#escalation-hierarchy)
- [Resolution Patterns by Dispute Type](#resolution-patterns-by-dispute-type)
- [Decision Records](#decision-records)
- [Deadlock Handling](#deadlock-handling)
- [Concrete Scenarios](#concrete-scenarios)
- [Prevention Strategies](#prevention-strategies)

---

## Purpose

Conflicts in BMAD arise when two agents (or an agent and a human) disagree on artifact content, scope boundaries, technical decisions, or priority ordering. This protocol formalizes how to detect, escalate, and resolve these disputes without stalling the workflow.

**Core principle**: Every conflict must produce a documented decision. Unresolved conflicts are more expensive than wrong decisions — a wrong decision can be revised; an unresolved conflict blocks all downstream work.

**Conflict vs. disagreement**: A disagreement is healthy multi-perspective input (e.g., Architect suggests PostgreSQL, Developer suggests SQLite). It becomes a conflict when no resolution is reached and work cannot proceed. This protocol activates at the conflict stage.

---

## Ownership Matrix

Each artifact type and decision domain has exactly one owner. The owner has final authority within their domain, subject to escalation.

### Artifact Ownership

| Artifact | Owner Agent | Can Modify | Must Consult Before Modifying |
|----------|-----------|------------|-------------------------------|
| product-brief.md | Mary (Analyst) | Mary, John (PM) | User (for scope changes) |
| PRD.md | John (PM) | John | Winston (Architect) for feasibility |
| ux-spec.md | Sally (UX) | Sally, John | John (PM) for requirement alignment |
| architecture.md | Winston (Architect) | Winston | Amelia (Developer) for implementability |
| ADRs | Winston (Architect) | Winston | John (PM) for scope impact |
| epics/*.md | John (PM) | John, Bob (SM) | Winston for technical decomposition |
| stories/*.md | Bob (Scrum Master) | Bob, John | Amelia for estimation accuracy |
| project-context.md | Orchestrator | Any agent (with review) | Owner of the section being changed |
| sprint-status.yaml | Bob (Scrum Master) | Bob, Amelia | None (operational status) |
| gate-result.json | Gate Reviewer | Gate Reviewer only | Winston (Architect) for remediation routing |
| Code | Amelia (Developer) | Amelia | Quinn (QA) for test impact |
| Tests | Quinn (QA) | Quinn, Amelia | None (quality artifacts are QA's domain) |

### Decision Domain Ownership

| Decision Domain | Owner | Authority Scope |
|----------------|-------|----------------|
| What to build (scope) | John (PM) | FR inclusion/exclusion, MoSCoW priority |
| Who it is for (users) | Sally (UX) | Persona definitions, UX flows |
| How to build it (architecture) | Winston (Architect) | Technology choices, component boundaries, ADRs |
| How to decompose it (stories) | Bob (Scrum Master) | Story sizing, sprint assignment, dependency ordering |
| How to implement it (code) | Amelia (Developer) | Implementation patterns, code structure |
| Whether it is correct (quality) | Quinn (QA) | Test strategy, acceptance criteria verification |
| Whether it is ready (gate) | Gate Reviewer | Gate pass/fail verdict |
| Which agent to activate (routing) | Orchestrator | Phase routing, agent selection |

**Rule**: When a conflict spans two domains (e.g., a scope question with architecture implications), the domain of the artifact being modified wins. If the PM wants to add an FR that the Architect says is infeasible, the Architect must document the infeasibility in an ADR. The PM then decides whether to keep the FR (accepting the cost) or remove it.

---

## Escalation Hierarchy

```
Level 0: Self-Resolution
  Agent resolves internally using its principles and domain expertise.
  Applies when: The issue falls entirely within one agent's domain.

Level 1: Peer Consultation
  Two agents discuss and reach consensus.
  Applies when: The issue spans two domains. Both agents must agree.
  Time limit: 1 workflow step (do not carry unresolved peer disputes across steps).

Level 2: Owner Arbitration
  The artifact owner makes the final call within their domain.
  Applies when: Peer consultation fails. The owner's domain determines who decides.
  Documentation: Owner must document the rationale in the artifact or an ADR.

Level 3: User Escalation
  The human user makes the decision.
  Applies when: (a) The dispute is between equal-authority agents, (b) the decision
  has business impact beyond technical scope, or (c) Level 2 produces a decision
  that another agent formally objects to.
  Documentation: Decision is recorded in project-context.md key decisions log.
```

### Escalation Timing

| Level | Maximum Duration | If Unresolved |
|-------|-----------------|---------------|
| Level 0 | Immediate (within current step) | Escalate to Level 1 |
| Level 1 | 1 workflow step | Escalate to Level 2 |
| Level 2 | End of current session | Escalate to Level 3 |
| Level 3 | User responds (async acceptable) | Block the conflicting work; proceed on non-conflicting work |

---

## Resolution Patterns by Dispute Type

### Scope Disputes

**Definition**: Disagreement on whether a feature, FR, or NFR is in scope.

**Owner**: John (PM).

**Resolution protocol**:
1. John reviews the product brief's scope boundaries
2. If the brief explicitly includes or excludes the item, the brief wins
3. If the brief is ambiguous, John decides and updates the brief with a `[SCOPE-CHANGE]` tag
4. If the scope change has architecture impact, Winston must review and update architecture.md
5. If the scope change affects sprint planning, Bob must re-estimate

**Tie-breaker**: When the PM cannot decide (equal business value both ways), escalate to user. The user's scope decision is final and must not be revisited in the same project cycle.

### Technical Disputes

**Definition**: Disagreement on technology choice, architecture pattern, or implementation approach.

**Owner**: Winston (Architect).

**Resolution protocol**:
1. Winston evaluates both options against NFRs (performance, scalability, maintainability)
2. Each option must be documented as an ADR candidate with: context, alternatives, consequences
3. Winston selects the option that best satisfies NFRs with the least risk
4. If both options satisfy NFRs equally, prefer the option with lower complexity
5. The decision is recorded as a formal ADR

**Tie-breaker**: When the Architect cannot decide (both options are technically equivalent), prefer the option the Developer is more experienced with (lower implementation risk). If still tied, user decides.

### Quality Disputes

**Definition**: Disagreement on whether an artifact or code meets quality standards.

**Owner**: Quinn (QA) for code quality; Gate Reviewer for artifact quality.

**Resolution protocol**:
1. Quinn or Gate Reviewer states the specific quality criterion that is not met
2. The producer (Developer, PM, Architect) either fixes the issue or provides evidence that the criterion is satisfied
3. If the producer disagrees with the criterion itself, escalate to Level 2 (artifact owner decides if the criterion applies)
4. Gate criteria cannot be overridden by the artifact producer — only by the override procedure in `references/implementation-readiness-gate.md`

**Rule**: Quality disputes never resolve by lowering the standard. They resolve by either meeting the standard or formally documenting an override with remediation plan.

### Timeline Disputes

**Definition**: Disagreement on sprint assignment, story ordering, or deadline feasibility.

**Owner**: Bob (Scrum Master).

**Resolution protocol**:
1. Bob reviews the dependency graph and velocity data
2. If the dispute is about estimation (Developer says 3 points, PM says 1 point), the Developer's estimate wins — the implementer estimates, the PM prioritizes
3. If the dispute is about ordering (which story goes first), Bob applies: (a) dependency order, (b) MoSCoW priority, (c) risk front-loading, in that sequence
4. If the dispute is about deadline feasibility, Bob presents velocity data and carry-over trends. The data decides, not opinions.

**Rule**: The person doing the work estimates the effort. The person owning the product decides the priority. Neither overrides the other.

### Cross-Artifact Consistency Disputes

**Definition**: Two artifacts contain contradictory information.

**Owner**: The owner of the upstream artifact (per the artifact flow chain).

**Resolution protocol**:
1. Identify which artifact is upstream (per `references/artifact-flow-chain.md`)
2. The upstream artifact is the source of truth unless a formal scope change has been processed
3. Update the downstream artifact to match the upstream artifact
4. If the downstream artifact reveals that the upstream artifact is wrong, the upstream owner must update their artifact first, then the downstream artifact is updated to match
5. Never update two artifacts simultaneously to avoid version conflicts

---

## Decision Records

Every resolved conflict must be documented. Use the ADR format for technical decisions; use the key decisions log in project-context.md for scope and process decisions.

### Conflict Resolution Record Format

```markdown
## CR-[NNN]: [Short Title]

**Date**: [ISO 8601]
**Type**: Scope | Technical | Quality | Timeline | Consistency
**Parties**: [Agent A] vs [Agent B]
**Escalation Level**: 0 | 1 | 2 | 3

### Context
[What triggered the conflict — 2-3 sentences max]

### Options Considered
1. [Option A — advocated by Agent A]: [1 sentence]
2. [Option B — advocated by Agent B]: [1 sentence]

### Decision
[Which option was selected and why — 1-2 sentences]

### Consequences
- [Impact on artifacts — which files were updated]
- [Impact on timeline — any sprint or phase changes]

### Resolution Authority
[Who made the final decision: agent name, "peer consensus", or "user"]
```

### Where to Store Conflict Records

| Decision Type | Storage Location |
|--------------|-----------------|
| Technical (architecture, technology) | `architecture/adrs/ADR-NNN.md` |
| Scope (FR inclusion/exclusion) | PRD changelog section |
| Process (workflow, ceremony changes) | `project-context.md` key decisions log |
| Sprint-level (ordering, assignment) | `sprint-status.yaml` notes field |

---

## Deadlock Handling

A deadlock occurs when two agents cannot agree after Level 2 escalation and the user is unavailable for Level 3.

### Deadlock Detection

A deadlock exists when:
1. Two agents have exchanged positions 2+ times without convergence
2. Neither agent's domain clearly owns the decision
3. The user has not responded to an escalation within 1 business day

### Deadlock Resolution Protocol

```
Step 1: FREEZE — Stop all work on the disputed artifact.
        Proceed with unrelated work only.

Step 2: DOCUMENT — Both agents write their position in 3 sentences max.
        No new arguments — only summarize existing positions.

Step 3: DEFAULT — Apply the default resolution rule:
        a. For scope deadlocks: the smaller scope wins (conservative)
        b. For technical deadlocks: the simpler option wins (less risk)
        c. For quality deadlocks: the higher standard wins (safety)
        d. For timeline deadlocks: the longer estimate wins (buffer)

Step 4: TAG — Mark the decision as [DEADLOCK-DEFAULT] in the record.
        This flags it for user review at the next available opportunity.

Step 5: CONTINUE — Proceed with the default decision.
        The user may override it later without penalty.
```

### Default Resolution Rules

| Dispute Type | Default Rule | Rationale |
|-------------|-------------|-----------|
| Scope | Exclude the disputed item | Safer to add later than remove after implementation |
| Technology | Use the more established option | Less risk, more community support |
| Architecture | Prefer the simpler design | Complexity is the enemy of correctness |
| Estimation | Use the higher estimate | Under-estimating causes more damage than over-estimating |
| Quality | Apply the stricter standard | Quality debt compounds; permissive standards create drift |

---

## Concrete Scenarios

### Scenario 1: PM Wants Feature X, Architect Says Infeasible

```
Conflict: John (PM) adds FR-NOTIF-001 (real-time notifications).
Winston (Architect) says the current architecture (REST-only) cannot
support real-time without adding WebSocket infrastructure.

Level 1 (Peer): John and Winston discuss. Options:
  A. Add WebSocket infrastructure (Winston estimates 2 sprints of infra work)
  B. Use polling instead (satisfies FR partially, no new infra)
  C. Defer FR-NOTIF-001 to v2

Level 2 (Owner): This is a scope decision with architecture implications.
  John owns scope: decides FR-NOTIF-001 is Must-have.
  Winston owns architecture: documents ADR-007 selecting polling for MVP,
  WebSocket for v2. FR-NOTIF-001 is rewritten to specify polling behavior.

Resolution: Option B for MVP. ADR-007 created. FR-NOTIF-001 updated.
No escalation to user needed — both agents agreed on the compromise.
```

### Scenario 2: Developer Estimate vs PM Expectation

```
Conflict: Bob assigns STORY-SRCH-003 (full-text search) at 8 points.
John expects it at 3 points based on a similar story in a previous project.

Level 1 (Peer): Amelia (Developer) explains: the previous project used
Elasticsearch (pre-configured). This project uses PostgreSQL — full-text
search requires tsvector columns, index creation, and query optimization.

Level 2 (Owner): Timeline disputes are Bob's domain. Bob applies the rule:
the implementer estimates, the PM prioritizes. 8 points stands.

John adjusts sprint capacity accordingly. No escalation needed.
Record: Sprint planning notes document the estimation rationale.
```

### Scenario 3: Gate Reviewer Fails Step, Architect Disagrees

```
Conflict: Gate Reviewer assigns FAIL on Step 12 (Deployment Strategy).
Winston (Architect) argues the deployment strategy is implied by the
CI/CD pipeline configuration already in the repo.

Level 1 (Peer): Gate Reviewer states: "Implied is not documented.
The gate requires explicit documentation per the gate specification."

Level 2 (Owner): Gate pass/fail is Gate Reviewer's domain. The FAIL stands.
Winston must document the deployment strategy explicitly before re-evaluation.

Resolution: Winston writes the deployment strategy section (30 minutes).
Gate step 12 passes on re-evaluation. No override needed.
```

### Scenario 4: Deadlock — Two Valid Architecture Options

```
Conflict: Winston proposes microservices. The user has expressed no
preference. Amelia argues monolith-first is more appropriate for the
team size (solo developer).

Level 1 (Peer): Both present valid arguments. Winston cites scalability
NFRs. Amelia cites implementation speed and operational simplicity.

Level 2 (Owner): Winston owns architecture. But this decision has
major timeline impact (Amelia's domain for estimation).

Level 3: User is unavailable for 2 days.

Deadlock Protocol:
  Step 3 DEFAULT: For technical deadlocks, the simpler option wins.
  Decision: Monolith-first. Tagged [DEADLOCK-DEFAULT].

  When user returns: User reviews and confirms monolith-first.
  The [DEADLOCK-DEFAULT] tag is replaced with [USER-CONFIRMED].
```

---

## Prevention Strategies

| Strategy | Implementation | Prevents |
|----------|---------------|----------|
| Pre-phase alignment | At each phase boundary, all agents confirm understanding of inputs | Cross-artifact consistency disputes |
| Explicit scope boundaries | PRD must have an out-of-scope section with specific items | Scope disputes |
| ADR for every technology choice | No technology enters the stack without an ADR | Technical disputes after implementation starts |
| Estimation calibration | Compare estimates to actuals every 3 sprints | Timeline disputes |
| Definition of Done consensus | All agents review and agree on DoD before Sprint 1 | Quality disputes |
| Shared vocabulary | Glossary in `references/methodology-overview.md` | Semantic disputes (same word, different meaning) |

---

## Assumptions

- All BMAD agents operate within their defined domains as specified in `references/agent-as-code.md`
- The user is available for Level 3 escalation within 1 business day (async communication is acceptable)
- Conflict resolution records are stored in version control alongside other BMAD artifacts

## Limits

- This protocol covers agent-to-agent and agent-to-human disputes within BMAD — it does NOT cover interpersonal team conflicts
- This protocol assumes good faith from all parties — it does NOT handle deliberate process sabotage
- Deadlock defaults are conservative by design — they may not produce the optimal decision, only a safe one

## Acceptance Criteria

- [ ] Every artifact type has exactly one owner in the ownership matrix
- [ ] Every dispute type has a resolution protocol with a defined owner and tie-breaker
- [ ] Deadlock handling produces a decision (never infinite wait) and tags it for user review
- [ ] At least 3 concrete scenarios demonstrate the protocol end-to-end
- [ ] Every resolution produces a documented decision record

See also: `references/agent-as-code.md`, `references/artifact-flow-chain.md`, `references/implementation-readiness-gate.md`, `references/enterprise-governance.md`, `references/methodology-overview.md`
