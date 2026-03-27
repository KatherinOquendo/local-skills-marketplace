#!/usr/bin/env python3
"""
lint_artifacts.py — Lint all BMAD artifacts in a project for quality issues.

Usage:
    python lint_artifacts.py <project-root>
    python lint_artifacts.py <project-root> --fix
    python lint_artifacts.py <project-root> --verbose
    python lint_artifacts.py <project-root> --dry-run

Checks:
  - YAML frontmatter validity in all .md files
  - Required fields present per schema (references/schemas.md)
  - ID format validation (FR-NNN, STORY-NNN, EPIC-NNN, ADR-NNN)
  - Cross-reference integrity (story refs epic that exists, epic refs FR)
  - Orphan detection (stories not in any epic, FRs not in any story)
  - Staleness detection (files not modified in >30 days during active sprint)

Output: lint report with severity (Error/Warning/Info), file, line, message.
Zero external dependencies.
"""

import argparse
import re
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# ANSI colours (disabled when stdout is not a terminal)
# ---------------------------------------------------------------------------
_IS_TTY = sys.stdout.isatty()

def _c(code: str) -> str:
    return code if _IS_TTY else ""

GREEN = _c("\033[92m")
YELLOW = _c("\033[93m")
CYAN = _c("\033[96m")
RED = _c("\033[91m")
DIM = _c("\033[2m")
BOLD = _c("\033[1m")
RESET = _c("\033[0m")

# ---------------------------------------------------------------------------
# Severity
# ---------------------------------------------------------------------------
ERROR = "Error"
WARNING = "Warning"
INFO = "Info"

SEVERITY_COLOR = {ERROR: RED, WARNING: YELLOW, INFO: CYAN}
SEVERITY_ORDER = {ERROR: 0, WARNING: 1, INFO: 2}

# ---------------------------------------------------------------------------
# Finding dataclass (plain dict to avoid dataclasses import on older Pythons)
# ---------------------------------------------------------------------------

def finding(severity: str, filepath: str, line: int, message: str) -> dict:
    return {"severity": severity, "file": filepath, "line": line, "message": message}


# ---------------------------------------------------------------------------
# YAML frontmatter parser (zero dependencies)
# ---------------------------------------------------------------------------

def extract_frontmatter_raw(filepath: Path) -> tuple:
    """Return (frontmatter_dict, frontmatter_end_line, full_text).

    Parses simple and nested YAML. Handles:
      - key: value
      - key: (multiline list via '- item' on subsequent indented lines)
    Returns ({}, 0, "") on parse failure.
    """
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return {}, 0, ""

    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}, 0, text

    fm_text = match.group(1)
    fm_end_line = fm_text.count("\n") + 2  # +2 for opening/closing ---

    fm: dict = {}
    current_key = None
    current_list = None

    for raw_line in fm_text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Detect list item under current key
        if raw_line.startswith("  ") and stripped.startswith("- ") and current_key:
            if current_list is None:
                current_list = []
            item = stripped[2:].strip().strip('"').strip("'")
            current_list.append(item)
            fm[current_key] = current_list
            continue

        # Detect nested key: value under a parent (e.g., sprint-status stories)
        if raw_line.startswith("  ") and ":" in stripped and current_key:
            sub_key, _, sub_val = stripped.partition(":")
            sub_val = sub_val.strip().strip('"').strip("'")
            if isinstance(fm.get(current_key), dict):
                fm[current_key][sub_key.strip()] = sub_val
            elif isinstance(fm.get(current_key), list) and fm[current_key]:
                # Nested under last list item — skip (too complex for simple parser)
                pass
            continue

        # Top-level key: value
        if ":" in stripped:
            current_list = None
            key, _, val = stripped.partition(":")
            current_key = key.strip()
            val = val.strip().strip('"').strip("'")
            fm[current_key] = val if val else ""

    return fm, fm_end_line, text


def find_line_number(text: str, pattern: str) -> int:
    """Find the 1-based line number where pattern first appears. Returns 0 if not found."""
    for i, line in enumerate(text.splitlines(), 1):
        if pattern in line:
            return i
    return 0


# ---------------------------------------------------------------------------
# ID format patterns
# ---------------------------------------------------------------------------

RE_FR_ID = re.compile(r"^FR-[A-Z]+-\d{3}$")
RE_STORY_ID = re.compile(r"^STORY-[A-Z]+-\d{3}$")
RE_EPIC_ID = re.compile(r"^EPIC-\d{3}$")
RE_ADR_ID = re.compile(r"^ADR-\d{3}$")

