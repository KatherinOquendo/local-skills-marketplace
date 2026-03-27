#!/bin/bash
# generate-manifests.sh — Auto-generate skill-manifest.json for each plugin
# Based on REGISTRY and canonical-decisions data
# Usage: ./scripts/generate-manifests.sh [REPO_ROOT]

set -euo pipefail

REPO_ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"

CSV="$REPO_ROOT/governance/canonical-decisions.csv"
if [ ! -f "$CSV" ]; then
  echo "ERROR: Run compare-duplicates.sh first to generate $CSV"
  exit 1
fi

# Plugin definitions: key -> relative path from repo root
declare -A PLUGINS
PLUGINS[sa]="plugins/javier-montano/sovereign-architect"
PLUGINS[pm]="plugins/javier-montano/pm-project-framework"
PLUGINS[scriba]="plugins/javier-montano/scriba"
PLUGINS[mdf]="plugins/metodologia/metodologia-discovery-framework"

# Canonical source paths (relative from plugin root)
declare -A CANONICAL_SOURCES
CANONICAL_SOURCES[sa]="../../../skills/javier-montano"
CANONICAL_SOURCES[pm]="../../../skills/javier-montano"
CANONICAL_SOURCES[scriba]="../../../skills/javier-montano"
CANONICAL_SOURCES[mdf]="../../../skills/metodologia"

# Secondary source for MDF (also needs javier-montano skills)
# MDF_SECONDARY="../../../skills/javier-montano"

echo "=== Skill Manifest Generator ==="
echo ""

# Build a lookup: skill_name -> recommended_source from CSV
declare -A CANONICAL_MAP
while IFS=',' read -r skill_name rec_source rec_owner canonical_path rest; do
  [ "$skill_name" = "skill_name" ] && continue  # skip header
  CANONICAL_MAP["$skill_name"]="$rec_source:$rec_owner:$canonical_path"
done < "$CSV"

for plugin_key in "${!PLUGINS[@]}"; do
  plugin_path="${PLUGINS[$plugin_key]}"
  full_plugin_path="$REPO_ROOT/$plugin_path"
  skills_dir="$full_plugin_path/skills"
  manifest_file="$full_plugin_path/skill-manifest.json"

  if [ ! -d "$skills_dir" ]; then
    echo "WARN: $skills_dir does not exist, skipping $plugin_key"
    continue
  fi

  echo "Generating manifest for $plugin_key ($plugin_path)..."

  inherited=()
  plugin_only=()

  for skill_dir in "$skills_dir"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name=$(basename "$skill_dir")
    [[ "$skill_name" == .* ]] && continue
    [ -f "$skill_dir/SKILL.md" ] || continue

    # Check if this skill is a duplicate with a canonical decision
    if [ -n "${CANONICAL_MAP[$skill_name]:-}" ]; then
      IFS=':' read -r rec_source rec_owner canonical_path <<< "${CANONICAL_MAP[$skill_name]}"

      # If the canonical source is THIS plugin, it stays as plugin_only (it IS the source)
      if [ "$rec_source" = "$plugin_key" ]; then
        # This plugin owns the canonical version — mark as canonical_source
        inherited+=("{\"name\": \"$skill_name\", \"source\": \"self\", \"overlay\": null, \"note\": \"this plugin is the canonical source\"}")
      else
        # This plugin has a copy that should inherit from canonical
        inherited+=("{\"name\": \"$skill_name\", \"source\": \"canonical\", \"canonical_owner\": \"$rec_owner\", \"overlay\": null}")
      fi
    else
      # Not a duplicate — plugin-only skill
      plugin_only+=("\"$skill_name\"")
    fi
  done

  # Count
  inherited_count=${#inherited[@]}
  plugin_only_count=${#plugin_only[@]}
  total=$((inherited_count + plugin_only_count))

  echo "  Total skills: $total (inherited/shared: $inherited_count, plugin-only: $plugin_only_count)"

  # Write JSON manifest
  {
    echo "{"
    echo "  \"plugin\": \"$plugin_key\","
    echo "  \"plugin_path\": \"$plugin_path\","
    echo "  \"generated\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
    echo "  \"canonical_sources\": {"
    echo "    \"javier-montano\": \"skills/javier-montano\","
    echo "    \"metodologia\": \"skills/metodologia\""
    echo "  },"
    echo "  \"total_skills\": $total,"
    echo "  \"inherited_count\": $inherited_count,"
    echo "  \"plugin_only_count\": $plugin_only_count,"

    # Inherited skills
    echo "  \"inherited_skills\": ["
    first=true
    for item in "${inherited[@]:-}"; do
      [ -z "$item" ] && continue
      if [ "$first" = true ]; then first=false; else echo ","; fi
      printf "    %s" "$item"
    done
    echo ""
    echo "  ],"

    # Plugin-only skills
    echo "  \"plugin_only_skills\": ["
    first=true
    for item in "${plugin_only[@]:-}"; do
      [ -z "$item" ] && continue
      if [ "$first" = true ]; then first=false; else echo ","; fi
      printf "    %s" "$item"
    done
    echo ""
    echo "  ]"
    echo "}"
  } > "$manifest_file"

  echo "  Written: $manifest_file"
  echo ""
done

echo "=== Manifests Generated ==="
echo ""
echo "Next: Run scripts/skill-sync.sh to sync canonical skills into plugins"
