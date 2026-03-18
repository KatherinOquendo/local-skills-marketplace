# Preferences Log — Registro de Preferencias del Usuario

## Protocolo

Capturar preferencias explícitas e implícitas del usuario. A diferencia de `self-improvement.md` (correcciones y errores), este log registra **cómo le gusta trabajar** — estilos, defaults, decisiones de diseño recurrentes.

### Cuándo Registrar
- Usuario declara preferencia explícita ("prefiero X sobre Y", "siempre usar Z")
- Patrón implícito detectado (3+ veces elige la misma opción)
- Decisión de diseño que establece precedente para futuras sesiones

### Formato

```markdown
### [{fecha ISO}] {preferencia}
**Tipo**: workflow | output | tooling | communication | design
**Señal**: {cómo se detectó — explícita o patrón implícito}
**Regla**: {regla derivada}
```

---

## Preferencias de Workflow

### [2026-03-16] Plan mode para tareas complejas
**Tipo**: workflow
**Señal**: Explícita — patrones del screenshot adjunto (Plan Mode Default)
**Regla**: Tareas con 3+ pasos → descomponer primero, validar plan, luego ejecutar

### [2026-03-16] Subagentes para trabajo pesado
**Tipo**: workflow
**Señal**: Explícita — patrones del screenshot (Subagent Strategy)
**Regla**: Offload investigación y análisis paralelo a subagentes. 1 tarea por subagente.

## Preferencias de Output

### [2026-03-16] File naming con tags de estado
**Tipo**: output
**Señal**: Explícita — corrección directa del usuario
**Regla**: Todo archivo generado lleva `{WIP}` o `{Aprobado}` en el nombre

### [2026-03-16] Markdown-Excellence como estándar
**Tipo**: output
**Señal**: Explícita — definido en CLAUDE.md y ontologías
**Regla**: TL;DR, prosa densa, tablas, Mermaid, evidence tags, ghost menu

### [2026-03-16] Español latinoamericano registro empresarial
**Tipo**: output
**Señal**: Explícita — todos los outputs en español salvo que se pida otro idioma
**Regla**: Español claro, directo, sin jerga académica sin explicar. Código en inglés.

## Preferencias de Tooling

### [2026-03-16] Plugins como sistema operativo
**Tipo**: tooling
**Señal**: Explícita — el usuario construye y opera 3 plugins como su herramienta principal
**Regla**: Siempre verificar qué plugin está activo antes de actuar. Respetar frontmatter.

## Preferencias de Communication

### [2026-03-16] Sin resúmenes al final
**Tipo**: communication
**Señal**: Implícita — anti-patrón registrado en self-improvement
**Regla**: No resumir lo que acabas de hacer. El usuario lee el diff.

### [2026-03-16] Reinterpretar inputs para máxima potencia
**Tipo**: communication
**Señal**: Explícita — "Re interpreta mis inputs para maxima potencia"
**Regla**: Aplicar input-amplifier 3-pass en cada input. Nunca tomar literalmente un input pobre.

## Preferencias de Design

### [2026-03-16] Red de archivos sobre monolito
**Tipo**: design
**Señal**: Explícita — "que el claude.md se convierta en una red de archivos"
**Regla**: Preferir federación sobre centralización. Hub lean + sub-archivos especializados.

### [2026-03-16] Meta-skills nivel MOAT
**Tipo**: design
**Señal**: Explícita — "todos nivel moat, de meta skills"
**Regla**: Cada archivo de orquestación debe ser tan riguroso como un SKILL.md de plugin.
