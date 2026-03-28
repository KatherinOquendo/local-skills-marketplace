---
name: asis-analysis
argument-hint: "project-name [codebase-path]"
description: 
  This skill should be used when the user asks to "analyze the codebase",
  "assess current architecture", "run an AS-IS analysis", "perform a technical audit",
  or "evaluate tech debt", or mentions current state, legacy system review,
  or technical health check. It produces a 10-section current-state technical
  assessment with C4 diagrams, code quality metrics, tech debt inventory,
  and prioritized recommendations. Use this skill whenever the user needs
  a baseline assessment before modernization, even if they don't explicitly
  ask for "AS-IS analysis". [EXPLICIT]
argument-hint: "project-name [codebase-path]"
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# AS-IS Technical Analysis

Generates a 10-section current-state technical assessment: executive dashboard, technology inventory, code structure, C4 architecture, code quality metrics, technical debt inventory, NFR heatmap, security posture, operational model, and risk register with prioritized recommendations. [EXPLICIT]

## Principio Rector

> *No se puede trazar un camino hacia el futuro sin comprender con honestidad brutal dónde se está parado hoy.*

1. **Diagnóstico basado en evidencia, no en opinión.** Cada hallazgo debe estar respaldado por métricas extraídas del código, configuración o historial operativo. La intuición guía la exploración; la evidencia sustenta la conclusión. [EXPLICIT]
2. **El presente contiene las semillas del futuro.** Las decisiones arquitectónicas heredadas no son errores — son contexto. Comprender *por qué* se tomaron revela restricciones que cualquier transformación debe respetar o explícitamente romper. [EXPLICIT]
3. **La deuda técnica es deuda de conocimiento.** Cada atajo no documentado, cada patrón inconsistente, cada test ausente representa conocimiento que el equipo decidió no capturar. El análisis AS-IS restaura ese conocimiento antes de que se pierda. [EXPLICIT]

## Inputs

- `$1` — Path to codebase root (default: current working directory)
- `$2` — Analysis depth: `full` (default), `executive` (sections 0,5,9,10 only)

Parse from `$ARGUMENTS`. [EXPLICIT]

**Parameters:**
- `{MODO}`: `piloto-auto` (default) | `desatendido` | `supervisado` | `paso-a-paso`
  - **piloto-auto**: Auto para extracción de métricas y análisis de código, HITL para hallazgos de seguridad y decisiones de escalamiento. [EXPLICIT]
  - **desatendido**: Cero interrupciones. Análisis completo automatizado. Supuestos documentados. [EXPLICIT]
  - **supervisado**: Autónomo con reportes al completar cada sección del framework. [EXPLICIT]
  - **paso-a-paso**: Confirma antes de cada sección del análisis. [EXPLICIT]
- `{FORMATO}`: `markdown` (default) | `html` | `dual`
- `{VARIANTE}`: `ejecutiva` (~40% — sections S0, S5, S9, S10 only) | `técnica` (full, default)

## Dynamic Context Injection

Auto-detect codebase characteristics before starting analysis:

```bash
# Language detection
find . -name "*.ts" -o -name "*.py" -o -name "*.java" -o -name "*.go" -o -name "*.rs" | head -30

# Build system detection
ls -la package.json pom.xml build.gradle Cargo.toml go.mod setup.py pyproject.toml Makefile 2>/dev/null

# Infrastructure detection
find . -name "Dockerfile" -o -name "*.yaml" -path "*/k8s/*" -o -name "docker-compose*" | head -10

# API surface detection
find . -name "*.yaml" -path "*/swagger/*" -o -name "openapi*" -o -name "*.proto" | head -10
```

Use detected languages, build tools, and infrastructure to scope each section. [EXPLICIT]

## Input Requirements

**Mandatory:**
- Complete codebase with commit history (or representative samples across all layers)
- Build configuration (Maven/Gradle/npm/setup.py) for LOC and dependency tree
- Deployment configuration (Docker/Kubernetes manifests, IaC)

**Recommended:**
- API specifications (Swagger/OpenAPI, gRPC proto files)
- Git history (last 24 months) for complexity trend analysis
- Operational logs (error rates, latency, failure incidents)
- Previous assessments or modernization reports

## Assumptions & Limits

**Assumptions:**
- Codebase is buildable (dependencies resolvable)
- System has operational history (incident/performance data available)
- Documentation in English or Spanish
- No production secrets embedded in source