VALID_STORY_POINTS = {1, 2, 3, 5, 8}
VALID_STORY_STATUSES = {"draft", "ready", "in-progress", "review", "done", "blocked"}
VALID_EPIC_STATUSES = {"draft", "ready", "in-progress", "done"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}

STALENESS_DAYS = 30


# ---------------------------------------------------------------------------
# Lint checks
# ---------------------------------------------------------------------------

def lint_frontmatter_presence(filepath: Path, fm: dict, text: str) -> list:
    """Check that markdown files in artifact directories have YAML frontmatter."""
    findings = []
    if not fm and text.strip():
        findings.append(finding(WARNING, str(filepath), 1,
                                "No YAML frontmatter found — BMAD artifacts require frontmatter"))
    return findings


def lint_story(filepath: Path, fm: dict, text: str, all_epics: set, all_frs: set) -> list:
    """Lint a single story file."""
    findings = []
    rel = filepath.name

    # Required fields
    required = {"story-id": RE_STORY_ID, "epic-ref": RE_EPIC_ID,
                "title": None, "status": None, "points": None, "priority": None}

    for key, pattern in required.items():
        val = fm.get(key, "")
        if not val:
            findings.append(finding(ERROR, rel, 1, f"Missing required field: {key}"))
            continue
        if pattern and not pattern.match(val):
            findings.append(finding(ERROR, rel, 1,
                                    f"Invalid {key} format: '{val}' — expected pattern {pattern.pattern}"))

    # Points validation
    points_str = fm.get("points", "")
    if points_str:
        try:
            points = int(points_str)
            if points == 13:
                findings.append(finding(ERROR, rel, 1,
                                        "Story estimated at 13 points — must be split (max 8)"))
            elif points not in VALID_STORY_POINTS:
                findings.append(finding(WARNING, rel, 1,
                                        f"Non-standard story points: {points} — expected one of {sorted(VALID_STORY_POINTS)}"))
        except ValueError:
            findings.append(finding(ERROR, rel, 1, f"Points is not an integer: '{points_str}'"))

    # Status validation
    status = fm.get("status", "")
    if status and status not in VALID_STORY_STATUSES:
        findings.append(finding(WARNING, rel, 1,
                                f"Unknown story status: '{status}' — expected one of {sorted(VALID_STORY_STATUSES)}"))

    # Priority validation
    priority = fm.get("priority", "")
    if priority and priority not in VALID_PRIORITIES:
        findings.append(finding(WARNING, rel, 1,
                                f"Unknown priority: '{priority}' — expected one of {sorted(VALID_PRIORITIES)}"))

    # Epic cross-reference
    epic_ref = fm.get("epic-ref", "")
    if epic_ref and all_epics and epic_ref not in all_epics:
        findings.append(finding(ERROR, rel, 1,
                                f"epic-ref '{epic_ref}' does not match any epic file"))

    # FR cross-reference
    fr_refs = fm.get("fr-refs", "")
    if isinstance(fr_refs, list):
        for fr in fr_refs:
            if not RE_FR_ID.match(fr):
                findings.append(finding(WARNING, rel, 1, f"FR reference has invalid format: '{fr}'"))
    elif isinstance(fr_refs, str) and fr_refs:
        if not RE_FR_ID.match(fr_refs):
            findings.append(finding(WARNING, rel, 1, f"FR reference has invalid format: '{fr_refs}'"))
    else:
        findings.append(finding(WARNING, rel, 1, "No fr-refs found — stories should trace to functional requirements"))

    # Acceptance criteria count
    ac_count_str = fm.get("acceptance-criteria-count", "")
    gwt_count = len(re.findall(r"(?i)^\s*\*?\*?Given\b", text, re.MULTILINE))
    if ac_count_str:
        try:
            ac_count = int(ac_count_str)
            if gwt_count > 0 and ac_count != gwt_count:
                findings.append(finding(WARNING, rel, 1,
                                        f"acceptance-criteria-count ({ac_count}) does not match "
                                        f"Given/When/Then blocks found ({gwt_count})"))
        except ValueError:
            pass
    if gwt_count == 0:
        findings.append(finding(WARNING, rel, 1,
                                "No Given/When/Then acceptance criteria found in story body"))

    return findings


