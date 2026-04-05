---
title: Sprint Lifecycle Tools — Status Fields, New Commands, and Unit Tests
story_key: sprint-lifecycle-tools
status: backlog
epic_slug: greeting-redesign
depends_on: []
touches:
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
change_type: code
---

# Sprint Lifecycle Tools — Status Fields, New Commands, and Unit Tests

## Description

The Impetus greeting redesign (Decision 36, sprint lifecycle state machine)
requires sprints/index.json to track status fields (`planning`, `ready`,
`active`, `done`) and retro completion timestamps. The momentum-tools.py CLI
must write these fields correctly during existing lifecycle commands and provide
new commands for transitions that currently have no CLI surface: `sprint ready`,
`sprint retro-complete`, and `session stats-update`.

This story covers ALL momentum-tools.py changes for the sprint lifecycle
redesign. It does not touch the Impetus greeting workflow or the sprint index
schema migration — those are separate stories.

## Acceptance Criteria (Plain English)

1. When `sprint plan` creates a new planning sprint, the resulting object in
   sprints/index.json includes `"status": "planning"`.

2. When `sprint activate` moves a planning sprint to active, the resulting
   object includes `"status": "active"`.

3. When `sprint complete` marks an active sprint as done, the resulting object
   includes `"status": "done"` and `"retro_run_at": null`.

4. A new `sprint ready` command exists that sets the planning sprint's status
   to `"ready"`. It fails with a non-zero exit code if no planning sprint
   exists.

5. A new `sprint retro-complete` command exists that finds the most recent
   completed sprint entry where `retro_run_at` is null and sets it to today's
   date.

6. When `sprint retro-complete` runs and a planning sprint exists with
   `"status": "ready"`, the planning sprint is auto-activated (moved to active
   using existing activate logic).

7. When `sprint retro-complete` runs and a planning sprint exists with
   `"status": "planning"`, no auto-activation occurs — the planning sprint
   stays as-is.

8. When `sprint retro-complete` runs and no completed sprint has
   `retro_run_at` set to null, the command fails with a non-zero exit code.

9. A new `session stats-update` command exists that reads
   `.claude/momentum/installed.json`, increments
   `session_stats.momentum_completions`, and updates `last_invocation`. It
   creates the `session_stats` section if absent.

10. A new `session greeting-state` command exists that deterministically
    detects the current greeting state by reading `sprints/index.json`,
    `stories/index.json`, and `.claude/momentum/installed.json`. It returns
    a JSON object with `state` (one of the 9 state names), `active_sprint`
    (name or null), `planning_sprint` (name or null), `planning_status`
    (status or null), and `momentum_completions` (integer). This is the
    single source of truth for greeting state — the workflow does not
    compute state detection itself.

11. All new and modified commands have passing unit tests in
    test-momentum-tools.py following the existing subprocess-based pattern.

## Dev Notes

### Existing commands to modify

**`cmd_sprint_plan` (around line 188):** When building the initial sprint
object, add `"status": "planning"` to the dict.

**`cmd_sprint_activate` (around lines 135-139):** After setting the `started`
timestamp, add `planning["status"] = "active"`.

**`cmd_sprint_complete` (around lines 154-158):** After setting the `completed`
timestamp, add `active["status"] = "done"` and `active["retro_run_at"] = None`.

### New commands to add

**`sprint ready`:** Reads sprints/index.json, finds the planning entry, sets
`planning["status"] = "ready"`, writes back. Exits non-zero with error message
if no planning sprint exists.

**`sprint retro-complete`:** Reads sprints/index.json, scans the `completed`
array for the most recent entry where `retro_run_at is None` (or key is
absent), sets `retro_run_at` to today's ISO date string. Then checks whether
`sprints["planning"]` exists and `planning["status"] == "ready"` — if so,
auto-activates by reusing `cmd_sprint_activate` logic (move planning to active,
set started, set status to active). If `planning["status"] == "planning"`,
skip auto-activation. Exits non-zero if no completed sprint has
`retro_run_at` unset.

