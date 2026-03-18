# Workflow Discipline — Patrones de Ejecución y Principios Fundamentales

## 1. Plan Mode Default

Para CUALQUIER tarea no-trivial (3+ pasos o decisiones arquitectónicas):

1. **Descomponer** — Listar pasos antes de ejecutar
2. **Validar plan** — Verificar que el plan cubre los requisitos del usuario
3. **Ejecutar paso a paso** — Marcar cada paso como completado
4. **Si algo sale mal** → STOP. Replantear. NO empujar hacia adelante con hacks
5. **Plan mode para verificación** — No solo para building, también para validar

**Excepciones** (ejecutar directo): typo fixes, lecturas de archivo, respuestas informativas cortas, cambios de 1 línea.

## 2. Subagent Strategy

- Usar subagentes **liberalmente** para mantener contexto principal limpio
- Offload investigación, exploración y análisis paralelo a subagentes
- Para problemas complejos, lanzar más compute via subagentes
- **1 tarea por subagente** — mandato enfocado

| Tipo | Cuándo |
|------|--------|
| Explore | Búsqueda abierta en codebase, entender patrones |
| Plan | Diseñar estrategia de implementación |
| General-purpose | Investigación multi-paso, búsqueda + análisis |

**Reglas**:
- Nunca duplicar trabajo: si delegas a subagente, NO hagas la misma búsqueda tú
- Máximo 3 subagentes paralelos por turno
- Proveer contexto suficiente para que trabajen autónomamente
- Esperar resultado antes de actuar sobre el output

## 3. Self-Improvement Loop

Después de CUALQUIER corrección del usuario:

1. **Reconocer** — Aceptar la corrección sin defensividad
2. **Actualizar `lessons-learned.md`** del plugin activo (formato: Contexto, Aprendizaje, Acción)
3. **Si es patrón cross-plugin** → actualizar `orchestration/self-improvement.md` también
4. **Escribir regla** — Si la corrección revela un patrón, formalizarla
5. **Iterar implacablemente** — Reducir tasa de errores cada sesión

> Revisar lessons-learned al inicio de cada sesión para no repetir errores.

## 4. Verification Before Done

NUNCA marcar tarea completa sin demostrar que funciona:

- **Código**: diff entre antes/después, tests pasan, output esperado
- **Archivos**: leer archivo creado para confirmar contenido
- **Configuración**: verificar que el sistema responde correctamente
- **Entregables**: checklist de criterios del skill cumplidos
- **Bug fix**: reproducir error antes, verificar ausencia después

> Preguntarte: "¿Un ingeniero staff aprobaría esto?" — Si no es SÍ claro, revisar.

## 5. Demand Elegance (Balanced)

Para cambios no-triviales, pausar y preguntar:

> "¿Existe una forma más elegante?"

Pero balanceado:
- **Trivial** (< 3 pasos): ejecutar directo, no buscar elegancia
- **Si se siente hacky**: "Sabiendo todo lo que sé ahora, implementar la solución elegante"
- **NUNCA over-engineer** — La cantidad correcta de complejidad es el MÍNIMO necesario
- Cuestionar tu propio trabajo antes de presentar

## 6. Autonomous Bug Fixing

Cuando encuentres un bug:

1. **Solo arréglalo** — No pidas permiso, no pidas hand-holding
2. **Apunta a logs, errores, tests fallidos** — luego resuélvelos
3. **Zero context switching del usuario** — El usuario no debería tener que pensar en tu bug
4. **Arregla tests de CI que fallen** sin que te lo pidan
5. **Escalar SOLO si**: el fix requiere decisión de diseño o cambia comportamiento visible

## 7. Task Management

1. **Plan First** — Escribir plan con items verificables
2. **Verify Plans** — Verificar con usuario antes de implementar
3. **Track Progress** — Marcar items completados conforme avanzas
4. **Explain Changes** — Resumen de alto nivel en cada milestone
5. **Document Results** — Agregar sección de review al plan
6. **Capture Lessons** — Actualizar `lessons-learned.md` ante correcciones

## 8. Core Principles

### Simplicity First
- Hacer cada cambio lo más simple posible
- Impacto mínimo en código existente
- Senior developer standards — código limpio, directo, legible

### No Laziness
- Encontrar root causes. No temporary fixes.
- Completar cada paso al 100%
- No atajos que dejen trabajo pendiente

### Minimal Impact
- Los cambios solo tocan lo necesario
- No introducir bugs nuevos
- No refactorear código que no fue pedido
- No agregar features, docstrings, o "mejoras" más allá de lo solicitado

## Prácticas Heredadas (del Build Practices original)

1. **Read before write** — SIEMPRE leer archivos antes de modificar
2. **Parallel when independent** — Lanzar múltiples herramientas/agentes para tareas independientes
3. **Sub-agents for heavy work** — Fork agentes especializados, mantener orchestrator ligero
4. **Tool restrictions** — Respetar `allowed-tools` en frontmatter de skills
5. **Cost outputs** — Solo drivers y magnitudes, NUNCA precios
6. **Evidence tags** — [CÓDIGO], [CONFIG], [DOC], [INFERENCIA], [SUPUESTO]
7. **Ontology-first** — Consultar `references/ontology/` para contexto profundo
