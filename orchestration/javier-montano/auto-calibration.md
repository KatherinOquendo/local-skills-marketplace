# Auto-Calibration — Gestión Dinámica de Contexto y Priming

## Máquina de Estados de Contexto

```
COLD  (0 priming files)    → Capacidad limitada. Sugerir /sdf:prime-repo o equivalente.
WARM  (1-2 priming files)  → Express OK. Deep discovery no recomendado.
HOT   (3-5 priming files)  → Pipeline completo viable.
DEEP  (6+ priming files)   → Óptimo para todos los modos.
```

## Protocolo de Inicio de Sesión

Al iniciar conversación, verificar en orden:

1. **¿Existe `discovery/session-state.json`?**
   - SÍ → Leer fase actual, gates pasados, skills activos. Continuidad.
   - NO → Sesión nueva. Detectar contexto desde cero.

2. **¿Existe `discovery/calibration-digest.md`?**
   - SÍ → Leer estado de priming (COLD/WARM/HOT/DEEP), dominios cubiertos.
   - NO → Asumir COLD. Hooks lo generarán si hay scripts disponibles.

3. **¿Existe `lessons-learned.md` (global o del plugin)?**
   - SÍ → Leer para evitar errores previos. Prioridad alta.
   - NO → Proceder sin lecciones previas.

4. **¿Existe `session-changelog.md`?**
   - SÍ → Leer últimas 20 entradas para contexto de continuidad.
   - NO → Sesión limpia.

## Ajuste Dinámico de Nivel de Carga

| Estado | Nivel Default | Cuándo Escalar |
|--------|---------------|----------------|
| COLD | L1 (metadata) | Si tarea requiere análisis profundo → sugerir priming primero |
| WARM | L1-L2 | Si tarea es de dominio cubierto por priming → L2 |
| HOT | L2 (core) | Si tarea es crítica o ambigua → L3 para skills relevantes |
| DEEP | L2 (core) | Si fase 3b (feasibility) o gate → L3 automático |

**Escalamiento explícito**: si una tarea específica necesita deep context de un skill:
```
lazy-load-resolver.sh <FASE> <TIPO_SERVICIO> <PLUGIN_DIR> L3
```

## Detección de Gaps de Priming

Al activar un pipeline o recibir tarea compleja:

1. Listar dominios requeridos para la tarea (ej. arquitectura, datos, seguridad)
2. Mapear contra priming files existentes
3. Identificar gaps: dominios sin cobertura
4. Sugerir acciones específicas:
   - "Falta contexto de infraestructura. ¿Puede compartir diagrama de arquitectura o URL de documentación?"
   - "Para análisis de datos completo, necesito acceso al schema de BD o modelo de datos."

## Recalibración Automática

Triggers de recalibración:
- Nuevo archivo `priming-rag-*.md` creado → actualizar `calibration-digest.md`
- Adjunto procesado → reclasificar cobertura
- Cambio de fase en pipeline → reevaluar nivel de carga necesario
- Corrección del usuario → actualizar `lessons-learned.md`

**Delegación**: la lógica de decisión vive aquí. La ejecución la hacen:
- `scripts/lazy-load-resolver.sh` → carga de agentes/skills por nivel
- `scripts/auto-prime-check.sh` → detección de estado de priming
- `scripts/post-prime-calibrate.sh` → regeneración de calibration-digest

## Continuidad Cross-Sesión

Para mantener coherencia entre conversaciones:

1. **session-state.json** persiste: fase, gates, skills activos, assumptions
2. **session-changelog.md** persiste: acciones, decisiones, timestamps
3. **calibration-digest.md** persiste: estado de priming, cobertura
4. **lessons-learned.md** persiste: correcciones, patrones, anti-patrones

Al detectar estos archivos → restaurar contexto automáticamente.
Al no detectarlos → sesión limpia, calibración desde cero.
