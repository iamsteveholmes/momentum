#!/usr/bin/env bash
# lint-format.sh — PostToolUse hook: auto-lint and auto-format on every file edit
# Fires after Write, Edit, or NotebookEdit tool use.
#
# Output format (always exactly one line):
#   [lint] ✓ checked [file path] — clean
#   [lint] ✓ auto-fixed [N issue(s)] in [file path]
#   [lint] ✗ [N issues] — [file:line of first] — [likely cause]
#   [lint] ◦ skipped — no lint tool configured
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

# --- Session state: record modified file ---
mkdir -p "$MOMENTUM_DIR"
echo "$FILE_PATH" >> "$SESSION_FILE"

# --- Lint tool detection ---
# Walk up from file's directory looking for project root markers (same dir as PROJECT_DIR)
detect_lint_tool() {
  local pkg_json="$PROJECT_DIR/package.json"
  local prettierrc="$PROJECT_DIR/.prettierrc"
  local prettierrc_json="$PROJECT_DIR/.prettierrc.json"
  local prettier_config="$PROJECT_DIR/prettier.config.js"
  local eslintrc="$PROJECT_DIR/.eslintrc"
  local eslintrc_json="$PROJECT_DIR/.eslintrc.json"
  local eslint_config="$PROJECT_DIR/eslint.config.js"
  local pyproject="$PROJECT_DIR/pyproject.toml"
  local setup_cfg="$PROJECT_DIR/setup.cfg"

  # 1. Check package.json scripts.lint or scripts.format
  if [[ -f "$pkg_json" ]]; then
    local lint_script
    lint_script=$(python3 -c "
import json, sys
try:
    data = json.load(open('$pkg_json'))
    scripts = data.get('scripts', {})
    if 'lint' in scripts:
        print('npm run lint')
    elif 'format' in scripts:
        print('npm run format')
except:
    pass
" 2>/dev/null || echo "")
    if [[ -n "$lint_script" ]]; then
      echo "$lint_script"
      return
    fi
  fi

  # 2. Prettier config files
  if [[ -f "$prettierrc" || -f "$prettierrc_json" || -f "$prettier_config" ]]; then
    echo "prettier --write"
    return
  fi

  # 3. ESLint config files
  if [[ -f "$eslintrc" || -f "$eslintrc_json" || -f "$eslint_config" ]]; then
    echo "eslint --fix"
    return
  fi

  # 4. Python tools: pyproject.toml with ruff or black
  if [[ -f "$pyproject" ]]; then
    if grep -q '\[tool\.ruff\]' "$pyproject" 2>/dev/null; then
      echo "ruff format"
      return
    fi
    if grep -q '\[tool\.black\]' "$pyproject" 2>/dev/null; then
      echo "black"
      return
    fi
  fi

  # 5. setup.cfg with flake8
  if [[ -f "$setup_cfg" ]] && grep -q '\[flake8\]' "$setup_cfg" 2>/dev/null; then
    echo "flake8"
    return
  fi

  # 6. No tool found
  echo ""
}

LINT_TOOL=$(detect_lint_tool)

if [[ -z "$LINT_TOOL" ]]; then
  echo "[lint] ◦ skipped — no lint tool configured"
  exit 0
fi

# --- Run lint tool ---
# Determine if the tool supports auto-fix (write-back) or is lint-only
LINT_CMD=""
IS_FIX_ONLY=false

case "$LINT_TOOL" in
  "prettier --write")
    LINT_CMD="prettier --write \"$FILE_PATH\""
    IS_FIX_ONLY=true
    ;;
  "eslint --fix")
    LINT_CMD="eslint --fix \"$FILE_PATH\""
    IS_FIX_ONLY=false
    ;;
  "ruff format")
    LINT_CMD="ruff format \"$FILE_PATH\""
    IS_FIX_ONLY=true
    ;;
  "black")
    LINT_CMD="black \"$FILE_PATH\""
    IS_FIX_ONLY=true
    ;;
  "flake8")
    LINT_CMD="flake8 \"$FILE_PATH\""
    IS_FIX_ONLY=false
    ;;
  npm\ run\ *)
    # npm scripts — run without file arg; they handle their own scope
    LINT_CMD="$LINT_TOOL"
    IS_FIX_ONLY=false
    ;;
  *)
    LINT_CMD="$LINT_TOOL \"$FILE_PATH\""
    IS_FIX_ONLY=false
    ;;
esac

# Capture output and exit code
LINT_OUTPUT=""
LINT_EXIT=0
LINT_OUTPUT=$(cd "$PROJECT_DIR" && eval "$LINT_CMD" 2>&1) || LINT_EXIT=$?

# --- Parse results and output one line ---
if [[ "$IS_FIX_ONLY" == "true" ]]; then
  # Fix-only tools (prettier, ruff format, black): any run = auto-fix applied
  # Check if file was actually changed by comparing with git
  GIT_DIFF_COUNT=$(cd "$PROJECT_DIR" && git diff --name-only -- "$FILE_PATH" 2>/dev/null | wc -l | tr -d ' ') || GIT_DIFF_COUNT=0
  if [[ "$GIT_DIFF_COUNT" -gt 0 ]]; then
    echo "[lint] ✓ auto-fixed 1 issue(s) in $FILE_PATH"
  else
    echo "[lint] ✓ checked $FILE_PATH — clean"
  fi
elif [[ $LINT_EXIT -eq 0 ]]; then
  echo "[lint] ✓ checked $FILE_PATH — clean"
else
  # Lint reported issues — extract location and cause from first issue line
  FIRST_ISSUE_LINE=$(echo "$LINT_OUTPUT" | head -1 | sed 's/[[:space:]]*$//')

  # Count actual issue lines (non-empty lines that look like lint output)
  ISSUE_COUNT=$(echo "$LINT_OUTPUT" | grep -c '[^[:space:]]' 2>/dev/null || echo "1")

  if [[ -n "$FIRST_ISSUE_LINE" ]]; then
    # Try to extract file:line reference — typical pattern: "file.ext:LINE:COL: message"
    # or "file.ext(LINE,COL): message" or just use the full first line
    FILE_LINE_REF=$(echo "$FIRST_ISSUE_LINE" | grep -oE '[^/[:space:]]+\.[a-z]+:[0-9]+[^:]*' | head -1 || echo "")
    if [[ -z "$FILE_LINE_REF" ]]; then
      FILE_LINE_REF="$FILE_PATH"
    fi
    # Extract cause: everything after the location reference
    CAUSE=$(echo "$FIRST_ISSUE_LINE" | sed 's/.*:[0-9][0-9]*:[[:space:]]*//' | sed 's/.*error:[[:space:]]*//' | sed 's/.*warning:[[:space:]]*//' | cut -c1-80)
    if [[ -z "$CAUSE" ]]; then
      CAUSE="$FIRST_ISSUE_LINE"
    fi
    echo "[lint] ✗ ${ISSUE_COUNT} issue(s) — ${FILE_LINE_REF} — ${CAUSE}"
  else
    echo "[lint] ✗ issue(s) found — $FILE_PATH — lint tool exited $LINT_EXIT"
  fi
fi

exit 0
