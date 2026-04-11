---
title: Impetus Lifecycle and Handoff Fix — Planning State Active, Return to Menu After Ad-Hoc
story_key: impetus-lifecycle-and-handoff-fix
status: backlog
epic_slug: impetus-core
depends_on: []
touches: []
---

# Impetus Lifecycle and Handoff Fix — Planning State Active, Return to Menu After Ad-Hoc

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a Impetus orchestrator,
I want correctly represent sprint lifecycle state (planning = active sprint, not pre-sprint) and return to menu after ad-hoc sub-skill dispatches complete,
so that Impetus always shows the right state — no more phantom pre-sprint mode during active planning, no stranded sessions after ad-hoc dispatches.

## Description

Two lifecycle UX gaps: (1) Sprint in planning phase is shown as 'pre-sprint' when it should display as 'active' with planning context. (2) After dispatching to an ad-hoc sub-skill (research, assessment, etc.) and that skill completes, the session ends instead of returning to the Impetus menu for the next dispatch.

**Pain context:** Sprint-2026-04-08 retro (#10). User was corrected repeatedly about the planning state display. The handoff issue means ad-hoc skill usage ends the session, requiring a new /momentum invocation.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Sprint in planning state displays as 'active (planning)' not 'pre-sprint'
- After ad-hoc sub-skill dispatch completes, Impetus menu re-displays
- Menu shows 'back' option after sub-skill completion
- Eval covers planning-state display and post-dispatch menu return

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
