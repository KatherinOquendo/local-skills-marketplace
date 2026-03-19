# 06 — Execution Backlog

> Backlog ejecutable priorizado para robustecer el Metodología-Discovery-Framework (MAO v1.4)
> Fecha: 2026-03-19 | Auditor: Claude Code (Principal Skill Auditor)

---

## Convenciones

- **Esfuerzo**: S = <1h, M = 1-4h, L = 4-8h, XL = 8h+
- **Impacto**: Crítico / Alto / Medio / Bajo
- **Estado**: Pendiente (todos — este backlog es output de la auditoría)
- **Herramienta sugerida**: skill del IDE de Claude Code que puede ejecutar la tarea

---

## Sprint 0: Quick Wins Sistémicos (Esfuerzo total: ~4h)

| # | Tarea | Archivos | Esfuerzo | Impacto | Herramienta |
|---|-------|----------|:---:|:---:|---|
| 0.1 | **Batch replace tokens legacy en 101 SKILL.md** | 101 archivos | M | Crítico | Script bash (sed/find) |
| 0.2 | **Batch replace tokens legacy en ~100 sample-output.html** | ~100 archivos | M | Alto | Script bash |
| 0.3 | **Corregir tokens Mermaid en pipeline-orchestration.md** | 1 archivo | S | Bajo | Edit manual |
| 0.4 | **Actualizar skills-catalog.md**: 108 → 111 | 1 archivo | S | Medio | Edit manual |
| 0.5 | **Actualizar CLAUDE.md** si conteo inconsistente | 1 archivo | S | Bajo | Edit manual |

**Resultado esperado**: Zero tokens legacy en SKILL.md. Catálogo refleja 111 skills. Pipeline diagram con colores correctos.

**Verificación**:
```bash
grep -rl '#6366F1\|#0F172A\|Montserrat' skills/*/SKILL.md | wc -l  # → 0
```

---

## Sprint 1: Frontmatter Standardization (Esfuerzo total: ~4h)

| # | Tarea | Archivos | Esfuerzo | Impacto | Herramienta |
|---|-------|----------|:---:|:---:|---|
| 1.1 | **Identificar skills sin model/context** en frontmatter | — | S | — | Grep |
| 1.2 | **Agregar model: opus + context: fork** a skills que no los tienen | ~40 archivos | M | Alto | surgeon-skill o script |
| 1.3 | **Migrar frontmatter batch** (quitar version/license/category/tags, agregar argument-hint) | ~67 archivos | M | Medio | surgeon-skill o script |
| 1.4 | **Agregar author field** donde falta (ej: input-analysis) | ~5 archivos | S | Bajo | Edit manual |

**Resultado esperado**: Todas las skills tienen frontmatter gold-standard uniforme.

**Verificación**:
```bash
grep -rL 'model:' skills/*/SKILL.md | wc -l  # → 0
grep -rL 'context:' skills/*/SKILL.md | wc -l  # → 0
```

---

## Sprint 2: Skills Palanca (Esfuerzo total: ~6h)

