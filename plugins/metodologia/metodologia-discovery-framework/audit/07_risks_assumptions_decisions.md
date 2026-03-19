# 07 — Riesgos, Supuestos y Decisiones

> Registro de riesgos, supuestos explícitos y decisiones de diseño observadas
> Fecha: 2026-03-19 | Auditor: Claude Code (Principal Skill Auditor)

---

## Riesgos Técnicos

| ID | Riesgo | Probabilidad | Impacto | Mitigación Sugerida |
|----|--------|:---:|:---:|-----|
| R01 | **Tokens legacy generan entregables con marca incorrecta** — 101/111 SKILL.md contienen #6366F1, #0F172A, Montserrat en output templates. Cada entregable generado por estas skills sale con marca prohibida. | Alta | Alto | Batch find-and-replace de tokens en 101 SKILL.md + HTML samples + references |
| R02 | **skills-catalog.md desactualizado** — Dice 108 skills pero hay 111. Los 3 faltantes no están documentados en la ontología. | Alta | Medio | Reconciliar catálogo con directorio real |
| R03 | **Pipeline Mermaid usa tokens legacy** — pipeline-orchestration.md tiene #22D3EE y #1A1A2E en el diagrama. | Alta | Bajo | Actualizar colores del Mermaid |
| R04 | **Sin evals/ en ninguna skill** — No hay forma de verificar automáticamente si una skill cumple estándares. | Alta | Alto | Crear evals/ al menos para skills palanca (5 skills) |
| R05 | **Frontmatter divergente** — Dos patrones incompatibles coexisten: gold-standard (model, context, argument-hint) vs batch (version, license, category, tags). Claude Code se comporta diferente con cada patrón. | Alta | Medio | Estandarizar frontmatter en todas las skills |
| R06 | **HTML samples propagan marca incorrecta** — ~100 sample-output.html en examples/ usan tokens legacy. Sirven como referencia visual incorrecta. | Alta | Medio | Regenerar HTML samples con tokens correctos |
| R07 | **plan.md v9.0 tiene fases incompletas** — Faltan fases 6 (prompts) y 7 (references). El plan activo podría conflictuar con la auditoría. | Media | Medio | Coordinar con plan existente, no duplicar esfuerzo |
| R08 | **Batch-generated skills podrían romperse si se modifican sin testing** — No hay evals ni tests para verificar que los cambios no degraden funcionalidad. | Media | Alto | Crear evals mínimos antes de batch-modify |
| R09 | **Lessons-learned.md siempre vacío** — Se llena por sesión y se resetea. Conocimiento acumulado se pierde entre sesiones. | Media | Medio | Persistir lecciones clave en un archivo no-efímero |
| R10 | **Hooks no validados en Windows** — Los scripts .sh usan sintaxis Unix. En entorno Windows (este repo) podrían fallar. | Media | Bajo | Verificar compatibilidad con Git Bash en Windows |

---

## Supuestos Explícitos de la Auditoría

| ID | Supuesto | Justificación | Impacto si incorrecto |
|----|----------|-------------|---------------------|
| S01 | Las skills con estructura idéntica al patrón batch-generated comparten los mismos problemas | 5 skills batch evaluadas en profundidad muestran patrón consistente | Podrían existir skills batch con calidad superior no detectada |
| S02 | Las 10 skills sin tokens legacy son las únicas limpias | Basado en grep exhaustivo de #6366F1, #0F172A, Montserrat | Podrían existir otros tokens legacy no buscados |
| S03 | El plan.md v9.0 es el plan de mejora vigente | Tiene fecha 2026-03-13 y estado "en progreso" | Podría haber sido abandonado o reemplazado |
| S04 | Las skills gold-standard fueron escritas manualmente y las batch-generated fueron auto-generadas | Inferido por la diferencia de profundidad y estilo | El autor podría tener un proceso diferente |
| S05 | El frontmatter con model/context es el patrón correcto (no version/license/category/tags) | Las skills más maduras usan model/context; es el patrón Anthropic estándar | Ambos patrones podrían ser válidos para diferentes propósitos |
| S06 | Los 111 directorios en skills/ son todos skills activas | Todos tienen SKILL.md | Algunas podrían ser deprecated o experimentales |
| S07 | La rúbrica de 8 dimensiones captura las diferencias de calidad relevantes | Basada en estándar Anthropic + necesidades observadas del framework | Podrían existir dimensiones no cubiertas |

