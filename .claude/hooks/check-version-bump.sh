#!/usr/bin/env bash
# Pre-push hook: block push if skills/momentum/ changed without plugin.json version bump.
# Momentum-project-specific — does NOT ship with the plugin.

set -euo pipefail

# Only check on git push
if [[ "${CLAUDE_TOOL_INPUT:-}" != *"git push"* ]]; then
  exit 0
fi

# Get the commits being pushed (unpushed commits)
UPSTREAM=$(git rev-parse --abbrev-ref '@{upstream}' 2>/dev/null || echo "")
if [[ -z "$UPSTREAM" ]]; then
  exit 0  # No upstream — can't compare
fi

COMMITS=$(git log "$UPSTREAM..HEAD" --name-only --pretty=format:"" 2>/dev/null | sort -u)

# Check if any commits touch skills/momentum/
if ! echo "$COMMITS" | grep -q "^skills/momentum/"; then
  exit 0  # No plugin changes — no version bump needed
fi

# Check if plugin.json was also changed
if echo "$COMMITS" | grep -q "skills/momentum/.claude-plugin/plugin.json"; then
  exit 0  # Version was bumped — good to go
fi

# Plugin changes without version bump — block
echo "BLOCK: Push includes changes to skills/momentum/ but plugin.json version was not bumped."
echo "Run: edit skills/momentum/.claude-plugin/plugin.json and bump the version before pushing."
exit 2
