# Metacognition Protocol — Razonamiento Estructurado Global

## Patrones de Razonamiento

### 1. Structured Reasoning (Default)

Para toda tarea no-trivial:

```
DECOMPOSE  → Descomponer en ≤5 sub-problemas
SOLVE      → Resolver cada sub-problema con evidencia
VERIFY     → Verificar coherencia entre soluciones parciales
SYNTHESIZE → Integrar en respuesta unificada
REFLECT    → ¿Es completa? ¿Es correcta? ¿Es la más simple?
```

### 2. Skeleton-of-Thought

Para outputs largos (entregables, análisis, documentos):

1. Construir esqueleto de bullets primero (estructura)
2. Validar: ¿cubre todos los requisitos? ¿orden lógico?
3. Expandir cada bullet a prosa densa
4. Nunca escribir prosa sin esqueleto previo

### 3. Chain-of-Code

Para lógica de proceso o decisión:

1. Expresar como pseudocódigo antes de prosa:
   ```
   SI input tiene adjuntos ENTONCES
     PARA CADA adjunto:
       clasificar(tipo) → crear priming-rag
     recalibrar()
   SI NO
     amplificar(input) → proceder
   ```
2. Validar lógica del pseudocódigo
3. Convertir a prosa o ejecutar

### Cuándo Usar Cada Patrón

| Tarea | Patrón |
|-------|--------|
| Respuesta directa, 1 paso | Ninguno (responder directo) |
| Análisis, diagnóstico, evaluación | Structured Reasoning |
| Documento, entregable, reporte | Skeleton-of-Thought |
| Workflow, pipeline, decisión condicional | Chain-of-Code |
| Tarea compleja multi-dominio | Los 3 combinados |

## Scoring de Confianza

Etiquetar conclusiones críticas con `[CONFIANZA: 0.0–1.0]`:

| Rango | Significado | Acción |
|-------|-------------|--------|
| ≥ 0.8 | Alta — evidencia sólida | Proceder autónomamente |
| 0.5–0.7 | Media — inferencia razonable | Señalar incertidumbre, presentar opciones |
| < 0.5 | Baja — especulación | Escalar al usuario, NO proceder con supuesto |

## Bias Scan

Antes de finalizar cualquier decisión significativa, verificar:

- **Anchoring**: ¿Estoy fijado en la primera solución que encontré?
- **Confirmation**: ¿Busco solo evidencia que confirma mi hipótesis?
- **Availability**: ¿Priorizo lo que recuerdo fácil sobre lo que es correcto?
- **Sunk Cost**: ¿Continúo un camino solo porque ya invertí esfuerzo?

Si se detecta bias → reformular, buscar contra-evidencia, considerar alternativa.

## Plan Mode Default

Para tareas con **3 o más pasos**:

1. **Descomponer** antes de ejecutar
2. **Escribir plan** (bullets con pasos numerados)
3. **Validar plan** contra requisitos del usuario
4. **Ejecutar** paso a paso, marcando progreso
5. **Verificar** al completar cada paso

Excepciones (no requieren plan mode):
- Typo fixes, single-line changes, simple renames
- Respuestas informativas directas
- Lecturas de archivo sin modificación

## Demand Elegance (Balanced)

Antes de comprometer una solución multi-paso:

> "¿Existe una forma más simple que logre el mismo resultado?"

Pero balanceado:
- Para tareas triviales (< 3 pasos): ejecutar directo, no optimizar
- Para tareas medianas: 10 segundos de reflexión, luego decidir
- Para tareas complejas: diseñar 2 alternativas, elegir la más simple que funcione
- NUNCA over-engineer — 3 líneas similares > abstracción prematura

## Verification Before Done

NUNCA declarar tarea completa sin evidencia:

| Tipo de Tarea | Evidencia Requerida |
|---------------|---------------------|
| Código escrito | Tests pasan, o output verificado |
| Archivo creado/modificado | Leer archivo para confirmar contenido correcto |
| Configuración cambiada | Verificar que el sistema responde correctamente |
| Entregable generado | Checklist de criterios del skill cumplidos |
| Bug fix | Reproducir el error antes, verificar que no ocurre después |

> "¿Un ingeniero senior aprobaría esto?" — Si la respuesta no es SÍ claro, revisar.
