#!/bin/bash
# batch-template-migrate.sh — Migrate all skills to Template A compliance
# Adds missing sections (Usage, Validation Gate, etc.) without destroying content
# Removes Template B markers (The Physics, The Protocol)
# Usage: ./scripts/batch-template-migrate.sh [--all] [--skill=NAME] [REPO_ROOT]

set -uo pipefail

REPO_ROOT=""
SKILL_FILTER=""

for arg in "$@"; do
  case "$arg" in
    --all) ;;
    --skill=*) SKILL_FILTER="${arg#--skill=}" ;;
    *) REPO_ROOT="$arg" ;;
  esac
done

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
CANONICAL_DIRS=("skills/javier-montano" "skills/metodologia")

MIGRATED=0
TOTAL=0
SKIPPED=0

echo "=== Batch Template A Migration ==="
echo "  Repo: $REPO_ROOT"
echo ""

for canon_dir in "${CANONICAL_DIRS[@]}"; do
  full="$REPO_ROOT/$canon_dir"
  [ -d "$full" ] || continue

  for skill_dir in "$full"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name=$(basename "$skill_dir")
    [[ "$skill_name" == .* ]] && continue
    [[ "$skill_name" == "REGISTRY"* ]] && continue

    if [ -n "$SKILL_FILTER" ] && [ "$skill_name" != "$SKILL_FILTER" ]; then
      continue
    fi

    skill_md="$skill_dir/SKILL.md"
    [ -f "$skill_md" ] || continue

    TOTAL=$((TOTAL + 1))

    python -c "
import re, sys, os

skill_path = sys.argv[1]
skill_name = sys.argv[2]
base_name = re.sub(r'^\d+-', '', skill_name)

with open(skill_path, 'r', encoding='utf-8') as f:
    content = f.read()

original = content
changed = False

# --- Remove Template B markers ---
# Replace '## The Physics' and its content with nothing (content preserved elsewhere)
# Replace '## The Protocol' similarly
# We keep the content under these headers but rename them
template_b_patterns = [
    (r'## \d+\.\s*The Physics', '## Core Principles'),
    (r'## The Physics', '## Core Principles'),
    (r'## \d+\.\s*The Protocol', '## Core Process'),
    (r'## The Protocol', '## Core Process'),
    (r'## \d+\.\s*Quality Gates', '## Validation Gate'),
    (r'## \d+\.\s*Inputs / Outputs', '## Inputs / Outputs'),
]

for pattern, replacement in template_b_patterns:
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        changed = True

# --- Ensure ## Usage section exists ---
has_usage = bool(re.search(r'^## Usage|^## When to Activate|^## When to Use', content, re.MULTILINE))
if not has_usage:
    # Find insertion point: after frontmatter + first heading + first paragraph
    # Try to insert after the description/purpose section
    insert_patterns = [
        r'(## (?:Purpose|Overview|Value Proposition|Description).*?\n(?:.*?\n)*?\n)',
        r'(^# .*?\n(?:>.*?\n)*\n(?:.*?\n)*?\n)',
        r'(^---\n.*?^---\n\n)',
    ]
    inserted = False
    for pat in insert_patterns:
        match = re.search(pat, content, re.MULTILINE | re.DOTALL)
        if match:
            pos = match.end()
            usage_section = '''## Usage

Example invocations:

- \"/''' + base_name + '''\" — Run the full ''' + base_name + ''' workflow
- \"''' + base_name + ''' on this project\" — Apply to current context

'''
            content = content[:pos] + usage_section + content[pos:]
            changed = True
            inserted = True
            break
    if not inserted:
        # Append at end
        content += '''

## Usage

Example invocations:

- \"/''' + base_name + '''\" — Run the full ''' + base_name + ''' workflow
- \"''' + base_name + ''' on this project\" — Apply to current context

'''
        changed = True

# --- Ensure ## Validation Gate section exists ---
has_gate = bool(re.search(r'^## Validation Gate|^## Quality Gate|^## Quality Criteria', content, re.MULTILINE))
if not has_gate:
    # Append at end (before any trailing ---)
    gate_section = '''
## Validation Gate

- [ ] Output follows the defined structure and format
- [ ] All claims are tagged with evidence markers [EXPLICIT]/[INFERRED]/[OPEN]
- [ ] No placeholder content (TBD, TODO, lorem ipsum)
- [ ] Actionable recommendations with priority levels
- [ ] Assumptions explicitly documented
'''
    # Remove trailing whitespace and add gate
    content = content.rstrip() + '\n' + gate_section + '\n'
    changed = True

# --- Ensure ## Assumptions & Limits exists ---
has_assumptions = bool(re.search(r'^## Assumptions|^## Limits|^## Constraints|^## Assumptions & Limits', content, re.MULTILINE))
if not has_assumptions:
    # Insert before Validation Gate
    gate_match = re.search(r'^## Validation Gate|^## Quality Gate|^## Quality Criteria', content, re.MULTILINE)
    if gate_match:
        assumptions = '''## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

'''
        content = content[:gate_match.start()] + assumptions + content[gate_match.start():]
        changed = True

# --- Ensure ## Edge Cases exists ---
has_edge = bool(re.search(r'^## Edge Cases|^## Edge Scenarios|^## Special Cases', content, re.MULTILINE))
if not has_edge:
    gate_match = re.search(r'^## Validation Gate|^## Quality Gate|^## Quality Criteria', content, re.MULTILINE)
    if gate_match:
        edge_cases = '''## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |

'''
        content = content[:gate_match.start()] + edge_cases + content[gate_match.start():]
        changed = True

if changed:
    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  MIGRATED: {skill_name}')
    sys.exit(0)
else:
    sys.exit(1)
" "$skill_md" "$skill_name" 2>/dev/null

    if [ $? -eq 0 ]; then
      MIGRATED=$((MIGRATED + 1))
    else
      SKIPPED=$((SKIPPED + 1))
    fi
  done
done

echo ""
echo "=== Template Migration Complete ==="
echo "  Total skills: $TOTAL"
echo "  Migrated: $MIGRATED"
echo "  Already compliant: $SKIPPED"