**`session stats-update`:** Reads `.claude/momentum/installed.json`. If
`session_stats` key is absent, creates it with `momentum_completions: 1` and
`last_invocation: today`. If present, increments `momentum_completions` by 1
and updates `last_invocation`. Writes back. This replaces the Write-tool-based
stats update that was producing ugly diffs during the Impetus greeting.

**`session greeting-state`:** Deterministic greeting state detection. Reads
three files: `sprints/index.json`, `stories/index.json`, and
`.claude/momentum/installed.json`. Applies the 9-state detection algorithm:

1. If `momentum_completions == 0` and no sprints exist → `first-session-ever`
2. If `active` is null and `planning` is null → `no-active-nothing-planned`
3. If `active` is null and `planning.status == "ready"` → `no-active-planned-ready`
4. If `active.status == "done"` and no planning sprint → `done-no-planned`
5. If `active.status == "done"` → `done-retro-needed`
6. If active exists and planning exists with `status == "planning"` → `active-planned-needs-work`
7. If any story in the active sprint has unmet `depends_on` → `active-blocked`
8. If all stories are `ready-for-dev` or `backlog` → `active-not-started`
9. Otherwise → `active-in-progress`

Returns JSON:
```json
{
  "state": "active-in-progress",
  "active_sprint": "sprint-2026-04-05",
  "planning_sprint": null,
  "planning_status": null,
  "momentum_completions": 3,
  "last_completed_sprint": "sprint-2026-04-04"
}
```

The workflow calls this once, gets the state, and looks up the template.
No file reads, no state computation in the workflow itself.

### Required unit tests

All tests follow the existing pattern: subprocess-based execution with temp
project directories and `assert_eq` assertions.

| Test Name | What It Verifies |
|---|---|
| test_sprint_plan_sets_status_planning | `sprint plan` includes `status: planning` |
| test_sprint_activate_sets_status_active | `sprint activate` sets `status: active` |
| test_sprint_complete_sets_status_done | `sprint complete` sets `status: done` and `retro_run_at: null` |
| test_sprint_ready_sets_status_ready | `sprint ready` sets `status: ready` |
| test_sprint_ready_no_planning | `sprint ready` fails when no planning sprint |
| test_sprint_retro_complete_basic | `sprint retro-complete` sets `retro_run_at` on most recent eligible entry |
| test_sprint_retro_complete_auto_activates | Auto-activates planning sprint when status is `ready` |
| test_sprint_retro_complete_no_auto_activate_when_planning | Skips auto-activate when planning status is `planning` |
| test_sprint_retro_complete_no_completed_sprints | Fails when no completed sprint has `retro_run_at` unset |
| test_session_stats_update_creates | Creates `session_stats` section when absent |
| test_session_stats_update_increments | Increments existing `momentum_completions` |
| test_session_stats_update_preserves_data | Preserves other data in installed.json |
| test_greeting_state_first_session | Returns `first-session-ever` when no sprints and completions == 0 |
| test_greeting_state_active_in_progress | Returns `active-in-progress` with stories moving |
| test_greeting_state_active_not_started | Returns `active-not-started` when all stories ready-for-dev |
| test_greeting_state_active_blocked | Returns `active-blocked` when story has unmet depends_on |
| test_greeting_state_done_retro_needed | Returns `done-retro-needed` when active.status == "done" |
| test_greeting_state_no_active_nothing_planned | Returns correct state when both null |
| test_greeting_state_no_active_planned_ready | Returns correct state with ready planning sprint |
| test_greeting_state_active_planned_needs_work | Returns correct state with planning sprint in "planning" |
| test_greeting_state_done_no_planned | Returns `done-no-planned` when done and no planning sprint |

### Files

- `skills/momentum/scripts/momentum-tools.py` — all command modifications and additions
- `skills/momentum/scripts/test-momentum-tools.py` — all unit tests
