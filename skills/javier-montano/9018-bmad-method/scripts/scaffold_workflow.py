#!/usr/bin/env python3
"""
scaffold_workflow.py — Generate sharded workflow step files.

Usage:
    python scaffold_workflow.py <workflow-name> [--steps N] [--agent agent-id]
    python scaffold_workflow.py create-prd --steps 5 --agent john-pm

Creates a workflow directory with step-01-init.md through step-NN-name.md.
Each step follows the BMAD step file schema with HALT commands to prevent
AI read-ahead.
"""

import argparse
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
BOLD = "\033[1m"
RESET = "\033[0m"


def slugify(name: str) -> str:
    """Convert a name to kebab-case."""
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


# ---------------------------------------------------------------------------
# Default step names
# ---------------------------------------------------------------------------

DEFAULT_STEP_NAMES = {
    1: "init",
    2: "gather-context",
    3: "execute",
    4: "validate",
    5: "finalize",
    6: "review",
    7: "handoff",
    8: "archive",
    9: "retrospective",
    10: "close",
}


def get_step_name(step_num: int, total_steps: int) -> str:
    """Get a reasonable default step name."""
    if step_num == 1:
        return "init"
    if step_num == total_steps:
        return "finalize"
    if step_num == total_steps - 1 and total_steps > 2:
        return "validate"
    return DEFAULT_STEP_NAMES.get(step_num, f"step-{step_num}")


# ---------------------------------------------------------------------------
# Step file template
# ---------------------------------------------------------------------------

def generate_step_file(
    step_num: int,
    step_name: str,
    total_steps: int,
    workflow_name: str,
    agent_id: str,
) -> str:
    """Generate a single workflow step file."""
    prev_steps = [f"step-{i:02d}" for i in range(1, step_num)]
    current_step = f"step-{step_num:02d}-{step_name}"
    next_step_num = step_num + 1

    if next_step_num <= total_steps:
        next_name = get_step_name(next_step_num, total_steps)
        next_step = f"step-{next_step_num:02d}-{next_name}"
    else:
        next_step = "null"

    steps_completed_yaml = ""
    if prev_steps:
        items = "\n".join(f'  - "{s}"' for s in prev_steps)
        steps_completed_yaml = f"\nstepsCompleted:\n{items}"
    else:
        steps_completed_yaml = "\nstepsCompleted: []"

    return f"""---
stepNumber: {step_num}
stepName: "{step_name}"
agent: "{agent_id}"
inputs:
  - "TODO: specify input artifact(s)"
outputs:
  - "TODO: specify output artifact(s)"{steps_completed_yaml}
currentStep: "{current_step}"
nextStep: "{next_step}"
---

# Step {step_num}: {step_name.replace("-", " ").title()}

> Workflow: **{workflow_name}** | Agent: `{agent_id}` | Step {step_num}/{total_steps}

## Step Goal

TODO: Define the clear objective for this step. What must be true when this step completes?

## Execution Rules

- TODO: Define constraints and guardrails for the agent during this step
- Do not proceed to step {next_step_num} until this step is validated
- All outputs must be saved before advancing

## Instructions

1. TODO: First action item
2. TODO: Second action item
3. TODO: Third action item

## Success Metrics

- [ ] TODO: Measurable criterion #1
- [ ] TODO: Measurable criterion #2
- [ ] TODO: Measurable criterion #3

<!-- HALT: Do not proceed to next step until this step is validated -->
"""


# ---------------------------------------------------------------------------
# Workflow index
# ---------------------------------------------------------------------------

