# Input Amplifier — Protocolo de Reinterpretación de Inputs

## Activación

Se ejecuta como **razonamiento interno** en CADA input del usuario. NO produce output visible salvo que se solicite explícitamente. Es un pre-proceso mental, no una invocación de skill.

## Protocolo de 3 Pases

### Pass A — Corrección de Superficie

Detectar y corregir mentalmente:
- Typos y abreviaciones comunes (q → que, xq → porque, tb → también)
- Spanglish: mezcla español/inglés → interpretar en el idioma dominante
- Consonantes sin vocales → probable typo (ej. "scnarios" → "escenarios")
- Comandos mal escritos → mapear al comando correcto (ej. "/sdf:asis" → `/sdf:diagnose-asis`)
- Referencias ambiguas → resolver con contexto de sesión

### Pass B — Amplificación de Intención

Aplicar 5-Whys comprimido (3 niveles):
1. **¿Qué pidió?** — Lectura literal del input
2. **¿Qué necesita realmente?** — Necesidad subyacente detrás de las palabras
3. **¿Qué resultado espera ver?** — Entregable, formato, nivel de detalle

Determinar:
- **OBJETIVO**: verbo + objeto + contexto (ej. "diagnosticar estado actual del sistema de pagos")
- **PLUGIN**: cuál plugin debe activarse (si aplica)
- **FASE**: en qué fase del pipeline estamos (si hay pipeline activo)
- **FORMATO**: markdown, HTML, tabla, diagrama, código
- **PROFUNDIDAD**: rápido (1 párrafo), estándar (1 página), profundo (multi-sección)

### Pass C — Inyección de Contexto

Antes de responder, verificar:
- ¿Hay un pipeline activo? → Leer `session-state.json` para fase actual
- ¿Hay priming disponible? → Leer `calibration-digest.md` para cobertura
- ¿Hay lecciones relevantes? → Revisar `self-improvement.md` + plugin `lessons-learned.md`
- ¿Hay entregables previos? → Verificar `discovery/` para continuidad
- ¿El input referencia trabajo anterior? → Buscar en changelog

## Escalación a Input Analysis Completo

Cuando el input es ambiguo O la confianza del amplifier es baja:

| Señal | Acción |
|-------|--------|
| Confianza ≥ 70% en los 3 pases | Proceder con amplificación interna |
| Confianza 50-69% | Aplicar amplificación + hacer 1 pregunta de clarificación |
| Confianza < 50% | Delegar a `sofka-input-analysis` skill (5-pass completo) |
| Input > 500 palabras con múltiples temas | Delegar a `sofka-input-analysis` |
| Input contiene adjuntos + instrucciones | Delegar a `sofka-input-analysis` |

**Skill de escalación**: `{plugin-activo}/skills/input-analysis/SKILL.md`
- SDF: `sofka-input-analysis` (5-pass: surface → intent → context → amplify → validate)
- MAO: `metodologia-input-analysis` (mismo protocolo, branding MetodologIA)

## Anti-patrones

- NUNCA mostrar el análisis de amplificación como output visible (a menos que el usuario lo pida)
- NUNCA inventar intención — si no es clara, preguntar
- NUNCA ignorar el contexto de sesión — siempre verificar estado del pipeline
- NUNCA asumir plugin — si la detección es ambigua, preguntar: "¿Qué contexto? Sofka / MetodologIA / JM Labs"
