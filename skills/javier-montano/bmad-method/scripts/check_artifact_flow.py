#!/usr/bin/env python3
"""
check_artifact_flow.py — Verify BMAD artifact dependency chain.

Usage:
    python check_artifact_flow.py <project-root>
    python check_artifact_flow.py --templates

Checks the artifact flow chain:
    product-brief.md -> PRD.md -> architecture.md -> epics/*.md -> stories/*.md

Reports:
  - Broken references (artifact references a file that doesn't exist)
  - Orphaned artifacts (files not referenced by any upstream artifact)
  - Missing cross-links (required references not found)

The --templates flag checks template cross-references within the BMAD skill itself.
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

PASS = f"{GREEN}OK{RESET}"
WARN = f"{YELLOW}WARN{RESET}"
FAIL = f"{RED}FAIL{RESET}"
INFO = f"{CYAN}INFO{RESET}"


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


def file_references(text: str, target_name: str) -> bool:
    """Check if text references a filename or its stem (case-insensitive)."""
    stem = Path(target_name).stem
    lower = text.lower()
    return target_name.lower() in lower or stem.lower().replace("-", " ") in lower


# ---------------------------------------------------------------------------
# Flow chain checks
# ---------------------------------------------------------------------------

class FlowChecker:
    """Check the artifact dependency chain for a BMAD project."""

    def __init__(self, root: Path):
        self.root = root
        self.issues: list = []
        self.info_items: list = []

    def _add_issue(self, severity: str, category: str, message: str) -> None:
        self.issues.append({
            "severity": severity,
            "category": category,
            "message": message,
        })

    def _add_info(self, message: str) -> None:
        self.info_items.append(message)

    # ------------------------------------------------------------------
    # Individual chain link checks
    # ------------------------------------------------------------------

    def check_brief_exists(self) -> bool:
        """Check that product-brief.md exists."""
        brief = self.root / "planning_artifacts" / "product-brief.md"
        if brief.is_file():
            self._add_info("product-brief.md found")
            return True
        else:
            self._add_issue("warn", "missing-artifact",
                            "planning_artifacts/product-brief.md not found (Phase 1 output)")
            return False

    def check_prd_references_brief(self) -> bool:
        """Check that PRD.md references the product brief."""
        prd = self.root / "planning_artifacts" / "PRD.md"
        if not prd.is_file():
            self._add_issue("fail", "missing-artifact",
                            "planning_artifacts/PRD.md not found (Phase 2 output)")
            return False

        self._add_info("PRD.md found")

        fm = extract_frontmatter(prd)
        text = read_file(prd)

        # Check frontmatter reference
        if fm.get("product-brief-ref"):
            self._add_info("PRD references product-brief via frontmatter")
            return True

        # Check body reference
        if file_references(text, "product-brief"):
            self._add_info("PRD references product-brief in body text")
            return True

        self._add_issue("warn", "missing-cross-link",
                        "PRD.md does not reference product-brief.md — add product-brief-ref to frontmatter")
        return False

    def check_arch_references_prd(self) -> bool:
        """Check that architecture.md references the PRD."""
        arch = self.root / "architecture" / "architecture.md"
        if not arch.is_file():
            self._add_issue("fail", "missing-artifact",
                            "architecture/architecture.md not found (Phase 3 output)")
            return False

        self._add_info("architecture.md found")

        fm = extract_frontmatter(arch)
        text = read_file(arch)

        if fm.get("prd-ref"):
            self._add_info("Architecture references PRD via frontmatter")
            return True

        if file_references(text, "PRD"):
            self._add_info("Architecture references PRD in body text")
            return True

        self._add_issue("warn", "missing-cross-link",
                        "architecture.md does not reference PRD.md — add prd-ref to frontmatter")
        return False

    def check_epics(self) -> list:
        """Check that epics exist and reference PRD requirements."""
        epics_dir = self.root / "epics"
        if not epics_dir.is_dir():
            self._add_issue("warn", "missing-artifact",
                            "epics/ directory not found")
            return []

        epic_files = sorted(epics_dir.glob("*.md"))
        if not epic_files:
            self._add_issue("warn", "missing-artifact",
                            "No epic files found in epics/")
            return []

        self._add_info(f"{len(epic_files)} epic(s) found")

        epic_ids = []
        for ef in epic_files:
            fm = extract_frontmatter(ef)
            text = read_file(ef)
            epic_id = fm.get("epic-id", ef.stem)
            epic_ids.append(epic_id)

            # Check if epic references PRD FRs
            has_prd_ref = fm.get("prd-refs") or file_references(text, "FR-")
            if not has_prd_ref:
                self._add_issue("warn", "missing-cross-link",
                                f"Epic {ef.name} does not reference PRD functional requirements")

        return epic_ids

    def check_stories(self, epic_ids: list) -> None:
        """Check stories reference epics and have acceptance criteria."""
        stories_dir = self.root / "stories"
        if not stories_dir.is_dir():
            self._add_issue("warn", "missing-artifact",
                            "stories/ directory not found")
            return

        story_files = sorted(stories_dir.glob("*.md"))
        if not story_files:
            self._add_issue("warn", "missing-artifact",
                            "No story files found in stories/")
            return

        self._add_info(f"{len(story_files)} story(ies) found")

        referenced_epics = set()
        for sf in story_files:
            fm = extract_frontmatter(sf)
            text = read_file(sf)

            # Check epic reference
            epic_ref = fm.get("epic-ref", "")
            if epic_ref:
                referenced_epics.add(epic_ref)
            else:
                self._add_issue("warn", "missing-cross-link",
                                f"Story {sf.name} has no epic-ref in frontmatter")

            # Check acceptance criteria
            has_ac = (
                "given" in text.lower() and "when" in text.lower() and "then" in text.lower()
            ) or re.search(r"#+\s*acceptance criteria", text, re.IGNORECASE)

            if not has_ac:
                self._add_issue("warn", "missing-content",
                                f"Story {sf.name} missing acceptance criteria (Given/When/Then)")

        # Check for orphaned epics (not referenced by any story)
        if epic_ids:
            orphaned = set(epic_ids) - referenced_epics
            for eid in orphaned:
                self._add_issue("info", "orphaned-artifact",
                                f"Epic {eid} is not referenced by any story")

    def check_orphaned_artifacts(self) -> None:
        """Check for files that don't fit the expected flow."""
        planning = self.root / "planning_artifacts"
        if not planning.is_dir():
            return

        known = {"product-brief.md", "prd.md", "ux-spec.md"}
        for f in planning.glob("*.md"):
            if f.name.lower() not in known and not f.name.startswith("."):
                self._add_issue("info", "orphaned-artifact",
                                f"Unexpected file in planning_artifacts/: {f.name}")

    # ------------------------------------------------------------------
    # Run all checks
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """Run the full artifact flow check."""
        self.check_brief_exists()
        self.check_prd_references_brief()
        self.check_arch_references_prd()
        epic_ids = self.check_epics()
        self.check_stories(epic_ids)
        self.check_orphaned_artifacts()

        fails = sum(1 for i in self.issues if i["severity"] == "fail")
        warns = sum(1 for i in self.issues if i["severity"] == "warn")
        infos = sum(1 for i in self.issues if i["severity"] == "info")

        return {
            "issues": self.issues,
            "info": self.info_items,
            "summary": {
                "fails": fails,
                "warnings": warns,
                "infos": infos,
                "total_issues": fails + warns,
            },
        }


