# Meta-Orchestrator — Comité Permanente de Orquestación

## Arquitectura de Dos Niveles

```
Tier 0 (Global)  ~/.claude/CLAUDE.md → orchestration/*.md
    ↓ detecta contexto, amplifica input, aplica metacognición
Tier 1 (Plugin)  {plugin}/CLAUDE.md → references/ontology/*.md
    ↓ activa conductor (discovery-conductor, pm-conductor)
Tier 2 (Skill)   {plugin}/skills/{skill}/SKILL.md → agents/ + references/ + prompts/
```

**Flujo estricto top-down. NUNCA referencias circulares.**

## Protocolo de Composición

El meta-orchestrator NO ejecuta análisis. Su rol es:

1. **Detectar contexto** → activar plugin correcto (via `plugin-router.md`)
2. **Amplificar input** → reinterpretar intención del usuario (via `input-amplifier.md`)
3. **Aplicar metacognición** → razonamiento estructurado (via `metacognition-protocol.md`)
4. **Delegar al conductor del plugin** → handoff completo al pipeline del plugin
5. **Supervisar calidad** → branding, formato, evidence tags (via `excellence-standards.md`)

Una vez el conductor del plugin (ej. `discovery-conductor`) toma control:
- El meta-orchestrator **se retira** de decisiones de dominio
- Mantiene supervisión SOLO de: branding, formato, hard rules globales
- El conductor del plugin decide: fases, gates, agentes, skills, entregables

## Spawning de Subagentes

| Condición | Acción |
|-----------|--------|
| Tarea aislada, archivo específico | 0 subagentes — ejecutar directamente |
| Exploración de codebase incierta | 1-3 subagentes Explore en paralelo |
| Análisis multi-dominio independiente | 1 subagente por dominio (max 3 paralelos) |
| Diseño de implementación | 1 subagente Plan |
| Ejecución heavy (discovery pipeline) | Delegar a conductor de plugin |

**Reglas de spawning**:
- Mandato claro: cada subagente recibe objetivo, inputs, formato de output esperado
- 1 tarea por subagente — nunca multi-tarea
- Max 3 subagentes paralelos por turno
- Nunca duplicar trabajo: si delegas, no ejecutes tú también

## Invocación Recursiva

Skills pueden invocar sub-agentes, que pueden invocar sub-skills. Guard rails:

- **Profundidad máxima**: 3 niveles (skill → sub-agente → sub-skill)
- **Declarar la cadena**: al invocar recursivamente, log the chain (ej. "asis-analysis → code-archaeologist → debt-classifier")
- **Nunca loop**: si un skill intenta invocarse a sí mismo, ABORT

## Resolución de Conflictos

| Dimensión | Gana |
|-----------|------|
| Branding, colores, tono | Global (excellence-standards.md) |
| Formato de output | Global (excellence-standards.md) |
| Evidence tags | Global (hard rule #1) |
| Metodología de dominio | Plugin (ontology del plugin) |
| Selección de agentes/skills | Plugin conductor |
| Fases y gates del pipeline | Plugin conductor |
| Nomenclatura de entregables | Plugin (output-standards.md del plugin) |

## Protocolo de Handoff

```
Meta-orchestrator activo:
  1. Input recibido
  2. Amplificación (input-amplifier.md)
  3. Detección de contexto (plugin-router.md)
  4. Metacognición aplicada (plan mode si 3+ pasos)

Handoff al plugin:
  5. Leer plugin CLAUDE.md
  6. Conductor del plugin toma control
  7. Meta-orchestrator entra en modo supervisión

Meta-orchestrator en supervisión:
  - Valida branding en cada output
  - Valida evidence tags presentes
  - Captura correcciones → self-improvement.md
  - NO interfiere en decisiones de pipeline
```

## Extensibilidad

Para agregar un nuevo plugin (ej. JM Labs):
1. Crear directorio del framework en `~/skills/plugins/jm-labs-framework/`
2. Agregar fila en `plugin-router.md` (registry table)
3. Crear `CLAUDE.md` del plugin con ontology propia
4. El meta-orchestrator lo detectará automáticamente via context detection
