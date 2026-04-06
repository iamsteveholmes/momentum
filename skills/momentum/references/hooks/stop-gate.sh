#!/usr/bin/env bash
# stop-gate.sh — Stop hook: conditional quality checks before session end
# Fires before Claude Code session closes.
#
# Output format (one line per check):
#   [stop-gate] ✓ checked lint — clean
#   [stop-gate] ✗ lint: [N issues] — [file:line of first] — fix before closing
#   [stop-gate] ◦ lint — no lint tool configured
#   [stop-gate] ✓ checked tests — [N] passed
#   [stop-gate] ✗ tests: [N failed] — [failing test name] — [failure summary]
#   [stop-gate] ◦ tests — no test runner configured
#
# Session state contract:
#   - Reads .claude/momentum/session-modified-files.txt (written by PostToolUse lint hook)
#   - Deletes session state file after reading (ensures clean state for next session)
#
# Exit codes:
#   0 — all checks passed or skipped (session may close)
#   1 — lint or tests failed (session close blocked)

set -uo pipefail

# --- Project root detection ---
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || echo "")}"
if [[ -z "$PROJECT_DIR" ]]; then
  # Can't determine project dir — skip silently (don't block session)
  exit 0
fi

MOMENTUM_DIR="$PROJECT_DIR/.claude/momentum"
SESSION_FILE="$MOMENTUM_DIR/session-modified-files.txt"

# --- Session state: determine if code was modified this session ---
CODE_MODIFIED=false
if [[ -s "$SESSION_FILE" ]]; then
  CODE_MODIFIED=true
fi

# Always clean up session state file (ensures clean state for next session)
rm -f "$SESSION_FILE"

# Track overall exit status
GATE_STATUS=0

# --- Lint tool detection (full-project mode, read-only — no auto-fix) ---
detect_lint_cmd() {
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
        print('npm run format -- --check')
except:
    pass
" 2>/dev/null || echo "")
    if [[ -n "$lint_script" ]]; then
      echo "$lint_script"
      return
    fi
  fi

  # 2. Prettier config files — check-only mode (no auto-fix at session close)
  if [[ -f "$prettierrc" || -f "$prettierrc_json" || -f "$prettier_config" ]]; then
    echo "prettier --check ."
    return
  fi

  # 3. ESLint config files
  if [[ -f "$eslintrc" || -f "$eslintrc_json" || -f "$eslint_config" ]]; then
    echo "eslint ."
    return
  fi

  # 4. Python tools: pyproject.toml with ruff or black
  if [[ -f "$pyproject" ]]; then
    if grep -q '\[tool\.ruff\]' "$pyproject" 2>/dev/null; then
      echo "ruff check ."
      return
    fi
    if grep -q '\[tool\.black\]' "$pyproject" 2>/dev/null; then
      echo "black --check ."
      return
    fi
  fi

  # 5. setup.cfg with [flake8]
  if [[ -f "$setup_cfg" ]]; then
    if grep -q '\[flake8\]' "$setup_cfg" 2>/dev/null; then
      echo "flake8 ."
      return
    fi
  fi

  # No lint tool found
  echo ""
}

