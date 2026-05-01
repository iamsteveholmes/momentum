---
title: Stop Gate Runs Conditional Quality Checks
story_key: stop-gate-runs-conditional-quality-checks
status: ready-for-dev
epic_slug: quality-enforcement
depends_on:
  - posttooluse-lint-and-format-hook-active
touches:
  - skills/momentum/hooks/hooks.json
  - skills/momentum/scripts/momentum-gate.sh
change_type: rule-hook + code
---

# Stop Gate Runs Conditional Quality Checks

## Description

The `hooks/hooks.json` currently has a placeholder echo for the Stop hook.
This story replaces the placeholder with a real implementation that runs
quality checks before a session ends.

The stop gate reads the session-modified-files list (populated by the
PostToolUse lint hook) and runs targeted checks on what was actually
changed. If no files were modified, it exits cleanly. If files were
modified, it runs a final lint pass and reports a summary.

The gate is advisory — it reports findings but does not block session
exit. Blocking session exit creates a poor UX (the developer wants to
leave), so findings are logged for the next session to surface.

## Acceptance Criteria (Plain English)

1. The Stop hook in `hooks/hooks.json` fires when a session ends and
   runs conditional quality checks based on what files were modified
   during the session.

2. When `.claude/momentum/session-modified-files.txt` does not exist or
   is empty, the hook exits cleanly with a single line:
   `[momentum-gate] ✓ no files modified this session`.

3. When modified files exist, the hook runs a final lint pass on each
   file (same logic as the PostToolUse hook) and reports a summary:
   `[momentum-gate] checked N files — M issues found`.

4. The hook checks for uncommitted changes (`git status --porcelain`)
   and warns if uncommitted work exists:
   `[momentum-gate] ! uncommitted changes detected — N files`.

5. The hook always exits with code 0 (advisory, never blocks session
   exit). Findings are written to
   `.claude/momentum/gate-findings.txt` for the next session to read.

6. The hook completes within 10 seconds even with many modified files
   (batch processing, not per-file subprocess spawning).

7. The hook script is executable and located at
   `skills/momentum/scripts/momentum-gate.sh`.

8. The `hooks/hooks.json` Stop entry references the real script
   instead of the placeholder echo command.

9. The hook cleans up `session-modified-files.txt` after reading it
   (the file is session-scoped and should not accumulate across
   sessions).

## Dev Notes

### Conditional execution

The key design is: **only check what was touched**. Reading
`session-modified-files.txt` gives the exact list of files the agent
modified. No full-project scans.

### Batch processing

Don't spawn a subprocess per file. Instead, group files by extension
and run one linter invocation per group:
- All `.py` files → one `ruff check file1.py file2.py` call
- All `.json` files → loop with `python3 -m json.tool`
- All `.md` files → one pass with simple checks

### gate-findings.txt format

```
# Momentum Gate Findings — {ISO_TIMESTAMP}
## Lint Issues
- path/to/file.py:12: E501 line too long
## Uncommitted Changes
- M path/to/modified.py
- ?? path/to/untracked.py
```

Impetus can read this at next session open and surface findings.

### Files

- `skills/momentum/scripts/momentum-gate.sh` — stop gate script (new)
- `skills/momentum/hooks/hooks.json` — update Stop entry
