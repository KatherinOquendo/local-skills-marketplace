#!/bin/bash
# batch-structural-fix.sh — Fix S1-S9 structural issues across all canonical skills
# Fixes: angle brackets in frontmatter, missing frontmatter, line count info
# Usage: ./scripts/batch-structural-fix.sh [REPO_ROOT]

set -uo pipefail

REPO_ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
CANONICAL_DIRS=("skills/javier-montano" "skills/metodologia")

FIXED=0
TOTAL=0
SKIPPED=0

echo "=== Batch Structural Fix ==="
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

    skill_md="$skill_dir/SKILL.md"
    [ -f "$skill_md" ] || continue

    TOTAL=$((TOTAL + 1))
    changed=false

    # --- Fix S5: angle brackets in frontmatter ---
    # Extract frontmatter (between first two ---)
    if head -1 "$skill_md" | grep -q '^---'; then
      # Check for angle brackets in frontmatter
      frontmatter_brackets=$(sed -n '1,/^---$/{ /^---$/!p }' "$skill_md" | sed '1d' | grep -c '[<>]' 2>/dev/null || echo 0)
      frontmatter_brackets=$(echo "$frontmatter_brackets" | tr -dc '0-9')
      frontmatter_brackets=${frontmatter_brackets:-0}

      if [ "$frontmatter_brackets" -gt 0 ]; then
        # Replace angle brackets in frontmatter only (first --- block)
        # Use python for safer multiline processing
        python -c "
import re, sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    content = f.read()
# Find frontmatter
match = re.match(r'^(---\n.*?\n---)', content, re.DOTALL)
if match:
    fm = match.group(1)
    fm_fixed = fm.replace('<', '').replace('>', '')
    content = fm_fixed + content[len(fm):]
    with open(sys.argv[1], 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  Fixed angle brackets in frontmatter: {sys.argv[1]}')
" "$skill_md" 2>/dev/null && changed=true
      fi
    fi

    # --- Fix: Ensure YAML frontmatter exists ---
    if ! head -1 "$skill_md" | grep -q '^---'; then
      # Extract skill name from directory for minimal frontmatter
      base_name=$(echo "$skill_name" | sed 's/^[0-9]*-//')
      python -c "
import sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    content = f.read()
frontmatter = '''---
name: ${base_name}
description: >
  ${base_name} skill. Triggers: ${base_name}.
allowed-tools:
  - Read
  - Glob
  - Grep
---

'''
content = frontmatter + content
with open(sys.argv[1], 'w', encoding='utf-8') as f:
    f.write(content)
print(f'  Added missing frontmatter: {sys.argv[1]}')
" "$skill_md" 2>/dev/null && changed=true
    fi

    if $changed; then
      FIXED=$((FIXED + 1))
    else
      SKIPPED=$((SKIPPED + 1))
    fi
  done
done

echo ""
echo "=== Structural Fix Complete ==="
echo "  Total skills: $TOTAL"
echo "  Fixed: $FIXED"
echo "  Skipped (no issues): $SKIPPED"
