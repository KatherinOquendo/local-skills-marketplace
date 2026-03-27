#!/bin/bash
# consolidate-canonical.sh — Copy best versions to canonical locations
# Based on approved canonical-decisions.csv
# Usage: ./scripts/consolidate-canonical.sh [--dry-run] [REPO_ROOT]

set -euo pipefail

DRY_RUN=false
REPO_ROOT=""

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    *) REPO_ROOT="$arg" ;;
  esac
done

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"

CSV="$REPO_ROOT/governance/canonical-decisions.csv"
if [ ! -f "$CSV" ]; then
  echo "ERROR: $CSV not found. Run compare-duplicates.sh first."
  exit 1
fi

# Source location paths
declare -A SOURCE_PATHS
SOURCE_PATHS[atomic]="skills/javier-montano"
SOURCE_PATHS[pm]="plugins/javier-montano/pm-project-framework/skills"
SOURCE_PATHS[sa]="plugins/javier-montano/sovereign-architect/skills"
SOURCE_PATHS[scriba]="plugins/javier-montano/scriba/skills"
SOURCE_PATHS[mdf]="plugins/metodologia/metodologia-discovery-framework/skills"

echo "=== Canonical Consolidation Engine ==="
[ "$DRY_RUN" = true ] && echo "  MODE: DRY RUN"
echo ""

total_copied=0
total_skipped=0
total_already=0
total_errors=0

# Skip header line
tail -n +2 "$CSV" | while IFS=',' read -r skill_name rec_source rec_owner canonical_path rest; do
  # Clean up any quotes
  skill_name=$(echo "$skill_name" | tr -d '"')
  rec_source=$(echo "$rec_source" | tr -d '"')
  rec_owner=$(echo "$rec_owner" | tr -d '"')
  canonical_path=$(echo "$canonical_path" | tr -d '"')

  # Skip empty/malformed lines
  [ -z "$skill_name" ] && continue
  [ -z "$rec_source" ] && continue

  # Source path
  source_base="${SOURCE_PATHS[$rec_source]:-}"
  if [ -z "$source_base" ]; then
    echo "  ERROR: Unknown source '$rec_source' for $skill_name"
    continue
  fi

  source_dir="$REPO_ROOT/$source_base/$skill_name"
  target_dir="$REPO_ROOT/$canonical_path"

  # If source IS already the canonical location, skip
  if [ "$source_base/$skill_name" = "$canonical_path" ]; then
    echo "  ALREADY CANONICAL: $skill_name (at $canonical_path)"
    continue
  fi

  # Verify source exists
  if [ ! -d "$source_dir" ] || [ ! -f "$source_dir/SKILL.md" ]; then
    echo "  ERROR: Source not found: $source_dir"
    continue
  fi

  # Check if target already exists and is identical
  if [ -f "$target_dir/SKILL.md" ]; then
    s_hash=$(md5sum "$source_dir/SKILL.md" | cut -d' ' -f1)
    t_hash=$(md5sum "$target_dir/SKILL.md" | cut -d' ' -f1)
    if [ "$s_hash" = "$t_hash" ]; then
      echo "  UNCHANGED: $skill_name"
      continue
    fi
  fi

  if [ "$DRY_RUN" = true ]; then
    s_lines=$(wc -l < "$source_dir/SKILL.md" | tr -d ' ')
    echo "  WOULD COPY: $skill_name ($rec_source → $canonical_path, $s_lines lines)"
  else
    # Create target directory
    mkdir -p "$target_dir"

    # Copy entire skill directory (SKILL.md + subdirs)
    cp -r "$source_dir"/* "$target_dir/" 2>/dev/null || true

    s_lines=$(wc -l < "$source_dir/SKILL.md" | tr -d ' ')
    echo "  COPIED: $skill_name ($rec_source → $canonical_path, $s_lines lines)"
  fi
done

echo ""
echo "=== Consolidation Complete ==="
[ "$DRY_RUN" = true ] && echo "  (DRY RUN — no files were modified)"
echo ""
echo "Next steps:"
echo "  1. Run scripts/validate-sync.sh to check drift"
echo "  2. Run scripts/skill-sync.sh to propagate canonical to plugins"
