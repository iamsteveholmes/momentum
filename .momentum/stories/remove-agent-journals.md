---
title: Remove Agent Journals — Delete Sprint-Log Write Infrastructure
story_key: remove-agent-journals
status: review
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
  - skills/momentum/skills/sprint-dev/workflow.md
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/quick-fix/workflow.md
  - skills/momentum/skills/retro/workflow.md
  - skills/momentum/skills/epic-grooming/workflow.md
  - skills/momentum/skills/dev/workflow.md
  - skills/momentum/hooks/subagent-start.sh
  - skills/momentum/hooks/subagent-stop.sh
  - skills/momentum/references/hooks-config.json
  - _bmad-output/planning-artifacts/prd.md
  - _bmad-output/planning-artifacts/architecture.md
change_type: script-code
derives_from:
  - path: _bmad-output/planning-artifacts/architecture.md
    relationship: derives_from
    section: "Decision 27 — DuckDB transcript audit replaces milestone logs"
---

# Remove Agent Journals — Delete Sprint-Log Write Infrastructure

## Story

As a Momentum maintainer,
I want to remove the agent journal system (momentum-tools log, sprint-log writes,
observability hooks) entirely,
so that workflows are simpler, there is no dead-write overhead, and the codebase
reflects the actual retro data path (DuckDB transcripts).

## Description

Decision 27 (2026-04-06) replaced milestone-log-based retro with DuckDB transcript
preprocessing and an auditor team. The transcript approach proved superior: 37
findings from 246 user messages + 97 subagents + 806 tool events vs. 2 findings
from 24 log events. Order of magnitude more signal.

Despite this, the agent journal infrastructure was never removed. It persists as
67+ `momentum-tools log` calls across 6 workflows, 2 hook scripts, a CLI command,
~150 lines of tests, and 4 functional requirements in the PRD. All of these write
JSONL files that nothing in production ever reads.

The retro workflow explicitly states: "Milestone logs are NOT the critical path —
retro proceeds and produces findings even when zero log events exist." The retro
already uses only DuckDB transcript queries (transcript-query.py) for all evidence.

This story removes the entire agent journal write infrastructure: the CLI command,
all workflow log calls, the observability hooks, the dead tests, and updates the
specs to reflect the actual architecture.

## Acceptance Criteria (Plain English)

### AC1: momentum-tools log Command Removed

- The `cmd_log()` function is removed from momentum-tools.py
- The `log` subcommand is removed from CLI registration
- The `VALID_EVENT_TYPES` constant is removed
- All log-related tests are removed from test-momentum-tools.py
- Remaining tests still pass

### AC2: All Workflow Log Calls Removed

- sprint-dev workflow: all 17 `momentum-tools log` calls removed
- sprint-planning workflow: all 15 `momentum-tools log` calls removed
- quick-fix workflow: all 11 `momentum-tools log` calls removed
- retro workflow: all 8 `momentum-tools log` calls removed
- epic-grooming workflow: 1 `momentum-tools log` reference removed (in a
  `<critical>` directive — reword the directive rather than deleting it)
- No `momentum-tools log` calls remain in any workflow
- Workflow logic is otherwise unchanged — only the log calls are removed, not the
  surrounding actions or decisions

### AC3: Observability Hooks Removed

- `skills/momentum/hooks/subagent-start.sh` is deleted
- `skills/momentum/hooks/subagent-stop.sh` is deleted
- Hook registrations for SubagentStart and SubagentStop are removed from
  `skills/momentum/hooks/hooks.json` (not hooks-config.json — the always-on
  hooks are registered in hooks.json)
- Any project-level settings.json entries for these hooks are removed

### AC4: Specifications Updated

- PRD: FR56 (Agent Observability), FR57 (Fault-Tolerant Logging), FR85 (Spawn
  Deduplication Logging), FR89 (SubagentStart/SubagentStop Hooks) are marked as
  removed with rationale: "Superseded by DuckDB transcript audit (Decision 27)"
- Architecture: Decision 24 (Agent Logging Infrastructure) is updated to state
  that agent journals were removed and transcript audit is the sole evidence source
- The refine workflow's existing `<critical>No momentum-tools log calls</critical>`
  directive becomes the default — add a note that logging was removed project-wide

### AC5: No Sprint-Log Directory Creation

- No workflow or tool creates `.claude/momentum/sprint-logs/` directories
- The `--sprint` flag on momentum-tools is removed or no longer creates log
  directories as a side effect
- Existing sprint-log directories in projects are not deleted (leave historical
  data alone) but nothing writes to them going forward

### AC6: Retro Workflow Unchanged

- The retro workflow continues to function identically using DuckDB transcript
  queries
- No retro Phase (1-6) is affected by this removal
- transcript-query.py is not modified

## Tasks / Subtasks

- [x] Task 1 — Remove momentum-tools log command and tests (AC: 1)
  - [x] Delete `cmd_log()` function from momentum-tools.py
  - [x] Delete CLI registration for `log` subcommand
  - [x] Delete `VALID_EVENT_TYPES` constant
  - [x] Delete all log-related tests from test-momentum-tools.py
  - [x] Run remaining tests to confirm no breakage

