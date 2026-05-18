---
title: sprint-planning pre-sprint activation — Class-1 deterministic pre-sprint render gate
story_key: sprint-planning-pre-sprint-class-1-render-gate
status: backlog
epic_slug: impetus-sprint-orchestrator
feature_slug: momentum-sprint-planning-to-ready
story_type: feature
depends_on: []
touches: []
---

# sprint-planning pre-sprint activation — Class-1 deterministic pre-sprint render gate

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to add a Class-1 deterministic pre-sprint render gate to sprint-planning that must be approved before sprint_activate fires,
so that every sprint starts from a provably clean slate — stories with missing contracts or AVFL failures are blocked at planning, not discovered mid-sprint.

## Description

Follow-on to the done story `sprint-planning-adds-per-story-approval-gate`. Adds a Class-1 deterministic pre-sprint planning render that must pass before sprint_activate is called. The render shows: story-readiness (AVFL-clean status), AC specs (frozen contract candidates), team-composition (which dev agent roles are needed), and any blocking flags. Developer approval of this render is what gates activation. Activation refuses if any member story lacks a frozen contract or is not validation-clean. This is the pre-sprint touchpoint in DEC-030 D5's two-touchpoint human model (pre-sprint planning + verification). Source: DEC-030 D3/D5.

**Pain context:** Pre-sprint planning is the human's first and most important touchpoint. Making it a Class-1 render with approval binding ensures the gate has integrity. DEC-030 D5 mandates this as a hard precondition for sprint_activate.

**Source:** triage — DEC-030 blast-radius discovery

**Proposed depends_on:** sprint-manager-frozen-scope-enforcement, feature-status-class-1-deterministic-projection

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- sprint-planning renders a pre-activation checklist showing story-readiness, AC specs, AVFL-clean status, team-composition
- the render is Class-1 deterministic — derived from structured data, no narrative
- developer approves the render to proceed to sprint_activate
- sprint_activate is refused if any member story lacks a frozen contract or has AVFL failures
- the pre-sprint render is the first of the two mandated human touchpoints (DEC-030 D5)

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
