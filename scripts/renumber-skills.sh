#!/bin/bash
# renumber-skills.sh — Rename numbered skills to canonical 0000-9999 order
# Based on governance/canonical-numbering.md
# Usage: ./scripts/renumber-skills.sh [--execute] [REPO_ROOT]

set -euo pipefail

EXECUTE=false
REPO_ROOT=""

for arg in "$@"; do
  case "$arg" in
    --execute) EXECUTE=true ;;
    *) REPO_ROOT="$arg" ;;
  esac
done

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
SKILLS_DIR="$REPO_ROOT/skills/javier-montano"

echo "=== Canonical Renumbering Engine ==="
echo "  Mode: $([ "$EXECUTE" = true ] && echo 'EXECUTE' || echo 'DRY RUN')"
echo ""

# Mapping: new_number:new_name:old_pattern (old_pattern matches directory names)
# Uses | as delimiter since names have spaces and braces
MAPPINGS=(
  # 0000-0999 Input & Analysis
  "0001|input-analysis|009-input-analysis*"
  "0002|asis-analysis|010-asis-analysis*"
  "0003|flow-mapping|011-flow-mapping*"
  "0004|stakeholder-mapping|013-stakeholder-mapping*"
  "0005|competitive-intelligence|016-competitive-intelligence*"
  "0006|scenario-analysis|014-scenario-analysis*"
  "0007|risk-assessment|015-risk-assessment*"
  "0008|cost-estimation|017-cost-estimation*"
  "0009|technical-feasibility|018-technical-feasibility*"
  "0010|dependency-analysis|021-dependency-analysis*"
  "0011|assumption-log|020-assumption-log*"
  "0012|user-story-writer|022-user-story-writer*"
  "0013|product-strategy|023-product-strategy*"
  "0014|functional-spec|012-functional-spec*"
  "0015|discovery-orchestrator|019-discovery-orchestrator*"
  # 1000-1999 Design & Architecture
  "1001|system-design|030-system-design*"
  "1002|architecture-tobe|035-architecture-tobe*"
  "1003|component-designer|029-component-designer*"
  "1004|responsive-design-system|034-responsive-design-system*"
  "1005|state-management-design|028-state-management-design*"
  "1006|data-flow-architecture|031-data-flow-architecture*"
  "1007|integration-architecture|032-integration-architecture*"
  "1008|api-designer|025-api-designer*"
  "1009|database-architecture|026-database-architecture*"
  "1010|firebase-architecture|024-firebase-architecture*"
  "1011|auth-architecture|027-auth-architecture*"
  "1012|pwa-architecture|033-pwa-architecture*"
  # 2000-2999 Frontend & UI
  "2001|scaffold-html-css|036-scaffold-html-css*"
  "2002|html-semantic-builder|040-html-semantic-builder*"
  "2003|css-architecture|039-css-architecture*"
  "2004|javascript-patterns|041-javascript-patterns*"
  "2005|scaffold-react-app|037-scaffold-react-app*"
  "2006|react-component-library|042-react-component-library*"
  "2007|scaffold-angular-app|038-scaffold-angular-app*"
  "2008|angular-module-builder|043-angular-module-builder*"
  "2009|form-builder|044-form-builder*"
  "2010|ui-kit-builder|047-ui-kit-builder*"
  "2011|animation-motion|045-animation-motion*"
  "2012|spa-routing|046-spa-routing*"
  "2013|data-visualization|048-data-visualization*"
  "2014|landing-page-builder|050-landing-page-builder*"
  "2015|email-template-builder|049-email-template-builder*"
  # 3000-3999 Backend & Logic
  "3001|node-api-builder|052-node-api-builder*"
  "3002|firebase-functions|051-firebase-functions*"
  "3003|server-middleware|054-server-middleware*"
  "3004|webhook-handler|056-webhook-handler*"
  "3005|background-jobs|055-background-jobs*"
  "3006|notification-service|058-notification-service*"
  "3007|file-storage|057-file-storage*"
  "3008|google-apis-integration|059-google-apis-integration*"
  "3009|firebase-extensions|053-firebase-extensions*"
  "3010|error-handling-patterns|060-error-handling-patterns*"
  "3011|caching-strategy|061-caching-strategy*"
  "3012|serverless-patterns|062-serverless-patterns*"
  # 4000-4999 Data & Storage
  "4001|firestore-schema-design|063-firestore-schema-design*"
  "4002|firestore-security-rules|064-firestore-security-rules*"
  "4003|realtime-database|065-realtime-database*"
  "4004|data-migration|066-data-migration*"
  "4005|data-validation|067-data-validation*"
  "4006|analytics-implementation|068-analytics-implementation*"
  "4007|search-implementation|069-search-implementation*"
  "4008|backup-recovery|070-backup-recovery*"
  # 5000-5999 Security & Auth
  "5001|firebase-auth-setup|071-firebase-auth-setup*"
  "5002|role-based-access|072-role-based-access*"
  "5003|oauth-social-login|073-oauth-social-login*"
  "5004|web-security-implementation|074-web-security-implementation*"
  "5005|api-security|075-api-security*"
  "5006|secrets-management|076-secrets-management*"
  "5007|privacy-compliance|077-privacy-compliance*"
  "5008|penetration-testing-guide|078-penetration-testing-guide*"
  # 6000-6999 Testing & Quality
  "6001|unit-testing|079-unit-testing*"
  "6002|integration-testing|080-integration-testing*"
  "6003|e2e-testing|081-e2e-testing*"
  "6004|accessibility-audit|082-accessibility-audit*"
  "6005|code-review-checklist|083-code-review-checklist*"
  "6006|quality-metrics|084-quality-metrics*"
  "6007|test-data-factory|085-test-data-factory*"
  "6008|visual-regression-testing|086-visual-regression-testing*"
  "6009|firebase-emulator-setup|087-firebase-emulator-setup*"
  # 7000-7999 DevOps & Deployment
  "7001|hostinger-deployment|088-hostinger-deployment*"
  "7002|firebase-hosting-setup|089-firebase-hosting-setup*"
  "7003|ci-cd-pipeline|090-ci-cd-pipeline*"
  "7004|environment-management|091-environment-management*"
  "7005|monitoring-alerting|092-monitoring-alerting*"
  "7006|domain-dns-setup|093-domain-dns-setup*"
  "7007|release-strategy|094-release-strategy*"
  "7008|build-optimization|095-build-optimization*"
  # 8000-8999 Performance & Optimization
  "8001|web-performance|096-web-performance*"
  "8002|seo-technical|097-seo-technical*"
  "8003|image-optimization|098-image-optimization*"
  "8004|bundle-analysis|099-bundle-analysis*"
  "8005|firebase-cost-optimization|100-firebase-cost-optimization*"
  # 9000-9999 Meta & Orchestration
  "9001|skill-forge|001-skill-forge*"
  "9002|workflow-forge|002-workflow-forge*"
  "9003|kit-orchestrator|003-kit-orchestrator*"
  "9004|scope-guard|004-scope-guard*"
  "9005|quality-gatekeeper|005-quality-gatekeeper*"
  "9006|context-optimizer|006-context-optimizer*"
  "9007|session-manager|007-session-manager*"
  "9008|output-contract-enforcer|008-output-contract-enforcer*"
  "9009|technical-documentation|101-technical-documentation*"
)

