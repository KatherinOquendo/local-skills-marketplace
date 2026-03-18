#!/usr/bin/env python3
"""
Ecosystem scaffolding toolkit.

Creates the directory structure for a new ecosystem with properly
named artifacts following naming-and-slugging conventions.

Usage:
  python forge_toolkit.py --domain "API Development" --skills api-builder --rules no-inline-sql typed-responses --workflows create-endpoint deploy-api
  python forge_toolkit.py --domain "Frontend" --skills component-builder --rules no-inline-styles
"""

import argparse
import os
import re
import sys


def slugify(value: str) -> str:
    """Convert any string to kebab-case slug."""
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = value.lower()
    value = re.sub(r'[_\s]+', '-', value)
    value = re.sub(r'[^a-z0-9-]', '', value)
    value = re.sub(r'-{2,}', '-', value)
    return value.strip('-')


def create_skill_scaffold(base_path: str, name: str):
    """Create a minimal but functional skill directory."""
    skill_dir = os.path.join(base_path, 'skills', name)
    ref_dir = os.path.join(skill_dir, 'reference')
    os.makedirs(ref_dir, exist_ok=True)

    skill_md = f"""---
name: {name}
description: "[TODO: Write a pushy, context-heavy description. Include what the skill does AND when to trigger it. See ecosystem-forge for description-writing guidance.]"
---

# {name.replace('-', ' ').title()}

[TODO: One paragraph explaining what this skill does and why it exists.]

## Quick Reference

[TODO: Add a quick reference table or code block showing the most common usage.]

## How to Use

### Step 1: [First action]

[TODO: Describe the first step with specific instructions.]

### Step 2: [Second action]

[TODO: Continue with concrete steps.]

## Quality Checklist

- [ ] [TODO: Add domain-specific quality checks]
- [ ] [TODO: Add verification criteria]

## Reference Files

- `reference/` — [TODO: Add reference files as needed for domain knowledge]
"""
    with open(os.path.join(skill_dir, 'SKILL.md'), 'w') as f:
        f.write(skill_md)

    print(f"  Created skill: {name}/")


def create_rule_scaffold(base_path: str, name: str):
    """Create a minimal but functional rule file."""
    rules_dir = os.path.join(base_path, 'rules')
    os.makedirs(rules_dir, exist_ok=True)

    rule_name = name if name.startswith('R-') else f'R-{name}'
    filename = f"{rule_name}.md"

    rule_md = f"""---
description: "[TODO: One-line summary of what this rule prevents]"
globs: "[TODO: Specific file patterns, e.g., **/*.ts]"
---
# {rule_name}

## The Constraint

[TODO: One sentence — the binary constraint. What is forbidden or required?]

## Why This Matters

[TODO: What bad outcome does this prevent? Be specific about the failure mode.]

## Examples

### Bad (Violation)

```
[TODO: Show code/content that violates this rule]
```

### Good (Compliance)

```
[TODO: Show the corrected version — minimal diff from the Bad example]
```
"""
    with open(os.path.join(rules_dir, filename), 'w') as f:
        f.write(rule_md)

    print(f"  Created rule: {filename}")


def create_workflow_scaffold(base_path: str, name: str):
    """Create a minimal but functional workflow file."""
    workflows_dir = os.path.join(base_path, 'workflows')
    os.makedirs(workflows_dir, exist_ok=True)

    filename = f"{name}.md"

    workflow_md = f"""---
description: "[TODO: Action-oriented summary of what this workflow accomplishes]"
---
# {name}

## Prerequisites

- [TODO: What must be true before running this workflow?]

## Steps

### 1. Load context  // turbo

[TODO: Read required configuration or reference files.]

### 2. [Action verb] [target]

[TODO: First real action step. Be atomic — one action per step.]

### 3. Verify results

- [ ] [TODO: Specific success check]
- If FAIL: [TODO: Remediation step]
"""
    with open(os.path.join(workflows_dir, filename), 'w') as f:
        f.write(workflow_md)

    print(f"  Created workflow: {filename}")


def scaffold_ecosystem(domain: str, skills: list, rules: list, workflows: list, output_dir: str):
    """Create the full ecosystem directory structure."""
    domain_slug = slugify(domain)
    base_path = os.path.join(output_dir, domain_slug)

    if os.path.exists(base_path):
        print(f"Warning: '{base_path}' already exists. Adding to existing structure.")

    os.makedirs(base_path, exist_ok=True)

    print(f"\nScaffolding ecosystem: {domain_slug}/")
    print("=" * 50)

    if skills:
        for skill in skills:
            create_skill_scaffold(base_path, slugify(skill))

    if rules:
        for rule in rules:
            create_rule_scaffold(base_path, slugify(rule))

    if workflows:
        for workflow in workflows:
            create_workflow_scaffold(base_path, slugify(workflow))

    print(f"\nEcosystem scaffolded at: {base_path}")
    print(f"Next steps: Fill in the [TODO] markers in each file.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scaffold a new artifact ecosystem with skills, rules, and workflows."
    )
    parser.add_argument("--domain", required=True, help="Name of the domain (e.g., 'API Development')")
    parser.add_argument("--skills", nargs="*", default=[], help="Skill names to create")
    parser.add_argument("--rules", nargs="*", default=[], help="Rule names to create (R- prefix added automatically)")
    parser.add_argument("--workflows", nargs="*", default=[], help="Workflow names to create")
    parser.add_argument("--output", default=".", help="Output directory (default: current directory)")

    args = parser.parse_args()

    if not args.skills and not args.rules and not args.workflows:
        print("Error: Specify at least one --skills, --rules, or --workflows")
        parser.print_help()
        sys.exit(1)

    scaffold_ecosystem(args.domain, args.skills, args.rules, args.workflows, args.output)
