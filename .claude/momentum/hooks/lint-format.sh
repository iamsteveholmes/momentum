#!/usr/bin/env bash
# lint-format.sh — PostToolUse hook: auto-lint and auto-format on every file edit
# Fires after Write, Edit, or NotebookEdit tool use.
#
# Output format (always exactly one line):
#   [momentum-lint] ✓ checked [file path] — clean
#   [momentum-lint] ✓ auto-fixed [N issue(s)] in [file path]
#   [momentum-lint] ✗ [N issues] — [file:line of first] — [likely cause]
#   [momentum-lint] ◦ skipped [file path] — no lint tool configured
#
# Per-extension dispatch:
#   .py  → ruff check FILE (if ruff available, skip if not)
#   .json → python3 -m json.tool FILE > /dev/null
#   .sh/.bash → shellcheck FILE (if available, skip if not)
#   .md  → trailing whitespace check on non-empty lines
#   Other → skip silently
#
# Session state: appends modified file path to .claude/momentum/session-modified-files.txt
# Re-entrancy: uses filesystem lockfile to prevent recursive hook firing

set -euo pipefail

FILE_PATH="${1:-}"

# --- Re-entrancy suppression (filesystem lockfile — process-boundary-safe) ---
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || echo "")}"
if [[ -z "$PROJECT_DIR" ]]; then
  # Can't determine project dir — skip silently
  exit 0
fi

MOMENTUM_DIR="$PROJECT_DIR/.claude/momentum"
LOCKFILE="$MOMENTUM_DIR/.lint-running"
SESSION_FILE="$MOMENTUM_DIR/session-modified-files.txt"

# Check lockfile — suppress re-entrancy
if [[ -f "$LOCKFILE" ]]; then
  exit 0
fi

# Create lockfile; remove on exit (covers normal exit and signals)
mkdir -p "$MOMENTUM_DIR"
touch "$LOCKFILE"
trap "rm -f '$LOCKFILE'" EXIT

# --- Validate file path ---
if [[ -z "$FILE_PATH" ]]; then
  # No file path provided — skip silently
  exit 0
fi

# --- Session state: record modified file (dedup) ---
mkdir -p "$MOMENTUM_DIR"
grep -qxF "$FILE_PATH" "$SESSION_FILE" 2>/dev/null || echo "$FILE_PATH" >> "$SESSION_FILE"

# --- Per-extension lint dispatch ---
EXT="${FILE_PATH##*.}"
LINT_CMD=""
IS_FIX_TOOL=false
IS_MD_CHECK=false

case "$EXT" in
  py)
    if command -v ruff >/dev/null 2>&1; then
      # Try ruff format first (auto-fix), then ruff check (lint)
      LINT_CMD="ruff format"
      IS_FIX_TOOL=true
    fi
    ;;
  json)
    LINT_CMD="python3 -m json.tool"
    ;;
  sh|bash)
    if command -v shellcheck >/dev/null 2>&1; then
      LINT_CMD="shellcheck"
    fi
    ;;
  md)
    IS_MD_CHECK=true
    ;;
  *)
    # Skip silently — no output for unsupported extensions
    exit 0
    ;;
esac

# If no tool available for this extension, skip silently
if [[ -z "$LINT_CMD" && "$IS_MD_CHECK" == "false" ]]; then
  exit 0
fi

# --- Run per-extension lint ---
if [[ "$IS_MD_CHECK" == "true" ]]; then
  # Markdown: check for trailing whitespace on non-empty lines
  MD_ISSUES=$(grep -nE '[^ ] +$' "$FILE_PATH" 2>/dev/null || true)
  if [[ -n "$MD_ISSUES" ]]; then
    ISSUE_COUNT=$(echo "$MD_ISSUES" | grep -c '.' 2>/dev/null || echo "1")
    FIRST_LINE=$(echo "$MD_ISSUES" | head -1 | cut -d: -f1)
    echo "[momentum-lint] ✗ ${ISSUE_COUNT} issue(s) — ${FILE_PATH}:${FIRST_LINE} — trailing whitespace"
  else
    echo "[momentum-lint] ✓ checked ${FILE_PATH} — clean"
  fi
  exit 0
