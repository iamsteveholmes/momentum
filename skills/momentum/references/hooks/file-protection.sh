#!/usr/bin/env bash
# PreToolUse hook: block writes to protected files and directories.
#
# Fires before Edit, Write, or NotebookEdit tools execute.
# Blocks the tool by exiting non-zero; allows silently by exiting 0.
#
# Protected paths (Momentum defaults — loaded from protected-paths.json):
#   tests/acceptance/     — acceptance-test-dir
#   **/*.feature          — acceptance-test-dir
#   .claude/rules/        — project-rules
#   _bmad-output/planning-artifacts/*.md  — planning-artifacts
#   _bmad-output/implementation-artifacts/stories/index.json — index-files
#   _bmad-output/implementation-artifacts/sprints/index.json — index-files
#
# Additional paths can be added via .claude/momentum/project-config.json
# under a "protected_paths" array.
#
# Allowlist: Momentum install/upgrade workflow bypasses protection via:
#   - MOMENTUM_INSTALLING=1 env var, OR
#   - .claude/momentum/.impetus-installing sentinel file

set -euo pipefail

# ---------------------------------------------------------------------------
# Resolve the target file path
# ---------------------------------------------------------------------------
# Claude Code passes hook data via stdin as JSON:
# {"tool_name": "Edit", "tool_input": {"file_path": "...", ...}}
# Also available as $1 if command template passes "$CLAUDE_TOOL_INPUT_FILE_PATH"
# or as CLAUDE_TOOL_INPUT env var (stringified JSON or path).

FILE_PATH=""

# Try $1 argument first (set by command template in hooks-config.json)
if [[ -n "${1:-}" ]]; then
  FILE_PATH="$1"
fi

# If no arg, try to read from stdin (Claude Code standard hook format)
if [[ -z "$FILE_PATH" ]]; then
  if read -r -t 0.1 STDIN_LINE 2>/dev/null; then
    # stdin has data — try to parse as JSON
    STDIN_DATA="$STDIN_LINE"
    # Read remaining stdin lines
    while IFS= read -r -t 0.1 line 2>/dev/null; do
      STDIN_DATA="$STDIN_DATA$line"
    done || true
    # Extract file_path from tool_input
    if command -v jq >/dev/null 2>&1; then
      FILE_PATH=$(echo "$STDIN_DATA" | jq -r '.tool_input.file_path // empty' 2>/dev/null || true)
    fi
  fi
fi

# If still no path, try CLAUDE_TOOL_INPUT env var (may be JSON or path string)
if [[ -z "$FILE_PATH" && -n "${CLAUDE_TOOL_INPUT:-}" ]]; then
  # Try JSON parse first
  if command -v jq >/dev/null 2>&1; then
    FILE_PATH=$(echo "${CLAUDE_TOOL_INPUT}" | jq -r '.file_path // .tool_input.file_path // empty' 2>/dev/null || true)
  fi
  # If still empty, use raw value as path (some contexts pass path directly)
  if [[ -z "$FILE_PATH" ]]; then
    FILE_PATH="${CLAUDE_TOOL_INPUT}"
  fi
fi

# If we can't determine the path, allow silently (fail open — don't block unknown)
if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

# ---------------------------------------------------------------------------
# Momentum install allowlist
# ---------------------------------------------------------------------------
# Impetus writes to .claude/rules/ during install/upgrade — must not be blocked.

if [[ "${MOMENTUM_INSTALLING:-}" = "1" ]]; then
  exit 0
fi

# Filesystem sentinel (fallback if env var doesn't cross process boundaries)
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
if [[ -f "${PROJECT_DIR}/.claude/momentum/.impetus-installing" ]]; then
  exit 0
fi

# ---------------------------------------------------------------------------
# Load protected paths from protected-paths.json (canonical source)
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROTECTED_PATHS_JSON="$SCRIPT_DIR/protected-paths.json"

# Default protected paths (fallback if JSON not found)
DEFAULT_PROTECTED_PATTERNS=(
  "tests/acceptance/*"
  "*.feature"
  ".claude/rules/*"
  "_bmad-output/planning-artifacts/*.md"
  "_bmad-output/implementation-artifacts/stories/index.json"
  "_bmad-output/implementation-artifacts/sprints/index.json"
)

# Load from JSON if available
PROTECTED_PATTERNS=()
if [[ -f "$PROTECTED_PATHS_JSON" ]] && command -v jq >/dev/null 2>&1; then
  while IFS= read -r pattern; do
    [[ -n "$pattern" ]] && PROTECTED_PATTERNS+=("$pattern")
  done < <(jq -r '.paths[].pattern // empty' "$PROTECTED_PATHS_JSON" 2>/dev/null || true)
fi

