---
title: PreToolUse File Protection Hooks Active
story_key: pretooluse-file-protection-hooks-active
status: ready-for-dev
epic_slug: quality-enforcement
depends_on: []
touches:
  - skills/momentum/hooks/hooks.json
  - skills/momentum/scripts/momentum-protect.sh
  - skills/momentum/references/protected-paths.json
change_type: rule-hook + code
---

# PreToolUse File Protection Hooks Active

## Description

The hooks-config.json currently has a placeholder echo for the PreToolUse
file protection hook. This story replaces the placeholder with a real
implementation that blocks writes to protected file paths.

Per Decision 2a, the protected paths are: `tests/acceptance/`,
`**/*.feature`, `_bmad-output/planning-artifacts/*.md`, and
`.claude/rules/`. These files should only be modified by their designated
sole-writer agents, not by general development agents.

The hook must exit non-zero to block the tool use when a protected path
is targeted. It must be fast and produce a clear message explaining why
the write was blocked.

## Acceptance Criteria (Plain English)

1. The PreToolUse hook in `hooks/hooks.json` fires before every Edit,
   Write, or NotebookEdit tool use and checks the target file path
   against the protected path list.

2. When a write targets a protected path, the hook exits with a non-zero
   exit code, which causes Claude Code to block the tool use. The hook
   outputs a message: `[momentum-protect] ✗ blocked write to {path} —
   {reason}`.

3. The following paths are protected by default:
   - `_bmad-output/planning-artifacts/*.md` — specs only modified by
     refine/planning workflows
   - `**/*.feature` — Gherkin specs only modified by sprint-planning
   - `.claude/rules/` — rules only modified by Impetus
   - `_bmad-output/implementation-artifacts/stories/index.json` — only
     modified by momentum-tools.py
   - `_bmad-output/implementation-artifacts/sprints/index.json` — only
     modified by momentum-tools.py

4. The protected path list is configurable via a JSON file at
   `skills/momentum/references/protected-paths.json` so new protections
   can be added without modifying the script.

5. When a write targets a non-protected path, the hook exits with code 0
   and produces no output (silent pass-through).

6. The hook completes within 2 seconds.

7. The hook script is executable and located at
   `skills/momentum/scripts/momentum-protect.sh`.

8. The `hooks/hooks.json` PreToolUse entry references the real script
   instead of the placeholder echo command.

## Dev Notes

### Hook event data

PreToolUse hooks receive the same environment variables as PostToolUse:
- `$TOOL_NAME` — Edit, Write, or NotebookEdit
- `$TOOL_INPUT` — JSON with `file_path`

### Protected paths config format

```json
{
  "protected": [
    {
      "pattern": "_bmad-output/planning-artifacts/*.md",
      "reason": "planning artifacts — modify via refine workflow only"
    },
    {
      "pattern": "**/*.feature",
      "reason": "Gherkin specs — modify via sprint-planning only"
    },
    {
      "pattern": ".claude/rules/*",
      "reason": "rules — modify via Impetus only"
    },
    {
      "pattern": "_bmad-output/implementation-artifacts/stories/index.json",
      "reason": "story index — modify via momentum-tools only"
    },
    {
      "pattern": "_bmad-output/implementation-artifacts/sprints/index.json",
      "reason": "sprint index — modify via momentum-tools only"
    }
  ]
}
```

### Pattern matching

Use bash `fnmatch`-style glob matching via `python3 -c` with
`fnmatch.fnmatch()`. Each protected entry's pattern is checked against
the target file path (relative to project root).

### Exit code semantics

- Exit 0 = allow the write (non-protected path)
- Exit non-zero = block the write (protected path matched)

Claude Code interprets non-zero exit from a PreToolUse hook as "deny
this tool use."

### Files

- `skills/momentum/scripts/momentum-protect.sh` — protection hook script (new)
- `skills/momentum/references/protected-paths.json` — protected paths config (new)
- `skills/momentum/hooks/hooks.json` — update PreToolUse entry
