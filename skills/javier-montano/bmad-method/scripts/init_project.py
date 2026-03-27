#!/usr/bin/env python3
"""
init_project.py — Scaffold a new BMAD project.

Usage:
    python init_project.py <project-name> [--greenfield|--brownfield]

Creates the standard BMAD directory structure with starter files:
    .bmad/           — Project configuration and custom agents
    planning_artifacts/ — PRD, UX spec, product brief
    architecture/    — Architecture docs and ADRs
    epics/           — Epic definitions
    stories/         — User stories
    sprints/         — Sprint status and plans
    project-knowledge/ — Codebase documentation (brownfield only)
"""

import argparse
import sys
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# ANSI colours
# ---------------------------------------------------------------------------
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def info(msg: str) -> None:
    print(f"{CYAN}[info]{RESET} {msg}")


def success(msg: str) -> None:
    print(f"{GREEN}[ok]{RESET}   {msg}")


def warn(msg: str) -> None:
    print(f"{YELLOW}[warn]{RESET} {msg}")


def error(msg: str) -> None:
    print(f"{RED}[err]{RESET}  {msg}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Templates (inline, zero-dependency)
# ---------------------------------------------------------------------------

def _project_context_content(project_name: str, project_type: str) -> str:
    today = date.today().isoformat()
    return f"""---
project-name: "{project_name}"
version: "0.1.0"
team-size: 1
created: "{today}"
last-updated: "{today}"
---

# {project_name} — Project Context

<!-- This is the project constitution. Every workflow and agent references it. -->

## Vision

<!-- One-paragraph north star. What does success look like? -->

TODO: Describe the project vision.

## Problem Statement

<!-- What pain point does this project address? Who feels it? -->

TODO: Describe the problem.

## Tech Stack

| Layer        | Technology | Version | Rationale |
|-------------|-----------|---------|-----------|
| Frontend    | TODO      | —       | —         |
| Backend     | TODO      | —       | —         |
| Database    | TODO      | —       | —         |
| Auth        | TODO      | —       | —         |
| Hosting     | TODO      | —       | —         |
| CI/CD       | TODO      | —       | —         |

## Constraints

- **Budget**: TODO
- **Timeline**: TODO
- **Regulatory**: TODO
- **Technical**: TODO

## Conventions

### Code Style
- Language standard: TODO
- Linter config: TODO
- Formatter: TODO

### Git Workflow
- Branching model: TODO
- Commit convention: TODO
- PR review policy: TODO

### Naming Conventions
- Files: TODO
- Components: TODO
- Database entities: TODO
- API endpoints: TODO

### Testing Strategy
- Unit test minimum coverage: TODO%
- Integration tests: TODO
- E2E tests: TODO

## Team

| Role           | Name | Contact | Responsibility |
|---------------|------|---------|----------------|
| Product Owner | TODO | —       | Requirements   |
| Tech Lead     | TODO | —       | Architecture   |
| Developer     | TODO | —       | Implementation |

## Links

| Resource      | URL  |
|--------------|------|
| Repository   | TODO |
| Project Board| TODO |
| CI/CD        | TODO |

---
<!-- Keep this file up to date. It is the single source of truth for project context. -->
"""


def _config_yaml_content(project_name: str, project_type: str) -> str:
    today = date.today().isoformat()
    return f"""# BMAD Configuration — {project_name}
# Generated: {today}

bmad:
  version: "v6-alpha"
  module: "bmm"

project:
  name: "{project_name}"
  type: "{project_type}"
  communication-language: "en"

paths:
  planning-artifacts: "planning_artifacts/"
  architecture: "architecture/"
  epics: "epics/"
  stories: "stories/"
  sprints: "sprints/"
  project-knowledge: "project-knowledge/"

user:
  name: "TODO"
  role: "TODO"
"""


def _readme_content(project_name: str, project_type: str) -> str:
    return f"""# {project_name}

> Scaffolded with **BMAD Method** (Breakthrough Method for Agile AI-Driven Development)

**Project type**: {project_type}

## Getting Started

1. Fill out `.bmad/project-context.md` — this is your project constitution.
2. Start **Phase 1 (Analysis)** by activating the Mary/Analyst agent.
3. Follow the phase-by-phase workflow to produce artifacts.

## Directory Structure

| Directory             | Purpose                                |
|-----------------------|----------------------------------------|
| `.bmad/`              | Project config, custom agents          |
| `planning_artifacts/` | PRD, UX spec, product brief            |
| `architecture/`       | Architecture docs and ADRs             |
| `epics/`              | Epic definitions                       |
| `stories/`            | User stories                           |
| `sprints/`            | Sprint status and plans                |
{"| `project-knowledge/`  | Codebase documentation                 |" if project_type == "brownfield" else ""}

## Phases

1. **Analysis** — Explore the problem space (Agent: Mary)
2. **Planning** — Define what to build (Agents: John, Sally)
3. **Solutioning** — Decide how to build it (Agents: Winston, Bob)
4. **Implementation** — Build it (Agents: Amelia, Quinn)
"""


def _gitkeep() -> str:
    return ""


def _brownfield_readme() -> str:
    return """# Project Knowledge

This directory holds documentation about the existing codebase.

Before proceeding with BMAD phases, run the **Document Project** workflow
to scan and document the current state:

- `codebase-overview.md` — High-level architecture of the existing system
- `dependency-map.md` — External dependencies and their versions
- `tech-debt-register.md` — Known technical debt items
- `api-inventory.md` — Existing API endpoints

These files become context for Phases 2-4.
"""


# ---------------------------------------------------------------------------
# Scaffolding logic
# ---------------------------------------------------------------------------

def scaffold_project(project_name: str, project_type: str, parent: Path) -> Path:
    """Create the full BMAD project directory tree and starter files."""

    root = parent / project_name
    if root.exists():
        error(f"Directory already exists: {root}")
        sys.exit(1)

    # Define directory tree
    dirs = [
        root / ".bmad",
        root / ".bmad" / "agents",
        root / "planning_artifacts",
        root / "architecture",
        root / "architecture" / "adr",
        root / "epics",
        root / "stories",
        root / "sprints",
    ]

    if project_type == "brownfield":
        dirs.append(root / "project-knowledge")

    # Create directories
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        success(f"Created {d.relative_to(parent)}/")

    # Write starter files
    files = {
        root / ".bmad" / "project-context.md": _project_context_content(project_name, project_type),
        root / ".bmad" / "config.yaml": _config_yaml_content(project_name, project_type),
        root / "README.md": _readme_content(project_name, project_type),
        root / "planning_artifacts" / ".gitkeep": _gitkeep(),
        root / "architecture" / ".gitkeep": _gitkeep(),
        root / "architecture" / "adr" / ".gitkeep": _gitkeep(),
        root / "epics" / ".gitkeep": _gitkeep(),
        root / "stories" / ".gitkeep": _gitkeep(),
        root / "sprints" / ".gitkeep": _gitkeep(),
    }

    if project_type == "brownfield":
        files[root / "project-knowledge" / "README.md"] = _brownfield_readme()

    for filepath, content in files.items():
        filepath.write_text(content, encoding="utf-8")
        success(f"Wrote   {filepath.relative_to(parent)}")

    return root


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a new BMAD project.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python init_project.py my-saas-app --greenfield
  python init_project.py legacy-rewrite --brownfield
  python init_project.py my-app --dry-run          # Preview without creating files
  python init_project.py my-app --verbose           # Detailed output

Exit codes:
  0  Success — project scaffolded
  1  Warning — project scaffolded with non-critical issues
  2  Error — project could not be scaffolded (directory exists, invalid name, etc.)
        """,
    )
    parser.add_argument("project_name", help="Name of the project (used as directory name)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--greenfield",
        dest="project_type",
        action="store_const",
        const="greenfield",
        help="New project from scratch (default)",
    )
    group.add_argument(
        "--brownfield",
        dest="project_type",
        action="store_const",
        const="brownfield",
        help="Existing codebase adoption — adds project-knowledge/ directory",
    )
    parser.set_defaults(project_type="greenfield")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be created without writing to disk",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output including file contents summary",
    )

    args = parser.parse_args()
    project_name: str = args.project_name
    project_type: str = args.project_type

    # Input validation
    import re as _re
    if not _re.match(r"^[a-zA-Z0-9][a-zA-Z0-9._-]*$", project_name):
        error(
            f"Invalid project name: '{project_name}'. "
            f"Use alphanumeric characters, hyphens, dots, or underscores. "
            f"Must start with a letter or number.\n"
            f"  Fix: rename to something like '{_re.sub(r'[^a-zA-Z0-9._-]', '-', project_name).strip('-')}'"
        )
        sys.exit(2)

    if len(project_name) > 100:
        error(
            f"Project name too long ({len(project_name)} chars). Maximum is 100 characters.\n"
            f"  Fix: use a shorter name."
        )
        sys.exit(2)

    print()
    print(f"{BOLD}BMAD Project Scaffolding{RESET}")
    print(f"  Project : {project_name}")
    print(f"  Type    : {project_type}")
    if args.dry_run:
        print(f"  Mode    : {YELLOW}DRY RUN (no files will be created){RESET}")
    print()

    if args.dry_run:
        root = Path.cwd() / project_name
        if root.exists():
            warn(f"Directory already exists: {root}")
        info("Would create the following structure:")
        dirs = [".bmad", ".bmad/agents", "planning_artifacts", "architecture",
                "architecture/adr", "epics", "stories", "sprints"]
        if project_type == "brownfield":
            dirs.append("project-knowledge")
        for d in dirs:
            print(f"    {CYAN}mkdir{RESET} {project_name}/{d}/")
        files = [".bmad/project-context.md", ".bmad/config.yaml", "README.md"]
        if project_type == "brownfield":
            files.append("project-knowledge/README.md")
        for f in files:
            print(f"    {GREEN}write{RESET} {project_name}/{f}")
        print(f"\n{YELLOW}Dry run complete. No files were created.{RESET}\n")
        sys.exit(0)

    root = scaffold_project(project_name, project_type, Path.cwd())

    if args.verbose:
        print()
        info(f"Project root: {root.resolve()}")
        file_count = sum(1 for _ in root.rglob("*") if _.is_file())
        dir_count = sum(1 for _ in root.rglob("*") if _.is_dir())
        info(f"Created {dir_count} directories and {file_count} files")

    print()
    print(f"{GREEN}{BOLD}Project scaffolded successfully!{RESET}")
    print()
    print(f"{BOLD}Next steps:{RESET}")
    print(f"  1. cd {root.name}")
    print(f"  2. Edit {CYAN}.bmad/project-context.md{RESET} — fill in your project constitution")
    print(f"  3. Start Phase 1: activate the Mary/Analyst agent to create a product brief")
    if project_type == "brownfield":
        print(f"  4. Run the {CYAN}Document Project{RESET} workflow to populate project-knowledge/")
    print()


if __name__ == "__main__":
    main()