**Cannot do:**
- Runtime profiling under production load (requires live monitoring)
- Live load testing or performance tuning
- Team interviews or org structure analysis (requires human interaction)
- Legal compliance review (requires legal expertise)

## Workarounds When Inputs Missing

| Missing Input | Impact | Workaround |
|---|---|---|
| No deployment config | Cannot assess infrastructure | Infer from Dockerfiles, K8s manifests, CI/CD scripts; flag as assumption |
| No API specs | Cannot fully document integrations | Reverse-engineer from code (HTTP clients, REST annotations, gRPC stubs) |
| No security audit | Cannot benchmark against standards | Lightweight SAST scan (SQL injection, hardcoded secrets, weak crypto patterns) |
| No performance data | Cannot assess NFR baseline | Code-level heuristics (complexity suggests bottlenecks) + recommend profiling |
| <1 year history | Cannot assess trends | Current snapshot only; flag as point-in-time analysis |
| Monorepo unclear | Cannot map boundaries | Infer from package naming, deployment units, team ownership patterns |

## Edge Cases

- **Monorepo:** Decompose per deployment unit. Analyze coupling between units.
- **No CI/CD:** Infer from Dockerfiles, cloud configs, README scripts. Flag inference risk.
- **No test suite:** Flag coverage as CRITICAL (0%). Extrapolate quality risk via complexity. Recommend test buildout.
- **Multiple languages:** Metrics per language separately. +1 risk per language for integration burden.
- **Microservices vs Monolith:** Check for multiple deployable units. Analyze per-service if microservices.
- **Legacy no docs:** Reverse-engineer from code structure + configuration. Flag confidence level.
- **System >500K LOC:** Phased analysis (Tier 1: core domains, Tier 2: supporting). Deliver executive summary + prioritized deep-dives.
- **Vendor lock-in detected:** Flag proprietary dependencies with migration cost estimates and open-source alternatives.
- **Outdated framework (EOL):** Escalate to CRITICAL risk. Document security exposure and upgrade path complexity.

## Trade-off Matrix

| Decision | Enables | Constrains | When to Use |
|---|---|---|---|
| **Full 10-section analysis** | Maximum depth, complete audit trail | 5-7 days, high token cost | High-stakes modernization, regulated environments |
| **Executive variant** (S0+S5+S9+S10) | Fast insights, decision-ready | Misses detailed architecture/quality data | Time-constrained, executive audience |
| **Security-focused** (S7 deep) | Compliance-ready, vulnerability inventory | Narrower scope | Pre-audit, compliance-driven engagements |
| **Quality-focused** (S4+S5 deep) | Actionable tech debt remediation plan | Less architecture context | Tech debt reduction initiatives |

## 10-Section Framework

### S0: Executive Dashboard
System snapshot: LOC, modules, integrations, team size, years in production, tech stack summary, development status, maintenance cost estimate. Health score (1-10) with color-coded indicators. [EXPLICIT]

### S1: Technology Inventory
Per layer: Backend, Frontend, Data, Infrastructure, Development. Dependency tree table with EOL status. Flag deprecated dependencies. Version currency score per component. [EXPLICIT]

### S2: Code Organization
Module decomposition, coupling analysis (afferent/efferent), layering assessment, cyclomatic complexity distribution, anti-patterns (god classes, circular dependencies, duplication). Package cohesion metrics. [EXPLICIT]

### S3: Architecture (C4 Model)
Level 1 (Context): system as black box with external actors. Level 2 (Containers): major services, databases, data flows. Pattern catalog with quality assessment. Architecture fitness functions where applicable. [EXPLICIT]

### S4: Code Quality Metrics
Complexity distribution (p50, p95), duplication %, test coverage by layer, dependency depth, code smells by type. Dashboard with severity-coded cards. Trend analysis if git history available. [EXPLICIT]

### S5: Technical Debt Inventory
Per item: description, category (7 types: design, code, test, build, documentation, infrastructure, dependency), severity, technical impact, business impact, remediation pathway, prioritization score (impact x cost-to-fix). [EXPLICIT]

**Conditional logic:**
- IF debt >30% of codebase OR average CC >15: flag CRITICAL, recommend refactoring before features
- IF test coverage <20%: CRITICAL quality risk
- IF dependency depth >5: recommend modularization
- IF >10 circular dependencies: architectural refactor required

### S6: NFR Heatmap
7x5 matrix: performance, security, maintainability, scalability, reliability, usability, interoperability. Scored 1-10 with evidence. Gap analysis against targets. Priority ranking by business impact. [EXPLICIT]

