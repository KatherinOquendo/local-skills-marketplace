#!/usr/bin/env python3
"""
generate_sprint_status.py — Create/update sprint-status.yaml.

Usage:
    python generate_sprint_status.py <project-root> --sprint N
    python generate_sprint_status.py . --sprint 1
    python generate_sprint_status.py ./my-project --sprint 3

Scans the stories/ directory, extracts status and metadata from YAML
frontmatter, and creates a sprint-status.yaml file in sprints/ with
story data populated per the BMAD sprint status schema.
"""

import argparse
import re
import sys
from datetime import date, timedelta
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
    """Extract YAML frontmatter as simple key-value dict."""
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


def yaml_escape(val: str) -> str:
    """Escape a string for YAML output."""
    if not val:
        return '""'
    if any(c in val for c in ":#{}[]|>&*!%@`"):
        return f'"{val}"'
    return f'"{val}"'


# ---------------------------------------------------------------------------
# Story scanner
# ---------------------------------------------------------------------------

def scan_stories(stories_dir: Path, sprint_number: int) -> list:
    """Scan story files and return those assigned to the given sprint."""
    stories = []
    if not stories_dir.is_dir():
        return stories

    for filepath in sorted(stories_dir.glob("*.md")):
        fm = extract_frontmatter(filepath)
        if not fm:
            continue

        # Include story if it matches the sprint or has no sprint assigned
        story_sprint = fm.get("sprint", "")
        try:
            story_sprint_num = int(story_sprint) if story_sprint else 0
        except ValueError:
            story_sprint_num = 0

        if story_sprint_num == sprint_number or (story_sprint_num == 0 and sprint_number == 1):
            story_id = fm.get("story-id", filepath.stem)
            stories.append({
                "id": story_id,
                "title": fm.get("title", filepath.stem.replace("-", " ").title()),
                "status": fm.get("status", "todo"),
                "points": fm.get("points", "0"),
                "assigned_to": fm.get("assigned-to", "unassigned"),
                "priority": fm.get("priority", "medium"),
                "epic_ref": fm.get("epic-ref", ""),
                "file": filepath.name,
            })

    return stories


def scan_all_stories(stories_dir: Path) -> list:
    """Scan all story files regardless of sprint assignment."""
    stories = []
    if not stories_dir.is_dir():
        return stories

    for filepath in sorted(stories_dir.glob("*.md")):
        fm = extract_frontmatter(filepath)
        if not fm:
            continue
        story_id = fm.get("story-id", filepath.stem)
        stories.append({
            "id": story_id,
            "title": fm.get("title", filepath.stem.replace("-", " ").title()),
            "status": fm.get("status", "todo"),
            "points": fm.get("points", "0"),
            "assigned_to": fm.get("assigned-to", "unassigned"),
            "priority": fm.get("priority", "medium"),
            "epic_ref": fm.get("epic-ref", ""),
            "sprint": fm.get("sprint", ""),
            "file": filepath.name,
        })

    return stories


# ---------------------------------------------------------------------------
# Sprint YAML generation
# ---------------------------------------------------------------------------

STATUS_MAP = {
    "draft": "todo",
    "ready": "todo",
    "in-progress": "in-progress",
    "review": "review",
    "done": "done",
    "blocked": "blocked",
}


