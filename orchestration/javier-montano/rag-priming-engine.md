# RAG Priming Engine — Auto-conversión de Inputs a Conocimiento Persistente

## Triggers de Auto-Priming

| Evento | Acción |
|--------|--------|
| Usuario comparte archivo (PDF, DOCX, XLSX, imagen) | Extraer → crear `priming-rag-{slug}.md` |
| Usuario comparte URL | Fetch → extraer → crear `priming-rag-{slug}.md` |
| Usuario pega texto largo (> 200 palabras) con contexto de negocio | Evaluar relevancia → crear si aporta conocimiento reutilizable |
| Usuario referencia documento externo ("ver el RFC de autenticación") | Solicitar acceso → procesar si se obtiene |
| Pipeline activo detecta gap de dominio | Sugerir fuentes específicas para priming |

## Protocolo de Extracción

Para cada input candidato a priming:

### 1. Clasificación
- **Tipo**: spec, constraint, org-chart, budget, business-data, architecture, prior-deliverable, external-doc
- **Dominio**: arquitectura, datos, seguridad, negocio, infraestructura, UX, gestión
- **Relevancia**: alta (afecta entregables directamente) / media (contexto útil) / baja (referencia marginal)

### 2. Extracción (formato estándar)

```markdown
---
source: {nombre del archivo o URL}
type: {tipo clasificado}
domain: {dominio}
relevance: {alta|media|baja}
created: {fecha ISO}
affects: {lista de entregables impactados, ej. "03_AS-IS, 06_Roadmap"}
---

## TL;DR
{3-5 bullets con la esencia del documento}

## Entidades Clave
{nombres, sistemas, procesos, tecnologías mencionados}

## Datos Cuantitativos
{números, métricas, SLAs, volúmenes — si aplican}

## Restricciones y Requisitos
{constraints explícitos del documento}

## Contexto para Discovery
{cómo este documento impacta el análisis y las recomendaciones}

## Keywords
{términos de búsqueda para retrieval futuro}
```

### 3. Naming y Ubicación

**Nombre**: `priming-rag-{slug-descriptivo}.md`
- Ejemplo: `priming-rag-arquitectura-pagos.md`, `priming-rag-requisitos-compliance.md`

**Ubicación** (decision tree):
- Si hay plugin activo con pipeline → `discovery/rag-priming/`
- Si es conocimiento persistente (reusable entre sesiones) → `{plugin}/references/`
- Si no hay plugin activo → `discovery/rag-priming/` (crear si no existe)

### 4. Recalibración

Después de crear/modificar un priming file:
1. Actualizar `calibration-digest.md` con nuevo conteo y cobertura
2. Evaluar impacto en entregables previos (si hay pipeline activo)
3. Log en `session-changelog.md`

## Cobertura y Gaps

Mapeo de priming files contra fases del pipeline:

| Fase | Dominios Necesarios |
|------|---------------------|
| 02 Brief Técnico | arquitectura, infraestructura, stack tecnológico |
| 03 AS-IS | código, config, tests, deuda técnica |
| 04 Flujos | procesos, integraciones, APIs, eventos |
| 05 Escenarios | negocio, restricciones, presupuesto |
| 06 Roadmap | capacidades del equipo, timeline, dependencias |
| 07 Spec Funcional | requisitos, user journeys, UX |

Si un dominio requerido no tiene priming → flag como gap + sugerir fuente.

## Delegación a Plugin

Cuando un plugin está activo, el priming engine delega al protocolo específico:
- SDF: `references/ontology/rag-priming-policy.md` (5-step attachment processing)
- MAO: mismo protocolo, branding MetodologIA
- PM-APEX: adaptado a documentos de gestión de proyectos

El engine global maneja el caso donde NO hay plugin activo.
