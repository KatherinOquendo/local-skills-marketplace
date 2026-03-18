# Plugins

Claude Code plugin frameworks. Each plugin is a self-contained directory with its own plugin.json, skills, agents, commands, and hooks.

## Catalog

| Plugin | Brand | Description | Skills | Agents | Commands |
|--------|-------|-------------|--------|--------|----------|
| `metodologia-discovery-framework/` | MetodologIA | Full discovery methodology pipeline | 111 | 101 | 109 |
| `pm-project-framework/` | JM Labs | Project management framework | TBD | TBD | TBD |
| `sovereign-architect/` | JM Labs | Software architecture analysis pipeline | TBD | TBD | TBD |
| `scriba/` | JM Labs | Note-taking and documentation automation | TBD | TBD | TBD |

## Installation

To install a plugin in Claude Code:

```bash
# From this repo
claude plugin add ./plugins/{plugin-name}

# Or symlink to ~/.claude/plugins/
ln -s $(pwd)/plugins/{plugin-name} ~/.claude/plugins/{plugin-name}
```
