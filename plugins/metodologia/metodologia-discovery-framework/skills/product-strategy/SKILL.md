---
name: metodologia-product-strategy
description: >
  Product roadmap prioritization, backlog strategy, value stream mapping, product-market fit validation.
  Use when the user asks to "define product roadmap", "prioritize backlog", "map value streams",
  "validate product-market fit", or mentions product vision, RICE scoring, opportunity trees, dual-track agile.
author: Javier Montaño · Comunidad MetodologIA
argument-hint: "<product-or-initiative-name> [etapa: inception|growth|maturity]"
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

# Product Strategy: Roadmap, Prioritization & Value Stream Design

Product strategy translates business objectives into actionable product plans. The skill produces product vision documents, prioritization matrices, and value hypothesis canvases that align development effort with measurable customer and business outcomes.

## Grounding Guideline

> *A product strategy without market data is opinion. A strategy with data but without vision is reaction.*

1. **Vision -> Strategy -> Tactics.** The order matters — without a clear vision, the strategy is a set of disconnected initiatives.
2. **User value first.** Features that do not solve real user problems are product debt.
3. **Measure outcomes, not outputs.** Success is not how many features ship — it is how much value they capture.

## TL;DR

- Defines product vision and roadmap strategy aligned with business objectives
- Prioritizes backlog with quantitative frameworks (RICE, WSJF, Opportunity Scoring)
- Maps value streams to identify waste and optimization opportunities
- Validates product-market fit with hypothesis canvas and traction metrics
- Structures dual-track agile: continuous discovery + disciplined delivery

## Inputs

The user provides a product or initiative name as `$ARGUMENTS`. Parse `$1` as the **product/initiative name**.

**Parameters:**
- `{MODO}`: `piloto-auto` (default) | `desatendido` | `supervisado` | `paso-a-paso`
- `{FORMATO}`: `markdown` (default) | `html` | `dual`
- `{VARIANTE}`: `ejecutiva` (~40%) | `tecnica` (full, default)
- `{ETAPA}`: `inception` | `growth` | `maturity` | `auto` (default — detected from context)

## Deliverables

1. **Product vision document** — North star, target personas, value proposition, success metrics
2. **Prioritization matrix** — RICE/WSJF scored backlog with effort-impact quadrants
3. **Value hypothesis canvas** — Assumptions, experiments, validation criteria per feature area
4. **Value stream map** — End-to-end flow from idea to customer value with waste identification
5. **Strategic roadmap** — Now/Next/Later roadmap with outcome-based milestones

## Process

1. **Establish vision and north star** — Define product vision statement, north star metric, and strategic guardrails
2. **Identify personas and jobs-to-be-done** — Map target user segments and their core jobs, pains, and gains
3. **Build opportunity tree** — Decompose desired outcomes into opportunities, then into solution ideas
4. **Prioritize with quantitative framework** — Score each opportunity using RICE (Reach, Impact, Confidence, Effort) or WSJF
5. **Map current value stream** — Document current flow from idea to production, measure lead times and wait times
6. **Identify waste** — Flag handoffs, wait states, rework loops, and gold plating in the value stream
7. **Design outcome-based roadmap** — Structure roadmap around outcomes (not features) with Now/Next/Later horizons
8. **Define value hypotheses** — For each major bet, document assumption, experiment, success criteria, and pivot trigger
9. **Establish traction metrics** — Define leading and lagging indicators for product-market fit validation

## Quality Criteria

- [ ] Vision statement is specific, measurable, and time-bound
- [ ] Prioritization uses quantitative framework with documented scores
- [ ] Value stream map includes cycle time and wait time measurements
- [ ] Roadmap is outcome-based, not feature-based
- [ ] Each major initiative has explicit value hypothesis with validation plan
- [ ] Personas are based on research or documented assumptions [SUPUESTO]
- [ ] Roadmap distinguishes committed vs. speculative items
- [ ] Product metrics include both leading and lagging indicators

## Assumptions & Limits

- Assumes product team exists or will be formed with clear ownership
- Does not replace user research — flags where primary research is needed
- Financial projections are directional estimates, not forecasts
- Market analysis relies on available data and documented assumptions

## Edge Cases

| Escenario | Estrategia de Manejo |
|---|---|
| Producto sin usuarios actuales (greenfield) | Usar Lean Canvas en lugar de data historica; todas las hipotesis marcadas [SUPUESTO]; enfasis en experimentos de validacion rapida |
| Multiples stakeholders con visiones conflictivas | Ejecutar ejercicio de alignment (vision statement vote) antes de priorizar; documentar desacuerdos como riesgos |
| Producto legacy con backlog heredado de +500 items | Aplicar triage agresivo: archivar items >12 meses sin actividad, re-score solo los top 50 por volumen de solicitud |
| Pivot en curso — cambio de mercado objetivo | Generar two-track roadmap (current + pivot), con decision gate y criterios explicitos de go/no-go |

## Decisions & Trade-offs

