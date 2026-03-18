#!/bin/bash
# Push to both remotes: origin (javiermontano-sofka/jm-labs) and personal (wip mirror)
# Usage: ./scripts/push-both.sh [branch]

BRANCH=${1:-main}

echo "Pushing to origin (jm-labs)..."
git push origin "$BRANCH"

echo "Pushing to personal (wip)..."
git push personal "$BRANCH"

echo "Both remotes synced on branch: $BRANCH"