def lint_epic(filepath: Path, fm: dict) -> list:
    """Lint a single epic file."""
    findings = []
    rel = filepath.name

    epic_id = fm.get("epic-id", "")
    if not epic_id:
        findings.append(finding(ERROR, rel, 1, "Missing required field: epic-id"))
    elif not RE_EPIC_ID.match(epic_id):
        findings.append(finding(ERROR, rel, 1,
                                f"Invalid epic-id format: '{epic_id}' — expected EPIC-NNN"))

    if not fm.get("title"):
        findings.append(finding(ERROR, rel, 1, "Missing required field: title"))

    status = fm.get("status", "")
    if status and status not in VALID_EPIC_STATUSES:
        findings.append(finding(WARNING, rel, 1,
                                f"Unknown epic status: '{status}' — expected one of {sorted(VALID_EPIC_STATUSES)}"))

    priority = fm.get("priority", "")
    if priority and priority not in VALID_PRIORITIES:
        findings.append(finding(WARNING, rel, 1,
                                f"Unknown priority: '{priority}' — expected one of {sorted(VALID_PRIORITIES)}"))

    prd_refs = fm.get("prd-refs", "")
    if not prd_refs:
        findings.append(finding(WARNING, rel, 1,
                                "No prd-refs found — epics should reference functional requirements"))

    return findings


def lint_architecture(filepath: Path, fm: dict, text: str) -> list:
    """Lint the architecture document."""
    findings = []
    rel = filepath.name

    for key in ("title", "status"):
        if not fm.get(key):
            findings.append(finding(ERROR, rel, 1, f"Missing required frontmatter field: {key}"))

    if not fm.get("prd-ref"):
        findings.append(finding(WARNING, rel, 1,
                                "Missing prd-ref — architecture should reference the PRD"))

    # Check for ADR references
    adrs_in_text = re.findall(r"ADR-\d{3}", text)
    if not adrs_in_text:
        findings.append(finding(INFO, rel, 1,
                                "No ADR references found in architecture document"))

    required_sections = [
        "System Overview", "Architecture Style", "Data Model",
        "API Design", "Security Architecture"
    ]
    for section in required_sections:
        if not re.search(rf"^##\s+.*{re.escape(section)}", text, re.MULTILINE | re.IGNORECASE):
            findings.append(finding(WARNING, rel,
                                    find_line_number(text, "## ") or 1,
                                    f"Missing expected section: {section}"))

    return findings


def lint_prd(filepath: Path, fm: dict, text: str) -> list:
    """Lint the PRD."""
    findings = []
    rel = filepath.name

    for key in ("title", "status", "version"):
        if not fm.get(key):
            findings.append(finding(ERROR, rel, 1, f"Missing required frontmatter field: {key}"))

    required_sections = [
        "Functional Requirements", "Non-Functional Requirements",
        "Success Metrics", "Scope"
    ]
    for section in required_sections:
        if not re.search(rf"^##\s+.*{re.escape(section)}", text, re.MULTILINE | re.IGNORECASE):
            findings.append(finding(WARNING, rel,
                                    find_line_number(text, "## ") or 1,
                                    f"Missing expected section: {section}"))

    # Check FR IDs exist
    fr_ids = re.findall(r"FR-[A-Z]+-\d{3}", text)
    if not fr_ids:
        findings.append(finding(WARNING, rel, 1,
                                "No FR-AREA-NNN identifiers found in PRD"))

    return findings


def lint_staleness(filepath: Path, active_sprint: bool) -> list:
    """Check if a file is stale (not modified in >30 days during an active sprint)."""
    if not active_sprint:
        return []
    try:
        mtime = filepath.stat().st_mtime
        age_days = (time.time() - mtime) / 86400
        if age_days > STALENESS_DAYS:
            return [finding(INFO, filepath.name, 0,
                            f"File not modified in {int(age_days)} days during active sprint — may be stale")]
    except OSError:
        pass
    return []


# ---------------------------------------------------------------------------
# Orphan detection
# ---------------------------------------------------------------------------

def detect_orphans(all_story_ids: dict, all_epic_ids: set,
                   story_epic_refs: dict, story_fr_refs: dict,
                   prd_fr_ids: set) -> list:
    """Detect orphan artifacts — stories without epics, FRs without stories."""
    findings = []

    # Stories not referencing any known epic
    for story_id, filepath in all_story_ids.items():
        epic_ref = story_epic_refs.get(story_id, "")
        if epic_ref and epic_ref not in all_epic_ids:
            findings.append(finding(WARNING, filepath, 1,
                                    f"Story {story_id} references epic '{epic_ref}' which does not exist"))

    # FRs in PRD not covered by any story
    all_story_frs = set()
    for fr_list in story_fr_refs.values():
        if isinstance(fr_list, list):
            all_story_frs.update(fr_list)
        elif isinstance(fr_list, str):
            all_story_frs.add(fr_list)

    for fr_id in sorted(prd_fr_ids):
        if fr_id not in all_story_frs:
            findings.append(finding(WARNING, "PRD", 0,
                                    f"FR {fr_id} has no story referencing it — potential orphan requirement"))

    return findings


