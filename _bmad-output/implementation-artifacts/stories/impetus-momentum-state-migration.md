---
title: Migrate Impetus State Reads to .momentum/
story_key: impetus-momentum-state-migration
status: backlog
epic_slug: impetus-core
feature_slug: 
story_type: maintenance
depends_on: []
touches: []
---

# Migrate Impetus State Reads to .momentum/

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want Impetus to read sprint and story state from `.momentum/` instead of `_bmad-output/implementation-artifacts/`,
so that Impetus has a single, clean state source aligned with the .momentum/ architecture.

## Description

After the `.momentum/` state migration completes, Impetus must be updated to read from
the new canonical paths. Currently Impetus reads `_bmad-output/implementation-artifacts/sprints/index.json`
and `_bmad-output/implementation-artifacts/stories/index.json`. Post-migration these live
at `.momentum/sprints/index.json` and `.momentum/stories/index.json`. In addition, Impetus
should read `.momentum/signals/` — a directory of retro-derived pending work flags that
tell him what's outstanding across the practice (uncleared triage queue, AVFL findings
awaiting upstream-fix, etc.).

This story should be triggered only after the .momentum/ state migration story is complete.
Impetus should treat `.momentum/` as his single state source for session orientation.

**Pain context:** Without this update, Impetus will continue reading from old paths after
the migration, silently getting stale or missing data. The .momentum/ signals directory
is new — no skill currently reads it — so this story also establishes the first consumer
of the signals pattern.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Impetus reads `.momentum/sprints/index.json` (not `_bmad-output/implementation-artifacts/sprints/index.json`)
- Impetus reads `.momentum/stories/index.json` (not `_bmad-output/implementation-artifacts/stories/index.json`)
- Impetus reads `.momentum/signals/` directory for retro-derived pending work flags
- All three reads happen silently at startup with no user-visible narration
- Impetus treats `.momentum/` as its single state source — no fallback to old paths
- If `.momentum/signals/` is empty or absent, Impetus degrades gracefully (no error)

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

<!-- DRAFT: No tasks have been analyzed or planned. This section MUST be populated by
     create-story, which will break down the work based on architecture analysis and
     implementation guidance. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

<!-- DRAFT: Not yet populated. Run create-story to enrich with architecture analysis,
     implementation guide, technical requirements, and Momentum-specific guidance. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

No technical analysis has been performed. The following sub-sections are all stubs.

### Architecture Compliance

<!-- DRAFT: Architecture compliance has not been assessed for this story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

<!-- DRAFT: Testing requirements have not been defined for this story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

<!-- DRAFT: No implementation guide has been generated. Create-story will inject
     Momentum-specific guidance based on change-type classification. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

<!-- DRAFT: File paths, skill directories, and structural alignment have not been
     analyzed. Create-story will populate this based on the relevant epic and
     existing codebase structure. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

<!-- DRAFT: No references have been identified. Create-story will add source citations
     from architecture docs, PRD, and relevant code. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