| Decision | Habilita | Restringe | Justificacion |
|---|---|---|---|
| RICE como framework default | Comparabilidad cuantitativa entre iniciativas | Requiere estimaciones de Reach y Confidence que pueden ser imprecisas | RICE es el mas adoptado y entendido; se complementa con WSJF para contextos SAFe |
| Roadmap Now/Next/Later en lugar de Gantt | Flexibilidad ante cambios, enfoque en outcomes | Menor precision temporal para stakeholders que piden fechas | Evita compromisos de fecha prematuros; se acompana de milestones medibles |
| Dual-track agile como default | Discovery continuo alimenta delivery | Requiere capacidad dedicada a discovery (minimo 20% del equipo) | Reduce riesgo de construir features sin validar; escalable con equipo pequeno |

## Knowledge Graph

```mermaid
graph TD
    subgraph Core["Product Strategy"]
        A[Vision de Producto] --> B[Opportunity Tree]
        A --> C[Priorizacion RICE/WSJF]
        B --> D[Value Hypothesis Canvas]
        C --> E[Roadmap Now/Next/Later]
    end
    subgraph Inputs["Inputs"]
        F[Objetivos de Negocio] --> A
        G[User Research / Personas] --> B
        H[Backlog Existente] --> C
    end
    subgraph Outputs["Outputs"]
        E --> I[Roadmap Estrategico]
        D --> J[Experimentos de Validacion]
        C --> K[Matriz de Priorizacion]
    end
    subgraph Related["Related Skills"]
        L[business-analysis] -.-> A
        M[software-architecture] -.-> C
        N[change-management] -.-> E
    end
```

## Output Templates

**Formato 1 — Markdown (default)**
- Filename: `Product_Strategy_{producto}_{WIP|Aprobado}.md`
- Estructura: Vision > Personas > Opportunity Tree > Priorizacion > Value Hypotheses > Roadmap > Metricas
- Incluye tablas de scoring y diagramas Mermaid inline

**Formato 2 — HTML (presentacion ejecutiva)**
- Filename: `Product_Strategy_{producto}_{WIP|Aprobado}.html`
- Estructura: Executive summary (1 pagina) > Roadmap visual > Priorizacion highlights > Appendix con datos completos
- Optimizado para compartir con stakeholders no tecnicos

**Formato 3 — DOCX (bajo demanda)**
- Filename: `{fase}_product_strategy_{cliente}_{WIP}.docx`
- Generado via python-docx con MetodologIA Design System v5. Portada, TOC automático, encabezados en Poppins (navy), cuerpo en Trebuchet MS, acentos en gold. Tablas de scoring RICE/WSJF y value hypotheses con zebra striping. Encabezados y pies de página con branding MetodologIA.

**Formato 4 — XLSX (bajo demanda)**
- Filename: `{fase}_product_strategy_{cliente}_{WIP}.xlsx`
- Generado via openpyxl con MetodologIA Design System v5. Headers navy con texto blanco Poppins, formato condicional por score RICE/WSJF y horizonte de roadmap (Now/Next/Later), auto-filtros en todas las columnas, valores calculados sin formulas. Hojas: Prioritization Matrix, Value Hypotheses, Value Stream Map, Roadmap.

**Formato 5 — PPTX (bajo demanda)**
- Filename: `{fase}_product_strategy_{cliente}_{WIP}.pptx`
- Generado via python-pptx con MetodologIA Design System v5. Slide master con gradiente navy, títulos en Poppins, cuerpo en Trebuchet MS, acentos en gold. Máx 20 slides ejecutivo / 30 técnico. Notas del presentador con referencias de evidencia. Slides: Vision y North Star, Personas y JTBD, Opportunity Tree, Prioritization Matrix RICE/WSJF, Value Hypotheses, Roadmap Now/Next/Later, Métricas de tracción.

## Evaluacion

| Dimension | Peso | Criterio |
|-----------|------|----------|
| Trigger Accuracy | 10% | Activa triggers correctos sin falsos positivos ante keywords de producto y estrategia |
| Completeness | 25% | Todos los entregables cubren vision, priorizacion, value stream, roadmap y metricas |
| Clarity | 20% | Instrucciones ejecutables sin ambiguedad; vision statement es especifica y medible |
| Robustness | 20% | Maneja edge cases (greenfield, pivot, backlog masivo) con estrategias documentadas |
| Efficiency | 10% | Proceso no tiene pasos redundantes; escala con variante ejecutiva al 40% |
| Value Density | 15% | Cada seccion aporta valor practico directo; metricas son actionable |

**Umbral minimo**: 7/10 en cada dimension para considerar el skill production-ready.

## Cross-References

- **metodologia-business-analysis:** Business requirements that feed product backlog
- **metodologia-software-architecture:** Technical feasibility constraints on product decisions
- **metodologia-change-management:** Organizational readiness for product changes

---
**Autor:** Javier Montaño · Comunidad MetodologIA | **Version:** 1.0.0
