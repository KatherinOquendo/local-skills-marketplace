# Prompt Integration Protocol

El orquestador es el receptor primario de los 16 prompts NL-HP v3.0. Cada prompt activa un subconjunto de skills: [EXPLICIT]

## Prompt -> Skill Mapping

| Prompt | Skill Primario | Skills de Soporte | Gate |
|--------|---------------|-------------------|------|
| `00-plan-discovery` | discovery-orchestrator | project-program-management, risk-controlling-dynamics | -- |
| `01-stakeholder-map` | stakeholder-mapping | workshop-facilitator | -- |
| `02-brief-tecnico` | asis-analysis (brief) | dynamic-sme, risk-controlling-dynamics | -- |
| `03-asis-analysis` | asis-analysis (full) | dynamic-sme, software-architecture, security-architecture, observability, database-architecture | -- |
| `04-mapeo-flujos` | flow-mapping | functional-toolbelt, api-architecture, event-architecture | -- |
| `05-escenarios` | scenario-analysis | technical-feasibility, software-viability, risk-controlling-dynamics | G1 |
| `06-solution-roadmap` | solution-roadmap | cost-estimation, commercial-model, risk-controlling-dynamics, project-program-management | G2 |
| `07-spec-funcional` | functional-spec | functional-toolbelt, flow-mapping, architecture-tobe | -- |
| `08-pitch-ejecutivo` | executive-pitch | commercial-model, cost-estimation, risk-controlling-dynamics | G3 |
| `09-handover` | discovery-handover | project-program-management, risk-controlling-dynamics, stakeholder-mapping | -- |
| `completo` | discovery-orchestrator | ALL pipeline skills | G1+G2+G3 |
| `intermedio` | discovery-orchestrator | asis->scenario->feasibility->roadmap->pitch->handover | G1+G2 |
| `express` | discovery-orchestrator | asis->scenario->pitch | -- |
| `revisar` | project-program-management (S5) | risk-controlling-dynamics, discovery-orchestrator | -- |
| `evolucionar` | discovery-orchestrator | skill for the specific deliverable | -- |
| `rescatar` | discovery-orchestrator | skills per missing phases | per state |

## Prompt Reception Protocol

1. **Identify prompt**: Detect which of the 16 prompts is being executed. [EXPLICIT]
2. **Activate primary skill**: Invoke the corresponding skill with its agents. [EXPLICIT]
3. **Activate governance**: `project-program-management` (tracking) + `risk-controlling-dynamics` (scanning). [EXPLICIT]
4. **Verify prerequisites**: Inputs from previous phases per Inter-Phase Data Contracts. [EXPLICIT]
5. **Execute per MODE**: Respect the interaction mode declared in the prompt. [EXPLICIT]
6. **Produce output**: Per the primary skill's Output Artifact, in the requested FORMAT. [EXPLICIT]
7. **Register in governance**: Update phase status in P-01 and risk register in P-02. [EXPLICIT]

## Asset Inventory

Each skill produces reference outputs in its `examples/` directory: [EXPLICIT]

| Skill | Example Asset | Description |
|-------|--------------|-------------|
| asis-analysis | `examples/sample-output.md` | AS-IS analysis 10 sections -- Acme Corp Banking |
| stakeholder-mapping | `examples/sample-output.md` | Stakeholder map with RACI -- Acme Corp Banking |
| flow-mapping | `examples/sample-output.md` | DDD taxonomy + 8 E2E flows -- Acme Corp Banking |
| scenario-analysis | `examples/sample-output.md` | 3 ToT scenarios with 6D scoring -- Acme Corp Banking |
| technical-feasibility | `examples/sample-output.md` | 6D feasibility with spikes -- Acme Corp Banking |
| software-viability | `examples/sample-output.md` | Viability forensics with scorecard -- Acme Corp Banking |
| solution-roadmap | `examples/sample-output.md` | 5-phase roadmap with Monte Carlo -- Acme Corp Banking |
| cost-estimation | `examples/sample-output.md` | Cost drivers + magnitudes -- Acme Corp Banking |
| commercial-model | `examples/sample-output.md` | Commercial model with deal canvas -- Acme Corp Banking |
| functional-spec | `examples/sample-output.md` | Modules + 8 UC + 6 BR -- Acme Corp Banking |
| executive-pitch | `examples/sample-output.md` | Business case C-level -- Acme Corp Banking |
| discovery-handover | `examples/sample-output.md` | Handover package with 90d plan -- Acme Corp Banking |
| project-program-management | `examples/sample-output.md` | P-01 Governance dashboard -- Acme Corp Banking |
| risk-controlling-dynamics | `examples/sample-output.md` | P-02 Risk register + pre-mortem -- Acme Corp Banking |

**Usage**: The examples/ serve as quality benchmarks. Each prompt's output must match or exceed the depth and structure of the corresponding example. [EXPLICIT]