renamed=0
skipped=0
not_found=0

for mapping in "${MAPPINGS[@]}"; do
  IFS='|' read -r new_num new_name old_pattern <<< "$mapping"

  new_dir="$SKILLS_DIR/${new_num}-${new_name}"

  # Find old directories matching pattern
  found=false
  for old_dir in "$SKILLS_DIR"/$old_pattern; do
    [ -d "$old_dir" ] || continue
    found=true
    old_name=$(basename "$old_dir")

    if [ "$old_dir" = "$new_dir" ]; then
      skipped=$((skipped + 1))
      continue
    fi

    if [ "$EXECUTE" = true ]; then
      # If target already exists, merge (keep the better SKILL.md)
      if [ -d "$new_dir" ]; then
        old_lines=$(wc -l < "$old_dir/SKILL.md" 2>/dev/null | tr -dc '0-9')
        new_lines=$(wc -l < "$new_dir/SKILL.md" 2>/dev/null | tr -dc '0-9')
        old_lines=${old_lines:-0}; new_lines=${new_lines:-0}
        if [ "$old_lines" -gt "$new_lines" ]; then
          rm -rf "$new_dir"
          mv "$old_dir" "$new_dir"
          echo "  RENAMED (better): $old_name → $(basename "$new_dir") ($old_lines > $new_lines lines)"
        else
          rm -rf "$old_dir"
          echo "  REMOVED (inferior dup): $old_name (${old_lines}L < ${new_lines}L at $(basename "$new_dir"))"
        fi
      else
        mv "$old_dir" "$new_dir"
        echo "  RENAMED: $old_name → $(basename "$new_dir")"
      fi
    else
      echo "  WOULD RENAME: $old_name → ${new_num}-${new_name}"
    fi
    renamed=$((renamed + 1))
  done

  if [ "$found" = false ]; then
    not_found=$((not_found + 1))
    [ "$EXECUTE" != true ] && echo "  NOT FOUND: $old_pattern"
  fi
done

# Clean up unnumbered duplicates (079-unit-testing without {Testing}, etc.)
echo ""
echo "=== Cleaning unnumbered duplicates ==="
for dup_dir in "$SKILLS_DIR"/0[0-9][0-9]-*; do
  [ -d "$dup_dir" ] || continue
  old_name=$(basename "$dup_dir")
  # These are old 3-digit numbered dirs that should have been caught above
  if [ "$EXECUTE" = true ]; then
    rm -rf "$dup_dir"
    echo "  REMOVED leftover: $old_name"
  else
    echo "  WOULD REMOVE leftover: $old_name"
  fi
done

echo ""
echo "=== Summary ==="
echo "  Renamed: $renamed"
echo "  Skipped (already correct): $skipped"
echo "  Not found: $not_found"
[ "$EXECUTE" != true ] && echo "  (DRY RUN — no changes made. Use --execute to apply)"
