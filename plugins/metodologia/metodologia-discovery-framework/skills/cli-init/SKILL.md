---
name: cli-init
description: CLI interactivo de inicialización que configura el entorno del cliente, pre-puebla discovery/, ejecuta G0 security scan y prepara el contexto para discovery.
author: Javier Montano · Comunidad MetodologIA
argument-hint: "<project-name> [industry]"
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

# cli-init

> CLI interactivo de inicialización para MetodologIA.
> Configura el entorno del cliente como paso previo a iniciar Claude Code.

## Grounding Guideline

> *The first impression of the framework is the initialization. If it fails, the user does not return.*

1. **Zero-config by default.** The user must be able to start without configuring anything — default values must be intelligent.
2. **Automatic context detection.** The init must read the repository, detect technologies, and pre-configure the discovery.
3. **Fail fast, fail clear.** If something is missing, say so immediately with remediation instructions.

---

## TL;DR

Wizard interactivo que pre-puebla `discovery/SESSION-README.md` con datos del cliente (nombre, tipo de servicio, industria), ejecuta auto-discovery del repositorio, corre el gate G0 de seguridad, y prepara toda la estructura de sesión. Reemplaza la activación manual propensa a errores.

---

## Core Responsibilities

1. **Interactive Wizard** — Preguntas por consola: nombre del cliente, TIPO_SERVICIO, contacto, industria
2. **Structure Generation** — Crear `discovery/` con todos los subdirectorios y archivos de sesión
3. **Auto-Discovery** — Ejecutar `index-repo.sh` para generar `repo-index.json` antes de que Claude despierte
4. **G0 Integration** — Ejecutar `secrets-scan.sh` durante inicialización para verificar seguridad
5. **Hook Configuration** — Enlazar ghost menu y changelog automático

---

## Assigned Skills

| Skill | Rol |
|-------|-----|
| `cli-init` (self) | Wizard de inicialización |
| `secrets-sanitization` | Integración G0 durante init |
| `discovery-orchestrator` | Contexto post-init para pipeline |

---

## Output Configuration

### Output Artifact

**Nombre**: `discovery/SESSION-README.md` + `discovery/session-state.json`

### Output Templates

| Formato | Especificación |
|---------|---------------|
| **Markdown** | SESSION-README.md con tabla de cliente, estado de discovery, quick start commands. Ghost menu. |
| **HTML** | Self-contained con tokens canónicos MetodologIA. Reporte de inicialización con status badges. WCAG AA. |
| **DOCX** | python-docx. Heading 1 = Poppins 700 #122562. Tabla de configuración del cliente. Header MetodologIA. |
| **XLSX** | openpyxl. Hoja "Init Config" con columnas: Parameter, Value, Status. Header navy #122562. |
| **PPTX** | python-pptx. 5 slides: Banner, Client Info, Service Type, G0 Status, Next Steps. Slide master navy. |

---

## Escalation Triggers

- G0 detecta secretos durante init → Warning prominente + instrucciones de remediación antes de discovery
- Repositorio vacío → Advertir que auto-discovery no generará `repo-index.json`
- TIPO_SERVICIO no reconocido → Default a SDA con confirmación

---

## Scripts

| Script | Ubicación | Propósito |
|--------|-----------|----------|
| `mao-init.sh` | `scripts/mao-init.sh` | Wizard interactivo de inicialización |
