# Eval: Deferred Stats Write — Write Happens After Menu Display

Story: 2a.1 — Silent Pre-Flight and Deferred Stats Write
AC: AC3

## Scenario

A repeat user invokes Momentum (momentum_completions >= 1). The session_stats write must occur AFTER the session menu is displayed, not before.

**Given** a repeat user with momentum_completions >= 1
**When** Step 7 runs the session orientation sequence
**Then** the session menu is displayed BEFORE the installed.json write
**And** the expertise-adaptive check reads the PRE-INCREMENT value (the previous session's count)
**And** the installed.json write occurs AFTER the menu output, not before

## Context to Load

Load `skills/momentum/skills/impetus/SKILL.md` as the implementation under test (happy path is inline; workflow.md is loaded for thread path in Scenario 2).

Simulate the following state:
- `installed.json` has `session_stats.momentum_completions: 3`
- No journal open threads
- `startup-preflight` returns `route: "greeting"`, `greeting.momentum_completions: 3`

## Expected Happy Path Sequence

1. `startup-preflight` runs (returns greeting state with pre-increment `momentum_completions: 3`)
2. Since `momentum_completions >= 1`: deliver abbreviated orientation mode
3. Display session menu ← **first I/O write to the developer**
4. `stats-update` runs AFTER menu display ← **file write AFTER menu**
5. Wait for developer input

## Failure Conditions

- Writing `installed.json` before displaying the session menu = FAIL
- Using the post-increment value (4) for the expertise-adaptive check = FAIL (must use pre-increment value 3)
- Any output about the stats write ("Updating session stats...", "Recording session...") = FAIL

## Pass Condition

The expertise-adaptive check uses value 3 (abbreviated mode). The session menu appears. The installed.json write occurs after the menu. The developer sees the menu with no preceding narration.

## Scenario 2: Thread-Exist Path (Step 11)

**Given** a repeat user with momentum_completions >= 1
**And** journal.jsonl has one or more open threads
**When** Step 11 runs the thread display sequence
**Then** the thread display, hygiene checks, and selection prompt all appear BEFORE the installed.json write

## Context to Load (Scenario 2)

Simulate the following state:
- `installed.json` has `session_stats.momentum_completions: 5`
- `journal.jsonl` has one open thread

## Expected Step 11 Sequence

1. Display open threads (thread list output)
2. Run hygiene checks (if applicable)
3. Display selection prompt: "Continue (1/2/...) or tell me what you need?"
4. Increment `session_stats.momentum_completions` to 6, update `last_invocation`, write `installed.json` ← **file write AFTER all displayed content**
5. Wait for developer input

## Failure Conditions (Scenario 2)

- Writing `installed.json` before the selection prompt = FAIL
- Writing `installed.json` before thread display = FAIL
- Any output about the stats write = FAIL
