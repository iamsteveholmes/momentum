---
title: Reconcile fix-disposition with Conductor scope-discipline reverts
story_key: reconcile-fix-disposition-with-conductor-scope-reverts
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: defect
priority: high
depends_on: []
---

# Reconcile fix-disposition with Conductor scope-discipline reverts

## Story
When the Conductor reverts a fix under scope discipline, the corresponding finding-card disposition and the build-results scorecard must stop reporting that finding as `fixed`.

## Why this exists
Retro finding (sprint-2026-06-02-conduct-core): `conduct-preflight-halts` finding card #3 (a §8 spec-citation error in the story Dev Notes) is recorded `disposition:fixed`, but the fixer's edit to the story file was reverted by the Conductor (commit 5ca370f) under scope discipline. The merged `.momentum/stories/conduct-preflight-halts.md` still reads the erroneous text. build-results reports 5/5 fixed with no note that one fix was reverted — so the scorecard overstates convergence.

## What's needed
- When a fix edits a non-deliverable (e.g. the story spec file) and is reverted, its finding-card disposition is re-evaluated, not left `fixed`.
- The correction is re-routed (e.g. to create-story/refine) so the defect is still addressed for the record.
- The end-gate scorecard cannot report a reverted fix as `fixed`.

## References
- Retro findings: `.momentum/sprints/sprint-2026-06-02-conduct-core/retro-transcript-audit.md`
- Related (dedup, adjacent): `conduct-merge-and-conflict-resolution` (Conductor git mutations / revert point), `conduct-endgate-decision-card-rendering`, `conduct-coverage-disposition-discharge-consumer` (disposition lifecycle)