fi

if [[ "$LINT_CMD" == "python3 -m json.tool" ]]; then
  # JSON validation — check only, no fix
  LINT_OUTPUT=""
  LINT_EXIT=0
  LINT_OUTPUT=$(python3 -m json.tool "$FILE_PATH" > /dev/null 2>&1) || LINT_EXIT=$?
  if [[ "$LINT_EXIT" -eq 0 ]]; then
    echo "[momentum-lint] ✓ checked ${FILE_PATH} — clean"
  else
    echo "[momentum-lint] ✗ 1 issue(s) — ${FILE_PATH} — invalid JSON"
  fi
  exit 0
fi

# --- Run lint/format tool ---
LINT_OUTPUT=""
LINT_EXIT=0
LINT_OUTPUT=$(cd "$PROJECT_DIR" && $LINT_CMD "$FILE_PATH" 2>&1) || LINT_EXIT=$?

if [[ "$IS_FIX_TOOL" == "true" ]]; then
  # Fix-only tools (ruff format): check if file was actually changed
  GIT_DIFF_COUNT=$(cd "$PROJECT_DIR" && git diff --name-only -- "$FILE_PATH" 2>/dev/null | wc -l | tr -d ' ') || GIT_DIFF_COUNT=0
  if [[ "$GIT_DIFF_COUNT" -gt 0 ]]; then
    echo "[momentum-lint] ✓ auto-fixed 1 issue(s) in $FILE_PATH"
  else
    echo "[momentum-lint] ✓ checked $FILE_PATH — clean"
  fi
  # Also run ruff check after formatting
  if command -v ruff >/dev/null 2>&1; then
    CHECK_OUTPUT=""
    CHECK_EXIT=0
    CHECK_OUTPUT=$(cd "$PROJECT_DIR" && ruff check "$FILE_PATH" 2>&1) || CHECK_EXIT=$?
    if [[ "$CHECK_EXIT" -ne 0 ]]; then
      ISSUE_COUNT=$(echo "$CHECK_OUTPUT" | grep -c '[^[:space:]]' 2>/dev/null || echo "1")
      FIRST_ISSUE=$(echo "$CHECK_OUTPUT" | head -1 | sed 's/[[:space:]]*$//')
      echo "[momentum-lint] ✗ ${ISSUE_COUNT} issue(s) — ${FIRST_ISSUE}"
    fi
  fi
elif [[ "$LINT_EXIT" -eq 0 ]]; then
  echo "[momentum-lint] ✓ checked $FILE_PATH — clean"
else
  # Lint reported issues
  FIRST_ISSUE_LINE=$(echo "$LINT_OUTPUT" | head -1 | sed 's/[[:space:]]*$//')
  ISSUE_COUNT=$(echo "$LINT_OUTPUT" | grep -c '[^[:space:]]' 2>/dev/null || echo "1")

  if [[ -n "$FIRST_ISSUE_LINE" ]]; then
    FILE_LINE_REF=$(echo "$FIRST_ISSUE_LINE" | grep -oE '[^/[:space:]]+\.[a-z]+:[0-9]+[^:]*' | head -1 || echo "")
    if [[ -z "$FILE_LINE_REF" ]]; then
      FILE_LINE_REF="$FILE_PATH"
    fi
    CAUSE=$(echo "$FIRST_ISSUE_LINE" | sed 's/.*:[0-9][0-9]*:[[:space:]]*//' | sed 's/.*error:[[:space:]]*//' | sed 's/.*warning:[[:space:]]*//' | cut -c1-80)
    if [[ -z "$CAUSE" ]]; then
      CAUSE="$FIRST_ISSUE_LINE"
    fi
    echo "[momentum-lint] ✗ ${ISSUE_COUNT} issue(s) — ${FILE_LINE_REF} — ${CAUSE}"
  else
    echo "[momentum-lint] ✗ issue(s) found — $FILE_PATH — lint tool exited $LINT_EXIT"
  fi
fi

exit 0
