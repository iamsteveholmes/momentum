#!/usr/bin/env bash
# stop-gate.sh — Stop hook: advisory quality checks before session end
# Fires before Claude Code session closes.
#
# Output format (one line per check):
#   [momentum-gate] ✓ checked N files — clean
#   [momentum-gate] ✗ lint: N issues found
#   [momentum-gate] ◦ lint — no lint tool configured
#   [momentum-gate] ! uncommitted changes detected — N files
#   [momentum-gate] ✓ no files modified this session
#   [momentum-gate] ✓ checked tests — N passed
#   [momentum-gate] ✗ tests: N failed — failing test name — failure summary
#   [momentum-gate] ◦ tests — no test runner configured
#
# Session state contract:
#   - Reads .claude/momentum/session-modified-files.txt (written by PostToolUse lint hook)
#   - Deletes session state file after reading (ensures clean state for next session)
#   - Writes findings to .claude/momentum/gate-findings.txt for next session
#
# Exit codes:
#   0 — ALWAYS (advisory only — never blocks session exit)

set -uo pipefail

# --- Project root detection ---
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || echo "")}"
if [[ -z "$PROJECT_DIR" ]]; then
  # Can't determine project dir — skip silently (don't block session)
  exit 0
fi

MOMENTUM_DIR="$PROJECT_DIR/.claude/momentum"
SESSION_FILE="$MOMENTUM_DIR/session-modified-files.txt"
GATE_FINDINGS_FILE="$MOMENTUM_DIR/gate-findings.txt"

# --- Session state: determine if code was modified this session ---
CODE_MODIFIED=false
SESSION_FILES=()
if [[ -s "$SESSION_FILE" ]]; then
  CODE_MODIFIED=true
  # Read unique file paths from session file
  while IFS= read -r line; do
    [[ -n "$line" ]] && SESSION_FILES+=("$line")
  done < <(sort -u "$SESSION_FILE")
fi

# Always clean up session state file (ensures clean state for next session)
rm -f "$SESSION_FILE"

# If no files were modified this session, report and exit clean
if [[ "$CODE_MODIFIED" == "false" ]]; then
  echo "[momentum-gate] ✓ no files modified this session"
  exit 0
fi

# Track findings for gate-findings.txt
FINDINGS_LINT=""
FINDINGS_UNCOMMITTED=""
HAS_FINDINGS=false

# --- Check uncommitted changes ---
UNCOMMITTED_OUTPUT=$(cd "$PROJECT_DIR" && git status --porcelain 2>/dev/null || echo "")
if [[ -n "$UNCOMMITTED_OUTPUT" ]]; then
  UNCOMMITTED_COUNT=$(echo "$UNCOMMITTED_OUTPUT" | grep -c '.' 2>/dev/null || echo "0")
  echo "[momentum-gate] ! uncommitted changes detected — ${UNCOMMITTED_COUNT} files"
  FINDINGS_UNCOMMITTED="$UNCOMMITTED_OUTPUT"
  HAS_FINDINGS=true
fi

# --- Per-extension lint dispatch on session-modified files ---
LINT_ISSUES=0
LINT_CHECKED=0
LINT_OUTPUT_ALL=""

for filepath in "${SESSION_FILES[@]}"; do
  # Skip files that no longer exist
  [[ -f "$PROJECT_DIR/$filepath" ]] || continue

  ext="${filepath##*.}"
  LINT_CMD=""
  LINT_RESULT=""
  LINT_EXIT=0

  case "$ext" in
    py)
      if command -v ruff >/dev/null 2>&1; then
        LINT_CMD="ruff check"
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
      # Basic check: trailing whitespace on non-empty lines
      LINT_CMD="__md_check__"
      ;;
  esac

  # Skip silently if no linter for this extension
  [[ -z "$LINT_CMD" ]] && continue

  LINT_CHECKED=$((LINT_CHECKED + 1))

  if [[ "$LINT_CMD" == "__md_check__" ]]; then
    # Custom markdown trailing whitespace check
    MD_ISSUES=$(grep -nE '[^ ] +$' "$PROJECT_DIR/$filepath" 2>/dev/null || true)
    if [[ -n "$MD_ISSUES" ]]; then
      ISSUE_COUNT=$(echo "$MD_ISSUES" | grep -c '.' 2>/dev/null || echo "0")
      LINT_ISSUES=$((LINT_ISSUES + ISSUE_COUNT))
      LINT_OUTPUT_ALL="${LINT_OUTPUT_ALL}${filepath}: trailing whitespace (${ISSUE_COUNT} lines)\n"
    fi
  elif [[ "$LINT_CMD" == "python3 -m json.tool" ]]; then
    LINT_RESULT=$(cd "$PROJECT_DIR" && python3 -m json.tool "$filepath" > /dev/null 2>&1) || LINT_EXIT=$?
    if [[ "$LINT_EXIT" -ne 0 ]]; then
      LINT_ISSUES=$((LINT_ISSUES + 1))
      LINT_OUTPUT_ALL="${LINT_OUTPUT_ALL}${filepath}: invalid JSON\n"
    fi
  else
    LINT_RESULT=$(cd "$PROJECT_DIR" && $LINT_CMD "$filepath" 2>&1) || LINT_EXIT=$?
    if [[ "$LINT_EXIT" -ne 0 ]]; then
      FILE_ISSUE_COUNT=$(echo "$LINT_RESULT" | grep -c '[^[:space:]]' 2>/dev/null || echo "1")
      LINT_ISSUES=$((LINT_ISSUES + FILE_ISSUE_COUNT))
      LINT_OUTPUT_ALL="${LINT_OUTPUT_ALL}${LINT_RESULT}\n"
    fi
  fi
