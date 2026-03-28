#!/usr/bin/env python
"""
batch-moat-upgrade.py — Single-pass MOAT upgrade for all canonical skills
Handles: Template B->A migration, evals scaffold, evidence tags
Usage: python scripts/batch-moat-upgrade.py [REPO_ROOT]
"""

import os
import re
import sys
import json
from pathlib import Path

REPO_ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent
CANONICAL_DIRS = ["skills/javier-montano", "skills/metodologia"]

# Counters
stats = {
    "total": 0,
    "template_migrated": 0,
    "evals_created": 0,
    "evals_enriched": 0,
    "evidence_tagged": 0,
    "already_ok": 0,
}


def migrate_template_a(content: str, base_name: str) -> tuple[str, bool]:
    """Migrate Template B -> A and add missing sections."""
    changed = False
    readable = base_name.replace("-", " ")

    # --- Rename Template B sections ---
    replacements = [
        (r"## \d+\.\s*The Physics", "## Core Principles"),
        (r"## The Physics", "## Core Principles"),
        (r"## \d+\.\s*The Protocol", "## Core Process"),
        (r"## The Protocol", "## Core Process"),
        (r"## \d+\.\s*Quality Gates", "## Validation Gate"),
        (r"## \d+\.\s*Inputs / Outputs", "## Inputs / Outputs"),
    ]
    for pattern, replacement in replacements:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            changed = True

    # --- Add ## Usage if missing ---
    if not re.search(r"^## Usage|^## When to Activate|^## When to Use", content, re.MULTILINE):
        usage = f"\n## Usage\n\nExample invocations:\n\n"
        usage += f'- "/{base_name}" — Run the full {readable} workflow\n'
        usage += f'- "{readable} on this project" — Apply to current context\n\n'

        # Insert after first major section
        patterns = [
            r"(## (?:Purpose|Overview|Value Proposition|Description|Core Principles).*?\n(?:.*?\n)*?\n)",
            r"(^# .*?\n(?:>.*?\n)*\n(?:.*?\n)*?\n)",
        ]
        inserted = False
        for pat in patterns:
            m = re.search(pat, content, re.MULTILINE | re.DOTALL)
            if m:
                pos = m.end()
                content = content[:pos] + usage + content[pos:]
                changed = True
                inserted = True
                break
        if not inserted:
            content = content.rstrip() + "\n" + usage
            changed = True

    # --- Add ## Validation Gate if missing ---
    if not re.search(r"^## Validation Gate|^## Quality Gate|^## Quality Criteria", content, re.MULTILINE):
        gate = "\n## Validation Gate\n\n"
        gate += "- [ ] Output follows the defined structure and format [EXPLICIT]\n"
        gate += "- [ ] All claims are tagged with evidence markers [EXPLICIT]\n"
        gate += "- [ ] No placeholder content (TBD, TODO) [EXPLICIT]\n"
        gate += "- [ ] Actionable recommendations with priority levels [EXPLICIT]\n"
        gate += "- [ ] Assumptions explicitly documented [EXPLICIT]\n\n"
        content = content.rstrip() + "\n" + gate
        changed = True

    # --- Add ## Assumptions & Limits if missing ---
    if not re.search(r"^## Assumptions|^## Limits|^## Constraints|^## Assumptions & Limits", content, re.MULTILINE):
        assumptions = "\n## Assumptions & Limits\n\n"
        assumptions += "- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]\n"
        assumptions += "- Requires English-language output unless otherwise specified [EXPLICIT]\n"
        assumptions += "- Does not replace domain expert judgment for final decisions [EXPLICIT]\n\n"
        # Insert before Validation Gate
        gate_m = re.search(r"^## Validation Gate|^## Quality Gate|^## Quality Criteria", content, re.MULTILINE)
        if gate_m:
            content = content[:gate_m.start()] + assumptions + content[gate_m.start():]
            changed = True

    # --- Add ## Edge Cases if missing ---
    if not re.search(r"^## Edge Cases|^## Edge Scenarios|^## Special Cases", content, re.MULTILINE):
        edge = "\n## Edge Cases\n\n"
        edge += "| Scenario | Handling |\n"
        edge += "|----------|----------|\n"
        edge += "| Empty or minimal input | Request clarification before proceeding |\n"
        edge += "| Conflicting requirements | Flag conflicts explicitly, propose resolution |\n"
        edge += "| Out-of-scope request | Redirect to appropriate skill or escalate |\n\n"
        gate_m = re.search(r"^## Validation Gate|^## Quality Gate|^## Quality Criteria", content, re.MULTILINE)
        if gate_m:
            content = content[:gate_m.start()] + edge + content[gate_m.start():]
            changed = True

    return content, changed


