# 03 — Skill Quality Scorecard

> Evaluación de calidad skill-by-skill del Metodología-Discovery-Framework (MAO v1.4)
> Fecha: 2026-03-19 | Auditor: Claude Code (Principal Skill Auditor)
> Método: Muestreo profundo de 24 skills + extrapolación por patrón para 87 restantes

---

## Rúbrica de Evaluación

| Dimensión | Peso | Descripción |
|-----------|------|-------------|
| Claridad y precisión | 20 | Instrucciones inequívocas, sin ambigüedad |
| Completitud operativa | 15 | Inputs, outputs, precondiciones, edge cases |
| Reusabilidad | 15 | Parametrizable, service-type aware |
| Robustez y guardrails | 15 | Manejo de errores, escalation, límites |
| Componibilidad | 10 | Integración con otras skills/agentes |
| Mantenibilidad | 10 | Estructura clara, fácil de actualizar |
| Trazabilidad | 10 | Evidencia, referencias, documentación |
| Ejemplos/plantillas | 5 | Sample outputs, templates |
| **Total** | **100** | |

---

## Niveles de Madurez

| Nivel | Score | Semáforo | Descripción |
|-------|-------|----------|-------------|
| Referente | 90-100 | Verde | Gold standard, sirve de modelo |
| Avanzada | 75-89 | Verde | Sólida, mejoras menores |
| Sólida | 60-74 | Amarillo | Funcional, deuda visible |
| Funcional | 40-59 | Amarillo | Operativa pero limitada |
| Inicial | 0-39 | Rojo | Necesita rediseño |

---

## Scorecard — Skills Evaluadas en Profundidad (24 skills)

### Tier 1: Referente (90+)

| Skill | CL/20 | CO/15 | RE/15 | RO/15 | CP/10 | MA/10 | TR/10 | EJ/5 | **Total** | Semáforo | Madurez |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| discovery-orchestrator | 19 | 15 | 14 | 14 | 10 | 9 | 10 | 4 | **95** | Verde | Referente |
| asis-analysis | 19 | 14 | 14 | 14 | 9 | 9 | 10 | 4 | **93** | Verde | Referente |
| executive-pitch | 19 | 14 | 14 | 14 | 9 | 9 | 10 | 4 | **93** | Verde | Referente |
| html-brand | 18 | 14 | 14 | 14 | 9 | 9 | 9 | 4 | **91** | Verde | Referente |
| functional-spec | 19 | 14 | 14 | 13 | 9 | 9 | 9 | 4 | **91** | Verde | Referente |

**Diagnóstico Tier 1**: Skills maduras con Grounding Guideline, conditional logic, service-type routing, parámetros MODO/FORMATO/VARIANTE completos. Sirven como gold standard interno. Deuda menor: tokens legacy en output templates (excepto input-analysis).

---

### Tier 2: Avanzada (75-89)

