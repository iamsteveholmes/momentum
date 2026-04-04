---
title: Simplify momentum-dev — Pure Executor with Agent Logging
status: ready-for-dev
epic_slug: impetus-core
depends_on:
  - agent-logging-tool
touches:
  - skills/momentum-dev/workflow.md
change_type: skill-instruction
---

# Simplify momentum-dev

## Goal

Strip momentum-dev down to a pure executor. Remove AVFL invocation and sprint-status
transition calls — both responsibilities move to the orchestration layer (Impetus / sprint-dev).
Wire in agent logging at key decision points so retrospectives have evidence. The result:
momentum-dev does worktree setup, runs bmad-dev-story inline, logs its work, and returns
merge-ready output. Nothing more.

## Acceptance Criteria

- momentum-dev no longer invokes momentum-avfl at any point during execution. AVFL runs
  at sprint level after all stories merge, not per-story.

- momentum-dev no longer calls `momentum-tools.py sprint status-transition` or any
  equivalent status-writing command. Status transitions are handled by the caller
  (Impetus or sprint-dev) after merge.

- momentum-dev emits `momentum-tools log` calls at these decision points: story selection,
  worktree creation, implementation start (bmad-dev-story invocation), implementation
  complete (bmad-dev-story returns), and merge proposal.

- Log calls use the format:
  `momentum-tools log --agent dev --story {{story_key}} --event <type> --detail "..."`
  with event types from the standard set (decision, error, retry, assumption, finding,
  ambiguity).

- The Momentum-specific DoD supplement (current Step 8) is removed. DoD verification
  moves to the verification phase at sprint level.

- The code review offer (current Step 10) is removed. Code review is an orthogonal
  concern managed by the caller.

- The completion output emits a structured signal (JSON) that the caller can parse:
  status, files modified, and test results from bmad-dev-story.

- Worktree lifecycle (create, crash recovery, merge proposal, cleanup) remains unchanged.

- momentum-dev can still be invoked standalone (not only via Impetus) — the logging calls
  should not fail if no sprint context exists.

## Dev Notes

### What exists today
- workflow.md has 10 steps spanning story selection through code review offer
- Step 5 calls `momentum-tools.py sprint status-transition --target in-progress`
- Step 6 ends with `momentum-tools.py sprint status-transition --target review`
- Step 7 is a full AVFL quality gate (~50 lines) with profile selection, domain expert
  determination, and three-outcome handling (CLEAN, CHECKPOINT_WARNING, GATE_FAILED)
- Step 8 is a Momentum-specific DoD supplement (~35 lines) checking skill, code, spec,
  rule-hook, and config-structure items
- Step 9 calls `momentum-tools.py sprint status-transition --target done`
- Step 10 offers optional bmad-code-review and emits a completion signal

### What to remove
1. **Step 5 status transition** — delete the `momentum-tools.py sprint status-transition
   --target in-progress` action. Keep the lock file creation.
2. **Step 6 status transition** — delete the `momentum-tools.py sprint status-transition
   --target review` action at the end of Step 6.
3. **Step 7 (entire step)** — remove the AVFL quality gate step completely. AVFL moves to
   sprint-dev (one pass after all stories merge).
4. **Step 8 (entire step)** — remove the Momentum DoD supplement step completely.
   Verification moves to the sprint-level verify phase.
5. **Step 9 status transition** — delete the `momentum-tools.py sprint status-transition
   --target done` action. Keep the merge proposal and worktree cleanup.
6. **Step 10 code review offer** — remove the code review offer. Keep the completion signal.
7. **Critical directive about AVFL** — remove the `<critical>` about AVFL running on
   complete story changeset (no longer applies).

### What to add
1. **Agent logging calls** — add `momentum-tools log` invocations via Bash tool at:
   - Step 2 (after story resolution): `--event decision --detail "Selected story {{story_key}}"`
   - Step 4 (after worktree creation): `--event decision --detail "Worktree created at .worktrees/story-{{story_key}}"`
   - Step 6 (before bmad-dev-story): `--event decision --detail "Starting implementation via bmad-dev-story"`
   - Step 6 (after bmad-dev-story returns): `--event decision --detail "Implementation complete, files: {{file_list}}"`
   - Step 9 (merge proposal): `--event decision --detail "Proposing merge of story/{{story_key}} into {{target_branch}}"`
2. **Error logging** — add `--event error` log calls in crash recovery (Step 3) when
   stale branches are found, and in merge conflict scenarios.
3. **Graceful log failures** — log calls should not block execution if they fail (e.g.,
   no sprint-logs directory yet, momentum-tools not available). Wrap in best-effort
   execution.

### What to keep unchanged
- Steps 1-4: branch capture, story resolution, crash recovery, worktree creation
- Step 6 core: bmad-dev-story invocation, worktree enter/exit, file list capture
- Step 9 core: merge proposal, rebase, conflict handling, worktree cleanup
- Completion signal JSON structure
- All `<critical>` directives about worktrees, merge gates, and main-tree writes
  (except the AVFL-related one)

### Step renumbering
After removals, the workflow collapses from 10 steps to ~7:
1. Capture target branch
2. Resolve story to develop (+ log)
3. Crash recovery check (+ error log)
4. Create git worktree (+ log)
5. Mark story in-progress (lock file only, no status transition)
6. Invoke bmad-dev-story (+ log start/complete)
7. Propose merge and clean up (+ log, completion signal)

### Architecture context
- Per Architecture Decision 24: every agent writes JSONL logs via momentum-tools log
- Per sprint-dev workflow: AVFL runs once after ALL stories merge, not per-story
- Per orchestration model: Impetus spawns momentum-dev, then calls sprint-manager for
  status transitions after merge confirmation
- momentum-dev is always spawned as a subagent — it should never manage its own status
