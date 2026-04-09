---
title: Hooks Global Distribution — Move Hook Scripts to Global Path
story_key: hooks-global-distribution
status: review
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum/references/hooks-config.json
  - skills/momentum/references/hooks/stop-gate.sh
  - skills/momentum/references/hooks/lint-format.sh
  - skills/momentum/references/hooks/file-protection.sh
  - skills/momentum/references/momentum-versions.json
change_type: config-structure
derives_from:
  - path: _bmad-output/planning-artifacts/prd.md
    relationship: derives_from
    section: "FR18-FR21: Enforcement & Quality Governance hooks"
---

# Hooks Global Distribution — Move Hook Scripts to Global Path

## Story

As a developer with Momentum installed as a global plugin,
I want hook scripts to live at a global path and work in every project,
so that I stop seeing "No such file or directory" errors in every non-Momentum project.

## Description

Momentum registers hooks (Stop, PostToolUse, PreToolUse) that call bash scripts via
`${CLAUDE_PROJECT_DIR}/.claude/momentum/hooks/stop-gate.sh` and similar project-local
paths. The hooks-config.json template assumes these scripts will be copied into every
project during install, but this never happens — the scripts only exist in the
Momentum project itself and in `skills/momentum/references/hooks/`.

The result: every project that doesn't have the scripts locally gets a
"No such file or directory" error on every session end (stop-gate.sh), every file
edit (lint-format.sh), and every file write (file-protection.sh). This has been
reported across nornspun, game-prep, and other projects.

The fix: hook scripts are project-agnostic (they auto-detect linters, test runners,
and use `$CLAUDE_PROJECT_DIR` for paths). They should live at a global location
(e.g., `~/.claude/momentum/hooks/`) and the hooks-config.json template should
reference that global path. The plugin install process should place them there.

## Acceptance Criteria (Plain English)

### AC1: Hook Scripts Live at Global Path

- All three hook scripts (stop-gate.sh, lint-format.sh, file-protection.sh) are
  installed to `~/.claude/momentum/hooks/` (or equivalent global Momentum path)
- Scripts are identical in functionality to current versions — no behavior changes

### AC2: hooks-config.json References Global Path

- `skills/momentum/references/hooks-config.json` is updated to reference the global
  path instead of `${CLAUDE_PROJECT_DIR}/.claude/momentum/hooks/`
- The path works regardless of which project is active

### AC3: No Errors in Non-Momentum Projects

- Running a session in any project (with or without Momentum project config) does
  not produce "No such file or directory" for hook scripts
- Hooks fire correctly in projects that have Momentum installed
- Hooks exit silently (exit 0) in projects that don't have Momentum-specific config

### AC4: Install/Upgrade Process Updated

- The Momentum install or upgrade process places hook scripts at the global path
- Existing project-local copies in `.claude/momentum/hooks/` continue to work during
  transition (graceful migration)
- momentum-versions.json includes an upgrade action for this change

### AC5: Project-Specific Hook Overrides Still Work

- If a project has a local `.claude/momentum/hooks/stop-gate.sh`, it takes precedence
  over the global one (project-level override pattern)
- This allows projects with custom linting or test requirements to override behavior

## Tasks / Subtasks

- [x] Task 1 — Update hooks-config.json to use global path (AC: 2)
  - [x] Change `${CLAUDE_PROJECT_DIR}/.claude/momentum/hooks/` to global path
  - [x] Determine correct global path pattern (`~/.claude/momentum/hooks/` or plugin path)

- [x] Task 2 — Update install/upgrade to distribute scripts globally (AC: 1, 4)
  - [x] Add upgrade action in momentum-versions.json to copy scripts to global path
  - [x] Ensure scripts have execute permission

- [x] Task 3 — Add project-local override support (AC: 5)
  - [x] Wrapper pattern: check project-local first, fall back to global
  - [x] Or: hook command itself checks for local override before running global

- [x] Task 4 — Verify no errors in non-Momentum projects (AC: 3)
  - [x] Test in a project without `.claude/momentum/` directory
  - [x] Confirm silent exit (exit 0) with no error output

## Dev Notes

### Current Hook Scripts

| Script | Hook | Purpose |
|---|---|---|
| stop-gate.sh | Stop | Advisory quality gate: lint modified files, check uncommitted changes, run tests |
| lint-format.sh | PostToolUse (Edit/Write) | Per-file lint on save |
| file-protection.sh | PreToolUse (Edit/Write) | Block writes to protected paths |

All three are project-agnostic — they use `$CLAUDE_PROJECT_DIR` and auto-detect
tools. No project-specific logic.

### Global Path Options

Option A: `~/.claude/momentum/hooks/` — consistent with existing `.claude/momentum/` structure
Option B: Use the plugin's own installed path — but plugins may not have a stable
filesystem path accessible from hook commands

Option A is simpler and more reliable.

### Override Pattern

The hook command in hooks-config.json could use a wrapper:
```bash
bash -c '[ -f "$CLAUDE_PROJECT_DIR/.claude/momentum/hooks/stop-gate.sh" ] && exec bash "$CLAUDE_PROJECT_DIR/.claude/momentum/hooks/stop-gate.sh" || exec bash "$HOME/.claude/momentum/hooks/stop-gate.sh"'
```

Or the scripts themselves could check for a project-local override at the top.

### What NOT to Change

- Hook script functionality — same behavior, different location
- Project-level `.claude/settings.json` hook registration — that's separate from where scripts live
- The hooks-config.json structure — only the paths change

### References

- [Source: skills/momentum/references/hooks-config.json] — current template with project-local paths
- [Source: skills/momentum/references/hooks/stop-gate.sh] — canonical stop-gate script
- [Source: ~/.claude/settings.json] — global hook registration

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — implementation was straightforward.

### Completion Notes List

- hooks-config.json updated: replaced project-local paths with wrapper commands that check project-local first, then fall back to `~/.claude/momentum/hooks/`. If neither exists, hook exits silently (exit 0).
- momentum-versions.json bumped to 1.1.0 with three global `add` actions (scope: global) to install hook scripts to `~/.claude/momentum/hooks/` with execute permission, plus a migration action referencing 1.1.0-hooks-global.md.
- Created migrations/1.1.0-hooks-global.md: instructions to update existing Momentum hook entries in `.claude/settings.json` to the new wrapper command format.
- Hook scripts themselves are unchanged — same functionality, new distribution path.
- Project-local override pattern implemented via wrapper: `$CLAUDE_PROJECT_DIR/.claude/momentum/hooks/<script>` takes precedence over `$HOME/.claude/momentum/hooks/<script>`.
- Existing project-local copies continue to work during transition (they take priority in the wrapper).

### File List

- skills/momentum/references/hooks-config.json (modified)
- skills/momentum/references/momentum-versions.json (modified)
- skills/momentum/references/migrations/1.1.0-hooks-global.md (created)