# --- Test runner detection ---
detect_test_cmd() {
  local pkg_json="$PROJECT_DIR/package.json"
  local jest_config_js="$PROJECT_DIR/jest.config.js"
  local jest_config_ts="$PROJECT_DIR/jest.config.ts"
  local vitest_config_js="$PROJECT_DIR/vitest.config.js"
  local vitest_config_ts="$PROJECT_DIR/vitest.config.ts"
  local pytest_ini="$PROJECT_DIR/pytest.ini"
  local pyproject="$PROJECT_DIR/pyproject.toml"
  local setup_cfg="$PROJECT_DIR/setup.cfg"

  # 1. Check package.json scripts.test
  if [[ -f "$pkg_json" ]]; then
    local test_script
    test_script=$(python3 -c "
import json, sys
try:
    data = json.load(open('$pkg_json'))
    scripts = data.get('scripts', {})
    if 'test' in scripts:
        print('npm test')
except:
    pass
" 2>/dev/null || echo "")
    if [[ -n "$test_script" ]]; then
      echo "$test_script"
      return
    fi
  fi

  # 2. Jest config
  if [[ -f "$jest_config_js" || -f "$jest_config_ts" ]]; then
    echo "npx jest --passWithNoTests"
    return
  fi

  # 3. Vitest config
  if [[ -f "$vitest_config_js" || -f "$vitest_config_ts" ]]; then
    echo "npx vitest run"
    return
  fi

  # 4. pytest
  if [[ -f "$pytest_ini" ]]; then
    echo "pytest"
    return
  fi
  if [[ -f "$pyproject" ]]; then
    if grep -q '\[tool\.pytest\.ini_options\]' "$pyproject" 2>/dev/null; then
      echo "pytest"
      return
    fi
  fi
  if [[ -f "$setup_cfg" ]]; then
    if grep -q '\[tool:pytest\]' "$setup_cfg" 2>/dev/null; then
      echo "pytest"
      return
    fi
  fi

  # No test runner found
  echo ""
}

# --- Run lint (unconditional — catches files modified outside Claude Code) ---
LINT_CMD=$(detect_lint_cmd)

if [[ -z "$LINT_CMD" ]]; then
  echo "[stop-gate] ◦ lint — no lint tool configured"
else
  # Run lint in project root, capture output and exit code
  cd "$PROJECT_DIR"
  LINT_OUTPUT=$(eval "$LINT_CMD" 2>&1) || LINT_EXIT=$?
  LINT_EXIT="${LINT_EXIT:-0}"

  if [[ "$LINT_EXIT" -eq 0 ]]; then
    echo "[stop-gate] ✓ checked lint — clean"
  else
    # Count issues (lines that look like errors/warnings, or just count output lines as proxy)
    ISSUE_COUNT=$(echo "$LINT_OUTPUT" | grep -c '.' 2>/dev/null || echo "?")
    # Extract first file:line reference if available
    FIRST_REF=$(echo "$LINT_OUTPUT" | grep -oE '[^[:space:]]+:[0-9]+' | head -1 || echo "")
    if [[ -n "$FIRST_REF" ]]; then
      echo "[stop-gate] ✗ lint: ${ISSUE_COUNT} issues — ${FIRST_REF} — fix before closing"
    else
      echo "[stop-gate] ✗ lint: ${ISSUE_COUNT} issues — fix before closing"
    fi
    GATE_STATUS=1
  fi
fi

# --- Run tests (conditional — only if code was modified this session) ---
if [[ "$CODE_MODIFIED" == "false" ]]; then
  # Tests skipped — no code modified this session
  :
else
  TEST_CMD=$(detect_test_cmd)

  if [[ -z "$TEST_CMD" ]]; then
    echo "[stop-gate] ◦ tests — no test runner configured"
  else
    cd "$PROJECT_DIR"
    TEST_OUTPUT=$(eval "$TEST_CMD" 2>&1) || TEST_EXIT=$?
    TEST_EXIT="${TEST_EXIT:-0}"

    if [[ "$TEST_EXIT" -eq 0 ]]; then
      # Try to extract pass count from output
      PASS_COUNT=$(echo "$TEST_OUTPUT" | grep -oE '[0-9]+ (passed|tests? passed|passing)' | grep -oE '^[0-9]+' | head -1 || echo "")
      if [[ -n "$PASS_COUNT" ]]; then
        echo "[stop-gate] ✓ checked tests — ${PASS_COUNT} passed"
      else
        echo "[stop-gate] ✓ checked tests — passed"
      fi
    else
      # Extract failure info
      FAIL_COUNT=$(echo "$TEST_OUTPUT" | grep -oE '[0-9]+ (failed|failing)' | grep -oE '^[0-9]+' | head -1 || echo "?")
      FAIL_NAME=$(echo "$TEST_OUTPUT" | grep -E '(FAIL|✗|×|●|FAILED)' | head -1 | sed 's/^[[:space:]]*//' | cut -c1-60 || echo "")
      FAIL_SUMMARY=$(echo "$TEST_OUTPUT" | grep -E '(Error|AssertionError|expect)' | head -1 | sed 's/^[[:space:]]*//' | cut -c1-50 || echo "")

      if [[ -n "$FAIL_NAME" && -n "$FAIL_SUMMARY" ]]; then
        echo "[stop-gate] ✗ tests: ${FAIL_COUNT} failed — ${FAIL_NAME} — ${FAIL_SUMMARY}"
      elif [[ -n "$FAIL_NAME" ]]; then
        echo "[stop-gate] ✗ tests: ${FAIL_COUNT} failed — ${FAIL_NAME}"
      else
        echo "[stop-gate] ✗ tests: ${FAIL_COUNT} failed — fix before closing"
      fi
      GATE_STATUS=1
    fi
  fi
fi

exit "$GATE_STATUS"