def generate_sprint_yaml(sprint_number: int, stories: list) -> str:
    """Generate sprint-status.yaml content."""
    today = date.today()
    end = today + timedelta(days=14)  # 2-week sprint default

    total_points = 0
    completed_points = 0

    story_blocks = []
    for s in stories:
        pts = 0
        try:
            pts = int(s["points"])
        except (ValueError, TypeError):
            pass
        total_points += pts

        status = STATUS_MAP.get(s["status"], s["status"])
        if status == "done":
            completed_points += pts

        branch = f"feature/{s['id'].lower()}"

        story_blocks.append(
            f'  - id: "{s["id"]}"\n'
            f'    title: {yaml_escape(s["title"])}\n'
            f'    status: "{status}"\n'
            f'    points: {pts}\n'
            f'    assigned-to: "{s["assigned_to"]}"\n'
            f'    branch: "{branch}"\n'
            f'    notes: ""'
        )

    stories_yaml = "\n".join(story_blocks) if story_blocks else "  []"

    velocity = completed_points  # First sprint, velocity = completed

    return f"""# Sprint Status — Sprint {sprint_number}
# Generated: {today.isoformat()}
# Schema: references/schemas.md > Sprint Status Schema

sprint:
  number: {sprint_number}
  start-date: "{today.isoformat()}"
  end-date: "{end.isoformat()}"
  goal: "TODO: Define the sprint goal"
  status: "planning"

stories:
{stories_yaml}

metrics:
  total-points: {total_points}
  completed-points: {completed_points}
  velocity: {velocity}
  burndown:
    - date: "{today.isoformat()}"
      remaining: {total_points}

blockers: []
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create/update sprint-status.yaml from story files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_sprint_status.py . --sprint 1        # Generate sprint 1 status
  python generate_sprint_status.py . --sprint 2 --all  # Include all stories
  python generate_sprint_status.py . --sprint 1 --dry-run  # Preview only

Exit codes:
  0  Success — sprint status file created
  1  Warning — created but with issues (e.g., no stories found)
  2  Error — could not create (invalid directory, missing stories/)
        """,
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="Path to BMAD project root (default: current directory)",
    )
    parser.add_argument(
        "--sprint", "-n",
        type=int,
        required=True,
        help="Sprint number to generate status for",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Include all stories regardless of sprint assignment",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview sprint status without writing files",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed story scanning output",
    )

    args = parser.parse_args()

    if args.sprint < 1:
        print(
            f"{RED}[err]{RESET} Sprint number must be >= 1.\n"
            f"  Fix: use --sprint with a positive integer.",
            file=sys.stderr,
        )
        sys.exit(2)

    root = Path(args.project_root).resolve()
    if not root.is_dir():
        print(
            f"{RED}[err]{RESET} Not a directory: {root}\n"
            f"  Fix: provide a valid path to a BMAD project root.",
            file=sys.stderr,
        )
        sys.exit(2)

    stories_dir = root / "stories"
    sprints_dir = root / "sprints"

    if not stories_dir.is_dir():
        print(
            f"{RED}[err]{RESET} stories/ directory not found in {root}\n"
            f"  Fix: ensure you are in a BMAD project root, or run init_project.py first.",
            file=sys.stderr,
        )
        sys.exit(2)

    if not sprints_dir.is_dir():
        sprints_dir.mkdir(parents=True)
        print(f"{CYAN}[info]{RESET} Created sprints/ directory")

    sprint_number = args.sprint

    # Scan stories
    if args.all:
        all_stories = scan_all_stories(stories_dir)
        stories = all_stories
        print(f"{CYAN}[info]{RESET} Including all {len(stories)} stories")
    else:
        stories = scan_stories(stories_dir, sprint_number)

    print(f"\n{BOLD}Sprint {sprint_number} Status Generation{RESET}")
    print(f"  Project  : {root}")
    print(f"  Stories  : {len(stories)} found for sprint {sprint_number}")
    print()

    if not stories:
        print(f"{YELLOW}[warn]{RESET} No stories found for sprint {sprint_number}.")
        print(f"       Assign stories to this sprint by setting 'sprint: {sprint_number}' in their frontmatter.")
        print(f"       Or use --all to include all stories.\n")

    # List stories
    for s in stories:
        status_color = GREEN if s["status"] == "done" else YELLOW if s["status"] in ("in-progress", "review") else RED if s["status"] == "blocked" else ""
        status_reset = RESET if status_color else ""
        print(f"    {s['id']:12s} {status_color}{s['status']:12s}{status_reset} [{s['points']:>2s} pts] {s['title']}")

    if stories:
        print()

    # Generate YAML
    yaml_content = generate_sprint_yaml(sprint_number, stories)

    if args.dry_run:
        print(f"\n{YELLOW}Dry run — preview of sprint-status.yaml:{RESET}")
        for line in yaml_content.splitlines()[:20]:
            print(f"  {DIM}{line}{RESET}")
        if yaml_content.count("\n") > 20:
            print(f"  {DIM}... ({yaml_content.count(chr(10))} total lines){RESET}")
        print(f"\n{YELLOW}Dry run complete. No files were written.{RESET}\n")
        sys.exit(0)

    out_path = sprints_dir / f"sprint-{sprint_number:02d}-status.yaml"
    out_path.write_text(yaml_content, encoding="utf-8")
    print(f"{GREEN}[ok]{RESET} Written to {out_path.relative_to(root)}")

    # Also write/overwrite a current sprint symlink-like file
    current = sprints_dir / "sprint-status.yaml"
    current.write_text(yaml_content, encoding="utf-8")
    print(f"{GREEN}[ok]{RESET} Updated  {current.relative_to(root)} (current)")

    total_pts = sum(int(s["points"]) for s in stories if s["points"].isdigit())
    print(f"\n  {BOLD}Total points{RESET}: {total_pts}")
    print(f"  {BOLD}Sprint goal{RESET} : TODO — edit sprint-status.yaml to set the goal\n")


if __name__ == "__main__":
    main()
