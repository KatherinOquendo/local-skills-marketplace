#!/usr/bin/env python3
"""
export_project_report.py — Export BMAD project state as a markdown report.

Usage:
    python export_project_report.py <project-root>
    python export_project_report.py <project-root> --output report.md

Generates a comprehensive report covering:
  - Project overview (from project-context.md)
  - Phase progress
  - Artifact inventory
  - Gate status (if gate-result.json exists)
  - Sprint velocity
  - Blockers
  - Team allocation
"""

import argparse
import json
import re
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
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_frontmatter(filepath: Path) -> dict:
    """Extract simple key-value YAML frontmatter."""
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
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm


def read_file(filepath: Path) -> str:
    try:
        return filepath.read_text(encoding="utf-8")
    except Exception:
        return ""


def read_json(filepath: Path) -> dict:
    try:
        return json.loads(filepath.read_text(encoding="utf-8"))
    except Exception:
        return {}


def parse_simple_yaml(filepath: Path) -> dict:
    """Parse a simple flat YAML file into a dict (handles basic nesting)."""
    result: dict = {}
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return result

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("-"):
            continue
        if ":" in stripped:
            key, _, val = stripped.partition(":")
            val = val.strip().strip('"').strip("'")
            if val:
                result[key.strip()] = val
    return result


def count_files(directory: Path, pattern: str = "*.md") -> int:
    """Count files matching a pattern in a directory."""
    if not directory.is_dir():
        return 0
    return len(list(directory.glob(pattern)))


# ---------------------------------------------------------------------------
# Report sections
# ---------------------------------------------------------------------------

def section_overview(root: Path) -> str:
    """Generate project overview section."""
    ctx = root / ".bmad" / "project-context.md"
    fm = extract_frontmatter(ctx) if ctx.is_file() else {}
    cfg = parse_simple_yaml(root / ".bmad" / "config.yaml")

    project_name = fm.get("project-name", cfg.get("name", root.name))
    version = fm.get("version", cfg.get("version", "0.1.0"))
    project_type = cfg.get("type", "unknown")
    created = fm.get("created", "unknown")

    lines = [
        "## Project Overview",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| **Name** | {project_name} |",
        f"| **Version** | {version} |",
        f"| **Type** | {project_type} |",
        f"| **Created** | {created} |",
        f"| **Report Date** | {date.today().isoformat()} |",
        "",
    ]

    # Extract vision if available
    if ctx.is_file():
        text = read_file(ctx)
        vision_match = re.search(
            r"##\s+Vision\s*\n+(.*?)(?=\n##|\Z)", text, re.DOTALL
        )
        if vision_match:
            vision = vision_match.group(1).strip()
            if vision and "TODO" not in vision:
                lines.extend(["### Vision", "", vision, ""])

    return "\n".join(lines)


def section_phase_progress(root: Path) -> str:
    """Generate phase progress section."""
    brief = (root / "planning_artifacts" / "product-brief.md").is_file()
    prd = (root / "planning_artifacts" / "PRD.md").is_file()
    ux = (root / "planning_artifacts" / "ux-spec.md").is_file()
    arch = (root / "architecture" / "architecture.md").is_file()
    adrs = count_files(root / "architecture" / "adr")
    epics = count_files(root / "epics")
    stories = count_files(root / "stories")
    sprints = count_files(root / "sprints", "*.yaml")

    def status_icon(done: bool) -> str:
        return "done" if done else "pending"

    phases = [
        ("Phase 1: Analysis", [
            (f"Product Brief", brief),
        ]),
        ("Phase 2: Planning", [
            (f"PRD", prd),
            (f"UX Spec", ux),
        ]),
        ("Phase 3: Solutioning", [
            (f"Architecture", arch),
            (f"ADRs ({adrs})", adrs > 0),
            (f"Epics ({epics})", epics > 0),
            (f"Stories ({stories})", stories > 0),
        ]),
        ("Phase 4: Implementation", [
            (f"Sprint configs ({sprints})", sprints > 0),
        ]),
    ]

    lines = ["## Phase Progress", ""]

    for phase_name, checks in phases:
        done = sum(1 for _, ok in checks if ok)
        total = len(checks)
        pct = int(done / total * 100) if total else 0
        bar_len = 20
        filled = int(bar_len * pct / 100)
        bar = f"{'#' * filled}{'.' * (bar_len - filled)}"

        lines.append(f"### {phase_name} [{bar}] {pct}%")
        lines.append("")
        for label, ok in checks:
            icon = "- [x]" if ok else "- [ ]"
            lines.append(f"{icon} {label}")
        lines.append("")

    return "\n".join(lines)


