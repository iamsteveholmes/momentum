---
title: Sprint Workflow Alignment — Fix Slug Extraction and Status Transitions
story_key: sprint-workflow-alignment
status: backlog
epic_slug: greeting-redesign
depends_on:
  - sprint-lifecycle-tools
touches:
  - skills/momentum/skills/sprint-dev/workflow.md
  - skills/momentum/skills/sprint-planning/workflow.md
change_type: skill-instruction
---

# Sprint Workflow Alignment — Fix Slug Extraction and Status Transitions

## Description

The sprint-dev and sprint-planning workflows need minor updates to work correctly
with the sprint lifecycle status fields introduced by Architecture Decision 36.
The sprint-dev workflow incorrectly describes how to extract the active sprint
slug, and the sprint-planning workflow skips the "ready" status transition before
activation.

## Acceptance Criteria

1. The sprint-dev workflow extracts the sprint slug from `active.slug` in
   `sprints/index.json`, not from the `active` field directly.
2. The sprint-dev workflow validates that `active.status` equals `"active"`
   before proceeding, and halts with an explanatory message if the sprint is not
   in active status.
3. The sprint-planning workflow calls `momentum-tools sprint ready` before
   calling `momentum-tools sprint activate`, ensuring `planning.status` is set
   to `"ready"` before activation transitions it to `"active"`.
4. The full status lifecycle (planning -> ready -> active) is represented in the
   sprint-planning workflow's activation sequence.

## Dev Notes

### sprint-dev workflow

**File:** `skills/momentum/skills/sprint-dev/workflow.md`

- Line 43 currently says `Store {{sprint_slug}} = the value of 'active' field
  (a string slug)`. The `active` field is an object with a `.slug` property, not
  a plain string. Fix the instruction to read `active.slug` from
  `sprints/index.json`.
- After reading the active sprint, add a guard: if `active.status != "active"`,
  halt execution with a message explaining the sprint is not in active status.

### sprint-planning workflow

**File:** `skills/momentum/skills/sprint-planning/workflow.md`

- Before the existing `momentum-tools sprint activate` call near the end of the
  workflow, insert a call to `momentum-tools sprint ready`.
- This ensures the planning sprint's status field transitions through `"ready"`
  before activation sets it to `"active"`.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
