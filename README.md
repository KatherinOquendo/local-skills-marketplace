# JM Labs

Private monorepo for Javier Montano's professional ecosystem.

## Brand Map

| Brand | Entity | License | Scope |
|-------|--------|---------|-------|
| **Sofka** | Sofka Technologies | All Rights Reserved | Enterprise discovery, client delivery |
| **MetodologIA** | MetodologIA (GPL-3.0) | GPL-3.0 | Open methodology, community tools |
| **Javier Montano** | Personal / JM Labs | MIT | Innovation, core tools, experiments |

## Structure

```
jm-labs/
├── skills/           → Level 1: Content type
│   ├── sofka/        → Level 2: Entity
│   │   ├── {skill}/  → Level 3: Atomic unit
│   │   └── index.md  → Entity-level index
│   ├── metodologia/
│   ├── javier-montano/
│   └── index.md      → Type-level index
├── plugins/
│   ├── sofka/
│   ├── metodologia/
│   └── javier-montano/
├── projects/
│   ├── sofka/
│   ├── metodologia/
│   └── javier-montano/
├── governance/
│   ├── sofka/
│   ├── metodologia/
│   └── javier-montano/
├── deliverables/
│   ├── sofka/
│   ├── metodologia/
│   └── javier-montano/
├── orchestration/
│   ├── sofka/
│   ├── metodologia/
│   └── javier-montano/
└── {changelog,tasklog,log,index}.md  → Root-level tracking
```

## Tracking Files (at every level)

| File | Purpose |
|------|---------|
| `index.md` | Catalog of items at this level with status and metadata |
| `changelog.md` | Chronological record of changes |
| `tasklog.md` | Active and completed tasks |
| `log.md` | Session logs, notes, observations |

## Quick Navigation

| I need to... | Go to |
|-------------|-------|
| Browse all skills | `skills/index.md` |
| See JM Labs personal skills | `skills/javier-montano/index.md` |
| Find a plugin | `plugins/index.md` |
| Check governance docs | `governance/index.md` |
| Review project deliverables | `deliverables/index.md` |
| Understand orchestration | `orchestration/index.md` |

## Related Repositories

| Repo | Brand | Visibility |
|------|-------|------------|
| `sofka-discovery-framework` | Sofka | Private |
| `sofka-presales-skills` | Sofka | Public |
| `sofka-discovery-framework-public` | Sofka | Public mirror |
