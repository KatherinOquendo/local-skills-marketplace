#!/usr/bin/env python3
"""
Validates ecosystem integrity: naming conventions, cross-references,
and structural consistency across skills, rules, and workflows.

Usage:
  python ecosystem-checker.py /path/to/ecosystem
  python ecosystem-checker.py /path/to/ecosystem --strict
"""

import os
import re
import sys

SLUG_PATTERN = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
RULE_PATTERN = re.compile(r'^R-[a-z0-9]+(-[a-z0-9]+)*$')


def find_artifacts(base_path: str) -> dict:
    """Discover all artifacts in the ecosystem."""
    artifacts = {'skills': [], 'rules': [], 'workflows': []}

    skills_dir = os.path.join(base_path, 'skills')
    if os.path.isdir(skills_dir):
        for d in os.listdir(skills_dir):
            if os.path.isdir(os.path.join(skills_dir, d)) and not d.startswith('.'):
                artifacts['skills'].append(d)

    rules_dir = os.path.join(base_path, 'rules')
    if os.path.isdir(rules_dir):
        for f in os.listdir(rules_dir):
            if f.endswith('.md') and not f.startswith('.'):
                artifacts['rules'].append(f.replace('.md', ''))

    workflows_dir = os.path.join(base_path, 'workflows')
    if os.path.isdir(workflows_dir):
        for f in os.listdir(workflows_dir):
            if f.endswith('.md') and not f.startswith('.'):
                artifacts['workflows'].append(f.replace('.md', ''))

    return artifacts


def check_naming(artifacts: dict) -> list:
    """Validate naming conventions for all artifacts."""
    issues = []

    for skill in artifacts['skills']:
        if not SLUG_PATTERN.match(skill):
            issues.append(f"ERROR: Skill '{skill}' doesn't follow kebab-case")

    for rule in artifacts['rules']:
        if not RULE_PATTERN.match(rule):
            issues.append(f"ERROR: Rule '{rule}' doesn't follow R-kebab-case pattern")

    for workflow in artifacts['workflows']:
        if not SLUG_PATTERN.match(workflow):
            issues.append(f"ERROR: Workflow '{workflow}' doesn't follow kebab-case")

    return issues


def check_skill_structure(base_path: str, artifacts: dict) -> list:
    """Validate each skill has required files."""
    issues = []

    for skill in artifacts['skills']:
        skill_md = os.path.join(base_path, 'skills', skill, 'SKILL.md')
        if not os.path.isfile(skill_md):
            issues.append(f"ERROR: Skill '{skill}' missing SKILL.md")
            continue

        with open(skill_md, 'r') as f:
            content = f.read()

        # Check frontmatter
        if not content.startswith('---'):
            issues.append(f"ERROR: Skill '{skill}/SKILL.md' missing YAML frontmatter")
        elif 'description:' not in content[:500]:
            issues.append(f"ERROR: Skill '{skill}/SKILL.md' missing description in frontmatter")

        # Check for TODO markers
        todo_count = content.count('[TODO')
        if todo_count > 0:
            issues.append(f"WARN: Skill '{skill}/SKILL.md' has {todo_count} unresolved [TODO] markers")

    return issues


def check_rule_structure(base_path: str, artifacts: dict) -> list:
    """Validate each rule has required sections."""
    issues = []

    for rule in artifacts['rules']:
        rule_path = os.path.join(base_path, 'rules', f'{rule}.md')
        if not os.path.isfile(rule_path):
            continue

        with open(rule_path, 'r') as f:
            content = f.read()

        if not content.startswith('---'):
            issues.append(f"ERROR: Rule '{rule}' missing YAML frontmatter")

        if not re.search(r'###?\s*(bad|violation|❌)', content, re.IGNORECASE):
            issues.append(f"WARN: Rule '{rule}' missing Bad/Violation example")

        if not re.search(r'###?\s*(good|compliance|✅)', content, re.IGNORECASE):
            issues.append(f"WARN: Rule '{rule}' missing Good/Compliance example")

    return issues


def check_workflow_structure(base_path: str, artifacts: dict) -> list:
    """Validate each workflow has required structure."""
    issues = []

    for workflow in artifacts['workflows']:
        wf_path = os.path.join(base_path, 'workflows', f'{workflow}.md')
        if not os.path.isfile(wf_path):
            continue

        with open(wf_path, 'r') as f:
            content = f.read()

        # Count steps
        steps = re.findall(r'###\s+\d+\.', content)
        if len(steps) > 10:
            issues.append(f"ERROR: Workflow '{workflow}' has {len(steps)} steps (max 10)")

        # Check for verification step
        if not re.search(r'(verify|verification|check)', content, re.IGNORECASE):
            issues.append(f"WARN: Workflow '{workflow}' may be missing a verification step")

        # Check for dangerous turbo
        turbo_lines = [line for line in content.split('\n') if '// turbo' in line.lower()]
        dangerous = ['rm ', 'push --force', 'drop ', 'truncate', 'delete']
        for line in turbo_lines:
            for d in dangerous:
                if d in line.lower():
                    issues.append(f"ERROR: Workflow '{workflow}' has dangerous action marked turbo: {line.strip()}")

    return issues


def run_checks(base_path: str, strict: bool = False) -> int:
    """Run all ecosystem checks."""
    print(f"Checking ecosystem at: {base_path}")
    print("=" * 60)

    artifacts = find_artifacts(base_path)

    total_artifacts = sum(len(v) for v in artifacts.values())
    print(f"Found: {len(artifacts['skills'])} skills, {len(artifacts['rules'])} rules, {len(artifacts['workflows'])} workflows")

    if total_artifacts == 0:
        print("\nNo artifacts found. Is this the right directory?")
        return 1

    all_issues = []
    all_issues.extend(check_naming(artifacts))
    all_issues.extend(check_skill_structure(base_path, artifacts))
    all_issues.extend(check_rule_structure(base_path, artifacts))
    all_issues.extend(check_workflow_structure(base_path, artifacts))

    errors = [i for i in all_issues if i.startswith('ERROR')]
    warnings = [i for i in all_issues if i.startswith('WARN')]

    print()
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(f"  {e}")

    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  {w}")

    if not errors and not warnings:
        print("All checks passed.")

    print(f"\nSummary: {len(errors)} errors, {len(warnings)} warnings")

    if errors or (strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ecosystem-checker.py /path/to/ecosystem [--strict]")
        sys.exit(1)

    path = sys.argv[1]
    strict_mode = '--strict' in sys.argv

    if not os.path.isdir(path):
        print(f"Error: '{path}' is not a directory")
        sys.exit(1)

    sys.exit(run_checks(path, strict=strict_mode))