---

## Decisiones de Diseño Observadas

| ID | Decisión | Contexto Observado | Evaluación |
|----|----------|-------------------|-----------|
| D01 | **Hub architecture en CLAUDE.md** — Archivo principal es un routing hub que delega a 13 sub-archivos | Reduce tamaño del CLAUDE.md a 217 líneas, escalable | Buena decisión. Mantenible y extensible. |
| D02 | **Scripts centralizados** (no por skill) | 19 scripts en scripts/ sirven a todo el framework | Apropiado para el volumen actual. Podría necesitar descentralización si crecen. |
| D03 | **Comité dinámico con 5 niveles** | 101 agentes organizados por urgencia/frecuencia de uso | Bien diseñado. El lazy-load-resolver.sh lo implementa correctamente. |
| D04 | **Progressive MOAT loading (L1/L2/L3)** | Optimización de context window con 3 niveles de carga | Excelente decisión para un framework con 111 skills. |
| D05 | **4 quality gates como hard stops** | G1, G1.5, G2, G3 con criterios explícitos y umbrales | Sólido. Criterios bien definidos en quality-gates.md. |
| D06 | **10 tipos de servicio con auto-detection** | Routing automático basado en artefactos detectados | Ambicioso y bien diseñado. Implementación consistente en skills gold-standard. |
| D07 | **Idioma interno en inglés, output en español** | Declarado en plan.md v9.0 como objetivo | Parcialmente implementado: skills gold-standard en inglés, batch-generated en español. |
| D08 | **Hook guard pattern** (active-plugin check) | Cada hook verifica que MAO es el plugin activo antes de ejecutar | Defensivo y correcto. Evita conflictos con otros plugins. |
| D09 | **brand-config-neoswiss.json como SSoT** | Un solo archivo JSON como fuente de verdad para todos los formatos | Buena decisión, pero 101 skills no lo respetan (usan tokens hardcodeados legacy). |
| D10 | **Tokens prohibidos declarados en CLAUDE.md** | Lista explícita de tokens legacy a no usar | Declaración correcta, enforcement inexistente. |

---

## Dependencias Externas

| Dependencia | Tipo | Riesgo |
|-------------|------|--------|
| Claude Code (Anthropic) | Entorno de ejecución | Bajo — framework diseñado para Claude Code |
| Git Bash (Windows) | Scripts .sh | Medio — scripts asumen Unix-like shell |
| Google Fonts (Poppins) | Tipografía HTML | Bajo — fallback system fonts definidos |
| python-docx, python-pptx, openpyxl | Generación DOCX/PPTX/XLSX | Medio — requiere Python instalado |
| Mermaid | Diagramas | Bajo — renderizado client-side |
| Playwright (MCP) | client-browser-audit | Medio — requiere MCP Playwright configurado |

---

## Vacíos Funcionales Detectados

| Vacío | Impacto | Recomendación |
|-------|---------|---------------|
| No hay skill de **evaluación de calidad** de skills (meta-skill) | No se puede evaluar calidad internamente | Usar x-ray-skill/certify-skill del IDE como palanca externa |
| No hay skill de **migración de tokens** | La limpieza de tokens legacy es manual | Crear script de migración batch |
| No hay **evals/** en ninguna skill | No hay verificación automatizada | Crear evals mínimos para skills palanca |
| No hay skill de **onboarding del framework** para nuevos usuarios | Curva de aprendizaje alta | cli-init cubre parcialmente; ampliar |
| No hay **changelog por skill** | No se sabe qué cambió en cada skill | El session-changelog es a nivel sesión, no skill |
| No hay **versionado por skill** | No se puede trackear evolución individual | Considerar versión en frontmatter |

---

*Entregable 07 de 07 — Auditoría MAO v1.4*
