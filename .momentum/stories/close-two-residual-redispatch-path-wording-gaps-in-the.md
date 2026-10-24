---
title: Close two residual redispatch-path wording gaps in the conductor merge gate (end-gate D2 residual)
story_key: close-two-residual-redispatch-path-wording-gaps-in-the
status: backlog
epic_slug: ad-hoc
feature_slug: 
story_type: defect
depends_on: []
touches: [skills/momentum/skills/conductor/workflow.md]
---

# Close two residual redispatch-path wording gaps in the conductor merge gate (end-gate D2 residual)

<!-- INTAKE STUB: captured by momentum:intake. NOT dev-ready. -->

_Backlog stub. Run `momentum:create-story` on it when ready to make it dev-ready._

## Story

As a developer,
I want the conductor merge gate's no-remote and redispatch paths to use the same DELETED-BRANCH FALLBACK,
so that a request-changes pass after a post-merge merge-gate-failed never runs git log against a deleted ref.

## Description

From the sprint-2026-08-03 end-gate fix pass: the D2 fix (merge-gate pending stamp skips any terminal outcome; a recorded merge-gate-failed is re-surfaced first) landed and verified, but its 3-attempt fix budget exhausted with two residual wording objections in skills/momentum/skills/conductor/workflow.md:

1. ~line 2642, the no-remote clause of MERGE-GATE PRE-DECISION DISCLOSURE says "(or {{sprint_tip_sha}} under the fallback)", contradicting the line above (DELETED-BRANCH FALLBACK), which says "Do NOT derive it from the rehydrated {{sprint_tip_sha}}" and uses git log origin/main..main. The no-remote + deleted-branch case is left undefined.
2. ~line 3078, the 5.RC.4 redispatch re-bind of {{pending_commits}} uses only git log origin/main..sprint/{{sprint_slug}} with no DELETED-BRANCH FALLBACK, so a request-changes pass after a post-merge merge-gate-failed (push failed after branch delete) runs git log against a deleted ref.

Fix both to reference the same fallback as the initial binding.

**Pain context:** Residual from end-gate D2; fix budget exhausted, so these remain as wording gaps in an otherwise verified fix.

## Acceptance Criteria

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- The no-remote clause of MERGE-GATE PRE-DECISION DISCLOSURE no longer contradicts DELETED-BRANCH FALLBACK; the no-remote + deleted-branch case is defined.
- The 5.RC.4 redispatch re-bind of {{pending_commits}} applies the same DELETED-BRANCH FALLBACK as the initial binding.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Architecture Compliance

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

_DRAFT — requires rewrite via create-story before this story is dev-ready._

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
