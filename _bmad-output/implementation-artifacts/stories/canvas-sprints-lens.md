---
title: Canvas Phase 3 — Sprints Lens with Closure Strip and Outcome Bands
story_key: canvas-sprints-lens
status: backlog
epic_slug: feature-orientation
feature_slug: momentum-canvas
story_type: feature
depends_on: []
touches: []
---

# Canvas Phase 3 — Sprints Lens with Closure Strip and Outcome Bands

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to ship Phase 3 of the canvas implementation per DEC-011,
so that sprint lifecycle and outcome data is visible in a single glanceable surface without manual git log traversal.

## Description

Second lens — Sprints. Reads .momentum/sprints/index.json. Renders the closure strip (sprint header, lifecycle states, outcome summary) and outcome bands across the active sprint. Collapses what would otherwise require manual git log + sprint folder traversal + retro path discovery into one glanceable surface. Depends on canvas-features-lens (data injection pattern) and on .momentum/sprints/ lifecycle states being final via impetus-momentum-state-migration. derives_from DEC-011.

**Pain context:** Phase 3 of DEC-011 implementation plan; absence blocks downstream phases and the canvas redesign from shipping. Predecessor (Pass 1 Variant B card grid) does not deliver the three-lens redesign.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Sprints lens reads .momentum/sprints/index.json
- Closure strip renders sprint header + lifecycle states + outcome summary
- Outcome bands render for active sprint
- Collapses git log / sprint folders / retro paths into single view
- depends_on: [canvas-features-lens, impetus-momentum-state-migration]

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
