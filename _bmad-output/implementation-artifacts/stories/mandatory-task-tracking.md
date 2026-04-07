---
title: Mandatory Task Tracking — Enforce TaskCreate in Long Sessions
story_key: mandatory-task-tracking
status: backlog
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum/skills/sprint-dev/workflow.md
  - skills/momentum/skills/sprint-planning/workflow.md
change_type: skill-instruction
priority: critical
---

# Mandatory Task Tracking — Enforce TaskCreate in Long Sessions

## Description

Sprint-dev and sprint-planning workflows already contain Phase 0 task
tracking steps, but compliance is not enforced — agents abandon task state
mid-session and fall back to ad-hoc narrative summaries. This defeats the
purpose of task tracking, which exists specifically to survive context
compression in long-running sessions.

The retro skill (which already has task tracking as a `<critical>` directive)
is the reference pattern. Sprint-dev and sprint-planning need the same
enforcement: a `<critical>` directive that makes task tracking non-optional,
plus a rule that agents can load independently to enforce the behavior even
when invoked outside a workflow context.

**Retro incident:** User hit peak frustration (ALL-CAPS escalation) when
task tracking was abandoned mid-session. Agent presented ad-hoc summaries
instead of using TaskCreate/TaskList tools. Three-message escalation:
"Where is the task list?" → "But that is not a claude code task list" →
"Seriously...WHy can't you create a task list?"

## Acceptance Criteria (Plain English)

1. The sprint-dev workflow (`skills/momentum/skills/sprint-dev/workflow.md`)
   contains a `<critical>` directive requiring TaskCreate/TaskUpdate usage
   for phase tracking — matching the pattern already present in the retro
   workflow. The directive explicitly states that ad-hoc narrative
   summaries are not a substitute for tool-queryable task state.

2. The sprint-planning workflow
   (`skills/momentum/skills/sprint-planning/workflow.md`) contains the same
   `<critical>` directive requiring TaskCreate/TaskUpdate usage for step
   tracking.

3. Every `<step>` in sprint-dev (phases 1-7) includes an explicit
   `<action>Update task N to in_progress</action>` at phase entry and
   `<action>Update task N to completed</action>` at phase exit — matching
   the retro workflow pattern.

4. Every `<step>` in sprint-planning (steps 1-8) includes the same
   in_progress/completed TaskUpdate actions at step entry and exit.

5. The `<critical>` directive wording is consistent across all three
   workflows (retro, sprint-dev, sprint-planning) — all mention
   TaskCreate/TaskUpdate by name and state that task tracking prevents
   context drift in long runs.

6. The retro workflow's existing task tracking `<critical>` directive and
   Phase 0 remain unchanged — they are the reference implementation.

## Dev Notes

### Reference pattern (retro workflow)

The retro workflow is the reference implementation. Key elements:

1. **`<critical>` directive** at workflow top (line 15):
   ```xml
   <critical>Use task tracking (TaskCreate/TaskUpdate) for retro phases —
   this prevents context drift in long runs.</critical>
   ```

2. **Phase 0** creates all tasks upfront via TaskCreate.

3. **Every subsequent phase** starts with `Update task N to in_progress`
   and ends with `Update task N to completed`.

### Current state analysis

**sprint-dev/workflow.md:**
- Phase 0 (line 24): creates 7 phase-level tasks — present and correct
- Phase 1 (line 41): creates per-story tasks via TaskCreate (line 94-99) — present
- Phase 2 (line 113): updates story tasks to in_progress (line 142) — present
- Phase 3 (line 156): updates story tasks on completion (line 203) — present
- Phases 4-7: no TaskUpdate actions for phase-level tasks
- Missing: `<critical>` directive mandating task tracking
- Missing: consistent in_progress/completed updates for every phase task

**sprint-planning/workflow.md:**
- Step 0 (line 17): creates 9 step-level tasks — present and correct
- Steps 1-8: zero TaskUpdate actions anywhere — tasks are created but
  never transitioned

### Tasks

1. Add `<critical>` directive to sprint-dev/workflow.md after existing
   critical directives (after line 18)
2. Audit sprint-dev phases 1-7 — add `Update task N to in_progress` at
   phase entry and `Update task N to completed` at phase exit for every
   phase missing them
3. Add `<critical>` directive to sprint-planning/workflow.md after
   existing critical directives (after line 15)
4. Add `Update task N to in_progress` and `Update task N to completed`
   actions to every step (1-8) in sprint-planning/workflow.md
5. Verify retro/workflow.md has complete coverage (read-only — no changes
   expected)
