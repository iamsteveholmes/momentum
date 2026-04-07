---
title: Mandatory Task Tracking — Enforce TaskCreate in Long Sessions
story_key: mandatory-task-tracking
status: backlog
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum/skills/sprint-dev/workflow.md
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/retro/workflow.md
  - skills/momentum/references/rules/
change_type: skill-instruction + rule-hook
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
   workflow.

2. The sprint-planning workflow
   (`skills/momentum/skills/sprint-planning/workflow.md`) contains the same
   `<critical>` directive requiring TaskCreate/TaskUpdate usage for step
   tracking.

3. A bundled rule file exists at
   `skills/momentum/references/rules/task-tracking.md` that states:
   long-running sessions (sprint-dev, sprint-planning, retro, and any
   workflow with more than 3 phases) MUST use TaskCreate at session start
   and maintain task state via TaskUpdate throughout execution. Ad-hoc
   narrative summaries are not a substitute for tool-queryable task state.

4. Every `<step>` in sprint-dev and sprint-planning workflows that does
   NOT already call TaskUpdate now includes an explicit TaskUpdate action
   at step completion (matching the retro workflow pattern where each
   phase ends with "Update task N to completed").

5. The retro workflow's existing task tracking `<critical>` directive and
   Phase 0 remain unchanged — they are the reference implementation and
   must not be modified.

## Dev Notes

### Reference pattern (retro workflow)

The retro workflow already does this correctly. Key elements:

1. **`<critical>` directive** at workflow top:
   ```xml
   <critical>Use task tracking (TaskCreate/TaskUpdate) for retro phases —
   this prevents context drift in long runs.</critical>
   ```

2. **Phase 0** creates all tasks upfront.

3. **Every subsequent phase** starts with `Update task N to in_progress`
   and ends with `Update task N to completed`.

### What to change

**sprint-dev/workflow.md:**
- Already has Phase 0 with TaskCreate and per-story task creation in Phase 1
- Already has TaskUpdate calls in Phase 3
- Needs: a `<critical>` directive at the workflow top (same language as retro)
- Audit all 7 phases to ensure every phase has explicit TaskUpdate at
  start (in_progress) and end (completed)

**sprint-planning/workflow.md:**
- Already has Step 0 with TaskCreate for 9 workflow steps
- Needs: a `<critical>` directive at the workflow top (same language as retro)
- Audit all 9 steps to ensure every step has explicit TaskUpdate at
  start (in_progress) and end (completed)

**New rule file:**
- `skills/momentum/references/rules/task-tracking.md` — standalone rule
  that agents load via rules deployment. Covers the "why" (context drift
  is the #1 failure in long sessions) and the "what" (TaskCreate at
  start, TaskUpdate throughout, never substitute narrative for tools).

### Why a rule AND workflow directives

The `<critical>` directives enforce behavior when the workflow is being
followed. The rule enforces behavior even when an agent is invoked
outside a strict workflow context (e.g., Impetus session mode, ad-hoc
skill invocations, or when context compression causes the agent to lose
track of workflow instructions).

### Files

- `skills/momentum/skills/sprint-dev/workflow.md` — add `<critical>` + audit TaskUpdate coverage
- `skills/momentum/skills/sprint-planning/workflow.md` — add `<critical>` + audit TaskUpdate coverage
- `skills/momentum/references/rules/task-tracking.md` — new rule file
