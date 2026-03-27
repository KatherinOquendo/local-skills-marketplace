#!/usr/bin/env python3
"""
diagnose_project.py — Diagnose BMAD project health and generate recommendations.

Usage:
    python diagnose_project.py <project-root>
    python diagnose_project.py <project-root> --output report.md
    python diagnose_project.py <project-root> --verbose

Checks:
  - Phase detection: which phase the project is in based on existing artifacts
  - Completeness score per phase (0-100%)
  - Artifact freshness: last modified dates, staleness warnings
  - Gate readiness prediction
  - Velocity trend (if sprint history exists)
  - Recommendations: prioritized list of what to do next

Zero external dependencies.
"""

import argparse
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# ANSI colours
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
# Frontmatter parser
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
    current_key = None
    for raw_line in match.group(1).splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if raw_line.startswith("  ") and stripped.startswith("- ") and current_key:
            existing = fm.get(current_key)
            if not isinstance(existing, list):
                existing = []
            existing.append(stripped[2:].strip().strip('"').strip("'"))
            fm[current_key] = existing
            continue
        if ":" in stripped:
            key, _, val = stripped.partition(":")
            current_key = key.strip()
            fm[current_key] = val.strip().strip('"').strip("'")
    return fm


def file_age_days(filepath: Path) -> float:
    """Return file age in days. Returns -1 on error."""
    try:
        return (time.time() - filepath.stat().st_mtime) / 86400
    except OSError:
        return -1


def file_mtime_iso(filepath: Path) -> str:
    """Return file modification time as ISO 8601 string."""
    try:
        ts = filepath.stat().st_mtime
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    except OSError:
        return "unknown"


# ---------------------------------------------------------------------------
# Phase detection
# ---------------------------------------------------------------------------

PHASE_SIGNALS = {
    1: {
        "name": "Analysis",
        "artifacts": [
            ("planning_artifacts/product-brief.md", 30),  # (path, weight)
        ],
    },
    2: {
        "name": "Planning",
        "artifacts": [
            ("planning_artifacts/PRD.md", 40),
            ("planning_artifacts/ux-spec.md", 20),
        ],
    },
    3: {
        "name": "Solutioning",
        "artifacts": [
            ("architecture/architecture.md", 30),
            ("epics/", 20),   # directory presence
            ("stories/", 25),  # directory with content
        ],
    },
    4: {
        "name": "Implementation",
        "artifacts": [
            ("sprint-status.yaml", 15),
            ("sprints/", 15),
        ],
    },
}


def detect_phases(root: Path) -> dict:
    """Detect which phases have artifacts and compute completeness scores.

    Returns {phase_num: {"name": str, "score": int, "present": [...], "missing": [...]}}.
    """
    results = {}
    for phase, config in PHASE_SIGNALS.items():
        present = []
        missing = []
        total_weight = 0
        earned_weight = 0

        for artifact_path, weight in config["artifacts"]:
            total_weight += weight
            full_path = root / artifact_path

            if artifact_path.endswith("/"):
                # Directory check: must exist and contain at least one file
                if full_path.is_dir() and any(full_path.iterdir()):
                    count = sum(1 for f in full_path.glob("*.md") if f.is_file())
                    present.append(f"{artifact_path} ({count} files)")
                    earned_weight += weight
                else:
                    missing.append(artifact_path)
            else:
                if full_path.is_file():
                    present.append(artifact_path)
                    earned_weight += weight
                else:
                    missing.append(artifact_path)

        score = int((earned_weight / total_weight * 100)) if total_weight > 0 else 0
        results[phase] = {
            "name": config["name"],
            "score": score,
            "present": present,
            "missing": missing,
        }

    return results


def detect_current_phase(phase_results: dict) -> int:
    """Determine which phase the project is currently in.

    Logic: the highest phase with >0% score where the previous phase is >=50%.
    """
    current = 0
    for phase in sorted(phase_results.keys()):
        if phase_results[phase]["score"] > 0:
            current = phase
        elif current > 0:
            break
    return current if current > 0 else 1


