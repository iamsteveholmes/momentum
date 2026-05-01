---
title: Decision Workflow — Retired-State-File Cleanup Checklist
story_key: decision-workflow-retire-state-file-checklist
status: ready-for-dev
epic_slug: impetus-core
story_type: practice
priority: medium
depends_on: []
touches:
  - skills/momentum/skills/decision/workflow.md
---

# Story: Decision Workflow — Retired-State-File Cleanup Checklist

Status: ready-for-dev

## Story

As the developer recording strategic decisions in `momentum:decision`,
I want the decision workflow to remind me to grep `agents/*` and `references/*` for any state file path being retired by the decision,
so that "retire a state file" decisions land atomically without leaving stranded references in agent definitions or reference docs.

## Context

Distilled from a finding surfaced during quick-fix `quickfix-2026-04-30` (which adopted DEC-012 retiring `.momentum/sprints/{slug}.json`). The post-merge code review found that `skills/momentum/agents/dev.md:23` still named the retired path in its "you never write to" list — exactly the kind of stale-reference drift DEC-012 was meant to eliminate. The dev.md fix was applied as a Tier 1 distill in the same session. This story addresses the upstream workflow gap so future "retire a state file" decisions don't repeat the omission.

Source: distill — Tier 2 escalation from quickfix-2026-04-30

## Acceptance Criteria

1. `skills/momentum/skills/decision/workflow.md` Step 7 (Bridge to Story Creation, or the closest equivalent step) includes a new checklist `<action>` that fires on retirement-class decisions, containing: "If any adopted decision retires a state file or canonical path, grep `skills/momentum/agents/*.md` and `skills/momentum/references/**` for the retired path. Fold any found references into the cleanup story so the retirement is atomic — no stranded references in 'never write to' lists, protected-paths lists, or doc cross-references."

2. The checklist item references DEC-012 as the precipitating example: "`sprints/{slug}.json` retired by DEC-012 without scrubbing `agents/dev.md` — the pattern to prevent."

3. The decision workflow's existing step structure is preserved — the new checklist item is additive, not a rewrite of the step.

4. A behavioral eval exists at `skills/momentum/skills/decision/evals/eval-decision-surfaces-state-file-cleanup.md` that describes: "Given a decision adopts the retirement of a state file path, the decision workflow prompts the developer to grep agent definitions and references for that path before recording the decision as adopted."

5. (Behavioral) After this change, running `momentum:decision` for a decision that retires a path surfaces the cleanup-grep prompt before the decision is recorded as adopted.

## Tasks / Subtasks

- [ ] **Task 1 — Read decision/workflow.md to find Step 7**
  - [ ] 1.1 Read `skills/momentum/skills/decision/workflow.md` and identify the step that bridges the decision to story creation (Step 7 or equivalent).
  - [ ] 1.2 Confirm the step's existing structure so the new checklist item can be inserted cleanly.

- [ ] **Task 2 — Add the cleanup checklist item to decision/workflow.md**
  - [ ] 2.1 Insert a new `<action>` block in Step 7 (or closest equivalent): "If any adopted decision retires a state file or canonical path, grep `skills/momentum/agents/*.md` and `skills/momentum/references/**` for the retired path. Fold any found references into the cleanup story so the retirement is atomic." Reference DEC-012 as the precipitating example.
  - [ ] 2.2 Preserve all existing step structure around the insertion.

- [ ] **Task 3 — Write behavioral eval**
  - [ ] 3.1 Create `skills/momentum/skills/decision/evals/eval-decision-surfaces-state-file-cleanup.md` with the scenario described in AC4.

- [ ] **Task 4 — EDD cycle**
  - [ ] 4.1 Run the eval against the updated workflow.md. Confirm the scenario passes.

## Dev Notes

### Why This Story Exists

The immediate symptom (dev.md:23 stale reference) was fixed inline as a Tier 1 distill alongside this Tier 2 escalation. This story closes the upstream gap — it adds a workflow prompt so future decision-recorders don't skip the cleanup step.

### Change Type

`skill-instruction` — single workflow.md edit + one eval.

### Distill Provenance

- Session: 2026-04-30
- Origin: code-reviewer finding on quickfix-2026-04-30 (cross-cutting observation #3)
- Tier 2 escalation reason: lesson target is `decision/workflow.md` (different skill than the code fix), making this multi-file in scope

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
