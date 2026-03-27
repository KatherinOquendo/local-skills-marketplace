#!/bin/bash
# skill-sync.sh — Sync canonical skills into plugin directories
# Copies canonical versions into plugins that inherit them, applying overlays
# Usage: ./scripts/skill-sync.sh [--plugin=PLUGIN_KEY] [--dry-run] [REPO_ROOT]
#
# Options:
#   --plugin=sa|pm|mdf|scriba  Sync only one plugin (default: all)
#   --dry-run                   Show what would change without modifying files
#   REPO_ROOT                   Repository root (default: auto-detect)

set -euo pipefail

DRY_RUN=false
TARGET_PLUGIN=""
REPO_ROOT=""

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --plugin=*) TARGET_PLUGIN="${arg#--plugin=}" ;;
    *) REPO_ROOT="$arg" ;;
  esac
done

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"

# Plugin definitions
declare -A PLUGINS
PLUGINS[sa]="plugins/javier-montano/sovereign-architect"
PLUGINS[pm]="plugins/javier-montano/pm-project-framework"
PLUGINS[scriba]="plugins/javier-montano/scriba"
PLUGINS[mdf]="plugins/metodologia/metodologia-discovery-framework"

echo "=== Skill Sync Engine ==="
[ "$DRY_RUN" = true ] && echo "  MODE: DRY RUN (no changes will be made)"
echo "  Repo root: $REPO_ROOT"
echo ""

total_synced=0
total_skipped=0
total_unchanged=0
total_errors=0

sync_plugin() {
  local plugin_key="$1"
  local plugin_rel="${PLUGINS[$plugin_key]}"
  local plugin_path="$REPO_ROOT/$plugin_rel"
  local manifest="$plugin_path/skill-manifest.json"

  if [ ! -f "$manifest" ]; then
    echo "WARN: No manifest at $manifest, skipping $plugin_key"
    return
  fi

  echo "--- Syncing $plugin_key ($plugin_rel) ---"

  local skills_dir="$plugin_path/skills"
  local overlays_dir="$plugin_path/overlays"

  # Parse inherited skills from manifest using simple grep/sed (no jq dependency)
  # Extract inherited skill entries
  local in_inherited=false
  local skill_name=""
  local skill_source=""
  local skill_owner=""
  local synced=0
  local skipped=0
  local unchanged=0

  while IFS= read -r line; do
    # Detect inherited_skills array
    if echo "$line" | grep -q '"inherited_skills"'; then
      in_inherited=true
      continue
    fi

    # Detect end of inherited_skills array
    if [ "$in_inherited" = true ] && echo "$line" | grep -q '^\s*\]'; then
      in_inherited=false
      continue
    fi

    if [ "$in_inherited" != true ]; then
      continue
    fi

    # Extract skill name
    if echo "$line" | grep -q '"name"'; then
      skill_name=$(echo "$line" | sed 's/.*"name": *"\([^"]*\)".*/\1/')
    fi

    # Extract source
    if echo "$line" | grep -q '"source"'; then
      skill_source=$(echo "$line" | sed 's/.*"source": *"\([^"]*\)".*/\1/')
    fi

    # Extract canonical_owner
    if echo "$line" | grep -q '"canonical_owner"'; then
      skill_owner=$(echo "$line" | sed 's/.*"canonical_owner": *"\([^"]*\)".*/\1/')
    fi

    # When we hit a closing brace, process the skill
    if echo "$line" | grep -q '}'; then
      if [ -z "$skill_name" ]; then
        continue
      fi

      # Skip if source is "self" (this plugin IS the canonical source)
      if [ "$skill_source" = "self" ]; then
        skipped=$((skipped + 1))
        skill_name=""
        skill_source=""
        skill_owner=""
        continue
      fi

      # Determine canonical path
      local canonical_dir="$REPO_ROOT/skills/${skill_owner:-javier-montano}/$skill_name"
      local target_dir="$skills_dir/$skill_name"

      if [ ! -d "$canonical_dir" ]; then
        echo "  WARN: Canonical source not found: $canonical_dir (skill: $skill_name)"
        skill_name=""
        skill_source=""
        skill_owner=""
        continue
      fi

      if [ ! -f "$canonical_dir/SKILL.md" ]; then
        echo "  WARN: No SKILL.md in canonical: $canonical_dir"
        skill_name=""
        skill_source=""
        skill_owner=""
        continue
      fi

      # Compare: is the canonical version different from what's in the plugin?
      if [ -f "$target_dir/SKILL.md" ]; then
        # Compare file content (ignoring the overlay section if present)
        canonical_hash=$(md5sum "$canonical_dir/SKILL.md" 2>/dev/null | cut -d' ' -f1 || echo "none")
        target_hash=$(md5sum "$target_dir/SKILL.md" 2>/dev/null | cut -d' ' -f1 || echo "none")

        if [ "$canonical_hash" = "$target_hash" ]; then
          unchanged=$((unchanged + 1))
          skill_name=""
          skill_source=""
          skill_owner=""
          continue
        fi
      fi

      # Sync: copy canonical into plugin
      if [ "$DRY_RUN" = true ]; then
        echo "  WOULD SYNC: $skill_name ($skill_owner → $plugin_key)"
      else
        mkdir -p "$target_dir"

        # Copy entire canonical skill directory
        cp -r "$canonical_dir"/* "$target_dir/" 2>/dev/null || true

        # Apply overlay if it exists
        local overlay_file="$overlays_dir/${skill_name}.md"
        if [ -f "$overlay_file" ]; then
          echo "" >> "$target_dir/SKILL.md"
          cat "$overlay_file" >> "$target_dir/SKILL.md"
          echo "  SYNCED+OVERLAY: $skill_name"
        else
          echo "  SYNCED: $skill_name"
        fi
      fi

      synced=$((synced + 1))

      # Reset for next skill
      skill_name=""
      skill_source=""
      skill_owner=""
    fi
  done < "$manifest"

  # Write sync timestamp
  if [ "$DRY_RUN" = false ] && [ "$synced" -gt 0 ]; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) synced=$synced skipped=$skipped unchanged=$unchanged" > "$plugin_path/.sync-timestamp"
  fi

  echo "  Summary: synced=$synced, self/skipped=$skipped, unchanged=$unchanged"
  echo ""

  total_synced=$((total_synced + synced))
  total_skipped=$((total_skipped + skipped))
  total_unchanged=$((total_unchanged + unchanged))
}

# Sync target plugins
if [ -n "$TARGET_PLUGIN" ]; then
  if [ -z "${PLUGINS[$TARGET_PLUGIN]:-}" ]; then
    echo "ERROR: Unknown plugin '$TARGET_PLUGIN'. Valid: sa, pm, mdf, scriba"
    exit 1
  fi
  sync_plugin "$TARGET_PLUGIN"
else
  for pk in sa pm mdf scriba; do
    sync_plugin "$pk"
  done
fi

echo "=== Sync Complete ==="
echo "  Total synced: $total_synced"
echo "  Total self/skipped: $total_skipped"
echo "  Total unchanged: $total_unchanged"
[ "$DRY_RUN" = true ] && echo "  (DRY RUN — no files were modified)"