def section_artifact_inventory(root: Path) -> str:
    """Generate artifact inventory section."""
    lines = ["## Artifact Inventory", ""]

    dirs_to_scan = [
        ("planning_artifacts", "*.md"),
        ("architecture", "*.md"),
        ("architecture/adr", "*.md"),
        ("epics", "*.md"),
        ("stories", "*.md"),
        ("sprints", "*.yaml"),
    ]

    lines.append("| Directory | File | Status | Last Modified |")
    lines.append("|-----------|------|--------|---------------|")

    total = 0
    for dir_rel, pattern in dirs_to_scan:
        d = root / dir_rel
        if not d.is_dir():
            continue
        for f in sorted(d.glob(pattern)):
            if f.name.startswith("."):
                continue
            total += 1
            fm = extract_frontmatter(f) if f.suffix == ".md" else {}
            status = fm.get("status", "—")
            # Get modification time
            try:
                mtime = date.fromtimestamp(f.stat().st_mtime).isoformat()
            except Exception:
                mtime = "—"
            lines.append(f"| `{dir_rel}/` | {f.name} | {status} | {mtime} |")

    lines.extend(["", f"**Total artifacts**: {total}", ""])
    return "\n".join(lines)


def section_gate_status(root: Path) -> str:
    """Generate gate status section from gate-result.json."""
    gate_file = root / "sprints" / "gate-result.json"
    if not gate_file.is_file():
        return "## Implementation Readiness Gate\n\n*Gate has not been run yet. Use `validate_prd.py` to run the 13-step check.*\n"

    gate = read_json(gate_file)
    if not gate:
        return "## Implementation Readiness Gate\n\n*Gate result file exists but could not be parsed.*\n"

    lines = [
        "## Implementation Readiness Gate",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| **Result** | {gate.get('result', '?')} |",
        f"| **Date** | {gate.get('date', '?')} |",
        f"| **Passed** | {gate.get('summary', {}).get('passed', '?')}/13 |",
        f"| **Warnings** | {gate.get('summary', {}).get('warnings', '?')} |",
        f"| **Failed** | {gate.get('summary', {}).get('failed', '?')} |",
        "",
    ]

    recommendation = gate.get("recommendation", "")
    if recommendation:
        lines.extend([f"> {recommendation}", ""])

    # Detail table
    checks = gate.get("checks", [])
    if checks:
        lines.append("| # | Check | Status |")
        lines.append("|---|-------|--------|")
        for c in checks:
            lines.append(f"| {c.get('step', '?')} | {c.get('name', '?')} | {c.get('status', '?')} |")
        lines.append("")

    return "\n".join(lines)


def section_sprint_status(root: Path) -> str:
    """Generate sprint velocity and status section."""
    sprint_file = root / "sprints" / "sprint-status.yaml"
    if not sprint_file.is_file():
        return "## Sprint Status\n\n*No active sprint. Use `generate_sprint_status.py` to create one.*\n"

    data = parse_simple_yaml(sprint_file)

    lines = [
        "## Sprint Status",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| **Sprint** | {data.get('number', '?')} |",
        f"| **Status** | {data.get('status', '?')} |",
        f"| **Start** | {data.get('start-date', '?')} |",
        f"| **End** | {data.get('end-date', '?')} |",
        f"| **Total Points** | {data.get('total-points', '?')} |",
        f"| **Completed Points** | {data.get('completed-points', '?')} |",
        f"| **Velocity** | {data.get('velocity', '?')} |",
        "",
    ]

    # Try to extract story list from the raw YAML
    raw = read_file(sprint_file)
    story_blocks = re.findall(
        r'-\s+id:\s*"?([^"\n]+)"?\s*\n\s+title:\s*"?([^"\n]+)"?\s*\n\s+status:\s*"?([^"\n]+)"?',
        raw,
    )
    if story_blocks:
        lines.append("### Stories in Sprint")
        lines.append("")
        lines.append("| ID | Title | Status |")
        lines.append("|----|-------|--------|")
        for sid, title, status in story_blocks:
            lines.append(f"| {sid} | {title} | {status} |")
        lines.append("")

    return "\n".join(lines)


def section_blockers(root: Path) -> str:
    """Generate blockers section."""
    sprint_file = root / "sprints" / "sprint-status.yaml"
    if not sprint_file.is_file():
        return ""

    raw = read_file(sprint_file)

    # Simple extraction of blocker entries
    blocker_blocks = re.findall(
        r'-\s+id:\s*"?([^"\n]+)"?\s*\n\s+description:\s*"?([^"\n]+)"?\s*\n\s+severity:\s*"?([^"\n]+)"?',
        raw,
    )

    if not blocker_blocks:
        return "## Blockers\n\n*No blockers reported.*\n"

    lines = [
        "## Blockers",
        "",
        "| ID | Description | Severity |",
        "|----|-------------|----------|",
    ]
    for bid, desc, sev in blocker_blocks:
        lines.append(f"| {bid} | {desc} | {sev} |")
    lines.append("")
    return "\n".join(lines)