### S7: Security Assessment
Authentication, authorization, encryption, data protection, known CVEs (SBOM analysis), compliance gaps. Severity-rated findings with remediation recommendations. OWASP Top 10 mapping where applicable. [EXPLICIT]

### S8: Operational Model
Deployment model, monitoring/observability, incident response (MTTR), release management, capacity management. Operational readiness scorecard. DevOps maturity assessment (DORA metrics if available). [EXPLICIT]

### S9: Risk Register
Top-10 risks: probability x impact matrix. Per risk: category, score, current mitigations, recommended improvements, owner, status. Risk velocity indicator (growing/stable/shrinking). [EXPLICIT]

### S10: Recommendations
Top 5-10 findings with root cause + business impact. Quick wins (under 5 eng-days). Strategic roadmap (immediate/short/medium/long-term). Refactor vs rewrite vs replace decision tree per major component. [EXPLICIT]

## Cross-Section Traceability

Every recommendation in S10 must reference evidence from S0-S9:
- S2 Code Structure to S5 Debt (coupling = architectural debt)
- S4 Quality to S5 Debt (low coverage = quality debt)
- S5 Debt to S9 Risks (high debt with uncertain remediation = risk)
- S6 NFR Gaps to S5 Debt (NFR miss = technical work required)
- S7 Security to S9 Risks (CVEs = security risk)
- S8 Ops Gaps to S9 Risks (manual deployment = operational risk)
- S9 Risks to S10 Roadmap (top risks = immediate roadmap items)

## Escalation to Human Architect

- Codebase doesn't match business description
- Multiple competing architectural patterns (MVC + microservices mixed)
- Undocumented integration logic requiring team interviews
- Code contradicts comments (conflicting evidence)
- Regulatory compliance ambiguity (PCI, HIPAA, GDPR)
- Rare/uncommon tech stack beyond standard tooling

## Execution Workflow

1. **Input Validation (30 min):** Verify completeness, collect manifests, flag gaps
2. **Automated Extraction (2-4 hours):** Parse metrics (LOC, complexity, duplication), generate dependency tree, scan vulnerabilities
3. **Architectural Analysis (4-6 hours):** Map C4 L1/L2, identify patterns, assess coupling
4. **Synthesis (4-6 hours):** Consolidate into 10 sections, prioritize by business impact, cross-reference validation

**Typical engagement:** 5-7 days for systems under 500K LOC.

## Output Artifact

**Primary:** `03_Analisis_AS-IS_{project}.md` (o `.html` si `{FORMATO}=html|dual`) — Full 10-section current-state assessment with C4 diagrams, code quality metrics, tech debt inventory, risk register, and prioritized recommendations.

**Secondary:** `02_Brief_Tecnico_{project}.md` — Executive summary (S0 + key findings).

**Diagramas incluidos:**
- C4 Context diagram: system boundaries and external actors
- C4 Container diagram: internal components and relationships
- Mindmap: technology stack overview
- Quadrant chart: NFR heatmap positioning

## Validation Gate

- [ ] All 10 sections populated with evidence-based content (no template placeholders)
- [ ] C4 L1 and L2 diagrams reflect actual system topology
- [ ] Every S10 recommendation linked to evidence source (S0-S9)
- [ ] Tech debt and risks scored quantitatively
- [ ] Security includes concrete vulnerability findings
- [ ] Technology inventory flags EOL versions with upgrade paths
- [ ] NFR scores cite metrics or estimation approach
- [ ] Recommendations sized in effort and sequenced by business criticality
- [ ] Cross-section traceability complete and verifiable

## Output Format Protocol

| Format | Default | Description |
|--------|---------|-------------|
| `markdown` | ✅ | Rich Markdown + Mermaid diagrams. Token-efficient. |
| `html` | On demand | Branded HTML (Design System). Visual impact. |
| `dual` | On demand | Both formats. |

Default output is Markdown with embedded Mermaid diagrams. HTML generation requires explicit `{FORMATO}=html` parameter. [EXPLICIT]

### Diagrams (Mermaid)
- C4 Context diagram: system boundaries and external actors
- C4 Container diagram: internal components and their relationships
- Mindmap: technology stack overview

---
**Author:** Javier Montano | **Last updated:** March 18, 2026

## Usage

Example invocations:

- "/asis-analysis" — Run the full asis analysis workflow
- "asis analysis on this project" — Apply to current context

