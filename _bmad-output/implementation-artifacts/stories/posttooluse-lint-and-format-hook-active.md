---
title: PostToolUse Lint and Format Hook Active
story_key: posttooluse-lint-and-format-hook-active
status: ready-for-dev
epic_slug: quality-enforcement
depends_on: []
touches:
  - skills/momentum/hooks/hooks.json
  - skills/momentum/scripts/momentum-lint.sh
change_type: rule-hook + code
---

# PostToolUse Lint and Format Hook Active

## Description

The `hooks/hooks.json` currently has a placeholder echo for the PostToolUse
lint hook. This story replaces the placeholder with a real implementation
that runs lint and format checks after every Edit/Write/NotebookEdit
operation.

The hook must be fast (under 5 seconds), non-blocking (warnings don't halt
the agent), and track which files were modified during the session for the
stop gate to use later.

## Acceptance Criteria (Plain English)

1. The PostToolUse hook in `hooks/hooks.json` fires after every
   Edit, Write, or NotebookEdit tool use and runs a lint/format check
   on the modified file.

2. The hook script accepts the file path from the tool use event and
   runs appropriate linting based on file extension:
   - `.py` files: check with `ruff` if available, skip silently if not
   - `.md` files: basic structural checks (no trailing whitespace on
     non-empty lines, consistent heading levels)
   - `.json` files: validate JSON syntax with `python3 -m json.tool`
   - `.sh`/`.bash` files: check with `shellcheck` if available, skip if not
   - Other extensions: skip with no output

3. The hook completes within 5 seconds. If the linter is slow or hangs,
   the hook times out gracefully without blocking the agent.

4. When lint issues are found, the hook outputs a single-line summary
   prefixed with `[momentum-lint]` (e.g., `[momentum-lint] ! 2 issues in
   foo.py`). It does NOT output anything when the file is clean.

5. The hook appends each modified file path to
   `.claude/momentum/session-modified-files.txt` (one path per line,
   deduped). This file is read by the stop gate hook.

6. The hook script is executable and located at
   `skills/momentum/scripts/momentum-lint.sh`.

7. The `hooks/hooks.json` PostToolUse entry references the real script
   instead of the placeholder echo command.

## Dev Notes

### Hook event data

Claude Code PostToolUse hooks receive the tool name and parameters via
environment variables. The script needs to extract the file path from:
- `$TOOL_NAME` — the tool that was used (Edit, Write, NotebookEdit)
- `$TOOL_INPUT` — JSON string with tool parameters (contains `file_path`)

Use `python3 -c` or `jq` to extract `file_path` from the JSON input.

### Script structure

```bash
#!/usr/bin/env bash
# momentum-lint.sh — PostToolUse lint and format hook
# Extracts file path from tool input, runs appropriate linter, tracks modified files.

set -euo pipefail

# Extract file path from TOOL_INPUT JSON
FILE_PATH=$(echo "$TOOL_INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('file_path',''))" 2>/dev/null)

# Track modified file
# Run linter based on extension
# Output only on failure
```

### Timeout handling

The `hooks.json` entry already has `"timeout": 5` (5 seconds). If the
script exceeds this, Claude Code kills it automatically. No internal
timeout logic needed — but avoid calling slow tools (e.g., full project
linters).

### session-modified-files.txt

This is a session-scoped tracking file. It does NOT persist across
sessions. The stop gate reads it to determine what to check. Each line
is an absolute file path. Dedup on append (grep before echo).

### Files

- `skills/momentum/scripts/momentum-lint.sh` — lint hook script (new)
- `skills/momentum/hooks/hooks.json` — update PostToolUse entry
