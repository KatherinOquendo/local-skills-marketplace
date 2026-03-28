# S2: Per-Phase Risk Scanning (The Anxious Controller in Action)

For EACH pipeline phase, the controller asks uncomfortable questions: [EXPLICIT]

## Phase 0: Stakeholder Mapping
- Are we talking to the right people? Is there a hidden stakeholder missing?
- Does the sponsor actually have decision authority?
- Are there political agendas that are not being declared?

## Phase 1: AS-IS
- Is the team telling the truth about the current state? (Confirmation bias)
- Is technical debt being minimized?
- Does codebase data contradict what stakeholders report?

## Phase 2: Flow Mapping
- Are ALL flows mapped or only the "happy paths"?
- Are edge cases captured?
- Are third-party integrations documented with real SLAs?

## Phase 3: Scenarios
- Was the winning scenario chosen by evidence or by bias?
- Was the "do nothing" scenario genuinely evaluated?
- Did the Tree of Thought cover orthogonal dimensions?

## Phase 3b: Feasibility/Viability
- Do proposed PoCs have real kill criteria?
- Did software viability cover ALL components, not just the known ones?
- Are refuted claims reflected in the roadmap?

## Phase 4: Roadmap + Cost
- Are magnitude ranges realistic or anchored to team optimism?
- Is the 5% innovation margin included?
- Is the Cone of Uncertainty communicated correctly?

## Phase 4b: Commercial Model
- Is the commercial model viable for BOTH parties?
- Is there risk of incentive misalignment?
- Are earned value milestones measurable?

## Phase 5a/5b: Spec + Pitch
- Does the pitch promise something the spec does not support?
- Do business cases have documented assumptions?
- Is the proposal honest about limitations?

## Phase 6: Handover
- Does the operations team have capacity to receive?
- Are knowledge gaps documented?
- Is the transition governance clear?

For each finding: identified risk -> probability x impact -> mitigation -> owner -> deadline. [EXPLICIT]

**Required diagram**: Mindmap (Mermaid) of risks per phase [EXPLICIT]

---

# Prompt Integration: Skill Inventory (48 monitored skills)

The risk controller activates in EVERY pipeline phase. It is the most cross-cutting skill -- it scans risks in every executed prompt. [EXPLICIT]

## Role in Each Prompt

| Prompt | Scanning Activated | Controller Section |
|--------|------------------|----------------------|
| `00-plan-discovery` | Initial risk register, assumption log | S4 (Register) + S3 (Assumptions) |
| `01-stakeholder-map` | Organizational risks, change resistance | S2 (Phase Scanning) |
| `02-brief-tecnico` | Technical risk traffic-light | S2 + S1 (Appetite) |
| `03-asis-analysis` | Deep scan: security, debt, observability | S2 + S4 |
| `04-mapeo-flujos` | Failure points, circular dependencies | S2 + S4 |
| `05-escenarios` | Scenario stress-testing, pre-mortem | S3 + S5 (Pre-Mortem) |
| `06-solution-roadmap` | Financial controls, magnitude drift | S6 (Financial Controls) |
| `07-spec-funcional` | Complexity-risk matrix validation | S2 + S4 |
| `08-pitch-ejecutivo` | Proposal hardening, red lines | S7 (Hardening) |
| `09-handover` | Final risk tracker, kill criteria | S4 + S7 |
| `revisar` | Cross-check of risks in deliverables | S2 + S4 |
| `evolucionar` | Risk update post-improvement | S4 |
| `rescatar` | Risk inheritance + new rescue risks | S4 + S5 |

## Skills by Domain

| Domain | Skills | Typical Risks |
|---------|--------|-----------------|
| Discovery Pipeline (16) | discovery-orchestrator, stakeholder-mapping, workshop-facilitator, asis-analysis, dynamic-sme, flow-mapping, scenario-analysis, technical-feasibility, software-viability, solution-roadmap, cost-estimation, commercial-model, functional-spec, executive-pitch, discovery-handover, mermaid-diagramming | Scope creep, assumption drift, gate failure, evidence gaps |
| Architecture Design (8) | software-architecture, architecture-tobe, enterprise-architecture, solutions-architecture, infrastructure-architecture, devsecops-architecture, design-system, functional-toolbelt | Technical debt, vendor lock-in, scalability limits, security gaps |
| Data Strategy (7) | data-science-architecture, bi-architecture, data-engineering, database-architecture, data-governance, data-quality, analytics-engineering | Data quality, privacy/compliance, model drift, pipeline reliability |
| Cloud & Mobile (4) | cloud-native-architecture, cloud-migration, mobile-architecture, mobile-assessment | Migration risk, cost overrun, platform dependency, performance |
| Engineering Excellence (5) | api-architecture, event-architecture, security-architecture, performance-engineering, observability | Integration failures, security vulnerabilities, SLA breaches |
| Consulting & Quality (3) | quality-engineering, testing-strategy, user-representative | Coverage gaps, user adoption, testing blind spots |
| Governance & Risk (2) | project-program-management, risk-controlling-dynamics | Governance overhead, risk register staleness |
| Delivery & Brand (3) | html-brand, ux-writing, roadmap-poc | Brand inconsistency, accessibility gaps |

## Asset Inventory

Each skill has `examples/sample-output.md` as a benchmark. The controller validates that the outputs produced by each prompt match or exceed the depth of the corresponding example. [EXPLICIT]