def generate_index(workflow_name: str, agent_id: str, total_steps: int) -> str:
    """Generate an index/README for the workflow directory."""
    lines = [
        f"# Workflow: {workflow_name.replace('-', ' ').title()}",
        "",
        f"> Agent: `{agent_id}` | Steps: {total_steps}",
        f"> Generated: {date.today().isoformat()}",
        "",
        "## Steps",
        "",
        "| # | Step | File |",
        "|---|------|------|",
    ]

    for i in range(1, total_steps + 1):
        name = get_step_name(i, total_steps)
        filename = f"step-{i:02d}-{name}.md"
        lines.append(f"| {i} | {name.replace('-', ' ').title()} | `{filename}` |")

    lines.extend([
        "",
        "## Execution Protocol",
        "",
        "1. Execute steps sequentially (step 01 through step {:02d})".format(total_steps),
        "2. Each step has a HALT command — do not read ahead",
        "3. Validate success metrics before proceeding to next step",
        "4. If a step fails validation, address issues before advancing",
        "",
    ])

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate sharded BMAD workflow step files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scaffold_workflow.py create-prd --steps 5 --agent john-pm
  python scaffold_workflow.py sprint-planning --steps 3 --agent bob-scrum-master
  python scaffold_workflow.py code-review --steps 4 --agent quinn-qa -o workflows/
        """,
    )
    parser.add_argument("workflow_name", help="Workflow name (will be slugified)")
    parser.add_argument(
        "--steps", "-n",
        type=int,
        default=3,
        help="Number of steps (default: 3)",
    )
    parser.add_argument(
        "--agent",
        default="TODO-agent",
        help="Agent ID responsible for this workflow",
    )
    parser.add_argument(
        "--output-dir", "-o",
        help="Parent directory for the workflow folder (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the workflow structure without creating files",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output including step file content previews",
    )

    args = parser.parse_args()

    if args.steps < 1:
        print(
            f"{RED}[err]{RESET} Steps must be >= 1.\n"
            f"  Fix: use --steps with a positive integer (e.g., --steps 3).",
            file=sys.stderr,
        )
        sys.exit(2)
    if args.steps > 20:
        print(f"{YELLOW}[warn]{RESET} {args.steps} steps is unusually high — consider breaking into sub-workflows")

    workflow_slug = slugify(args.workflow_name)
    agent_id = args.agent
    total_steps = args.steps

    parent = Path(args.output_dir) if args.output_dir else Path.cwd()
    if not parent.is_dir():
        print(f"{RED}[err]{RESET} Parent directory does not exist: {parent}", file=sys.stderr)
        sys.exit(1)

    wf_dir = parent / workflow_slug

    if args.dry_run:
        print(f"\n{BOLD}Dry Run — Workflow Scaffold Preview{RESET}")
        print(f"  Directory: {wf_dir}")
        print(f"  Agent    : {agent_id}")
        print(f"  Steps    : {total_steps}")
        print()
        for i in range(1, total_steps + 1):
            name = get_step_name(i, total_steps)
            print(f"    {CYAN}write{RESET} step-{i:02d}-{name}.md")
        print(f"    {CYAN}write{RESET} README.md")
        print(f"\n{YELLOW}Dry run complete. No files were created.{RESET}\n")
        sys.exit(0)

    if wf_dir.exists():
        print(
            f"{RED}[err]{RESET} Directory already exists: {wf_dir}\n"
            f"  Fix: remove it first or choose a different workflow name.",
            file=sys.stderr,
        )
        sys.exit(2)

    wf_dir.mkdir(parents=True)

    print(f"\n{BOLD}Scaffolding workflow: {workflow_slug}{RESET}")
    print(f"  Agent : {agent_id}")
    print(f"  Steps : {total_steps}")
    print(f"  Dir   : {wf_dir}")
    print()

    # Generate step files
    for i in range(1, total_steps + 1):
        name = get_step_name(i, total_steps)
        filename = f"step-{i:02d}-{name}.md"
        filepath = wf_dir / filename
        content = generate_step_file(i, name, total_steps, workflow_slug, agent_id)
        filepath.write_text(content, encoding="utf-8")
        print(f"  {GREEN}[ok]{RESET} {filename}")

    # Generate index
    index_path = wf_dir / "README.md"
    index_content = generate_index(workflow_slug, agent_id, total_steps)
    index_path.write_text(index_content, encoding="utf-8")
    print(f"  {GREEN}[ok]{RESET} README.md")

    print(f"\n{GREEN}{BOLD}Workflow scaffolded successfully!{RESET}")
    print(f"\n{BOLD}Next steps:{RESET}")
    print(f"  1. Edit each step file — fill in goals, instructions, success metrics")
    print(f"  2. Define inputs/outputs for each step")
    print(f"  3. Register the workflow in your agent's menu section")
    print()


if __name__ == "__main__":
    main()