# ---------------------------------------------------------------------------
# Artifact freshness
# ---------------------------------------------------------------------------

def analyze_freshness(root: Path) -> list:
    """Return freshness data for key artifacts."""
    artifacts = [
        ".bmad/project-context.md",
        "planning_artifacts/product-brief.md",
        "planning_artifacts/PRD.md",
        "planning_artifacts/ux-spec.md",
        "architecture/architecture.md",
    ]

    results = []
    for rel in artifacts:
        path = root / rel
        if path.is_file():
            age = file_age_days(path)
            mtime = file_mtime_iso(path)
            stale = age > 30
            results.append({
                "file": rel,
                "modified": mtime,
                "age_days": int(age),
                "stale": stale,
            })

    # Add story files summary
    stories_dir = root / "stories"
    if stories_dir.is_dir():
        story_files = list(stories_dir.glob("*.md"))
        if story_files:
            ages = [file_age_days(f) for f in story_files]
            oldest = max(ages)
            newest = min(ages)
            results.append({
                "file": f"stories/ ({len(story_files)} files)",
                "modified": f"newest: {int(newest)}d ago, oldest: {int(oldest)}d ago",
                "age_days": int(oldest),
                "stale": oldest > 30,
            })

    return results


# ---------------------------------------------------------------------------
# Gate readiness prediction
# ---------------------------------------------------------------------------

GATE_PREREQUISITES = [
    ("PRD exists", "planning_artifacts/PRD.md"),
    ("Architecture exists", "architecture/architecture.md"),
    ("Stories exist", "stories/"),
    ("Epics exist", "epics/"),
    ("Project context exists", ".bmad/project-context.md"),
]


def predict_gate_readiness(root: Path) -> dict:
    """Predict whether the project is likely to pass the Implementation Readiness Gate."""
    checks = []
    passed = 0

    for label, rel_path in GATE_PREREQUISITES:
        path = root / rel_path
        if rel_path.endswith("/"):
            exists = path.is_dir() and any(path.glob("*.md"))
        else:
            exists = path.is_file()
        checks.append({"check": label, "passed": exists})
        if exists:
            passed += 1

    # Additional quality checks
    prd_path = root / "planning_artifacts" / "PRD.md"
    if prd_path.is_file():
        text = prd_path.read_text(encoding="utf-8")
        has_frs = bool(re.findall(r"FR-[A-Z]+-\d{3}", text))
        checks.append({"check": "PRD has FR identifiers", "passed": has_frs})
        if has_frs:
            passed += 1

        has_nfr = bool(re.search(r"(?i)non.?functional|NFR", text))
        checks.append({"check": "PRD has NFR section", "passed": has_nfr})
        if has_nfr:
            passed += 1

    arch_path = root / "architecture" / "architecture.md"
    if arch_path.is_file():
        text = arch_path.read_text(encoding="utf-8")
        has_security = bool(re.search(r"(?i)security", text))
        checks.append({"check": "Architecture addresses security", "passed": has_security})
        if has_security:
            passed += 1

        has_data_model = bool(re.search(r"(?i)data model|entity|ERD", text))
        checks.append({"check": "Architecture has data model", "passed": has_data_model})
        if has_data_model:
            passed += 1

    # Stories quality
    stories_dir = root / "stories"
    if stories_dir.is_dir():
        story_files = list(stories_dir.glob("*.md"))
        stories_with_ac = 0
        for sf in story_files:
            text = sf.read_text(encoding="utf-8")
            if re.search(r"(?i)Given\b", text):
                stories_with_ac += 1
        if story_files:
            ac_ratio = stories_with_ac / len(story_files)
            has_good_ac = ac_ratio >= 0.8
            checks.append({
                "check": f"Stories have acceptance criteria ({stories_with_ac}/{len(story_files)})",
                "passed": has_good_ac,
            })
            if has_good_ac:
                passed += 1

    total = len(checks)
    score = int((passed / total * 100)) if total > 0 else 0
    prediction = "LIKELY PASS" if score >= 80 else "LIKELY FAIL" if score < 50 else "UNCERTAIN"

    return {"checks": checks, "score": score, "prediction": prediction, "passed": passed, "total": total}


