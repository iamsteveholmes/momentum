---
title: Feature Dashboard UX Wireframes — Hierarchical Drill-Down
story_key: dashboard-ux-wireframes
status: backlog
epic_slug: feature-orientation
depends_on: []
touches: []
derives_from: dec-006-artifact-redesign-dual-audience-2026-04-14.md
---

# Feature Dashboard UX Wireframes — Hierarchical Drill-Down

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want wireframes for the hierarchical feature dashboard (index → feature drill-down → story drill-down),
so that the Phase 3 `feature-status` rewrite has a reviewed UX design to implement against rather than ad-hoc structure.

## Description

The current feature-status dashboard is a flat single-page HTML report. DEC-006 D2 redesigns it as an HTML directory: a top-level `index.html` listing all features with state, per-feature drill-down pages with full summary + stories + gaps, and story drill-down pages collapsed to the human section. Navigation (back, breadcrumbs) must be designed explicitly.

This is a design spike — no code. Deliverable is wireframes produced by the BMAD UX expert. Wireframes are the gating input for the Phase 3 dashboard generation rewrite of `feature-status` and should not be skipped.

**Pain context:** Without wireframes, the dashboard rewrite will produce whatever the implementer imagines — which historically drifts from what the developer actually wants. The BMAD UX expert has produced good work on past UI tasks and is the right agent for this.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Dashboard index page wireframe shows all features with their state (using DEC-005 D6 terminal states: Done / Shelved / Abandoned / Rejected, plus active states)
- Feature drill-down page wireframe shows full feature summary, list of stories with gaps, and navigation back to index
- Story drill-down view wireframe collapses to the human section of the story (DEC-006 D1), not the full LLM spec
- Navigation (back-link, breadcrumbs) is explicitly designed across all three levels
- Wireframes reviewed and approved by the developer before implementation begins
- Wireframes are compatible with DEC-005 D6 terminal state badges and DEC-006 D3 story-level dependency graph (even if dependency graph is a separate wireframe deliverable)

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

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- DEC-006: `_bmad-output/planning-artifacts/decisions/dec-006-artifact-redesign-dual-audience-2026-04-14.md`

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
