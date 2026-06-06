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

## Status (verified 2026-06-06, sprint-planning AVFL)
A convergence commit landed AFTER conduct-core merge but BEFORE this story's intake, so two of the
fixes below are **already present** on this branch — confirm-then-verify, do NOT re-author:
- approve path already routes `review`→`verify`→`done` (`conductor/workflow.md` ~L1212–1214, commit `9e72bb2`).
- terminal→terminal transitions are already rejected (`skills/momentum/scripts/momentum-tools.py` ~L55–56, `--force` required).
The **genuinely-open** deliverable is the governance guard (last bullet): a MAJOR residual must not leave a sprint without a linked backlog stub. Treat the two transition fixes as regression-verification (the evals still apply), and focus implementation on the residual-linkage guard.

## What's needed
- Confirm (regression) both runtime-rejected transitions are fixed in `conductor/workflow.md` / `momentum-tools`.
- Keep the approve path routing merged stories `review`→`verify`→`done`.
- Keep the guard preventing terminal-to-terminal status transitions.
- Add an eval scenario per defect (regression coverage).
- **PRIMARY OPEN WORK:** No residual carrying MAJOR severity leaves a future sprint without a linked backlog stub.

## References
- Retro findings (v2): `.momentum/sprints/sprint-2026-06-02-conduct-core/retro-transcript-audit.md`
- Source: AVFL residual cards + `conduct-core-finding-cards-by-story.json` (triaged-out set)
- Related: `momentum-tools` status-transition validation (`ORDERED_STATES`)