# ---------------------------------------------------------------------------
# Velocity trend
# ---------------------------------------------------------------------------

def analyze_velocity(root: Path) -> list:
    """Extract velocity data from sprint status files."""
    sprints = []

    # Check sprints/ directory
    sprints_dir = root / "sprints"
    if sprints_dir.is_dir():
        for sp_file in sorted(sprints_dir.glob("sprint-*.yaml")):
            data = _parse_sprint_file(sp_file)
            if data:
                sprints.append(data)

    # Check root sprint-status.yaml
    root_sprint = root / "sprint-status.yaml"
    if root_sprint.is_file():
        data = _parse_sprint_file(root_sprint)
        if data:
            sprints.append(data)

    return sprints


def _parse_sprint_file(filepath: Path) -> dict:
    """Parse a sprint status file for velocity data."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return {}

    number_match = re.search(r"number:\s*(\d+)", text)
    status_match = re.search(r"status:\s*(\w+)", text)
    total_match = re.search(r"total-points:\s*(\d+)", text)
    completed_match = re.search(r"completed-points:\s*(\d+)", text)
    velocity_match = re.search(r"velocity:\s*([\d.]+)", text)

    if not number_match:
        return {}

    return {
        "number": int(number_match.group(1)),
        "status": status_match.group(1) if status_match else "unknown",
        "total_points": int(total_match.group(1)) if total_match else 0,
        "completed_points": int(completed_match.group(1)) if completed_match else 0,
        "velocity": float(velocity_match.group(1)) if velocity_match else 0.0,
        "file": filepath.name,
    }


# ---------------------------------------------------------------------------
# Recommendations
# ---------------------------------------------------------------------------

def generate_recommendations(phase_results: dict, current_phase: int,
                             freshness: list, gate: dict, velocity: list) -> list:
    """Generate prioritized recommendations based on diagnosis."""
    recs = []

    # Phase-based recommendations
    if current_phase <= 1 and phase_results[1]["score"] < 100:
        for m in phase_results[1]["missing"]:
            recs.append(("HIGH", f"Create {m} to complete Phase 1 analysis"))

    if current_phase >= 1 and phase_results[2]["score"] == 0:
        recs.append(("HIGH", "Begin Phase 2: create PRD from the product brief"))

    if current_phase >= 2 and phase_results[2]["score"] < 100:
        for m in phase_results[2]["missing"]:
            recs.append(("MEDIUM", f"Create {m} to complete Phase 2 planning"))

    if current_phase >= 2 and phase_results[3]["score"] == 0:
        recs.append(("HIGH", "Begin Phase 3: create architecture document and decompose into stories"))

    if current_phase >= 3 and phase_results[3]["score"] < 100:
        for m in phase_results[3]["missing"]:
            recs.append(("MEDIUM", f"Create/populate {m} to complete Phase 3 solutioning"))

    # Gate readiness
    if current_phase >= 3 and gate["prediction"] == "LIKELY FAIL":
        failed_checks = [c["check"] for c in gate["checks"] if not c["passed"]]
        for check in failed_checks[:3]:
            recs.append(("HIGH", f"Gate blocker: {check}"))

    if current_phase >= 3 and gate["prediction"] == "UNCERTAIN":
        recs.append(("MEDIUM", "Run the Implementation Readiness Gate to identify gaps before proceeding"))

    # Freshness
    stale = [f for f in freshness if f.get("stale")]
    if stale:
        recs.append(("MEDIUM",
                      f"{len(stale)} artifact(s) not modified in >30 days — review for accuracy"))

    # Project context
    ctx_missing = not (Path(".bmad") / "project-context.md").name in [f["file"] for f in freshness]
    # Actually check root
    # (freshness already checks this, so just look for staleness)

    # Velocity
    if velocity and len(velocity) >= 2:
        recent = velocity[-1]
        prev = velocity[-2]
        if recent["completed_points"] < prev["completed_points"] * 0.7:
            recs.append(("MEDIUM",
                          f"Velocity dropped: Sprint {recent['number']} completed "
                          f"{recent['completed_points']}pts vs {prev['completed_points']}pts "
                          f"in Sprint {prev['number']} — investigate impediments"))

    if not recs:
        if gate["prediction"] == "LIKELY PASS":
            recs.append(("INFO", "Project appears healthy. Proceed with the Implementation Readiness Gate."))
        else:
            recs.append(("INFO", "No critical issues detected. Continue current phase work."))

    return recs


# ---------------------------------------------------------------------------
# Report output
# ---------------------------------------------------------------------------

def format_bar(score: int, width: int = 20) -> str:
    """Format a progress bar."""
    filled = int(width * score / 100)
    bar = "#" * filled + "." * (width - filled)
    if score >= 80:
        color = GREEN
    elif score >= 50:
        color = YELLOW
    else:
        color = RED
    return f"[{color}{bar}{RESET}] {score}%"


def print_console_report(root: Path, phase_results: dict, current_phase: int,
                          freshness: list, gate: dict, velocity: list,
                          recommendations: list, verbose: bool) -> None:
    """Print the health report to stdout."""
    print(f"\n{BOLD}BMAD Project Health Diagnosis{RESET}")
    print(f"  Project: {root}")
    print(f"  Diagnosed: {datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print()

    # Current phase
    phase_name = phase_results.get(current_phase, {}).get("name", "Unknown")
    print(f"  {BOLD}Current Phase{RESET}: {current_phase} — {phase_name}")
    print()

    # Phase completeness
    print(f"  {BOLD}Phase Completeness{RESET}")
    for phase in sorted(phase_results.keys()):
        pr = phase_results[phase]
        bar = format_bar(pr["score"])
        marker = " <--" if phase == current_phase else ""
        print(f"    Phase {phase} ({pr['name']:14s}): {bar}{marker}")
        if verbose and pr["missing"]:
            for m in pr["missing"]:
                print(f"      {DIM}missing: {m}{RESET}")
    print()

    # Freshness
    if freshness:
        print(f"  {BOLD}Artifact Freshness{RESET}")
        for f in freshness:
            stale_flag = f"  {RED}STALE{RESET}" if f.get("stale") else ""
            print(f"    {f['file']:45s}  {DIM}{f['modified']}{RESET}{stale_flag}")
        print()

    # Gate prediction
    gate_color = GREEN if gate["prediction"] == "LIKELY PASS" else RED if gate["prediction"] == "LIKELY FAIL" else YELLOW
    print(f"  {BOLD}Gate Readiness Prediction{RESET}: {gate_color}{gate['prediction']}{RESET} "
          f"({gate['passed']}/{gate['total']} checks)")
    if verbose:
        for c in gate["checks"]:
            icon = f"{GREEN}*{RESET}" if c["passed"] else f"{RED}x{RESET}"
            print(f"    {icon} {c['check']}")
    print()

    # Velocity
    if velocity:
        print(f"  {BOLD}Sprint Velocity{RESET}")
        for sp in velocity:
            vel_str = f"  velocity: {sp['velocity']:.1f}" if sp['velocity'] else ""
            print(f"    Sprint {sp['number']:3d}: "
                  f"{sp['completed_points']:3d}/{sp['total_points']:3d} pts "
                  f"({sp['status']}){vel_str}")
        print()

    # Recommendations
    print(f"  {BOLD}Recommendations{RESET} (priority order)")
    for priority, msg in recommendations:
        color = RED if priority == "HIGH" else YELLOW if priority == "MEDIUM" else CYAN
        print(f"    {color}[{priority:6s}]{RESET} {msg}")
    print()


def write_markdown_report(output_path: Path, root: Path, phase_results: dict,
                           current_phase: int, freshness: list, gate: dict,
                           velocity: list, recommendations: list) -> None:
    """Write the health report as a markdown file."""
    lines = []
    ts = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines.append(f"# BMAD Project Health Report")
    lines.append(f"")
    lines.append(f"**Project**: `{root}`")
    lines.append(f"**Generated**: {ts}")
    lines.append(f"**Current Phase**: {current_phase} -- {phase_results.get(current_phase, {}).get('name', 'Unknown')}")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    # Phase completeness
    lines.append(f"## Phase Completeness")
    lines.append(f"")
    lines.append(f"| Phase | Name | Score | Missing |")
    lines.append(f"|-------|------|-------|---------|")
    for phase in sorted(phase_results.keys()):
        pr = phase_results[phase]
        missing_str = ", ".join(pr["missing"]) if pr["missing"] else "none"
        marker = " (current)" if phase == current_phase else ""
        lines.append(f"| {phase}{marker} | {pr['name']} | {pr['score']}% | {missing_str} |")
    lines.append(f"")

    # Freshness
    if freshness:
        lines.append(f"## Artifact Freshness")
        lines.append(f"")
        lines.append(f"| File | Modified | Stale |")
        lines.append(f"|------|----------|-------|")
        for f in freshness:
            stale = "YES" if f.get("stale") else "no"
            lines.append(f"| {f['file']} | {f['modified']} | {stale} |")
        lines.append(f"")

    # Gate prediction
    lines.append(f"## Gate Readiness Prediction")
    lines.append(f"")
    lines.append(f"**Prediction**: {gate['prediction']} ({gate['passed']}/{gate['total']} checks)")
    lines.append(f"")
    for c in gate["checks"]:
        status = "PASS" if c["passed"] else "FAIL"
        lines.append(f"- [{status}] {c['check']}")
    lines.append(f"")

    # Velocity
    if velocity:
        lines.append(f"## Sprint Velocity")
        lines.append(f"")
        lines.append(f"| Sprint | Completed | Total | Status | Velocity |")
        lines.append(f"|--------|-----------|-------|--------|----------|")
        for sp in velocity:
            lines.append(f"| {sp['number']} | {sp['completed_points']} | "
                         f"{sp['total_points']} | {sp['status']} | "
                         f"{sp['velocity']:.1f} |")
        lines.append(f"")

    # Recommendations
    lines.append(f"## Recommendations")
    lines.append(f"")
    for priority, msg in recommendations:
        lines.append(f"- **[{priority}]** {msg}")
    lines.append(f"")

    output_path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def diagnose(root: Path, output: str, verbose: bool) -> int:
    """Run full project diagnosis. Returns exit code."""
    phase_results = detect_phases(root)
    current_phase = detect_current_phase(phase_results)
    freshness = analyze_freshness(root)
    gate = predict_gate_readiness(root)
    velocity = analyze_velocity(root)
    recommendations = generate_recommendations(phase_results, current_phase,
                                                freshness, gate, velocity)

    print_console_report(root, phase_results, current_phase,
                          freshness, gate, velocity, recommendations, verbose)

    if output:
        output_path = Path(output).resolve()
        write_markdown_report(output_path, root, phase_results, current_phase,
                               freshness, gate, velocity, recommendations)
        print(f"  {GREEN}Report written to{RESET}: {output_path}\n")

    # Exit code: 1 if gate prediction is LIKELY FAIL, 0 otherwise
    return 1 if gate["prediction"] == "LIKELY FAIL" else 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Diagnose BMAD project health and generate recommendations.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python diagnose_project.py ./my-project                    # Console report
  python diagnose_project.py ./my-project --output report.md # Also write markdown
  python diagnose_project.py ./my-project --verbose          # Show all gate checks

Exit codes:
  0  Project health is acceptable
  1  Gate prediction is LIKELY FAIL
  2  Invalid project directory
        """,
    )
    parser.add_argument(
        "project_root",
        help="Path to BMAD project root directory",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        default="",
        help="Write health report to a markdown file",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed gate checks and missing artifact details",
    )
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    if not root.is_dir():
        print(f"{RED}[err]{RESET} Not a directory: {root}", file=sys.stderr)
        sys.exit(2)

    code = diagnose(root, output=args.output, verbose=args.verbose)
    sys.exit(code)


if __name__ == "__main__":
    main()