done

if [[ "$LINT_CHECKED" -eq 0 ]]; then
  echo "[momentum-gate] ◦ lint — no lint tool configured"
else
  if [[ "$LINT_ISSUES" -eq 0 ]]; then
    echo "[momentum-gate] ✓ checked ${LINT_CHECKED} files — 0 issues found"
  else
    echo "[momentum-gate] ✗ checked ${LINT_CHECKED} files — ${LINT_ISSUES} issues found"
    FINDINGS_LINT="$LINT_OUTPUT_ALL"
    HAS_FINDINGS=true
  fi
fi

# --- Run tests (conditional — only if code was modified this session) ---
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

TEST_CMD=$(detect_test_cmd)

if [[ -z "$TEST_CMD" ]]; then
  echo "[momentum-gate] ◦ tests — no test runner configured"
else
  cd "$PROJECT_DIR"
  TEST_OUTPUT=$(eval "$TEST_CMD" 2>&1) || TEST_EXIT=$?
  TEST_EXIT="${TEST_EXIT:-0}"

  if [[ "$TEST_EXIT" -eq 0 ]]; then
    # Try to extract pass count from output
    PASS_COUNT=$(echo "$TEST_OUTPUT" | grep -oE '[0-9]+ (passed|tests? passed|passing)' | grep -oE '^[0-9]+' | head -1 || echo "")
    if [[ -n "$PASS_COUNT" ]]; then
      echo "[momentum-gate] ✓ checked tests — ${PASS_COUNT} passed"
    else
      echo "[momentum-gate] ✓ checked tests — passed"
    fi
  else
    # Extract failure info
    FAIL_COUNT=$(echo "$TEST_OUTPUT" | grep -oE '[0-9]+ (failed|failing)' | grep -oE '^[0-9]+' | head -1 || echo "?")
    FAIL_NAME=$(echo "$TEST_OUTPUT" | grep -E '(FAIL|✗|×|●|FAILED)' | head -1 | sed 's/^[[:space:]]*//' | cut -c1-60 || echo "")
    FAIL_SUMMARY=$(echo "$TEST_OUTPUT" | grep -E '(Error|AssertionError|expect)' | head -1 | sed 's/^[[:space:]]*//' | cut -c1-50 || echo "")

    if [[ -n "$FAIL_NAME" && -n "$FAIL_SUMMARY" ]]; then
      echo "[momentum-gate] ✗ tests: ${FAIL_COUNT} failed — ${FAIL_NAME} — ${FAIL_SUMMARY}"
    elif [[ -n "$FAIL_NAME" ]]; then
      echo "[momentum-gate] ✗ tests: ${FAIL_COUNT} failed — ${FAIL_NAME}"
    else
      echo "[momentum-gate] ✗ tests: ${FAIL_COUNT} failed — fix before closing"
    fi
    HAS_FINDINGS=true
  fi
fi

# --- Write gate findings file for next session ---
if [[ "$HAS_FINDINGS" == "true" ]]; then
  mkdir -p "$MOMENTUM_DIR"
  {
    echo "# Gate Findings"
    echo ""
    echo "Generated: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
    echo ""
    if [[ -n "$FINDINGS_LINT" ]]; then
      echo "## Lint Issues"
      echo ""
      echo -e "$FINDINGS_LINT"
    fi
    if [[ -n "$FINDINGS_UNCOMMITTED" ]]; then
      echo "## Uncommitted Changes"
      echo ""
      echo "$FINDINGS_UNCOMMITTED"
    fi
  } > "$GATE_FINDINGS_FILE"
fi

# Advisory only — always exit 0
exit 0
