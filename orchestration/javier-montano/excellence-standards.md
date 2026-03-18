# Excellence Standards — Formato, Branding y Nomenclatura

## Formato Markdown-Excellence

Todo output sigue el estándar Markdown-Excellence:

- **TL;DR** al inicio de cada sección significativa (3-5 bullets)
- **Prosa densa** — sin filler, cada oración aporta información
- **Tablas** para datos estructurados (preferir sobre listas cuando hay 2+ dimensiones)
- **Mermaid** para diagramas (max 20 nodos, IDs descriptivos, edges etiquetados)
- **Callouts** para advertencias, notas, decisiones (`> **⚠️ ADVERTENCIA**:`)
- **Evidence tags** en toda afirmación: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`
- **Cross-references** entre entregables cuando aplique
- **Ghost menu** en entregables importantes (fase activa, progreso, navegación)

## Idioma

- **Default**: Español (Latinoamericano, registro empresarial)
- **Tono**: Directo, claro, conciso. Sin jerga académica sin explicar.
- **Código/config**: En inglés (convención técnica estándar)
- **Cambio de idioma**: Solo si el usuario lo solicita explícitamente

## File Naming

**Tags de estado**:
- `{WIP}` — Trabajo en progreso
- `{Aprobado}` — Versión final aprobada

**Patrón de slugging**:
```
{fase}_{entregable}_{contexto}_{WIP|Aprobado}.{ext}
```
Ejemplo: `03_ASIS_Bancoomeva_{WIP}.md`

## Naming Conventions

| Asset | Patrón | Autor |
|-------|--------|-------|
| Skills Sofka | `sofka-{domain}` | `author: Equipo PreSales Sofka` |
| Skills MetodologIA | `metodologia-{domain}` | `author: MetodologIA Community` |
| Agents | `{brand}-{role}` | `co-authored-by: Javier Montaño (with Claude Code)` |
| Commands | `{verb}-{context}` | Verbos: run, generate, diagnose, trace, evaluate, validate, chart, write, craft, deliver, present, report, review, discover, assess, audit, improve, rescue |
| Packages | `{brand}-{name}.skill` (ZIP) | Incluye SKILL.md + references/ + prompts/ + examples/ |

## Branding Rules

| Brand | License | Primary | Background | Success | Key Rule |
|-------|---------|---------|------------|---------|----------|
| **Sofka** | All Rights Reserved | #FF7E08 (orange) | #EFEAE4 (beige) | #FFD700 (gold) | NUNCA verde para success |
| **MetodologIA** | GPL-3.0 Copyleft | #6366F1 (indigo) | #0F172A (dark) | #10B981 (emerald) | Open, community, copyleft |
| **APEX** | All Rights Reserved | #2563EB (royal blue) | #0F172A (dark) | #F59E0B (amber) | NUNCA verde para success |
| **JM Labs** | Personal | #14B8A6 (teal) | #F0FDFA (teal wash) | #22D3EE (cyan) | Innovation, experiments |

### Brand Isolation Rule (HARD)
- **NUNCA** mezclar colores, logos o tono de marcas en el mismo output
- Identificar contexto de marca PRIMERO antes de generar cualquier output
- Si el contexto cambia mid-conversation → reconocer explícitamente
- Cada marca tiene su propio design system, tono y templates

Para tokens CSS detallados → referir `{plugin}/references/ontology/canonical-tokens.md`
Para orquestación multi-marca → referir `{plugin}/references/ontology/brand-orchestration.md`

## Output Defaults

- **Formato**: Markdown-first (markdown-excellence standard)
- **Diagramas**: Mermaid embebido en markdown
- **Archivos**: Guardar outputs como archivos, NO inline
- **HTML/DOCX/XLSX**: Solo cuando se solicite explícitamente
- **Excellence Loop**: Rúbrica de 10 criterios en cada entregable
- **Cost outputs**: Solo drivers y magnitudes. NUNCA precios, tarifas ni montos en moneda.

## Token Efficiency

Para maximizar efectividad y uso de tokens:

- **Tablas > prosa** para datos estructurados
- **Mermaid > ASCII art** para diagramas
- **Bullets > párrafos** para listas de items
- **Frontmatter YAML** para metadata (parseable, compacto)
- **NO repetir** información disponible en sub-archivos — referenciar
- **Comprimir changelogs** > 150 líneas (via `context-prune.sh`)
- **Lazy-load** skills a L1 por default, L2/L3 solo cuando se necesite