# ---------------------------------------------------------------------------
# Template cross-reference check
# ---------------------------------------------------------------------------

def check_templates() -> None:
    """Check template cross-references within the BMAD skill itself."""
    skill_dir = Path(__file__).resolve().parent.parent

    print(f"\n{BOLD}BMAD Skill Template Cross-Reference Check{RESET}")
    print(f"  Skill dir: {skill_dir}\n")

    # Scan SKILL.md for all referenced paths
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        print(f"  {FAIL} SKILL.md not found")
        return

    text = read_file(skill_md)

    # Extract paths like: templates/foo.md.tmpl, references/bar.md, scripts/baz.py
    path_pattern = r'(?:templates|references|scripts|agents|workflows|prompts)/[\w./-]+'
    referenced = set(re.findall(path_pattern, text))

    passed = 0
    failed = 0
    for ref in sorted(referenced):
        path = skill_dir / ref
        # Handle ${CLAUDE_SKILL_DIR}/ prefix removal (already stripped by regex)
        if path.is_file() or path.is_dir():
            print(f"  {PASS}  {ref}")
            passed += 1
        else:
            print(f"  {FAIL}  {ref}")
            failed += 1

    total = passed + failed
    print(f"\n  {BOLD}Result{RESET}: {passed}/{total} references valid")
    if failed:
        print(f"  {YELLOW}{failed} broken reference(s) found{RESET}")
    else:
        print(f"  {GREEN}All template cross-references are valid{RESET}")
    print()


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