- [x] Task 2 — Remove all workflow log calls (AC: 2)
  - [x] sprint-dev/workflow.md: remove 17 log calls
  - [x] sprint-planning/workflow.md: remove 15 log calls
  - [x] quick-fix/workflow.md: remove 11 log calls
  - [x] retro/workflow.md: remove 8 log calls
  - [x] epic-grooming/workflow.md: reword 1 `<critical>` directive that references
    momentum-tools log (remove the log instruction, keep the directive's intent)
  - [x] Verify no `momentum-tools log` calls remain anywhere in the project

- [x] Task 3 — Remove observability hooks (AC: 3)
  - [x] Delete subagent-start.sh and subagent-stop.sh
  - [x] Remove SubagentStart/SubagentStop entries from hooks/hooks.json
  - [x] Check for and remove any project-level hook registrations

- [x] Task 4 — Verify specifications already updated (AC: 4)
  - [x] Confirm PRD FR56, FR57, FR89 are already marked REMOVED (applied in
    sprint planning spec impact step)
  - [x] Confirm FR85 already updated to reference DuckDB transcript audit
  - [x] Confirm architecture Decision 24 already marked Historical
  - [x] No spec writes needed — already applied

- [x] Task 5 — Verify retro still works (AC: 6)
  - [x] Confirm retro workflow has no references to sprint-logs or momentum-tools log
  - [x] Confirm transcript-query.py is unaffected

## Dev Notes

### Removal Pattern

For each workflow, the log calls follow a consistent pattern:
```
<action>Log: `momentum-tools log --agent NAME --event TYPE --detail "MESSAGE" --sprint {{sprint_slug}}`</action>
```

These are standalone `<action>` elements that can be deleted without affecting
surrounding workflow logic. In most cases the log call is the only content in its
`<action>` tag. Search for `momentum-tools log` and delete the containing `<action>`
element.

In some workflows, the log call shares an `<action>` with other logic (e.g.,
"Store result AND log it"). In those cases, remove only the log line, not the
entire action.

### Files to Delete

- `skills/momentum/hooks/subagent-start.sh`
- `skills/momentum/hooks/subagent-stop.sh`

### Files to Modify

| File | Change |
|---|---|
| `skills/momentum/scripts/momentum-tools.py` | Remove cmd_log, VALID_EVENT_TYPES, CLI registration |
| `skills/momentum/scripts/test-momentum-tools.py` | Remove ~150 lines of log tests |
| `skills/momentum/skills/sprint-dev/workflow.md` | Remove 17 log actions |
| `skills/momentum/skills/sprint-planning/workflow.md` | Remove 15 log actions |
| `skills/momentum/skills/quick-fix/workflow.md` | Remove 11 log actions |
| `skills/momentum/skills/retro/workflow.md` | Remove 8 log actions |
| `skills/momentum/skills/epic-grooming/workflow.md` | Reword 1 `<critical>` directive |
| `skills/momentum/hooks/hooks.json` | Remove SubagentStart/Stop entries |

### What NOT to Change

- `transcript-query.py` — the replacement system, untouched
- Retro workflow logic — only log calls removed, phases unchanged
- Session journal system (`journal.jsonl`, `journal-status`, `journal-hygiene`) — completely separate system
- Existing `.claude/momentum/sprint-logs/` directories — leave historical data, just stop writing
- `momentum-tools` commands other than `log` — unaffected

### Risk

Low. Zero production readers means zero behavior change. The only risk is missing
a log call somewhere, which would cause a "command not found" error at runtime.
Mitigation: grep the entire project for `momentum-tools log` after removal to
confirm none remain.

### References

- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 27] — DuckDB transcript audit rationale
- [Source: skills/momentum/skills/retro/workflow.md:14] — "Milestone logs are NOT the critical path"
- [Source: skills/momentum/scripts/momentum-tools.py:991] — cmd_log implementation
- [Source: skills/momentum/hooks/subagent-start.sh] — hook to delete
- [Source: skills/momentum/hooks/subagent-stop.sh] — hook to delete

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None.

### Completion Notes List

- Removed `cmd_log()`, `VALID_EVENT_TYPES`, and `log` CLI registration from momentum-tools.py
- Removed 16 log test functions and their runner calls from test-momentum-tools.py (subagent event type block at bottom also removed)
- Removed 17 `momentum-tools log` action elements from sprint-dev/workflow.md (including `<critical>` directive, dedup log suppression text, and Phase 4d cleanup log)
- Removed 15 `momentum-tools log` calls from sprint-planning/workflow.md (including `<critical>` directive and all inline log actions)
- Removed 11 `momentum-tools log` calls from quick-fix/workflow.md
- Removed 8 `momentum-tools log` calls from retro/workflow.md
- Rewrote epic-grooming `<critical>` directive to reference completion notes for decision traceability instead of momentum-tools log
- Deleted subagent-start.sh and subagent-stop.sh hook scripts
- Removed SubagentStart and SubagentStop entries from hooks/hooks.json
- Confirmed settings.json has no SubagentStart/SubagentStop registrations
- Confirmed PRD FR56, FR57, FR89 already REMOVED; FR85 updated; architecture Decision 24 already marked Historical
- Updated sprint-dev dedup eval to remove log emission expectation
- Updated epic-grooming logging eval to document via completion notes instead of momentum-tools log
- 346 tests pass (0 failed)

### File List

- skills/momentum/scripts/momentum-tools.py
- skills/momentum/scripts/test-momentum-tools.py
- skills/momentum/skills/sprint-dev/workflow.md
- skills/momentum/skills/sprint-planning/workflow.md
- skills/momentum/skills/quick-fix/workflow.md
- skills/momentum/skills/retro/workflow.md
- skills/momentum/skills/epic-grooming/workflow.md
- skills/momentum/hooks/hooks.json
- skills/momentum/hooks/subagent-start.sh (deleted)
- skills/momentum/hooks/subagent-stop.sh (deleted)
- skills/momentum/skills/sprint-dev/evals/eval-dedup-guard-blocks-duplicate.md
- skills/momentum/skills/epic-grooming/evals/eval-applies-changes-with-logging.md
- _bmad-output/implementation-artifacts/stories/remove-agent-journals.md
