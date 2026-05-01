---
title: Canvas Phase 5 — Level-2 Feature Detail with Replace-View Nav
story_key: canvas-level-2-feature-detail
status: backlog
epic_slug: feature-orientation
feature_slug: momentum-canvas
story_type: feature
depends_on: []
touches: []
---

# Canvas Phase 5 — Level-2 Feature Detail with Replace-View Nav

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to ship Phase 5 of the canvas implementation per DEC-011,
so that feature drill-down detail is accessible via replace-view navigation with story list and deps visible without leaving the canvas.

## Description

Drill-down detail panel for a single feature, accessed from the Features lens via replace-view navigation. Shows story list, list-only deps (no graph view, no mode pill — per iq-20260424205304; the graph mode and direct-only mode pills from Pass 5 design are explicitly retired), and feature metadata. Reading-mode lock applies. Independent of Phases 3 and 4 — only requires Phase 2's data injection pattern. derives_from DEC-011.

**Pain context:** Phase 5 of DEC-011 implementation plan; absence blocks downstream phases and the canvas redesign from shipping. Predecessor (Pass 1 Variant B card grid) does not deliver the three-lens redesign.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Replace-view navigation from Features lens to Level-2 detail
- Story list renders for the selected feature
- Deps render as list only — no graph view, no mode pill
- Feature metadata (acceptance condition, value analysis, status) visible
- Reading-mode lock applies on this surface
- depends_on: [canvas-features-lens]

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
