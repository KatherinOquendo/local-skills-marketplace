---
name: context-optimization
description: Optimización del context window mediante lazy loading de agentes, pruning semántico del changelog y vectorización selectiva de la ontología.
author: Javier Montano · Comunidad MetodologIA
argument-hint: "[phase-number] [tipo-servicio]"
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

# context-optimization

> Optimización del context window y carga dinámica de skills/agentes.
> Reduce consumo de tokens, mejora precisión en fases avanzadas del pipeline.

## Grounding Guideline

> *A saturated context window produces degraded responses. Context optimization is not optional — it is a quality prerequisite.*

1. **Load what is needed, not what is available.** Lazy loading by phase and service type is the base strategy.
2. **Compress without losing decisions.** Changelog pruning must preserve critical decisions and discard noise.
3. **Measure before optimizing.** Without per-phase token usage metrics, optimization is blind.

---

## TL;DR

Con múltiples agentes, 101+ skills y 20+ archivos de RAG-priming, el contexto se satura rápidamente. Este skill implementa tres estrategias: lazy loading de agentes por fase, pruning semántico del changelog, y vectorización selectiva de la ontología.

---

## Core Responsibilities

1. **Lazy Loading** — Solo cargar agentes y skills relevantes a la fase actual y `{TIPO_SERVICIO}` detectado
2. **Semantic Pruning** — Comprimir `session-changelog.md` cuando supera 150 líneas, preservando decisiones críticas
3. **Selective Vectorization** — Consultar `references/ontology/` dinámicamente según necesidad, no inyectar todo al inicio

---

## Assigned Skills

| Skill | Rol |
|-------|-----|
| `context-optimization` (self) | Estrategia de optimización de context window |
| `discovery-orchestrator` | Integración con conductor para lazy loading |
| `pipeline-governance` | Validación de que la optimización no omite assets críticos |

---

## Output Configuration

### Output Artifact

**Nombre**: `{fase}_Context_Optimization_{cliente}_{WIP|Aprobado}.md`

### Output Templates

| Formato | Especificación |
|---------|---------------|
| **Markdown** | Reporte de optimización: tokens antes/después, agentes cargados vs total, changelog lines comprimidas. Ghost menu. |
| **HTML** | Self-contained con tokens canónicos MetodologIA (#122562, #1F2833). Gráficas de uso de contexto. WCAG AA. |
| **DOCX** | python-docx. Heading 1 = Poppins 700 #122562. Tabla comparativa de contexto por fase. Header con logo MetodologIA. |
| **XLSX** | openpyxl. Hojas: "Context Budget", "Agent Loading Matrix", "Pruning Log". Header navy #122562. |
| **PPTX** | python-pptx. Max 10 slides. Slide master navy. Gráfica de optimización. Speaker notes con métricas. |

---

## Escalation Triggers

- Context window > 80% de capacidad en fase temprana (0-2) → Activar pruning inmediato
- Lazy loader no encuentra agents para una fase → Escalar a `discovery-conductor`
- Changelog con > 300 líneas post-pruning → Escalación manual para revisión

---

## Scripts

| Script | Ubicación | Propósito |
|--------|-----------|----------|
| `context-prune.sh` | `scripts/context-prune.sh` | Pruning semántico del changelog |
| `lazy-load-resolver.sh` | `scripts/lazy-load-resolver.sh` | Resolver agentes/skills por fase y tipo |