# ---------------------------------------------------------------------------
# Auto-fix
# ---------------------------------------------------------------------------

def apply_fixes(filepath: Path, fm: dict, text: str) -> tuple:
    """Apply simple auto-fixes. Returns (fixed_text, fix_descriptions)."""
    fixes = []
    fixed = text

    # Fix: normalize story status casing
    status = fm.get("status", "")
    if status and status != status.lower() and status.lower() in VALID_STORY_STATUSES:
        fixed = fixed.replace(f"status: {status}", f"status: {status.lower()}", 1)
        fixes.append(f"Normalized status '{status}' -> '{status.lower()}'")

    # Fix: normalize priority casing
    priority = fm.get("priority", "")
    if priority and priority != priority.lower() and priority.lower() in VALID_PRIORITIES:
        fixed = fixed.replace(f"priority: {priority}", f"priority: {priority.lower()}", 1)
        fixes.append(f"Normalized priority '{priority}' -> '{priority.lower()}'")

    return fixed, fixes


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def print_report(all_findings: list, verbose: bool) -> None:
    """Print the lint report sorted by severity then file."""
    if not all_findings:
        print(f"\n  {GREEN}{BOLD}No issues found.{RESET}\n")
        return

    all_findings.sort(key=lambda f: (SEVERITY_ORDER.get(f["severity"], 9), f["file"], f["line"]))

    counts = {ERROR: 0, WARNING: 0, INFO: 0}
    current_file = None

    for f in all_findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1

        if verbose or f["severity"] != INFO:
            if f["file"] != current_file:
                current_file = f["file"]
                print(f"\n  {BOLD}{current_file}{RESET}")

            color = SEVERITY_COLOR.get(f["severity"], "")
            line_ref = f":{f['line']}" if f["line"] > 0 else ""
            print(f"    {color}{f['severity']:7s}{RESET} {DIM}{line_ref:>5s}{RESET}  {f['message']}")

    # Summary
    print(f"\n  {'=' * 50}")
    print(f"  {RED}{BOLD}{counts[ERROR]}{RESET} error(s)  "
          f"{YELLOW}{BOLD}{counts[WARNING]}{RESET} warning(s)  "
          f"{CYAN}{BOLD}{counts[INFO]}{RESET} info")
    print()


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------

