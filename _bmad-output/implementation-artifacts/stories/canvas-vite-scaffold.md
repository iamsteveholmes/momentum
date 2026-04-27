---
title: Canvas Phase 1 — Vite Scaffold, Design Tokens, Pane Shell, Skill Rename
story_key: canvas-vite-scaffold
status: backlog
epic_slug: feature-orientation
feature_slug: momentum-canvas
story_type: feature
depends_on: []
touches: []
---

# Canvas Phase 1 — Vite Scaffold, Design Tokens, Pane Shell, Skill Rename

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to ship Phase 1 of the canvas implementation per DEC-011,
so that the scaffold, design tokens, pane shell, and skill rename are in place as the foundation all subsequent lens phases build on.

## Description

Foundation phase for the project canvas redesign per DEC-011. Scaffold a Vite project with vite-plugin-singlefile that bundles JS+CSS into a single dist/index.html opened via file:// in a cmux browser pane (no runtime transpile, no external deps). Establish the design token system, primitive components, pane shell layout, and anchor rail navigation that all subsequent lens stories build on. Hard rename feature-status → momentum:canvas at the same time — directory moves from skills/momentum/skills/feature-status/ to skills/momentum/skills/canvas/, slash command becomes /momentum:canvas, no shim, no backward-compat (solo practice, no external consumers per iq-20260424205300). Phase 1 may build against stub JSON files in dev until impetus-momentum-state-migration lands; the dependency is a merge gate per DEC-011 Gate G1 (iq-20260424205257). derives_from DEC-011.

**Pain context:** Phase 1 of DEC-011 implementation plan; absence blocks downstream phases and the canvas redesign from shipping. Predecessor (Pass 1 Variant B card grid) does not deliver the three-lens redesign.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Vite + vite-plugin-singlefile project scaffold under skills/momentum/skills/canvas/
- dist/index.html builds as a single self-contained file (inline JS, inline CSS)
- Page opens via file:// in a cmux browser pane with no runtime transpile cost
- Design tokens (colors, spacing, typography) defined and consumed by primitives
- Pane shell + anchor rail render with empty lens placeholders
- Skill renamed: feature-status → momentum:canvas (directory + slash command, hard rename)
- All references to /momentum:feature-status updated to /momentum:canvas
- Phase 1 reads stub JSON until Impetus state-relocation lands; merge gate G1 enforced
- depends_on: [impetus-momentum-state-migration]

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
