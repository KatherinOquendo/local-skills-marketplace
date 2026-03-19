---
name: secrets-sanitization
description: Motor de sanitización y enmascaramiento de datos sensibles pre-LLM. Implementa Gate G0 de seguridad para interceptar credenciales antes de inyectarlas al contexto de Claude.
author: Javier Montano · Comunidad MetodologIA
argument-hint: "<codebase-path>"
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

# secrets-sanitization

> Sensitive data sanitization and masking engine (Pre-LLM).
> Gate G0: intercept credentials, tokens, and private keys before they enter Claude's context window.

## Grounding Guideline

> *An exposed secret is not a bug — it is a breach of trust that cannot be reversed.*

1. **Gate G0: before everything.** No pipeline analysis should execute on code with visible credentials.
2. **Reversible masking.** Placeholders must preserve the architectural context without exposing sensitive values.
3. **Zero false negatives.** A false positive (masking something that is not a secret) is preferable to letting a real credential through.

---

## TL;DR

Scans the client repository to detect secrets (API keys, tokens, passwords, connection strings, private keys) and masks them with reversible placeholders (`[MAO_MASKED_CREDENTIAL]`). Implements Gate G0 as the first line of defense before G1.

---

## Core Responsibilities

1. **Secret detection** — Regex scanning of source and configuration files with 14 patterns (AWS, GitHub, JWT, Slack, Azure, Anthropic, OpenAI, Stripe, generic)
2. **Reversible masking** — Replace sensitive values with standardized placeholders while preserving the architectural context of the code
3. **Gate G0** — Mandatory pre-pipeline validation that aborts `/mao:run-auto` and `/mao:run-deep` if unmasked files are detected
4. **Local audit** — Finding registry in `discovery/mao-secrets-audit.log` (gitignored, no conductor access)

---

## Assigned Skills

| Skill | Rol |
|-------|-----|
| `secrets-sanitization` (self) | Motor principal de detección y enmascaramiento |
| `discovery-orchestrator` | Integración con pipeline — G0 gate check |
| `quality-engineering` | Definición de umbrales y criterios de paso |

---

## Output Configuration

### Output Artifact

**Nombre**: `{fase}_Secrets_Sanitization_{cliente}_{WIP|Aprobado}.md`

### Output Templates

| Formato | Especificación |
|---------|---------------|
| **Markdown** | Reporte de hallazgos con tabla de secretos detectados, clasificación por severidad, estado de enmascaramiento. Ghost menu + evidence tags. |
| **HTML** | Self-contained con tokens canónicos MetodologIA (#122562, #1F2833). Tabla de hallazgos con badges de severidad. WCAG AA. |
| **DOCX** | python-docx. Heading 1 = Poppins 700 #122562. Tabla de hallazgos con colores por severidad. Header con logo MetodologIA. |
| **XLSX** | openpyxl. Hoja "Secrets Audit" con columnas: ID, Tipo, Archivo, Línea, Severidad, Estado. Header navy #122562. |
| **PPTX** | python-pptx. Max 10 slides ejecutivo. Slide master navy. Resumen de hallazgos + recomendaciones. Speaker notes con evidencia. |

---

## Escalation Triggers

- >10 secretos detectados en un solo repositorio → Escalar a `risk-controller`
- Private key detectada → Alerta CRÍTICA inmediata
- `.env` con valores de producción → Bloqueo obligatorio de pipeline
- Secrets en archivos de CI/CD → Escalar a `devsecops-architect`

---

## Protocolo de Escaneo

### Patrones detectados

| Categoría | Patrón | Ejemplo |
|-----------|--------|---------|
| AWS Access Key | `AKIA[0-9A-Z]{16}` | `AKIAIOSFODNN7EXAMPLE` |
| GitHub Token | `gh[ps]_[A-Za-z0-9_]{36,}` | `ghp_xxxxxxxxxxxx` |
| API Key genérica | `api[_-]?key\s*[=:]\s*...` | `API_KEY=abc123...` |
| Password genérico | `(secret\|password\|pwd)\s*[=:]...` | `DB_PASSWORD="..."` |
| Bearer Token | `bearer\s+...` | `Authorization: Bearer eyJ...` |
| Connection String | `(mongodb\|postgres\|mysql)://...` | `postgres://user:pass@host/db` |
| Private Key | `-----BEGIN...PRIVATE KEY-----` | RSA/EC/DSA/OPENSSH |
| JWT | `eyJ...` (3 segmentos base64) | `eyJhbGciOiJIUzI1NiJ9...` |
| Slack Token | `xox[bpors]-...` | `xoxb-123456-abcdef` |
| Anthropic Key | `sk-ant-...` | `sk-ant-api03-xxxxx` |
| OpenAI Key | `sk-[A-Za-z0-9]{32,}` | `sk-xxxxxxxxxxxxxxxx` |
| Stripe Key | `[sr]k_(live\|test)_...` | `sk_live_xxxxxxxxxxxx` |

### Archivos excluidos

- Binarios (png, jpg, zip, jar, exe, dll, etc.)
- `node_modules/`, `.git/`, `vendor/`, `dist/`, `__pycache__/`
- `discovery/` (propio directorio de sesión)
- Archivos > 1MB

### Flujo de enmascaramiento

```
Detección → Clasificación → Placeholder → Mapa reversible → Auditoría
                                ↓
                    [MAO_MASKED_{N}]
                                ↓
                    mao-secrets-map.json (NUNCA commitear)
```

---

## Scripts

| Script | Ubicación | Propósito |
|--------|-----------|----------|
| `secrets-scan.sh` | `scripts/secrets-scan.sh` | Escaneo de secretos con regex |
| `secrets-mask.sh` | `scripts/secrets-mask.sh` | Enmascaramiento reversible |

---

## Evidence Tags

- `[SECURITY]` — Hallazgo de seguridad confirmado por escaneo
- `[CÓDIGO]` — Patrón detectado en código fuente
- `[CONFIG]` — Patrón detectado en archivo de configuración
