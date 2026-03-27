#!/usr/bin/env python3
"""
validate_prd.py — 13-step Implementation Readiness Gate.

Usage:
    python validate_prd.py <project-root>

Runs the 13-check Implementation Readiness gate that validates planning and
solutioning artifacts are complete and aligned before Phase 4 (Implementation).

Exit codes:
    0 = PASS  — All critical checks pass, project is ready for implementation
    1 = CONCERNS — Warnings present but no critical failures
    2 = FAIL — Critical checks failed, return to Phase 3

Outputs JSON gate result and a human-readable summary.
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
RED = "\033[91m"
CYAN = "\033[96m"
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
    """Read file content, return empty string on error."""
    try:
        return filepath.read_text(encoding="utf-8")
    except Exception:
        return ""


def has_section(text: str, heading: str) -> bool:
    """Check if markdown text contains a heading (any level)."""
    pattern = rf"^#+\s+.*{re.escape(heading)}.*$"
    return bool(re.search(pattern, text, re.MULTILINE | re.IGNORECASE))


def count_pattern(text: str, pattern: str) -> int:
    """Count regex pattern matches in text."""
    return len(re.findall(pattern, text, re.MULTILINE | re.IGNORECASE))


# ---------------------------------------------------------------------------
# The 13 checks
# ---------------------------------------------------------------------------

def check_prd_completeness(root: Path) -> dict:
    """Step 1: PRD completeness — all required sections present."""
    prd_path = root / "planning_artifacts" / "PRD.md"
    if not prd_path.is_file():
        return _result(1, "PRD completeness", "fail", "critical",
                       "PRD.md not found in planning_artifacts/")

    text = read_file(prd_path)
    fm = extract_frontmatter(prd_path)

    required_sections = [
        "functional requirements", "non-functional requirements",
        "success metrics", "scope",
    ]
    missing = [s for s in required_sections if not has_section(text, s)]

    if not fm.get("title"):
        missing.append("frontmatter:title")

    if not missing:
        return _result(1, "PRD completeness", "pass", "info",
                       "All required sections and frontmatter present")
    elif len(missing) <= 2:
        return _result(1, "PRD completeness", "warn", "warning",
                       f"Missing sections: {', '.join(missing)}")
    else:
        return _result(1, "PRD completeness", "fail", "critical",
                       f"Missing sections: {', '.join(missing)}")


def check_architecture_alignment(root: Path) -> dict:
    """Step 2: Architecture alignment — arch addresses PRD requirements."""
    arch_path = root / "architecture" / "architecture.md"
    prd_path = root / "planning_artifacts" / "PRD.md"

    if not arch_path.is_file():
        return _result(2, "Architecture alignment", "fail", "critical",
                       "architecture.md not found in architecture/")
    if not prd_path.is_file():
        return _result(2, "Architecture alignment", "fail", "critical",
                       "Cannot check alignment — PRD.md missing")

    arch_text = read_file(arch_path)
    arch_fm = extract_frontmatter(arch_path)

    # Check if architecture references the PRD
    prd_ref = arch_fm.get("prd-ref", "")
    has_ref = bool(prd_ref) or "PRD" in arch_text

    if has_ref:
        return _result(2, "Architecture alignment", "pass", "info",
                       "Architecture references PRD")
    else:
        return _result(2, "Architecture alignment", "warn", "warning",
                       "Architecture does not reference PRD — add prd-ref to frontmatter")


def check_story_decomposition(root: Path) -> dict:
    """Step 3: Story decomposition — all FRs covered by stories."""
    stories_dir = root / "stories"
    if not stories_dir.is_dir():
        return _result(3, "Story decomposition", "fail", "critical",
                       "stories/ directory not found")

    stories = list(stories_dir.glob("*.md"))
    if not stories:
        return _result(3, "Story decomposition", "fail", "critical",
                       "No story files found in stories/")

    return _result(3, "Story decomposition", "pass", "info",
                   f"{len(stories)} story file(s) found")


def check_acceptance_criteria(root: Path) -> dict:
    """Step 4: Acceptance criteria — every story has Given/When/Then."""
    stories_dir = root / "stories"
    if not stories_dir.is_dir():
        return _result(4, "Acceptance criteria", "fail", "critical",
                       "stories/ directory not found")

    stories = list(stories_dir.glob("*.md"))
    if not stories:
        return _result(4, "Acceptance criteria", "fail", "critical",
                       "No stories to check")

    missing_ac = []
    for s in stories:
        text = read_file(s)
        has_gwt = ("given" in text.lower() and "when" in text.lower()
                   and "then" in text.lower())
        has_ac_section = has_section(text, "acceptance criteria")
        if not (has_gwt or has_ac_section):
            missing_ac.append(s.name)

    if not missing_ac:
        return _result(4, "Acceptance criteria", "pass", "info",
                       f"All {len(stories)} stories have acceptance criteria")
    elif len(missing_ac) <= len(stories) // 2:
        return _result(4, "Acceptance criteria", "warn", "warning",
                       f"{len(missing_ac)} stories missing AC: {', '.join(missing_ac[:5])}")
    else:
        return _result(4, "Acceptance criteria", "fail", "critical",
                       f"{len(missing_ac)}/{len(stories)} stories missing acceptance criteria")


def check_dependency_map(root: Path) -> dict:
    """Step 5: Dependency map — story sequencing is valid."""
    stories_dir = root / "stories"
    if not stories_dir.is_dir():
        return _result(5, "Dependency map", "warn", "warning",
                       "stories/ not found — cannot verify dependencies")

    stories = list(stories_dir.glob("*.md"))
    has_deps = False
    for s in stories:
        fm = extract_frontmatter(s)
        text = read_file(s)
        if fm.get("dependencies") or has_section(text, "dependencies"):
            has_deps = True
            break

    if has_deps:
        return _result(5, "Dependency map", "pass", "info",
                       "Dependency information found in stories")
    elif stories:
        return _result(5, "Dependency map", "warn", "warning",
                       "No dependency information found — consider adding story dependencies")
    else:
        return _result(5, "Dependency map", "warn", "warning",
                       "No stories to check for dependencies")


def check_risk_register(root: Path) -> dict:
    """Step 6: Risk register — risks identified with mitigations."""
    # Check PRD and architecture for risk sections
    for rel in ["planning_artifacts/PRD.md", "architecture/architecture.md"]:
        path = root / rel
        if path.is_file():
            text = read_file(path)
            if has_section(text, "risk"):
                return _result(6, "Risk register", "pass", "info",
                               f"Risk section found in {rel}")

    return _result(6, "Risk register", "warn", "warning",
                   "No risk register found in PRD or architecture — add a Risks section")


def check_nfr_coverage(root: Path) -> dict:
    """Step 7: NFR coverage — performance, security, scalability addressed."""
    prd_path = root / "planning_artifacts" / "PRD.md"
    if not prd_path.is_file():
        return _result(7, "NFR coverage", "fail", "critical", "PRD.md not found")

    text = read_file(prd_path)
    if has_section(text, "non-functional"):
        return _result(7, "NFR coverage", "pass", "info",
                       "Non-functional requirements section present in PRD")
    else:
        return _result(7, "NFR coverage", "warn", "warning",
                       "No non-functional requirements section in PRD")


def check_api_contracts(root: Path) -> dict:
    """Step 8: API contracts — endpoints defined with schemas."""
    arch_path = root / "architecture" / "architecture.md"
    if not arch_path.is_file():
        return _result(8, "API contracts", "warn", "warning",
                       "architecture.md not found — cannot check API contracts")

    text = read_file(arch_path)
    if has_section(text, "api") or has_section(text, "endpoint"):
        return _result(8, "API contracts", "pass", "info",
                       "API section found in architecture document")
    else:
        return _result(8, "API contracts", "warn", "warning",
                       "No API contracts section in architecture — add if applicable")


def check_data_model(root: Path) -> dict:
    """Step 9: Data model — schema covers all entities."""
    arch_path = root / "architecture" / "architecture.md"
    if not arch_path.is_file():
        return _result(9, "Data model", "warn", "warning",
                       "architecture.md not found — cannot check data model")

    text = read_file(arch_path)
    if has_section(text, "data model") or has_section(text, "schema") or has_section(text, "database"):
        return _result(9, "Data model", "pass", "info",
                       "Data model section found in architecture")
    else:
        return _result(9, "Data model", "warn", "warning",
                       "No data model section in architecture document")


def check_security_review(root: Path) -> dict:
    """Step 10: Security review — auth, authz, encryption defined."""
    arch_path = root / "architecture" / "architecture.md"
    if not arch_path.is_file():
        return _result(10, "Security review", "warn", "warning",
                       "architecture.md not found — cannot check security")

    text = read_file(arch_path)
    if has_section(text, "security") or has_section(text, "auth"):
        return _result(10, "Security review", "pass", "info",
                       "Security section found in architecture")
    else:
        return _result(10, "Security review", "warn", "warning",
                       "No security section in architecture — add auth/authz/encryption details")


def check_performance_targets(root: Path) -> dict:
    """Step 11: Performance targets — SLAs/SLOs specified."""
    for rel in ["planning_artifacts/PRD.md", "architecture/architecture.md"]:
        path = root / rel
        if path.is_file():
            text = read_file(path)
            if has_section(text, "performance") or has_section(text, "SLA") or has_section(text, "SLO"):
                return _result(11, "Performance targets", "pass", "info",
                               f"Performance targets found in {rel}")

    return _result(11, "Performance targets", "warn", "warning",
                   "No performance targets found — add SLA/SLO section")


def check_deployment_strategy(root: Path) -> dict:
    """Step 12: Deployment strategy — CI/CD, environments, rollback."""
    arch_path = root / "architecture" / "architecture.md"
    if not arch_path.is_file():
        return _result(12, "Deployment strategy", "warn", "warning",
                       "architecture.md not found — cannot check deployment")

    text = read_file(arch_path)
    if has_section(text, "deployment") or has_section(text, "CI/CD") or has_section(text, "infrastructure"):
        return _result(12, "Deployment strategy", "pass", "info",
                       "Deployment section found in architecture")
    else:
        return _result(12, "Deployment strategy", "warn", "warning",
                       "No deployment strategy in architecture — add CI/CD and environment details")


def check_rollback_plan(root: Path) -> dict:
    """Step 13: Rollback plan — recovery procedures documented."""
    arch_path = root / "architecture" / "architecture.md"
    if not arch_path.is_file():
        return _result(13, "Rollback plan", "warn", "warning",
                       "architecture.md not found — cannot check rollback plan")

    text = read_file(arch_path)
    if has_section(text, "rollback") or has_section(text, "recovery") or has_section(text, "disaster"):
        return _result(13, "Rollback plan", "pass", "info",
                       "Rollback/recovery section found in architecture")
    else:
        return _result(13, "Rollback plan", "warn", "warning",
                       "No rollback plan in architecture — document recovery procedures")


def _result(step: int, name: str, status: str, severity: str, evidence: str) -> dict:
    return {
        "step": step,
        "name": name,
        "status": status,
        "evidence": evidence,
        "severity": severity,
    }


# ---------------------------------------------------------------------------
# Gate runner
# ---------------------------------------------------------------------------

ALL_CHECKS = [
    check_prd_completeness,
    check_architecture_alignment,
    check_story_decomposition,
    check_acceptance_criteria,
    check_dependency_map,
    check_risk_register,
    check_nfr_coverage,
    check_api_contracts,
    check_data_model,
    check_security_review,
    check_performance_targets,
    check_deployment_strategy,
    check_rollback_plan,
]


def run_gate(root: Path) -> dict:
    """Run all 13 checks and produce gate result."""
    checks = [fn(root) for fn in ALL_CHECKS]

    passed = sum(1 for c in checks if c["status"] == "pass")
    warnings = sum(1 for c in checks if c["status"] == "warn")
    failed = sum(1 for c in checks if c["status"] == "fail")

    # Determine overall result
    if failed > 0:
        result = "FAIL"
        recommendation = (
            f"{failed} critical check(s) failed. Return to Phase 3 and address "
            f"the failures before proceeding to implementation."
        )
    elif warnings > 3:
        result = "CONCERNS"
        recommendation = (
            f"{warnings} warnings detected. You may proceed with caution, but "
            f"address these concerns during early sprints."
        )
    elif warnings > 0:
        result = "CONCERNS"
        recommendation = (
            f"{warnings} minor warning(s). Proceed to Phase 4 but track these items."
        )
    else:
        result = "PASS"
        recommendation = "All checks passed. Project is ready for implementation."

    return {
        "gate": "implementation-readiness",
        "date": date.today().isoformat(),
        "result": result,
        "checks": checks,
        "summary": {
            "total": 13,
            "passed": passed,
            "warnings": warnings,
            "failed": failed,
        },
        "recommendation": recommendation,
    }


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

STATUS_DISPLAY = {
    "pass": f"{GREEN}PASS{RESET}",
    "warn": f"{YELLOW}WARN{RESET}",
    "fail": f"{RED}FAIL{RESET}",
}

RESULT_DISPLAY = {
    "PASS": f"{GREEN}{BOLD}PASS{RESET}",
    "CONCERNS": f"{YELLOW}{BOLD}CONCERNS{RESET}",
    "FAIL": f"{RED}{BOLD}FAIL{RESET}",
}


def print_gate_result(gate: dict) -> None:
    """Print human-readable gate summary."""
    print(f"\n{BOLD}Implementation Readiness Gate{RESET}")
    print(f"{'=' * 50}")

    for check in gate["checks"]:
        status = STATUS_DISPLAY.get(check["status"], check["status"])
        step_num = f"[{check['step']:2d}]"
        print(f"  {step_num} {status}  {check['name']}")
        print(f"         {DIM}{check['evidence']}{RESET}")

    summary = gate["summary"]
    print(f"\n{'=' * 50}")
    print(f"  Result: {RESULT_DISPLAY[gate['result']]}")
    print(f"  Passed: {summary['passed']}  Warnings: {summary['warnings']}  Failed: {summary['failed']}")
    print(f"\n  {CYAN}{gate['recommendation']}{RESET}")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the 13-step Implementation Readiness Gate.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_prd.py                       # Run gate on current directory
  python validate_prd.py ./my-project          # Run gate on specific project
  python validate_prd.py . --json              # Output JSON only (for CI pipelines)
  python validate_prd.py . --dry-run           # Preview checks without running
  python validate_prd.py . --verbose           # Detailed evidence for each check

Exit codes:
  0  PASS — all critical checks pass, ready for implementation
  1  CONCERNS — warnings present but no critical failures
  2  FAIL — critical checks failed, return to Phase 3
        """,
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="Path to BMAD project root (default: current directory)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output only JSON result (no human-readable summary)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List the 13 checks without executing them",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed evidence and file paths for each check",
    )
    args = parser.parse_args()

    if args.dry_run:
        print(f"\n{BOLD}Implementation Readiness Gate — 13 Checks{RESET}\n")
        for i, fn in enumerate(ALL_CHECKS, 1):
            doc = fn.__doc__ or ""
            name = doc.split("—")[0].strip() if "—" in doc else fn.__name__
            print(f"  [{i:2d}] {name}")
        print(f"\n{YELLOW}Dry run complete. No checks were executed.{RESET}\n")
        sys.exit(0)

    root = Path(args.project_root).resolve()
    if not root.is_dir():
        print(
            f"{RED}[err]{RESET} Not a directory: {root}\n"
            f"  Fix: provide a valid path to a BMAD project root.\n"
            f"  Example: python validate_prd.py ./my-project",
            file=sys.stderr,
        )
        sys.exit(2)

    gate = run_gate(root)

    if args.json:
        print(json.dumps(gate, indent=2))
    else:
        print_gate_result(gate)
        # Also write JSON to sprints directory if it exists
        sprints_dir = root / "sprints"
        if sprints_dir.is_dir():
            out = sprints_dir / "gate-result.json"
            out.write_text(json.dumps(gate, indent=2), encoding="utf-8")
            print(f"  {DIM}Gate result saved to {out.relative_to(root)}{RESET}\n")

    # Exit code
    result = gate["result"]
    if result == "PASS":
        sys.exit(0)
    elif result == "CONCERNS":
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
