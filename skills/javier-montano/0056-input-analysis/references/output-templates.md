# Output Templates — Input Analysis

> **Skill:** input-analysis | **Framework:** MetodologIA Discovery Framework

---

## Formatos disponibles

| Formato | Nombre | Contenido |
|---|---|---|
| **Markdown** | `Input_Analysis_{timestamp}.md` | Analisis completo: input original, confianza, pases ejecutados, correcciones de superficie, causa raiz, impacto, brechas de intencion y prompt reformulado con objetivo, contexto, intencion, restricciones y calibracion. |
| **DOCX** | `Input_Analysis_Report_{timestamp}.docx` | Reporte formal de analisis para documentar decisiones de interpretacion en contexto de discovery; util cuando el input ambiguo requiere trazabilidad de la reformulacion. |
| **HTML** | `Input_Analysis_{timestamp}_{WIP}.html` | Mismo contenido en HTML branded (Design System MetodologIA v5). Self-contained, WCAG AA, responsive. Light-First Technical. Incluye tabla de correcciones de superficie con indicador de confianza, cadena de 5 Porques colapsable, y prompt reformulado resaltado. |
| **XLSX** | `{fase}_{entregable}_{cliente}_{WIP}.xlsx` | Generado con openpyxl bajo MetodologIA Design System v5. Headers con fondo navy y tipografia Poppins blanca, formato condicional, auto-filtros activados, valores sin formulas. Hojas: Correcciones de Superficie, Analisis de Causa Raiz, Impacto, Brechas de Intencion, Prompt Reformulado. |
| **PPTX** | `{fase}_{entregable}_{cliente}_{WIP}.pptx` | Generado con python-pptx bajo MetodologIA Design System v5. Slide master con degradado navy, titulos Poppins, cuerpo Trebuchet MS, acentos dorados. Max 20 slides variante ejecutiva / 30 variante tecnica. Notas de orador con referencias de evidencia ([CODIGO], [DOC], [INFERENCIA], [SUPUESTO]). |

## Convenciones de Naming

- Los archivos siguen el patron `{fase}_{entregable}_{cliente}_{timestamp}` [EXPLICIT]
- El timestamp usa formato ISO 8601 compacto (YYYYMMDD-HHmmss) [EXPLICIT]
- Los formatos branded (HTML, DOCX, PPTX, XLSX) incluyen el Design System MetodologIA v5 [EXPLICIT]
- El markdown es el source of truth; los demas formatos se derivan de el [EXPLICIT]

## Reglas de Generacion

- Todo formato branded debe incluir header con logo, colores navy/gold, y tipografia Poppins [EXPLICIT]
- XLSX siempre incluye auto-filtros y formato condicional por severidad [EXPLICIT]
- PPTX no excede 20 slides (ejecutiva) o 30 slides (tecnica) [EXPLICIT]
- HTML es self-contained (inline CSS, no external dependencies) y WCAG AA compliant [EXPLICIT]
