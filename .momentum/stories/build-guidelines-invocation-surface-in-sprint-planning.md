---
title: Build-guidelines invocation surface in sprint-planning
story_key: build-guidelines-invocation-surface-in-sprint-planning
status: backlog
epic_slug: momentum-agent-composition-pipeline
feature_slug: momentum-composable-specialist-agents
story_type: feature
priority: medium
depends_on: []
touches: []
---

# Build-guidelines invocation surface in sprint-planning

<!-- BACKFILL STUB: this story's index entry (stories/index.json) claimed
     story_file: true with no backing file — a phantom entry found by the
     2026-07-06 retro audit of sprint-2026-06-28. This stub repairs the
     phantom by giving the entry a real backing file. It is a backlog stub,
     NOT a dev-ready story. -->

_This story is a backlog stub — run `momentum:create-story` on it when ready to
make it dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer running sprint planning,
I want `momentum:sprint-planning` to invoke `momentum:build-guidelines` at the appropriate point in its workflow,
so that project-specific agent composition (base body + constitution + manifesto) is produced as part of planning a sprint, rather than requiring a separate manual step.

## Description

This story's own scope is narrow: give `sprint-planning` an invocation surface for `build-guidelines` — where in the planning workflow it is called, what triggers it (e.g. new project onboarding vs. an existing composed-agent set), and what its output feeds into for that sprint's stories. This scope belongs to this slug alone; it does not absorb or duplicate the fixture-population work owned by `conduct-live-run-against-fixture-sprint` or the composition pipeline itself (`build-guidelines`, `agent-builder`), which are separate stories.

## Acceptance Criteria

_Not yet defined — run `momentum:create-story` to enrich this stub with validated, testable acceptance criteria._

## Tasks / Subtasks

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- Source: 2026-07-06 retro transcript audit of sprint-2026-06-28 (`audit-return.json` priority items 1 + 3), dedup-verified 2026-07-06.
- Repaired by: `.momentum/stories/repair-phantom-story-file-entries-and-backfill-live-fixture-scope.md` (this story's backing-file repair, not its scope).
- Epic context: `momentum-agent-composition-pipeline` (from `_bmad-output/planning-artifacts/epics.json`).

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