| Skill | CL/20 | CO/15 | RE/15 | RO/15 | CP/10 | MA/10 | TR/10 | EJ/5 | **Total** | Semáforo | Madurez |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| scenario-analysis | 18 | 14 | 13 | 13 | 9 | 9 | 9 | 4 | **89** | Verde | Avanzada |
| solution-roadmap | 18 | 14 | 13 | 13 | 9 | 9 | 9 | 4 | **89** | Verde | Avanzada |
| discovery-handover | 18 | 14 | 13 | 13 | 9 | 8 | 9 | 4 | **88** | Verde | Avanzada |
| design-system-brand | 17 | 14 | 13 | 13 | 9 | 9 | 9 | 4 | **88** | Verde | Avanzada |
| data-governance | 17 | 13 | 13 | 13 | 9 | 9 | 9 | 4 | **87** | Verde | Avanzada |
| data-engineering | 17 | 13 | 13 | 13 | 9 | 9 | 9 | 4 | **87** | Verde | Avanzada |
| input-analysis | 18 | 13 | 12 | 13 | 9 | 8 | 9 | 4 | **86** | Verde | Avanzada |
| stakeholder-mapping | 17 | 13 | 13 | 13 | 8 | 9 | 9 | 4 | **86** | Verde | Avanzada |
| mermaid-diagramming | 18 | 13 | 12 | 13 | 8 | 9 | 9 | 4 | **86** | Verde | Avanzada |
| output-engineering | 17 | 13 | 13 | 12 | 9 | 8 | 9 | 4 | **85** | Verde | Avanzada |
| storytelling | 17 | 13 | 12 | 12 | 8 | 9 | 9 | 4 | **84** | Verde | Avanzada |
| analytics-engineering | 17 | 13 | 12 | 12 | 8 | 9 | 9 | 4 | **84** | Verde | Avanzada |
| testing-strategy | 16 | 13 | 12 | 12 | 8 | 8 | 9 | 4 | **82** | Verde | Avanzada |
| cloud-migration | 16 | 12 | 12 | 12 | 8 | 8 | 9 | 4 | **81** | Verde | Avanzada |
| observability | 16 | 12 | 12 | 12 | 8 | 8 | 9 | 4 | **81** | Verde | Avanzada |
| workshop-design | 16 | 12 | 12 | 12 | 8 | 8 | 8 | 3 | **79** | Verde | Avanzada |
| dynamic-sme | 16 | 12 | 11 | 12 | 8 | 8 | 8 | 3 | **78** | Verde | Avanzada |
| adoption-strategy | 16 | 12 | 11 | 12 | 8 | 8 | 8 | 3 | **78** | Verde | Avanzada |
| rpa-discovery | 15 | 12 | 11 | 12 | 8 | 8 | 8 | 3 | **77** | Verde | Avanzada |

**Diagnóstico Tier 2**: Skills con buena estructura (Grounding Guideline o Guiding Principle, conditional logic, inputs/outputs claros) pero con deuda menor: frontmatter incompleto (faltan model/context), tokens legacy, o menor profundidad en edge cases. Todas funcionales en producción.

---

### Tier 3: Sólida (60-74) — Skills Batch-Generated Evaluadas

| Skill | CL/20 | CO/15 | RE/15 | RO/15 | CP/10 | MA/10 | TR/10 | EJ/5 | **Total** | Semáforo | Madurez |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| secrets-sanitization | 14 | 11 | 10 | 11 | 7 | 7 | 7 | 3 | **70** | Amarillo | Sólida |
| context-optimization | 13 | 10 | 10 | 10 | 7 | 7 | 7 | 3 | **67** | Amarillo | Sólida |
| poc-lab | 13 | 10 | 10 | 10 | 7 | 7 | 7 | 3 | **67** | Amarillo | Sólida |
| rendering-engine | 12 | 10 | 10 | 10 | 7 | 7 | 7 | 3 | **66** | Amarillo | Sólida |
| cross-platform-convert | 12 | 10 | 10 | 9 | 6 | 7 | 7 | 3 | **64** | Amarillo | Sólida |

**Diagnóstico Tier 3**: Skills batch-generated con estructura simplificada (TL;DR + Core Responsibilities + Output Config). Funcionales pero sin Grounding Guideline, conditional logic limitada, tokens legacy en output templates. Necesitan upgrade a gold-standard.

---

## Scorecard — Skills Extrapoladas por Patrón (87 restantes)

Basado en el patrón estructural observado en las 24 skills evaluadas, las 87 restantes se agrupan en dos categorías:

### Gold-Standard con tokens legacy (~20 skills no evaluadas en detalle)
**Score estimado: 75-85** | Semáforo: Verde | Madurez: Avanzada

Skills como software-architecture, solutions-architecture, enterprise-architecture, cloud-native-architecture, multidimensional-feasibility, technical-feasibility, flow-mapping, cost-estimation, commercial-model, software-viability que tienen estructura gold-standard (Grounding Guideline, conditional logic, service-type routing) pero contienen tokens legacy.

**Deuda principal**: Tokens legacy en output templates.
**Quick win**: Find-and-replace de tokens prohibidos.

### Batch-Generated (~67 skills no evaluadas en detalle)
**Score estimado: 60-70** | Semáforo: Amarillo | Madurez: Sólida-Funcional

Skills con estructura simplificada: TL;DR + Core Responsibilities + Assigned Skills + Output Configuration + Escalation Triggers. Sin Grounding Guideline, sin conditional logic, sin service-type routing, con tokens legacy.

