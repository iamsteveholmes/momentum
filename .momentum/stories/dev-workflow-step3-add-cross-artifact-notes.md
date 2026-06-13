---
title: Add cross_artifact_notes to the dev workflow Step 3 success template
story_key: dev-workflow-step3-add-cross-artifact-notes
status: backlog
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: defect
priority: low
change_type:
  - skill-instruction
depends_on: []
touches:
  - skills/momentum/skills/dev/workflow.md
---

# Add cross_artifact_notes to the dev workflow Step 3 success template

## Story

As the maintainer of the dev↔Conductor seam,
I want the dev workflow's green-field success signal to emit `cross_artifact_notes` like the canonical dev.md schema does,
so that a dev following the workflow template verbatim does not under-emit the field the Conductor routes to momentum:triage.

## Why this exists (triaged-out finding ca-07 from sprint-2026-06-10)

Pre-existing seam drift: `skills/momentum/skills/dev/workflow.md` Step 3's `AGENT_OUTPUT` success template carries `status`, `story_key`, `files_changed`, `part_a_self_check`, and `test_results` but omits `cross_artifact_notes`, while `agents/dev.md`'s success schema includes it and the Conductor routes those notes to momentum:triage. An agent following the workflow template literally under-emits the field. The dev-commit-authority story correctly did not touch this (its regression guard forbade schema changes), so it was triaged out as a follow-up.

## Acceptance Criteria

1. The Step 3 green-field success `AGENT_OUTPUT` template in `dev/workflow.md` includes `cross_artifact_notes` (defaulting to `[]`), byte-matching the field set in `agents/dev.md`'s success schema so the Conductor's parse contract holds whichever surface the agent followed.

## Tasks / Subtasks
- [ ] Add `cross_artifact_notes` to the Step 3 success template; confirm the two surfaces agree.

## Dev Agent Record