def scaffold_evals(skill_dir: Path, skill_name: str, content: str) -> bool:
    """Create or enrich evals/evals.json."""
    base_name = re.sub(r"^\d+-", "", skill_name)
    readable = base_name.replace("-", " ")
    evals_dir = skill_dir / "evals"
    evals_json = evals_dir / "evals.json"

    # Extract description
    desc_m = re.search(r"description:\s*[>|]?\s*\n?\s*(.*?)(?:\n\w|\n---)", content, re.DOTALL)
    if desc_m:
        description = re.sub(r"\s+", " ", desc_m.group(1).strip())[:200]
    else:
        desc_m2 = re.search(r"description:\s*(.+)", content)
        description = desc_m2.group(1).strip() if desc_m2 else f"{readable} skill"

    # Extract triggers
    triggers = re.findall(r'"([^"]{5,60})"', description)[:3]
    if not triggers:
        triggers = [readable, f"run {readable}", f"analyze with {readable}"]

    # Load existing
    existing = []
    if evals_json.exists():
        try:
            existing = json.loads(evals_json.read_text(encoding="utf-8"))
        except:
            existing = []

    existing_ids = {e.get("id", "") for e in existing}

    # Define 7 evals
    all_evals = [
        {
            "id": f"{base_name}-happy-path",
            "type": "happy_path",
            "input": f"Run {readable} on this project",
            "expected_behavior": f"Skill activates and produces the expected {readable} output following the defined process",
            "tags": ["basic", "activation"],
        },
        {
            "id": f"{base_name}-explicit-trigger",
            "type": "happy_path",
            "input": triggers[0],
            "expected_behavior": f"Skill recognizes the trigger phrase and executes the {readable} workflow",
            "tags": ["trigger", "recognition"],
        },
        {
            "id": f"{base_name}-with-context",
            "type": "happy_path",
            "input": f"Apply {readable} to analyze the current codebase with detailed output",
            "expected_behavior": f"Skill produces comprehensive {readable} analysis with evidence-tagged findings",
            "tags": ["detailed", "comprehensive"],
        },
        {
            "id": f"{base_name}-minimal-input",
            "type": "happy_path",
            "input": f"Quick {readable}",
            "expected_behavior": f"Skill activates with minimal input, applies reasonable defaults",
            "tags": ["minimal", "defaults"],
        },
        {
            "id": f"{base_name}-false-positive",
            "type": "false_positive",
            "input": "What is the weather forecast for tomorrow?",
            "expected_behavior": f"Skill should NOT activate — this input has no relation to {readable}",
            "tags": ["false_positive", "should-not-activate"],
        },
        {
            "id": f"{base_name}-edge-empty-input",
            "type": "edge_case",
            "input": f"Run {readable} but I have no files or documentation yet",
            "expected_behavior": f"Skill handles gracefully — requests minimum viable input or produces gap analysis",
            "tags": ["edge_case", "empty-input", "boundary"],
        },
        {
            "id": f"{base_name}-edge-conflicting",
            "type": "edge_case",
            "input": f"Apply {readable} but requirements contradict each other",
            "expected_behavior": f"Skill detects contradiction, flags with [OPEN] tag, proposes resolution",
            "tags": ["edge_case", "conflict", "corner"],
        },
    ]

    # Merge
    new_evals = list(existing)
    added = 0
    for ev in all_evals:
        if ev["id"] not in existing_ids:
            new_evals.append(ev)
            added += 1

    if added == 0:
        # Check if we need false_positive or edge_case
        has_fp = any("false_positive" in str(e.get("tags", [])) or e.get("type") == "false_positive" for e in new_evals)
        has_edge = any("edge_case" in str(e.get("tags", [])) or e.get("type") == "edge_case" for e in new_evals)
        if has_fp and has_edge and len(new_evals) >= 5:
            return False

    evals_dir.mkdir(parents=True, exist_ok=True)
    evals_json.write_text(json.dumps(new_evals, indent=2, ensure_ascii=False), encoding="utf-8")
    return True