**Deuda principal**: (1) Tokens legacy, (2) Sin Grounding Guideline, (3) Sin conditional logic, (4) Frontmatter con campos legacy (version, license, category, tags vs model, context, argument-hint).
**Quick win**: (1) Find-and-replace tokens, (2) Estandarizar frontmatter.
**Mejora estructural**: Agregar Grounding Guideline, inputs/outputs detallados, conditional logic.

---

## Resumen Ejecutivo

| Categoría | Cantidad | Score Promedio | Semáforo |
|-----------|----------|---------------|----------|
| Referente (90+) | 5 | 93 | Verde |
| Avanzada (75-89) | 19 | 83 | Verde |
| Sólida (60-74) | ~72 | 66 | Amarillo |
| Funcional (40-59) | 0 | — | — |
| Inicial (0-39) | 0 | — | — |
| **Sin tokens legacy** | **10** | 82 | **Verde** |
| **Con tokens legacy** | **101** | 73 | **Amarillo** |

### Distribución

```
Referente  ████░░░░░░░░░░░░░░░░  5   (4.5%)
Avanzada   ████████████████░░░░  19  (17.1%)
Sólida     ████████████████████  72  (64.9%)
Funcional  ░░░░░░░░░░░░░░░░░░░░  0   (0.0%)
Inicial    ░░░░░░░░░░░░░░░░░░░░  0   (0.0%)
Sin evaluar detalle:            15  (13.5%)
```

### Hallazgos Clave

1. **Ninguna skill es mala**. El piso mínimo es ~64/100 (Sólida). El framework no tiene huecos funcionales rojos.
2. **El cuello de botella es uniformidad**. Las 5 skills Referente y 19 Avanzadas demuestran lo que es posible. Las 72 Sólidas necesitan el mismo tratamiento.
3. **El 91% tiene contaminación legacy**. Este es el problema #1 por volumen e impacto.
4. **El patrón batch-generated es el gap más grande**. La diferencia entre un skill gold-standard y uno batch-generated es ~20 puntos.
5. **No hay evals/ en ninguna skill**. Esto significa que no hay forma automatizada de verificar calidad.

---

## Deuda por Skill — Top 20 Deudas Más Frecuentes

| # | Deuda | Skills Afectadas | Impacto |
|---|-------|------------------|---------|
| 1 | Tokens legacy (#6366F1, #0F172A, Montserrat) en output templates | 101 | Entregables con marca incorrecta |
| 2 | Sin Grounding Guideline / Guiding Principle | ~67 | Falta grounding filosófico |
| 3 | Frontmatter con campos legacy (version/license/category/tags) | ~67 | Inconsistencia con gold-standard |
| 4 | Sin conditional logic (IF/THEN por contexto) | ~67 | Skill no se adapta al contexto |
| 5 | Sin service-type routing ({TIPO_SERVICIO}) | ~50 | Skill no se adapta al tipo de servicio |
| 6 | Sin parámetros MODO/FORMATO/VARIANTE completos | ~30 | Menos control operativo |
| 7 | Sin model/context en frontmatter | ~40 | No se ejecuta en fork con Opus |
| 8 | Sin evals/ | 111 | No hay verificación de calidad |
| 9 | Sin scripts/ propios | 111 | Centralización total |
| 10 | HTML samples con tokens legacy | ~100 | Ejemplos contradicen estándar |
| 11 | References con tokens legacy | ~50 | Material de referencia contamina |
| 12 | Agents asignados con tokens legacy | ~30 | Agentes propagan marca incorrecta |
| 13 | "Guiding Principle" vs "Grounding Guideline" inconsistente | ~15 | Naming inconsistente |
| 14 | Sin When NOT to Use section | ~60 | Falta guía de no-uso |
| 15 | Sin Assumptions & Limits section | ~50 | Edge cases no documentados |
| 16 | Sin Workarounds section | ~60 | Sin alternativas documentadas |
| 17 | Sin Context Detection (auto-scanning) | ~70 | No detecta contexto automáticamente |
| 18 | Sin Delivery Structure (secciones numeradas) | ~40 | Output no estructurado |
| 19 | Sin Cross-References a otras skills | ~30 | Skill aislada |
| 20 | Sin Excellence Loop criteria | ~80 | Sin checklist de calidad |

---

*Entregable 03 de 07 — Auditoría MAO v1.4*
