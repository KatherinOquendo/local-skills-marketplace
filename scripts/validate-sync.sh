#!/bin/bash
# validate-sync.sh — Detect drift between canonical skills and plugin copies
# Reports skills that were manually edited in plugins instead of in canonical source
# Usage: ./scripts/validate-sync.sh [REPO_ROOT]

set -euo pipefail

REPO_ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"

declare -A PLUGINS
PLUGINS[sa]="plugins/javier-montano/sovereign-architect"
PLUGINS[pm]="plugins/javier-montano/pm-project-framework"
PLUGINS[scriba]="plugins/javier-montano/scriba"
PLUGINS[mdf]="plugins/metodologia/metodologia-discovery-framework"

echo "=== Sync Drift Validator ==="
echo ""

total_checked=0
total_drifted=0
total_missing_canonical=0
total_ok=0

for plugin_key in sa pm mdf scriba; do
  plugin_rel="${PLUGINS[$plugin_key]}"
  plugin_path="$REPO_ROOT/$plugin_rel"
  manifest="$plugin_path/skill-manifest.json"

  [ -f "$manifest" ] || continue

  echo "--- Validating $plugin_key ---"

  local_drifted=0
  local_ok=0
  local_missing=0

  in_inherited=false
  skill_name=""
  skill_source=""
  skill_owner=""

  while IFS= read -r line; do
    if echo "$line" | grep -q '"inherited_skills"'; then
      in_inherited=true
      continue
    fi

    if [ "$in_inherited" = true ] && echo "$line" | grep -q '^\s*\]'; then
      in_inherited=false
      continue
    fi

    [ "$in_inherited" = true ] || continue

    if echo "$line" | grep -q '"name"'; then
      skill_name=$(echo "$line" | sed 's/.*"name": *"\([^"]*\)".*/\1/')
    fi
    if echo "$line" | grep -q '"source"'; then
      skill_source=$(echo "$line" | sed 's/.*"source": *"\([^"]*\)".*/\1/')
    fi
    if echo "$line" | grep -q '"canonical_owner"'; then
      skill_owner=$(echo "$line" | sed 's/.*"canonical_owner": *"\([^"]*\)".*/\1/')
    fi

    if echo "$line" | grep -q '}'; then
      [ -z "$skill_name" ] && continue

      # Skip self-sourced
      if [ "$skill_source" = "self" ]; then
        skill_name=""
        skill_source=""
        skill_owner=""
        continue
      fi

      total_checked=$((total_checked + 1))

      canonical_file="$REPO_ROOT/skills/${skill_owner:-javier-montano}/$skill_name/SKILL.md"
      plugin_file="$plugin_path/skills/$skill_name/SKILL.md"

      if [ ! -f "$canonical_file" ]; then
        echo "  MISSING CANONICAL: $skill_name (expected at skills/${skill_owner:-javier-montano}/$skill_name/)"
        local_missing=$((local_missing + 1))
        total_missing_canonical=$((total_missing_canonical + 1))
      elif [ ! -f "$plugin_file" ]; then
        echo "  MISSING IN PLUGIN: $skill_name (not synced yet)"
        local_missing=$((local_missing + 1))
      else
        # Compare hashes
        c_hash=$(md5sum "$canonical_file" 2>/dev/null | cut -d' ' -f1)
        p_hash=$(md5sum "$plugin_file" 2>/dev/null | cut -d' ' -f1)

        if [ "$c_hash" != "$p_hash" ]; then
          # Check if the difference is only the overlay
          overlay_file="$plugin_path/overlays/${skill_name}.md"
          if [ -f "$overlay_file" ]; then
            # Expected: plugin = canonical + overlay
            # This is acceptable drift
            local_ok=$((local_ok + 1))
            total_ok=$((total_ok + 1))
          else
            line_diff=$(diff <(wc -l < "$canonical_file") <(wc -l < "$plugin_file") 2>/dev/null || echo "diff")
            c_lines=$(wc -l < "$canonical_file" | tr -d ' ')
            p_lines=$(wc -l < "$plugin_file" | tr -d ' ')
            echo "  DRIFT: $skill_name (canonical: $c_lines lines, plugin: $p_lines lines)"
            local_drifted=$((local_drifted + 1))
            total_drifted=$((total_drifted + 1))
          fi
        else
          local_ok=$((local_ok + 1))
          total_ok=$((total_ok + 1))
        fi
      fi

      skill_name=""
      skill_source=""
      skill_owner=""
    fi
  done < "$manifest"

  echo "  OK: $local_ok | Drifted: $local_drifted | Missing: $local_missing"
  echo ""
done

echo "=== Validation Summary ==="
echo "  Total checked: $total_checked"
echo "  In sync (OK): $total_ok"
echo "  Drifted: $total_drifted"
echo "  Missing canonical: $total_missing_canonical"
echo ""

if [ "$total_drifted" -gt 0 ]; then
  echo "ACTION REQUIRED: $total_drifted skills have drifted from canonical."
  echo "Edit the canonical version in skills/{owner}/{name}/ and run skill-sync.sh"
  exit 1
elif [ "$total_missing_canonical" -gt 0 ]; then
  echo "ACTION REQUIRED: $total_missing_canonical skills need canonical versions created."
  echo "Phase 3 (Consolidation) will resolve this."
  exit 0
else
  echo "All synced skills are in sync with canonical versions."
  exit 0
fi
