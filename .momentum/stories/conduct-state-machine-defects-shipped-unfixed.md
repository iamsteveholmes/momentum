---
title: Fix two MAJOR conduct state-machine defects shipped unfixed (terminal→terminal + verify-skip)
story_key: conduct-state-machine-defects-shipped-unfixed
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: defect
priority: critical
depends_on: []
---

# Fix two MAJOR conduct state-machine defects shipped unfixed (terminal→terminal + verify-skip)

## Story
Two MAJOR status-transition defects were found during the conduct-core build, triaged-out with no backlog linkage, and shipped unfixed. Fix both and guard against the class.

## Why this exists
Retro finding (sprint-2026-06-02-conduct-core, **critical**): the AVFL "— residual" card set surfaced two MAJOR defects that were both triaged-out with no follow-up story (a `grep` of `.momentum/stories/*.md` finds no linked stub):
1. An **illegal terminal-to-terminal status transition** at approve (rejected by the state machine at runtime).
2. **approve jumps merged stories `review`→`done`, skipping the required `verify` state** (also rejected at runtime).

A MAJOR severity finding leaving a sprint with no backlog linkage is itself the deeper defect — the triage-out path must not silently drop MAJOR residuals.

## What's needed
- Identify both runtime-rejected transitions in `conductor/workflow.md`.
- Fix the approve path to route merged stories `review`→`verify`→`done`.
- Add a guard preventing terminal-to-terminal status transitions.
- Add an eval scenario per defect.
- No residual carrying MAJOR severity leaves a future sprint without a linked backlog stub.

## References
- Retro findings (v2): `.momentum/sprints/sprint-2026-06-02-conduct-core/retro-transcript-audit.md`
- Source: AVFL residual cards + `conduct-core-finding-cards-by-story.json` (triaged-out set)
- Related: `momentum-tools` status-transition validation (`ORDERED_STATES`)