| # | Tarea | Skill | Esfuerzo | Impacto |
|---|-------|-------|:---:|:---:|
| 2.1 | **Actualizar catálogo interno** de discovery-orchestrator (59 → 111) | discovery-orchestrator | M | Alto |
| 2.2 | **Renombrar "Guiding Principle" → "Grounding Guideline"** en output-engineering | output-engineering | S | Medio |
| 2.3 | **Agregar Validation Protocol** en design-system-brand | design-system-brand | S | Medio |
| 2.4 | **Agregar Grounding Guideline + frontmatter** en input-analysis | input-analysis | S | Medio |
| 2.5 | **Crear evals/** para las 5 skills palanca | 5 skills | L | Alto |
| 2.6 | **Verificar y limpiar sample-output.html** de las 5 skills palanca | 5 archivos | M | Medio |

**Resultado esperado**: 5 skills palanca a score ≥ 92. Evals presentes.

---

## Sprint 3: Ontología Sync (Esfuerzo total: ~2h)

| # | Tarea | Archivos | Esfuerzo | Impacto |
|---|-------|----------|:---:|:---:|
| 3.1 | **Reconciliar skills-catalog.md** con directorio real | 1 archivo | M | Medio |
| 3.2 | **Identificar las 3 skills no documentadas** en catálogo | — | S | Medio |
| 3.3 | **Actualizar agent-committee.md** si hay inconsistencias | 1 archivo | S | Bajo |
| 3.4 | **Verificar commands-reference.md** contra directorio commands/ | 1 archivo | S | Bajo |

**Resultado esperado**: Ontología refleja estado real del repositorio.

---

## Sprint 4: Batch Elevation — Arquitectura (Esfuerzo total: ~8h)

| # | Tarea | Skills | Esfuerzo | Impacto |
|---|-------|--------|:---:|:---:|
| 4.1 | **Upgrade 7 skills batch de Arquitectura** a gold-standard | database-architecture, devsecops-architecture, documentation-architecture, event-architecture, infrastructure-architecture, integration-architecture, security-architecture | L | Alto |

**Método**: Para cada skill: (1) x-ray-skill, (2) surgeon-skill con spec de Grupo C, (3) certify-skill.

---

## Sprint 5: Batch Elevation — Calidad & Ops (Esfuerzo total: ~8h)

| # | Tarea | Skills | Esfuerzo | Impacto |
|---|-------|--------|:---:|:---:|
| 5.1 | **Upgrade 9 skills batch de Calidad & Ops** | compliance-assessment, incident-management, onboarding-playbook, performance-engineering, pipeline-governance, quality-engineering, release-strategy, sla-design, vendor-assessment | L | Alto |

---

## Sprint 6: Batch Elevation — Service Discovery + Gestión (Esfuerzo total: ~8h)

| # | Tarea | Skills | Esfuerzo | Impacto |
|---|-------|--------|:---:|:---:|
| 6.1 | **Upgrade 9 skills batch de Service Discovery** | cloud-service-discovery, digital-transformation-discovery, management-discovery, mobile-assessment, mobile-platform-assessment, qa-service-discovery, staff-augmentation-discovery, user-representative, ux-design-discovery | L | Medio |
| 6.2 | **Upgrade 7 skills batch de Gestión & Estrategia** | competitive-intelligence, execution-burndown, governance-framework, product-strategy, project-program-management, risk-controlling-dynamics, sector-intelligence | L | Medio |

---

## Sprint 7: Batch Elevation — Resto (Esfuerzo total: ~8h)

| # | Tarea | Skills | Esfuerzo | Impacto |
|---|-------|--------|:---:|:---:|
| 7.1 | **Upgrade skills batch de Data** | data-mesh-strategy, data-quality, data-science-architecture, data-storytelling, data-viz-storytelling | M | Medio |
| 7.2 | **Upgrade skills batch de Cloud & Platform** | capacity-planning, disaster-recovery, finops, sustainability-assessment | M | Medio |
| 7.3 | **Upgrade skills batch de Editorial, Cambio, Innovación, DX** | copywriting, functional-toolbelt, technical-writing, ux-writing, mentoring-training-discovery, workshop-facilitator, hypothesis-driven-development, migration-playbook, roadmap-poc, technology-vigilance, cli-init, developer-experience, mini-apps-discovery, team-topology | L | Medio |

---

## Sprint 8: Evals & Regression (Esfuerzo total: ~8h)

| # | Tarea | Archivos | Esfuerzo | Impacto |
|---|-------|----------|:---:|:---:|
| 8.1 | **Crear template de eval reutilizable** | 1 template | M | Alto |
| 8.2 | **Crear evals para 10 skills más usadas** | 10 evals | L | Alto |
| 8.3 | **Verificación final**: grep tokens legacy = 0 en todo el framework | — | S | Crítico |
| 8.4 | **Regenerar HTML samples** con tokens correctos para skills palanca | 5 archivos | M | Medio |

---

## Resumen de Sprints

| Sprint | Foco | Esfuerzo | Skills Impactadas | Dependencias |
|--------|------|:---:|:---:|---|
| **0** | Quick wins sistémicos | ~4h | 111 | Ninguna |
| **1** | Frontmatter | ~4h | ~67 | Sprint 0 |
| **2** | Skills palanca | ~6h | 5 | Sprint 0+1 |
| **3** | Ontología | ~2h | N/A | Sprint 0 |
| **4** | Batch: Arquitectura | ~8h | 7 | Sprint 0+1+2 |
| **5** | Batch: Calidad & Ops | ~8h | 9 | Sprint 0+1+2 |
| **6** | Batch: Service + Gestión | ~8h | 16 | Sprint 0+1+2 |
| **7** | Batch: Resto | ~8h | 14 | Sprint 0+1+2 |
| **8** | Evals & Regression | ~8h | 15 | Todos |
| **Total** | | **~56h** | **111 skills** | |

---

## Orden de Ejecución Recomendado

```
Sprint 0 ──→ Sprint 1 ──→ Sprint 2
                │              │
                ├── Sprint 3   │
                │              │
                └──────────────┼──→ Sprint 4 ──→ Sprint 5 ──→ Sprint 6 ──→ Sprint 7
                               │
                               └──→ Sprint 8 (después de todos)
```

Sprint 0 y 3 pueden ejecutarse en paralelo.
Sprints 4-7 pueden ejecutarse en cualquier orden después de Sprint 2.
Sprint 8 es el último.

---

*Entregable 06 de 07 — Auditoría MAO v1.4*
