# Self-Improvement — Mejora Continua y Lecciones Aprendidas

## Protocolo de Procesamiento de Correcciones

Cuando el usuario corrige algo:

1. **Reconocer** — Aceptar sin defensividad, agradecer la corrección
2. **Categorizar**:
   - **Formato**: estilo, branding, naming, estructura de output
   - **Contenido**: datos incorrectos, análisis erróneo, conclusión equivocada
   - **Proceso**: orden incorrecto, paso omitido, herramienta mal usada
   - **Tono**: lenguaje inapropiado, nivel de detalle incorrecto, audiencia mal calibrada
3. **Rutear actualización**:
   - Si es específico del dominio → actualizar `{plugin}/references/ontology/lessons-learned.md`
   - Si es cross-cutting (aplica a todos los plugins) → actualizar este archivo (sección Global Lessons)
   - Si es sobre formato/branding → verificar contra `excellence-standards.md` y actualizar si necesario
4. **Formalizar regla** — Si la corrección revela un patrón, escribir regla explícita
5. **Verificar no-repetición** — En la próxima acción similar, aplicar la lección

## Formato de Lección

```markdown
### [{fecha ISO}] {título descriptivo}
**Categoría**: formato | contenido | proceso | tono
**Contexto**: {qué se estaba haciendo}
**Corrección**: {qué dijo el usuario}
**Regla**: {regla formalizada para el futuro}
```

## Global Lessons (Cross-Plugin)

_Las lecciones se acumulan aquí conforme se reciben correcciones cross-cutting._

### [2026-03-16] File naming tags obligatorios
**Categoría**: formato
**Contexto**: Generación de archivos de entregables
**Corrección**: Usuario requiere `{WIP}` y `{Aprobado}` en nombres de archivos
**Regla**: Todo archivo generado lleva tag de estado en el nombre

## Anti-Patterns (Comportamientos Rechazados)

_Se acumulan conforme se identifican._

- NUNCA resumir lo que acabas de hacer al final de cada respuesta (el usuario lee el diff)
- NUNCA mezclar colores de marca en un mismo output
- NUNCA presentar inferencias como hechos sin evidence tag
- NUNCA agregar docstrings, comments o type annotations a código que no se modificó
- NUNCA over-engineer — no agregar abstracciones prematuras

## Propagación Cross-Plugin

Si una lección aprendida en SDF aplica a MAO o PM-APEX:

1. Escribir la lección en el plugin donde ocurrió
2. Evaluar: ¿es universal? (formato, tono, proceso general)
3. Si SÍ → agregar también a Global Lessons (arriba)
4. Si NO → dejar solo en el plugin específico

## Revisión al Inicio de Sesión

Al comenzar cada conversación:

1. Leer `~/.claude/orchestration/self-improvement.md` (este archivo) — Global lessons
2. Leer `{plugin-activo}/references/ontology/lessons-learned.md` — Plugin lessons
3. Leer `~/.claude/projects/{project}/memory/` — Memory files relevantes
4. Aplicar todas las lecciones activas durante la sesión
