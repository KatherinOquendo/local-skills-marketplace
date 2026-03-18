# Conversation Log — Registro General de Conversaciones

## Protocolo

Registrar el **resumen ejecutivo** de cada conversación significativa. NO transcribir — solo capturar decisiones, outcomes, y contexto para continuidad cross-sesión.

### Cuándo Registrar
- Al final de cada conversación que produzca cambios significativos
- Cuando se tomen decisiones arquitectónicas
- Cuando se completen hitos de proyecto
- Cuando se identifique contexto que futuras sesiones necesitarán

### Formato

```markdown
### [{fecha ISO}] {título} — {plugin/contexto}
**Duración**: {aprox}
**Objetivo**: {qué se pidió}
**Outcome**: {qué se logró}
**Decisiones clave**: {lista}
**Archivos modificados**: {lista de paths principales}
**Pendientes**: {si quedó algo abierto}
**Contexto para siguiente sesión**: {qué necesita saber la próxima conversación}
```

---

## Registro

### [2026-03-16] Red de Orquestación Meta-Cognitiva — Global

**Objetivo**: Transformar `~/.claude/CLAUDE.md` monolítico en red federada de archivos de orquestación con metacognición, input amplification, auto-calibración, RAG priming, workflow discipline.

**Outcome**:
- Hub reescrito: 132 → 50 líneas (-62%)
- 12 archivos de orquestación creados en `~/.claude/orchestration/`
- Project CLAUDE.md actualizado con referencia

**Decisiones clave**:
- Arquitectura Two-Tier: Global (Tier 0) → Plugin (Tier 1) → Skill (Tier 2)
- Flujo top-down estricto, nunca referencias circulares
- Input amplifier como reasoning protocol (no skill visible)
- Lazy-load on-demand: NUNCA cargar todos los sub-archivos a la vez
- 8 patrones de workflow del screenshot integrados en workflow-discipline.md
- 4 marcas en branding: Sofka, MetodologIA, APEX, JM Labs

**Archivos creados**:
- `~/.claude/orchestration/` (12 archivos: meta-orchestrator, input-amplifier, metacognition-protocol, auto-calibration, rag-priming-engine, workflow-discipline, plugin-router, excellence-standards, self-improvement, changelog, tasklog, index-of-indexes)

**Archivos modificados**:
- `~/.claude/CLAUDE.md` — Reescrito como hub lean
- `~/skills/plugins/CLAUDE.md` — Referencia a orchestration network

**Pendientes**:
- Validar cold start en sesión nueva
- Crear JM Labs framework
- Poblar self-improvement con lecciones existentes
- Auditar consistencia orchestration ↔ plugin ontologies
