# Quality Gates -- Detailed Specifications

## Gate 1: Scenario Approval (after Phase 3 -- HARD STOP)

| Criterion | Evidence Required |
|-----------|------------------|
| 3+ scenarios evaluated | Scenario IDs and names |
| Complete scoring (no pending) | Cost/complexity/risk per scenario |
| Decision tree explicit | Trade-off documentation |
| Recommended scenario justified | Written rationale |
| 3+ assumptions documented | Assumption log entries |
| Steering committee approved | User confirmation |

**On failure:** Do NOT proceed. Options: (a) refine trade-offs, (b) add scenarios, (c) reduce scope. Timeline impact: +3-5 days. [EXPLICIT]

### Phase 3b: Technical Feasibility & Software Viability (after Gate 1)

After scenario approval, validate the chosen scenario before committing resources: [EXPLICIT]

**3b-A: Technical Feasibility** (Skill: `technical-feasibility`)
1. Extract every technical claim from the approved scenario
2. Evaluate 6 feasibility dimensions: technical, organizational, timeline, financial, regulatory, operational
3. Design spikes/PoCs for unvalidated claims
4. Identify blockers and showstoppers
5. Produce feasibility verdict: FEASIBLE / FEASIBLE WITH CONDITIONS / NOT FEASIBLE

**3b-B: Software Viability** (Skill: `software-viability`)
1. Forensic validation of EVERY technology, framework, and AI/ML component proposed
2. Maturity assessment: lifecycle, community health, production evidence
3. AI-specific validation: claims vs benchmarks, training data, drift monitoring
4. Vendor risk: funding, retention, lock-in, exit cost
5. Produce viability scorecard: SUBSTANCIA / PROMESA VIABLE / RIESGO ALTO / HUMO

**CHECKPOINT 3b:** Present combined verdict. If any technology = HUMO or feasibility = NOT FEASIBLE -> HOLD. Options: (a) pivot to alternative scenario, (b) replace technology, (c) run spikes in Sprint 0. Do NOT proceed to Phase 4 with unresolved critical findings. [EXPLICIT]

## Gate 2: Budget & Roadmap Approval (after Phase 4 -- HARD STOP)

| Criterion | Evidence Required |
|-----------|------------------|
| Realistic roadmap for team size | FTE vs. scope analysis |
| 9+ prerequisites with owners | Checklist with dates |
| Budget breakdown (not lump sum) | Line-item budget |
| Acceptable timeline | Business confirmation |
| 4+ risks with mitigation | Risk register entries |
| Executive sponsor approved | User confirmation |

**On failure:** Do NOT proceed to 5a. Generate 5b only (pitch for budget justification). Options: (a) reduce scope/MVP, (b) extend timeline, (c) phase investment. [EXPLICIT]

## Pre-Gate 3: Proposal QA & Risk Assessment (after Phase 5a+5b)

Before presenting Gate 3 to the client, run the governance and risk validation: [EXPLICIT]

**QA-A: Proposal QA Validation** (Skill: `project-program-management`, S5)
1. Coherence check: roadmap vs scenario vs AS-IS
2. Completeness audit: all deliverables substantive, no stubs
3. Viability verification: pitch claims backed by spec evidence
4. Alignment review: AS-IS problems addressed, feasibility guardrails reflected

**QA-B: Risk Controller Final Assessment** (Skill: `risk-controlling-dynamics`, S7)
1. Risk profile summary: open risks, exposure level
2. Unvalidated assumptions count and impact
3. Financial controls status: contingency, innovation margin, magnitude drift
4. Proposal hardening: disclosures, red lines, confidence bands

**PROPOSAL QA CHECKPOINT:** Proposal QA composite >=3.5/5.0 AND Risk profile != CRITICAL -> proceed to Gate 3. Otherwise: remediate before presenting to client. NEVER send a proposal that fails QA. [EXPLICIT]

## Gate 3: Final Approval (after Proposal QA)

| Criterion | Evidence Required |
|-----------|------------------|
| All deliverables populated | File manifest check |
| Cross-references consistent | Phase 4 tech <-> Phase 3 scenario <-> Phase 1 metrics |
| Proposal QA passed | QA scorecard >=3.5/5.0, no dimension <3 |
| Risk assessment complete | Risk controller final assessment delivered |
| Client approved | User confirmation |

**On failure:** Request specific revisions; re-present. [EXPLICIT]

## Phase 6: Handover Operacional (after Gate 3 approval)

Once Gate 3 is approved, invoke `discovery-handover` to generate the operational transition package: [EXPLICIT]

1. Ask user: recipient is **Operaciones**, **Comercial**, or **Ambos** (default: Ambos)
2. Validate all 7 discovery deliverables exist (01-08 files)
3. Generate `09_Handover_Operaciones.html` with 8 sections:
   - S1: Resumen Ejecutivo de Transicion
   - S2: Paquete de Activacion Comercial (pricing, proposal narrative, closing timeline)
   - S3: Checklist de Readiness Operacional (team, infra, accesos)
   - S4: Plan de Kickoff -- Primeros 90 Dias (Sprint 0 + Sprints 1-6)
   - S5: Protocolo de Transicion de Gobernanza (roles, ceremonias, escalation)
   - S6: Tracker de Validacion de Supuestos y Riesgos (assumptions, early warnings, kill criteria)
   - S7: Matriz de Transicion de Stakeholders (discovery roles -> execution roles)
   - S8: Anexos y Referencias Cruzadas

**Data Contract Phase 5 -> Phase 6:**
| Required Input | Source |
|---------------|--------|
| Approved roadmap with 5 phases | `06_Solution_Roadmap.html` |
| Functional spec with modules + use cases | `07_Especificacion_Funcional.html` |
| Executive pitch with financial model | `08_Pitch_Ejecutivo.html` |
| Risk register with cascade failures | `06_Solution_Roadmap.html` |
| Stakeholder map with RACI | `01_Stakeholder_Map.html` |
| Gate 3 approval | User confirmation |

**On completion:** Discovery engagement is formally closed. All 10 deliverables (00-09) constitute the complete engagement package. [EXPLICIT]
