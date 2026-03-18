# Changelog — Registro de Cambios de la Red de Orquestación

## Formato

```markdown
### [{fecha ISO}] {versión} — {título}
**Archivos**: {lista de archivos creados/modificados/eliminados}
**Impacto**: {alto|medio|bajo} — {descripción de impacto}
**Razón**: {por qué se hizo el cambio}
```

---

## Registro

### [2026-03-16] v1.0.0 — Red de Orquestación Inicial

**Archivos creados**:
- `~/.claude/CLAUDE.md` — Reescrito como hub lean (132 → 46 líneas, -65%)
- `orchestration/meta-orchestrator.md` — Composición Tier 0/1/2, spawning, handoff
- `orchestration/input-amplifier.md` — 3-pass silencioso, escalación a input-analysis
- `orchestration/metacognition-protocol.md` — Structured Reasoning, Plan Mode, Demand Elegance
- `orchestration/auto-calibration.md` — Estado COLD→DEEP, lazy-load integration
- `orchestration/rag-priming-engine.md` — Auto-conversión de inputs a priming-rag-*.md
- `orchestration/workflow-discipline.md` — 8 patrones + Build Practices + Core Principles
- `orchestration/plugin-router.md` — Detección, registry, cheat sheets SDF/MAO/PM
- `orchestration/excellence-standards.md` — Formato, branding 4 marcas, naming
- `orchestration/self-improvement.md` — Correcciones, anti-patrones, propagación

**Archivos modificados**:
- `~/skills/plugins/CLAUDE.md` — Agregada referencia a orchestration network

**Impacto**: alto — Transformación completa de monolito a red federada
**Razón**: Convertir CLAUDE.md en comité permanente de meta-orquestación con metacognición, amplificación de inputs, auto-calibración, RAG-priming, y disciplina de workflow

### [2026-03-16] v1.1.0 — Changelog, Tasklog, Index-of-Indexes

**Archivos creados**:
- `orchestration/changelog.md` — Este archivo. Registro de cambios de la red.
- `orchestration/tasklog.md` — Registro de tareas y progreso cross-sesión.
- `orchestration/index-of-indexes.md` — Mapa maestro de repos, archivos, ontologías.

**Impacto**: medio — Trazabilidad y navegación mejoradas
**Razón**: El usuario necesita tracking de cambios, tareas, y un mapa completo de paths

### [2026-03-16] v1.2.0 — Preferences Log + Conversation Log

**Archivos creados**:
- `orchestration/preferences-log.md` — Registro de preferencias del usuario (workflow, output, tooling, communication, design)
- `orchestration/conversation-log.md` — Registro ejecutivo de conversaciones (decisiones, outcomes, pendientes)

**Archivos modificados**:
- `~/.claude/CLAUDE.md` — Agregadas 2 filas al network index
- `orchestration/index-of-indexes.md` — Agregados 2 nuevos archivos
- `orchestration/changelog.md` — Esta entrada

**Impacto**: medio — Persistencia de preferencias y continuidad conversacional
**Razón**: El usuario necesita que se capturen preferencias y resúmenes de conversación para continuidad cross-sesión