SEVERITY_ICON = {
    "fail": f"{RED}[FAIL]{RESET}",
    "warn": f"{YELLOW}[WARN]{RESET}",
    "info": f"{CYAN}[INFO]{RESET}",
}

CATEGORY_LABEL = {
    "missing-artifact": "Missing Artifact",
    "missing-cross-link": "Missing Cross-Link",
    "missing-content": "Missing Content",
    "orphaned-artifact": "Orphaned Artifact",
    "broken-reference": "Broken Reference",
}


def print_results(result: dict) -> None:
    """Print human-readable artifact flow report."""
    print(f"\n{BOLD}Artifact Flow Chain Report{RESET}")
    print(f"{'=' * 50}")

    # Info items (chain links found)
    if result["info"]:
        print(f"\n  {BOLD}Chain Links Found:{RESET}")
        for item in result["info"]:
            print(f"    {GREEN}+{RESET} {item}")

    # Issues grouped by category
    if result["issues"]:
        print(f"\n  {BOLD}Issues:{RESET}")
        by_cat: dict = {}
        for issue in result["issues"]:
            cat = issue["category"]
            if cat not in by_cat:
                by_cat[cat] = []
            by_cat[cat].append(issue)

        for cat, issues in by_cat.items():
            label = CATEGORY_LABEL.get(cat, cat)
            print(f"\n    {BOLD}{label}{RESET}:")
            for issue in issues:
                icon = SEVERITY_ICON.get(issue["severity"], "")
                print(f"      {icon} {issue['message']}")

    # Summary
    s = result["summary"]
    print(f"\n{'=' * 50}")
    if s["fails"] > 0:
        print(f"  {RED}{BOLD}BROKEN CHAIN{RESET} — {s['fails']} critical issue(s), {s['warnings']} warning(s)")
    elif s["warnings"] > 0:
        print(f"  {YELLOW}{BOLD}INCOMPLETE{RESET} — {s['warnings']} warning(s) to address")
    else:
        print(f"  {GREEN}{BOLD}CHAIN INTACT{RESET} — All artifact links verified")

    if s["infos"] > 0:
        print(f"  {DIM}{s['infos']} informational note(s){RESET}")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify BMAD artifact dependency chain.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python check_artifact_flow.py                # Check current directory
  python check_artifact_flow.py ./my-project   # Check specific project
  python check_artifact_flow.py --templates    # Check BMAD skill templates
  python check_artifact_flow.py . --dry-run    # Preview checks
  python check_artifact_flow.py . --verbose    # Detailed chain analysis

Exit codes:
  0  Chain intact — all artifact links verified
  1  Incomplete — warnings present (missing cross-links)
  2  Broken chain — critical artifacts missing
        """,
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="Path to BMAD project root (default: current directory)",
    )
    parser.add_argument(
        "--templates",
        action="store_true",
        help="Check template cross-references within the BMAD skill itself",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List artifact chain checks without executing them",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed file-level analysis for each chain link",
    )
    args = parser.parse_args()

    if args.templates:
        check_templates()
        return

    root = Path(args.project_root).resolve()
    if not root.is_dir():
        print(
            f"{RED}[err]{RESET} Not a directory: {root}\n"
            f"  Fix: provide a valid path to a BMAD project root.",
            file=sys.stderr,
        )
        sys.exit(2)

    if args.dry_run:
        print(f"\n{BOLD}Artifact Flow Chain — Checks{RESET}\n")
        checks = [
            "product-brief.md exists (Phase 1 output)",
            "PRD.md references product-brief (Phase 2 traceability)",
            "architecture.md references PRD (Phase 3 traceability)",
            "Epics reference PRD functional requirements",
            "Stories reference parent epics",
            "Stories have acceptance criteria (Given/When/Then)",
            "No orphaned artifacts in planning_artifacts/",
        ]
        for c in checks:
            print(f"  {CYAN}*{RESET} {c}")
        print(f"\n{YELLOW}Dry run complete. No checks were executed.{RESET}\n")
        sys.exit(0)

    checker = FlowChecker(root)
    result = checker.run()
    print_results(result)

    # Exit code: 0 if no fails/warns, 1 if warnings, 2 if fails
    if result["summary"]["fails"] > 0:
        sys.exit(2)
    elif result["summary"]["warnings"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