def section_team_allocation(root: Path) -> str:
    """Generate team allocation section from story assignments."""
    stories_dir = root / "stories"
    if not stories_dir.is_dir():
        return "## Team Allocation\n\n*No stories found to analyze allocation.*\n"

    allocation: dict = {}
    for sf in stories_dir.glob("*.md"):
        fm = extract_frontmatter(sf)
        assigned = fm.get("assigned-to", "unassigned")
        status = fm.get("status", "unknown")
        pts = 0
        try:
            pts = int(fm.get("points", "0"))
        except ValueError:
            pass

        if assigned not in allocation:
            allocation[assigned] = {"stories": 0, "points": 0, "statuses": {}}
        allocation[assigned]["stories"] += 1
        allocation[assigned]["points"] += pts
        allocation[assigned]["statuses"][status] = allocation[assigned]["statuses"].get(status, 0) + 1

    if not allocation:
        return "## Team Allocation\n\n*No story assignments found.*\n"

    lines = [
        "## Team Allocation",
        "",
        "| Assignee | Stories | Points | Status Breakdown |",
        "|----------|---------|--------|-----------------|",
    ]
    for assignee, data in sorted(allocation.items()):
        status_str = ", ".join(f"{k}: {v}" for k, v in sorted(data["statuses"].items()))
        lines.append(f"| {assignee} | {data['stories']} | {data['points']} | {status_str} |")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------

def generate_report(root: Path) -> str:
    """Generate the full project report."""
    ctx_fm = extract_frontmatter(root / ".bmad" / "project-context.md")
    project_name = ctx_fm.get("project-name", root.name)

    sections = [
        f"# {project_name} — BMAD Project Report",
        "",
        f"> Generated: {date.today().isoformat()}",
        f"> Project root: `{root}`",
        "",
        "---",
        "",
        section_overview(root),
        section_phase_progress(root),
        section_artifact_inventory(root),
        section_gate_status(root),
        section_sprint_status(root),
        section_blockers(root),
        section_team_allocation(root),
        "---",
        "",
        f"*Report generated by BMAD `export_project_report.py` on {date.today().isoformat()}.*",
        "",
    ]

    return "\n".join(sections)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export BMAD project state as a markdown report.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python export_project_report.py                         # Report for current dir
  python export_project_report.py ./my-project            # Report for specific project
  python export_project_report.py . -o status.md          # Custom output file
  python export_project_report.py . --dry-run             # Preview sections
  python export_project_report.py . --verbose             # Show section details

Exit codes:
  0  Success — report generated
  1  Warning — report generated with incomplete data
  2  Error — could not generate report
        """,
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="Path to BMAD project root (default: current directory)",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output file path (default: <project-root>/report.md)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview report sections without writing the file",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed artifact counts and section sizes",
    )

    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    if not root.is_dir():
        print(
            f"{RED}[err]{RESET} Not a directory: {root}\n"
            f"  Fix: provide a valid path to a BMAD project root.",
            file=sys.stderr,
        )
        sys.exit(2)

    # Check this is a BMAD project
    if not (root / ".bmad").is_dir():
        print(
            f"{YELLOW}[warn]{RESET} No .bmad/ directory found. Is this a BMAD project?\n"
            f"       Fix: run 'python init_project.py <name>' to scaffold one."
        )

    if args.dry_run:
        print(f"\n{BOLD}Dry Run — Report Sections{RESET}\n")
        sections = [
            "Project Overview (from project-context.md)",
            "Phase Progress (artifact presence check)",
            "Artifact Inventory (file listing with status)",
            "Implementation Readiness Gate (from gate-result.json)",
            "Sprint Status (from sprint-status.yaml)",
            "Blockers (from sprint-status.yaml)",
            "Team Allocation (from story assignments)",
        ]
        for s in sections:
            print(f"  {CYAN}*{RESET} {s}")
        print(f"\n{YELLOW}Dry run complete. No report was generated.{RESET}\n")
        sys.exit(0)

    print(f"\n{BOLD}Generating BMAD Project Report{RESET}")
    print(f"  Project: {root}\n")

    report = generate_report(root)

    # Determine output path
    if args.output:
        out_path = Path(args.output)
        if not out_path.is_absolute():
            out_path = root / out_path
    else:
        out_path = root / "report.md"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")

    # Count report stats
    line_count = report.count("\n")
    section_count = report.count("\n## ")

    print(f"  {GREEN}[ok]{RESET} Report written to {out_path}")
    print(f"  {DIM}{line_count} lines, {section_count} sections{RESET}")
    print()


if __name__ == "__main__":
    main()
