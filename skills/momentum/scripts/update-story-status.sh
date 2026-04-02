#!/usr/bin/env bash
# DEPRECATED: Use momentum-sprint-manager skill instead. This script will be removed in a future version.
# All story status transitions should go through the momentum-sprint-manager executor subagent
# via Agent tool dispatch with Action: status_transition.
#
# update-story-status.sh — Centralized dual-file story status updater
# Updates both sprint-status.yaml (development_status) and story file status field.
# Handles both YAML frontmatter (process stories: `status: <value>`) and
# body section format (product stories: `Status: <value>`).
#
# Usage: update-story-status.sh <story-key> <status>
# Valid statuses: ready-for-dev, in-progress, review, done
#
# Environment: $CLAUDE_PROJECT_DIR must be set (or script infers from git root)

set -euo pipefail

# --- Arguments ---
if [[ $# -ne 2 ]]; then
  echo "Usage: update-story-status.sh <story-key> <status>" >&2
  echo "Valid statuses: ready-for-dev, in-progress, review, done" >&2
  exit 1
fi

STORY_KEY="$1"
NEW_STATUS="$2"

# --- Validate status ---
case "$NEW_STATUS" in
  ready-for-dev|in-progress|review|done) ;;
  *)
    echo "Error: Invalid status '$NEW_STATUS'. Must be one of: ready-for-dev, in-progress, review, done" >&2
    exit 1
    ;;
esac

# --- Resolve project root ---
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null)}"
if [[ -z "$PROJECT_DIR" ]]; then
  echo "Error: Cannot determine project root. Set CLAUDE_PROJECT_DIR or run from a git repo." >&2
  exit 1
fi

SPRINT_STATUS="$PROJECT_DIR/_bmad-output/implementation-artifacts/sprint-status.yaml"

if [[ ! -f "$SPRINT_STATUS" ]]; then
  echo "Error: sprint-status.yaml not found at $SPRINT_STATUS" >&2
  exit 1
fi

# --- Update sprint-status.yaml development_status ---
# Use awk to scope the update to the development_status section only
SPRINT_UPDATED=0
CURRENT_STATUS=""

# Extract current status from development_status section only
CURRENT_STATUS=$(awk '
  /^development_status:/ { in_section=1; next }
  /^[a-zA-Z]/ && in_section { exit }
  in_section && $0 ~ "^  '"${STORY_KEY}"':" { sub(/^.*: */, ""); print; exit }
' "$SPRINT_STATUS")

if [[ -z "$CURRENT_STATUS" ]]; then
  echo "Error: Story key '$STORY_KEY' not found in sprint-status.yaml development_status" >&2
  exit 1
fi

if [[ "$CURRENT_STATUS" == "$NEW_STATUS" ]]; then
  SPRINT_UPDATED=1
  echo "sprint-status.yaml: status already '$NEW_STATUS' (no change needed)"
else
  # Update only within development_status section using awk
  awk -v key="$STORY_KEY" -v status="$NEW_STATUS" '
    /^development_status:/ { in_section=1 }
    /^[a-zA-Z]/ && !/^development_status:/ && in_section { in_section=0 }
    in_section && $0 ~ "^  " key ":" { print "  " key ": " status; next }
    { print }
  ' "$SPRINT_STATUS" > "${SPRINT_STATUS}.tmp" && mv "${SPRINT_STATUS}.tmp" "$SPRINT_STATUS"

  # Update last_updated to today
  TODAY=$(date +%Y-%m-%d)
  sed -i '' "s/^last_updated: .*$/last_updated: ${TODAY}/" "$SPRINT_STATUS"

  SPRINT_UPDATED=1
  echo "sprint-status.yaml: $STORY_KEY → $NEW_STATUS"
fi

# --- Locate story file from momentum_metadata ---
STORY_FILE=""
IN_METADATA=0
IN_STORY_BLOCK=0

while IFS= read -r line; do
  # Detect momentum_metadata section
  if [[ "$line" =~ ^momentum_metadata: ]]; then
    IN_METADATA=1
    continue
  fi

  # Only process within momentum_metadata
  if [[ $IN_METADATA -eq 0 ]]; then
    continue
  fi

  # Detect our story's block (top-level key under momentum_metadata, 2-space indent)
  if [[ "$line" =~ ^"  ${STORY_KEY}:" ]]; then
    IN_STORY_BLOCK=1
    continue
  fi

  # If we hit another top-level key under momentum_metadata (2-space indent with colon), stop
  if [[ $IN_STORY_BLOCK -eq 1 && "$line" =~ ^"  "[a-zA-Z0-9].*: && ! "$line" =~ ^"    " ]]; then
    break
  fi

  # Extract story_file value
  if [[ $IN_STORY_BLOCK -eq 1 && "$line" =~ story_file: ]]; then
    STORY_FILE=$(echo "$line" | sed 's/.*story_file: *"*\([^"]*\)"*/\1/')
    break
  fi
done < "$SPRINT_STATUS"

if [[ -z "$STORY_FILE" ]]; then
  echo "Warning: No story_file found in momentum_metadata for '$STORY_KEY'. Sprint-status updated, but story file not updated." >&2
  exit 0
fi

# Resolve relative to project root
STORY_FILE_PATH="$PROJECT_DIR/$STORY_FILE"

if [[ ! -f "$STORY_FILE_PATH" ]]; then
  echo "Warning: Story file not found at $STORY_FILE_PATH. Sprint-status updated, but story file not updated." >&2
  exit 0
fi

# --- Update story file status field ---
# Process stories use YAML frontmatter: `status: <value>` (lowercase)
# Product stories use body section: `Status: <value>` (capitalized)
# Try lowercase first (frontmatter), then capitalized (body section)
STORY_UPDATED=0

if grep -q "^status: " "$STORY_FILE_PATH"; then
  CURRENT_STORY_STATUS=$(grep "^status: " "$STORY_FILE_PATH" | head -1 | sed 's/^status: *//')
  if [[ "$CURRENT_STORY_STATUS" == "$NEW_STATUS" ]]; then
    echo "story file: status already '$NEW_STATUS' (no change needed)"
  else
    sed -i '' "s/^status: .*$/status: ${NEW_STATUS}/" "$STORY_FILE_PATH"
    echo "story file: $STORY_KEY → $NEW_STATUS"
  fi
  STORY_UPDATED=1
elif grep -q "^Status: " "$STORY_FILE_PATH"; then
  CURRENT_STORY_STATUS=$(grep "^Status: " "$STORY_FILE_PATH" | head -1 | sed 's/^Status: *//')
  if [[ "$CURRENT_STORY_STATUS" == "$NEW_STATUS" ]]; then
    echo "story file: Status already '$NEW_STATUS' (no change needed)"
  else
    sed -i '' "s/^Status: .*$/Status: ${NEW_STATUS}/" "$STORY_FILE_PATH"
    echo "story file: $STORY_KEY → $NEW_STATUS (body section)"
  fi
  STORY_UPDATED=1
fi

if [[ $STORY_UPDATED -eq 0 ]]; then
  echo "Warning: No 'status:' or 'Status:' field found in story file at $STORY_FILE_PATH" >&2
fi

exit 0