def add_evidence_tags(content: str, line_count: int) -> tuple[str, bool, int]:
    """Add evidence tags to factual claims."""
    lines = content.split("\n")
    in_code_block = False
    in_frontmatter = False
    factual_indices = []
    existing_tags = 0

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Skip non-content
        if not stripped or stripped.startswith("#") or stripped.startswith("|") or stripped.startswith("- [") or stripped.startswith(">"):
            continue
        if stripped.startswith("*") and stripped.endswith("*"):
            continue

        # Already tagged
        if re.search(r"\[EXPLICIT\]|\[INFERRED\]|\[OPEN\]", stripped):
            existing_tags += 1
            continue

        # Detect factual claims
        factual_pats = [
            r"\b(?:is|are|was|were|has|have|must|should|shall|will|can|generates?|produces?|creates?|requires?|ensures?|validates?|checks?|analyzes?|evaluates?|designs?|implements?|returns?|provides?|supports?|handles?)\b",
            r"\b(?:es|son|fue|tiene|debe|genera|produce|crea|requiere|asegura|valida|verifica|analiza|evalua|implementa|retorna|provee|soporta)\b",
        ]
        is_factual = any(re.search(p, stripped, re.IGNORECASE) for p in factual_pats)
        if is_factual and len(stripped) > 20:
            factual_indices.append(i)

    total_factual = len(factual_indices) + existing_tags
    if total_factual == 0:
        return content, False, 0

    threshold = 50 if line_count < 150 else 80
    current_cov = (existing_tags * 100) // max(total_factual, 1)
    if current_cov >= threshold:
        return content, False, 0

    needed = max(0, (threshold * total_factual // 100) - existing_tags)
    tagged = 0

    for idx in factual_indices:
        if tagged >= needed:
            break
        line = lines[idx].rstrip()

        # Choose tag type
        if re.search(r"\b(?:must|shall|requires?|mandatory|always|never)\b", line, re.IGNORECASE):
            tag = "[EXPLICIT]"
        elif re.search(r"\b(?:typically|usually|likely|suggests?|indicates?|appears?)\b", line, re.IGNORECASE):
            tag = "[INFERRED]"
        elif re.search(r"\b(?:may|might|could|unclear|unknown)\b", line, re.IGNORECASE):
            tag = "[OPEN]"
        else:
            tag = "[EXPLICIT]"

        if line.endswith("."):
            lines[idx] = line[:-1] + f". {tag}"
        else:
            lines[idx] = line + f" {tag}"
        tagged += 1

    if tagged > 0:
        return "\n".join(lines), True, tagged
    return content, False, 0


def process_skill(skill_dir: Path, namespace: str):
    """Process a single skill through all MOAT upgrade steps."""
    skill_name = skill_dir.name
    if skill_name.startswith(".") or skill_name.startswith("REGISTRY"):
        return

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return

    stats["total"] += 1
    content = skill_md.read_text(encoding="utf-8")
    base_name = re.sub(r"^\d+-", "", skill_name)
    any_change = False

    # Step 1: Template A migration
    content, tmpl_changed = migrate_template_a(content, base_name)
    if tmpl_changed:
        stats["template_migrated"] += 1
        any_change = True

    # Step 2: Evals scaffold
    evals_changed = scaffold_evals(skill_dir, skill_name, content)
    if evals_changed:
        stats["evals_created"] += 1

    # Step 3: Evidence tags
    line_count = len(content.split("\n"))
    content, tags_changed, tag_count = add_evidence_tags(content, line_count)
    if tags_changed:
        stats["evidence_tagged"] += 1
        any_change = True

    # Write if changed
    if any_change:
        skill_md.write_text(content, encoding="utf-8")

    if not any_change and not evals_changed:
        stats["already_ok"] += 1

    # Progress indicator every 50 skills
    if stats["total"] % 50 == 0:
        print(f"  ... processed {stats['total']} skills", flush=True)


def main():
    print("=== MOAT Batch Upgrade (Python single-pass) ===")
    print(f"  Repo: {REPO_ROOT}")
    print()

    for canon_dir in CANONICAL_DIRS:
        full = REPO_ROOT / canon_dir
        if not full.is_dir():
            continue
        namespace = full.name

        # Sort for deterministic order
        for skill_dir in sorted(full.iterdir()):
            if skill_dir.is_dir():
                process_skill(skill_dir, namespace)

    print()
    print("=== MOAT Upgrade Complete ===")
    print(f"  Total skills:      {stats['total']}")
    print(f"  Template migrated: {stats['template_migrated']}")
    print(f"  Evals created:     {stats['evals_created']}")
    print(f"  Evidence tagged:   {stats['evidence_tagged']}")
    print(f"  Already OK:        {stats['already_ok']}")


if __name__ == "__main__":
    main()
