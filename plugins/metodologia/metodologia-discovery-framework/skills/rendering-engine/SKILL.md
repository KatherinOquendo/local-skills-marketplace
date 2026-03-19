---
name: rendering-engine
description: Motor de renderizado automático para generación de diagramas (PNG) desde Mermaid y exportación de propuestas a PDF con branding MetodologIA.
author: Javier Montano · Comunidad MetodologIA
argument-hint: "<source-file> [png|pdf|all]"
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

# rendering-engine

> Automatic rendering engine: Mermaid -> PNG, Markdown -> PDF.
> Strict MetodologIA branding in all visual outputs.

## Grounding Guideline

> *An invisible rendering engine is a successful rendering engine. The user sees the result, not the process.*

1. **Brand fidelity in every pixel.** Every visual output must comply with Neo-Swiss v6 tokens without exception.
2. **Self-containment.** Every generated artifact must be portable — no external dependencies, no broken links.
3. **Formats as first-class citizens.** PNG, PDF, HTML, and Markdown deserve the same level of quality.

---

## TL;DR

Converts Mermaid code blocks into static PNG images and compiles complete deliverables to professional PDF with MetodologIA branding. Evidence tags `[CÓDIGO]`, `[DOC]`, etc. are rendered as visual badges in the final document.

---

## Core Responsibilities

1. **PNG Generation** — Detectar bloques ` ```mermaid ` en entregables, renderizar con Mermaid CLI a `discovery/assets/`
2. **PDF Compilation** — Compilar markdown a PDF con Pandoc + wkhtmltopdf (o Typst como alternativa)
3. **Branding Enforcement** — Paleta MetodologIA (#122562, #1F2833), tipografía Poppins/Trebuchet MS
4. **Evidence Badges** — Tags de evidencia renderizados como badges HTML coloreados por tipo

---

## Assigned Skills

| Skill | Rol |
|-------|-----|
| `rendering-engine` (self) | Motor principal de renderizado |
| `design-system` | Tokens canónicos y componentes de branding |
| `mermaid-diagramming` | Validación de sintaxis Mermaid |

---

## Output Configuration

### Output Artifact

**Nombre**: `{fase}_{entregable}_{cliente}_{WIP|Aprobado}.pdf`

### Output Templates

| Formato | Especificación |
|---------|---------------|
| **Markdown** | Source de verdad — contiene bloques Mermaid originales + evidence tags en texto. |
| **HTML** | Self-contained con CSS MetodologIA. Mermaid renderizado inline. Evidence tags como badges. WCAG AA. |
| **DOCX** | python-docx. Poppins/Trebuchet MS font. Imágenes PNG embebidas desde `discovery/assets/`. Header MetodologIA. |
| **XLSX** | openpyxl. Hoja "Rendering Log" con columnas: Diagram ID, Source File, Output PNG, Status. |
| **PPTX** | python-pptx. PNGs de diagramas como imágenes full-slide. Slide master navy MetodologIA. |

---

## Escalation Triggers

- `mmdc` no instalado → Warning graceful, no bloqueo (diagramas permanecen como código)
- Pandoc/wkhtmltopdf no instalados → Export como HTML en lugar de PDF
- Diagrama Mermaid con sintaxis inválida → Log error, continuar con siguientes bloques

---

## Scripts

| Script | Ubicación | Propósito |
|--------|-----------|----------|
| `render-mermaid.sh` | `scripts/render-mermaid.sh` | Renderizar bloques Mermaid a PNG |
| `export-pdf.sh` | `scripts/export-pdf.sh` | Compilar entregable a PDF con branding |

---

## Branding Rules (Inmutable)

- **Primary**: #122562 (navy) — headers, bordes, acentos
- **Background**: #1F2833 (dark) — fondo de tablas alternas, backgrounds
- **Typography**: Poppins/Trebuchet MS (pesos 300-700)
- **Evidence badges**: Coloreados por tipo (CÓDIGO=green bg, CONFIG=blue bg, DOC=indigo bg, INFERENCIA=purple bg, SUPUESTO=red bg)