def lint_project(root: Path, fix: bool, dry_run: bool, verbose: bool) -> int:
    """Run all lint checks on a BMAD project. Returns exit code."""
    print(f"\n{BOLD}BMAD Artifact Linter{RESET}")
    print(f"  Project: {root}")
    if fix:
        print(f"  Mode: {YELLOW}auto-fix enabled{RESET}")
    if dry_run:
        print(f"  Mode: {CYAN}dry run — no files will be modified{RESET}")
    print()

    all_findings: list = []
    fix_count = 0

    # Detect active sprint
    sprint_status_path = None
    sprints_dir = root / "sprints"
    if sprints_dir.is_dir():
        for sp in sorted(sprints_dir.glob("sprint-*.yaml"), reverse=True):
            sprint_status_path = sp
            break
    if not sprint_status_path:
        sprint_status_path = root / "sprint-status.yaml"
        if not sprint_status_path.is_file():
            sprint_status_path = None

    active_sprint = False
    if sprint_status_path and sprint_status_path.is_file():
        try:
            sp_text = sprint_status_path.read_text(encoding="utf-8")
            if "status: active" in sp_text or "status: planning" in sp_text:
                active_sprint = True
        except Exception:
            pass

    # Collect all epic IDs
    all_epic_ids: set = set()
    epics_dir = root / "epics"
    if epics_dir.is_dir():
        for ep_file in sorted(epics_dir.glob("*.md")):
            fm, _, _ = extract_frontmatter_raw(ep_file)
            eid = fm.get("epic-id", "")
            if eid:
                all_epic_ids.add(eid)
            all_findings.extend(lint_epic(ep_file, fm))
            all_findings.extend(lint_staleness(ep_file, active_sprint))

    # Collect all FR IDs from PRD
    prd_fr_ids: set = set()
    prd_path = root / "planning_artifacts" / "PRD.md"
    if prd_path.is_file():
        fm, _, text = extract_frontmatter_raw(prd_path)
        all_findings.extend(lint_prd(prd_path, fm, text))
        prd_fr_ids = set(re.findall(r"FR-[A-Z]+-\d{3}", text))
        all_findings.extend(lint_staleness(prd_path, active_sprint))

    # Lint architecture
    arch_path = root / "architecture" / "architecture.md"
    if arch_path.is_file():
        fm, _, text = extract_frontmatter_raw(arch_path)
        all_findings.extend(lint_architecture(arch_path, fm, text))
        all_findings.extend(lint_staleness(arch_path, active_sprint))

    # Lint stories and collect cross-reference data
    all_story_ids: dict = {}
    story_epic_refs: dict = {}
    story_fr_refs: dict = {}
    stories_dir = root / "stories"
    if stories_dir.is_dir():
        for st_file in sorted(stories_dir.glob("*.md")):
            fm, _, text = extract_frontmatter_raw(st_file)
            all_findings.extend(lint_frontmatter_presence(st_file, fm, text))
            all_findings.extend(lint_story(st_file, fm, text, all_epic_ids, prd_fr_ids))
            all_findings.extend(lint_staleness(st_file, active_sprint))

            sid = fm.get("story-id", "")
            if sid:
                all_story_ids[sid] = st_file.name
                story_epic_refs[sid] = fm.get("epic-ref", "")
                fr = fm.get("fr-refs", "")
                story_fr_refs[sid] = fr

            # Auto-fix
            if fix and not dry_run:
                fixed_text, fixes = apply_fixes(st_file, fm, text)
                if fixes:
                    st_file.write_text(fixed_text, encoding="utf-8")
                    for desc in fixes:
                        all_findings.append(finding(INFO, st_file.name, 0, f"AUTO-FIX: {desc}"))
                        fix_count += 1

    # Lint project-context.md
    ctx_path = root / ".bmad" / "project-context.md"
    if ctx_path.is_file():
        fm, _, text = extract_frontmatter_raw(ctx_path)
        all_findings.extend(lint_frontmatter_presence(ctx_path, fm, text))
        if not fm.get("project-name"):
            all_findings.append(finding(WARNING, "project-context.md", 1,
                                        "Missing project-name in frontmatter"))
        all_findings.extend(lint_staleness(ctx_path, active_sprint))

    # Lint product brief
    brief_path = root / "planning_artifacts" / "product-brief.md"
    if brief_path.is_file():
        fm, _, text = extract_frontmatter_raw(brief_path)
        all_findings.extend(lint_frontmatter_presence(brief_path, fm, text))
        if not fm.get("title"):
            all_findings.append(finding(WARNING, "product-brief.md", 1,
                                        "Missing title in frontmatter"))

    # Orphan detection
    all_findings.extend(detect_orphans(all_story_ids, all_epic_ids,
                                       story_epic_refs, story_fr_refs, prd_fr_ids))

    # Report
    print_report(all_findings, verbose)

    if fix and fix_count > 0:
        print(f"  {GREEN}Applied {fix_count} auto-fix(es).{RESET}\n")

    # Exit code: 1 if errors, 0 otherwise
    error_count = sum(1 for f in all_findings if f["severity"] == ERROR)
    return 1 if error_count > 0 else 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lint BMAD project artifacts for quality issues.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python lint_artifacts.py ./my-project              # Lint with default settings
  python lint_artifacts.py ./my-project --verbose     # Include info-level findings
  python lint_artifacts.py ./my-project --fix         # Auto-fix simple issues
  python lint_artifacts.py ./my-project --dry-run     # Show what would be checked

Exit codes:
  0  No errors (warnings and info are acceptable)
  1  One or more errors found
  2  Invalid project directory
        """,
    )
    parser.add_argument(
        "project_root",
        help="Path to BMAD project root directory",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix simple issues (status/priority casing)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List checks without modifying any files",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Include info-level findings in the report",
    )
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    if not root.is_dir():
        print(f"{RED}[err]{RESET} Not a directory: {root}", file=sys.stderr)
        sys.exit(2)

    code = lint_project(root, fix=args.fix, dry_run=args.dry_run, verbose=args.verbose)
    sys.exit(code)


if __name__ == "__main__":
    main()