# Fall back to defaults if JSON loading failed
if [[ ${#PROTECTED_PATTERNS[@]} -eq 0 ]]; then
  PROTECTED_PATTERNS=("${DEFAULT_PROTECTED_PATTERNS[@]}")
fi

# ---------------------------------------------------------------------------
# Load project-specific protected paths from project-config.json
# ---------------------------------------------------------------------------
PROJECT_CONFIG="${PROJECT_DIR}/.claude/momentum/project-config.json"
PROJECT_PROTECTED_PATHS=()

if [[ -f "$PROJECT_CONFIG" ]] && command -v jq >/dev/null 2>&1; then
  while IFS= read -r path; do
    [[ -n "$path" ]] && PROJECT_PROTECTED_PATHS+=("$path")
  done < <(jq -r '.protected_paths[]? // empty' "$PROJECT_CONFIG" 2>/dev/null || true)
fi

# ---------------------------------------------------------------------------
# Path matching helpers
# ---------------------------------------------------------------------------

block_write() {
  local policy="$1"
  local reason="$2"
  echo "[momentum-protect] ✗ blocked write to ${FILE_PATH} — ${policy}: ${reason}"
  exit 1
}

# Normalize path: strip leading ./ for consistent matching
NORM_PATH="${FILE_PATH#./}"

# Policy name lookup from protected-paths.json
get_policy_name() {
  local pattern="$1"
  if [[ -f "$PROTECTED_PATHS_JSON" ]] && command -v jq >/dev/null 2>&1; then
    jq -r --arg p "$pattern" '.paths[] | select(.pattern == $p) | .policy // "protected"' "$PROTECTED_PATHS_JSON" 2>/dev/null || echo "protected"
  else
    echo "protected"
  fi
}

get_policy_reason() {
  local pattern="$1"
  if [[ -f "$PROTECTED_PATHS_JSON" ]] && command -v jq >/dev/null 2>&1; then
    jq -r --arg p "$pattern" '.paths[] | select(.pattern == $p) | .reason // "path is protected"' "$PROTECTED_PATHS_JSON" 2>/dev/null || echo "path is protected"
  else
    echo "path is protected"
  fi
}

# ---------------------------------------------------------------------------
# Check Momentum default protected paths
# ---------------------------------------------------------------------------

# 1. tests/acceptance/ — any path containing this directory
if [[ "$NORM_PATH" == *"/tests/acceptance/"* ]] || [[ "$NORM_PATH" == tests/acceptance/* ]]; then
  block_write "acceptance-test-dir" "no modification after ATDD phase begins"
fi

# 2. **/*.feature — any .feature file anywhere in the tree
if [[ "$NORM_PATH" == *.feature ]]; then
  block_write "acceptance-test-dir" "no modification after ATDD phase begins"
fi

# 3. .claude/rules/ — project-scoped only (not global ~/.claude/rules/)
#    Match if path contains /.claude/rules/ or starts with .claude/rules/
if [[ "$NORM_PATH" == *"/.claude/rules/"* ]] || [[ "$NORM_PATH" == .claude/rules/* ]]; then
  block_write "project-rules" "project rules are read-only during implementation"
fi

# 4. _bmad-output/planning-artifacts/*.md — direct children only (not subdirectories)
#    Matches: _bmad-output/planning-artifacts/foo.md
#    Does NOT match: _bmad-output/planning-artifacts/sub/foo.md
if [[ "$NORM_PATH" == _bmad-output/planning-artifacts/*.md ]] || \
   [[ "$NORM_PATH" == */_bmad-output/planning-artifacts/*.md ]]; then
  # Ensure it's a direct child (no additional slashes after the directory)
  BASENAME="${NORM_PATH##*/_bmad-output/planning-artifacts/}"
  BASENAME="${BASENAME##_bmad-output/planning-artifacts/}"
  if [[ "$BASENAME" == *.md ]] && [[ "$BASENAME" != */* ]]; then
    block_write "planning-artifacts" "spec files are read-only during implementation"
  fi
fi

# 5. Index files — exact path matches
if [[ "$NORM_PATH" == _bmad-output/implementation-artifacts/stories/index.json ]] || \
   [[ "$NORM_PATH" == */_bmad-output/implementation-artifacts/stories/index.json ]]; then
  block_write "index-files" "index files are managed by sprint-manager only"
fi

if [[ "$NORM_PATH" == _bmad-output/implementation-artifacts/sprints/index.json ]] || \
   [[ "$NORM_PATH" == */_bmad-output/implementation-artifacts/sprints/index.json ]]; then
  block_write "index-files" "index files are managed by sprint-manager only"
fi

# ---------------------------------------------------------------------------
# Check project-specific protected paths
# ---------------------------------------------------------------------------

for pattern in "${PROJECT_PROTECTED_PATHS[@]:-}"; do
  [[ -z "$pattern" ]] && continue
  # Support glob-style patterns using bash case matching
  case "$NORM_PATH" in
    $pattern)
      block_write "project-protected" "path protected by project configuration"
      ;;
  esac
  # Also check if path contains the pattern as a directory segment
  if [[ "$NORM_PATH" == *"$pattern"* ]]; then
    block_write "project-protected" "path protected by project configuration"
  fi
done

# ---------------------------------------------------------------------------
# Allow — silent pass-through
# ---------------------------------------------------------------------------
exit 0
