#!/usr/bin/env python3
"""
validate_project.py — Validate BMAD project completeness.

Usage:
    python validate_project.py [project-root]
    python validate_project.py --self-check

Checks:
  - Required directories exist
  - project-context.md exists and has required sections
  - Artifact files have valid YAML frontmatter
  - Reports completeness percentage by phase

Self-check mode validates the BMAD skill installation itself.
"""

import argparse
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# ANSI colours
# ---------------------------------------------------------------------------
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"

PASS = f"{GREEN}PASS{RESET}"
WARN = f"{YELLOW}WARN{RESET}"
FAIL = f"{RED}FAIL{RESET}"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_frontmatter(filepath: Path) -> dict:
    """Extract YAML frontmatter from a markdown file as a simple dict.

    Handles basic key: value pairs (no nesting needed for validation).
    Returns empty dict if no frontmatter found.
    """
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return {}

    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}

    fm: dict = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm


def has_heading(filepath: Path, heading: str) -> bool:
    """Check if a markdown file contains a specific H2 heading."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return False
    pattern = rf"^##\s+{re.escape(heading)}\s*$"
    return bool(re.search(pattern, text, re.MULTILINE))


# ---------------------------------------------------------------------------
# Phase completeness checks
# ---------------------------------------------------------------------------

REQUIRED_DIRS = [
    ".bmad",
    "planning_artifacts",
    "architecture",
    "architecture/adr",
    "epics",
    "stories",
    "sprints",
]

CONTEXT_REQUIRED_SECTIONS = [
    "Vision",
    "Tech Stack",
    "Constraints",
    "Conventions",
    "Team",
    "Links",
]

PHASE_ARTIFACTS = {
    "Phase 1 — Analysis": [
        ("planning_artifacts/product-brief.md", ["title"]),
    ],
    "Phase 2 — Planning": [
        ("planning_artifacts/PRD.md", ["title", "status"]),
        ("planning_artifacts/ux-spec.md", []),
    ],
    "Phase 3 — Solutioning": [
        ("architecture/architecture.md", ["title", "status"]),
    ],
    "Phase 4 — Implementation": [],
}


def validate_directories(root: Path) -> list:
    """Check that all required directories exist."""
    results = []
    for d in REQUIRED_DIRS:
        path = root / d
        exists = path.is_dir()
        results.append({
            "check": f"Directory {d}/",
            "status": "pass" if exists else "fail",
            "detail": "exists" if exists else "missing",
        })
    return results


def validate_project_context(root: Path) -> list:
    """Validate .bmad/project-context.md exists and has required sections."""
    results = []
    ctx = root / ".bmad" / "project-context.md"

    if not ctx.is_file():
        results.append({
            "check": "project-context.md",
            "status": "fail",
            "detail": "File not found at .bmad/project-context.md",
        })
        return results

    results.append({
        "check": "project-context.md exists",
        "status": "pass",
        "detail": str(ctx.relative_to(root)),
    })

    # Check frontmatter
    fm = extract_frontmatter(ctx)
    if fm.get("project-name"):
        results.append({
            "check": "project-context.md frontmatter",
            "status": "pass",
            "detail": f"project-name: {fm['project-name']}",
        })
    else:
        results.append({
            "check": "project-context.md frontmatter",
            "status": "warn",
            "detail": "Missing or empty project-name in frontmatter",
        })

    # Check required sections
    for section in CONTEXT_REQUIRED_SECTIONS:
        found = has_heading(ctx, section)
        if found:
            results.append({
                "check": f"Section: ## {section}",
                "status": "pass",
                "detail": "present",
            })
        else:
            results.append({
                "check": f"Section: ## {section}",
                "status": "warn",
                "detail": "missing — fill in this section",
            })

    return results


def validate_config(root: Path) -> list:
    """Validate .bmad/config.yaml exists."""
    results = []
    cfg = root / ".bmad" / "config.yaml"
    if cfg.is_file():
        results.append({
            "check": "config.yaml",
            "status": "pass",
            "detail": "exists",
        })
    else:
        results.append({
            "check": "config.yaml",
            "status": "warn",
            "detail": "Missing .bmad/config.yaml — run init_project.py to create",
        })
    return results


def validate_phase_artifacts(root: Path) -> dict:
    """Check artifact presence per phase. Returns dict of phase -> results."""
    phase_results = {}
    for phase, artifacts in PHASE_ARTIFACTS.items():
        results = []
        if not artifacts:
            results.append({
                "check": "Sprint/story files",
                "status": "info",
                "detail": "Check stories/ and sprints/ for content",
            })
        for rel_path, expected_fm_keys in artifacts:
            path = root / rel_path
            if not path.is_file():
                results.append({
                    "check": rel_path,
                    "status": "warn",
                    "detail": "not yet created",
                })
                continue

            results.append({
                "check": rel_path,
                "status": "pass",
                "detail": "exists",
            })

            if expected_fm_keys:
                fm = extract_frontmatter(path)
                for key in expected_fm_keys:
                    val = fm.get(key, "")
                    if val and val != "TODO":
                        results.append({
                            "check": f"  {rel_path} -> {key}",
                            "status": "pass",
                            "detail": val,
                        })
                    else:
                        results.append({
                            "check": f"  {rel_path} -> {key}",
                            "status": "warn",
                            "detail": "missing or TODO",
                        })

        phase_results[phase] = results

    # Check for epics and stories dynamically
    epics = list((root / "epics").glob("*.md")) if (root / "epics").is_dir() else []
    stories = list((root / "stories").glob("*.md")) if (root / "stories").is_dir() else []

    phase_results["Phase 3 — Solutioning"].append({
        "check": f"Epics ({len(epics)} files)",
        "status": "pass" if epics else "warn",
        "detail": f"{len(epics)} epic(s) found" if epics else "no epics yet",
    })
    phase_results["Phase 3 — Solutioning"].append({
        "check": f"Stories ({len(stories)} files)",
        "status": "pass" if stories else "warn",
        "detail": f"{len(stories)} story(ies) found" if stories else "no stories yet",
    })

    return phase_results


def validate_story_frontmatter(root: Path) -> list:
    """Validate that story files have proper YAML frontmatter."""
    results = []
    stories_dir = root / "stories"
    if not stories_dir.is_dir():
        return results

    for story_file in sorted(stories_dir.glob("*.md")):
        fm = extract_frontmatter(story_file)
        name = story_file.name
        if not fm:
            results.append({
                "check": f"stories/{name} frontmatter",
                "status": "warn",
                "detail": "no YAML frontmatter found",
            })
            continue

        required = ["story-id", "title", "status"]
        missing = [k for k in required if not fm.get(k)]
        if missing:
            results.append({
                "check": f"stories/{name} frontmatter",
                "status": "warn",
                "detail": f"missing keys: {', '.join(missing)}",
            })
        else:
            results.append({
                "check": f"stories/{name} frontmatter",
                "status": "pass",
                "detail": f"{fm.get('story-id', '?')} — {fm.get('status', '?')}",
            })

    return results


# ---------------------------------------------------------------------------
# Self-check mode
# ---------------------------------------------------------------------------

def self_check() -> None:
    """Validate the BMAD skill installation itself."""
    skill_dir = Path(__file__).resolve().parent.parent
    print(f"\n{BOLD}BMAD Skill Self-Check{RESET}")
    print(f"  Skill dir: {skill_dir}\n")

    expected_files = [
        "SKILL.md",
        "references/schemas.md",
        "references/methodology-overview.md",
        "templates/project-context.md.tmpl",
    ]

    expected_agents = [
        "agents/mary-analyst.md",
        "agents/john-pm.md",
        "agents/sally-ux.md",
        "agents/winston-architect.md",
        "agents/bob-scrum-master.md",
        "agents/amelia-developer.md",
        "agents/quinn-qa.md",
        "agents/barry-quick-flow.md",
        "agents/orchestrator.md",
        "agents/gate-reviewer.md",
    ]

    expected_scripts = [
        "scripts/init_project.py",
        "scripts/validate_project.py",
        "scripts/validate_prd.py",
        "scripts/scaffold_agent.py",
        "scripts/scaffold_workflow.py",
        "scripts/generate_sprint_status.py",
        "scripts/check_artifact_flow.py",
        "scripts/export_project_report.py",
    ]

    all_expected = expected_files + expected_agents + expected_scripts
    passed = 0
    failed = 0

    for rel in all_expected:
        path = skill_dir / rel
        if path.is_file():
            print(f"  {PASS}  {rel}")
            passed += 1
        else:
            print(f"  {FAIL}  {rel}")
            failed += 1

    total = passed + failed
    print(f"\n  {BOLD}Result{RESET}: {passed}/{total} files present")
    if failed:
        print(f"  {YELLOW}Missing {failed} file(s) — skill installation is incomplete.{RESET}")
        sys.exit(1)
    else:
        print(f"  {GREEN}Skill installation is complete.{RESET}")
    print()


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

STATUS_ICON = {
    "pass": f"{GREEN}*{RESET}",
    "warn": f"{YELLOW}~{RESET}",
    "fail": f"{RED}x{RESET}",
    "info": f"{CYAN}i{RESET}",
}


def print_results(label: str, results: list) -> tuple:
    """Print a results section, return (pass_count, total_count)."""
    if not results:
        return (0, 0)

    print(f"  {BOLD}{label}{RESET}")
    p = 0
    t = 0
    for r in results:
        icon = STATUS_ICON.get(r["status"], " ")
        t += 1
        if r["status"] == "pass":
            p += 1
        detail = f" {DIM}— {r['detail']}{RESET}" if r.get("detail") else ""
        print(f"    {icon} {r['check']}{detail}")
    print()
    return (p, t)


def validate_project(root: Path) -> int:
    """Run full project validation. Returns exit code."""
    print(f"\n{BOLD}BMAD Project Validation{RESET}")
    print(f"  Project root: {root}\n")

    total_pass = 0
    total_checks = 0

    # Directory structure
    p, t = print_results("Directory Structure", validate_directories(root))
    total_pass += p
    total_checks += t

    # Project context
    p, t = print_results("Project Context", validate_project_context(root))
    total_pass += p
    total_checks += t

    # Config
    p, t = print_results("Configuration", validate_config(root))
    total_pass += p
    total_checks += t

    # Phase artifacts
    phase_results = validate_phase_artifacts(root)
    for phase, results in phase_results.items():
        p, t = print_results(phase, results)
        total_pass += p
        total_checks += t

    # Story frontmatter
    story_results = validate_story_frontmatter(root)
    if story_results:
        p, t = print_results("Story Frontmatter Validation", story_results)
        total_pass += p
        total_checks += t

    # Summary
    pct = (total_pass / total_checks * 100) if total_checks else 0
    bar_len = 30
    filled = int(bar_len * pct / 100)
    bar = f"{'#' * filled}{'.' * (bar_len - filled)}"

    color = GREEN if pct >= 80 else YELLOW if pct >= 50 else RED
    print(f"  {BOLD}Completeness{RESET}: [{color}{bar}{RESET}] {pct:.0f}%")
    print(f"  {total_pass}/{total_checks} checks passed\n")

    return 0 if pct >= 80 else 1


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate BMAD project completeness.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_project.py                    # Validate current directory
  python validate_project.py ./my-project       # Validate a specific project
  python validate_project.py --self-check       # Validate BMAD skill installation
  python validate_project.py . --verbose        # Show detailed check output

Exit codes:
  0  Completeness >= 80%
  1  Completeness < 80% (warnings present)
  2  Error (invalid directory or critical failure)
        """,
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="Path to BMAD project root (default: current directory)",
    )
    parser.add_argument(
        "--self-check",
        action="store_true",
        help="Validate the BMAD skill installation itself",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List checks that would be performed without running them",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output for each check including file paths",
    )
    args = parser.parse_args()

    if args.self_check:
        self_check()
        return

    root = Path(args.project_root).resolve()
    if not root.is_dir():
        print(
            f"{RED}[err]{RESET} Not a directory: {root}\n"
            f"  Fix: provide a valid path to a BMAD project directory.\n"
            f"  Example: python validate_project.py ./my-project",
            file=sys.stderr,
        )
        sys.exit(2)

    if args.dry_run:
        print(f"\n{BOLD}Checks that would be performed on: {root}{RESET}\n")
        checks = [
            "Directory structure (7 required directories)",
            "project-context.md existence and sections",
            "config.yaml existence",
            "Phase 1 artifacts (product-brief.md)",
            "Phase 2 artifacts (PRD.md, ux-spec.md)",
            "Phase 3 artifacts (architecture.md, epics, stories)",
            "Phase 4 artifacts (sprint files)",
            "Story frontmatter validation",
        ]
        for c in checks:
            print(f"  {CYAN}*{RESET} {c}")
        print(f"\n{YELLOW}Dry run complete. No checks were executed.{RESET}\n")
        sys.exit(0)

    # Quick sanity: check for .bmad/ to confirm it's a BMAD project
    if not (root / ".bmad").is_dir():
        print(f"{YELLOW}[warn]{RESET} No .bmad/ directory found. Is this a BMAD project?")
        print(f"       Fix: run 'python init_project.py <name>' to scaffold one.\n")

    code = validate_project(root)
    sys.exit(code)


if __name__ == "__main__":
    main()
