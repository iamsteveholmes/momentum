---
title: E2E Client-Side Coverage — Layer 2 UI Interaction Validation
story_key: e2e-client-side-coverage
status: backlog
epic_slug: agent-team-model
depends_on: []
touches: []
---

# E2E Client-Side Coverage — Layer 2 UI Interaction Validation

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As an E2E validator,
I want a two-layer coverage model that includes client-side UI interaction validation alongside API behavioral tests,
so that a sprint's E2E validation is not declared complete when fundamental UI interaction bugs remain invisible to automated tests.

## Description

The current E2E skill defines "covered" as: all Gherkin scenarios validated against live FastAPI endpoints (API-level). Client-integration flows — UI state management, screen transitions, context isolation between agents — are not included in the coverage requirement. This creates a false sense of completeness: a sprint can pass 57/71 API scenarios and still have fundamental user-facing bugs that only manifest in the client.

Two-layer model:
- **Layer 1 (current):** API behavioral coverage — all Gherkin scenarios against live FastAPI endpoints
- **Layer 2 (required addition):** Client interaction coverage — UI state transitions, end-to-end user flows via Maestro (Android) and desktop UI testing, connection handling and error state display

A sprint's E2E validation must not be declared complete until both layers pass. If Layer 2 is absent, the skill should surface a warning rather than declaring success.

**Pain context:** D3 sprint (nornspun-2026-04-10-2-retro.md, Issue 5, High). After automated E2E passed 57/71 API scenarios, 30 minutes of user manual testing found: norn switching didn't work, context wasn't isolated between norns, connection errors occurred. These were invisible to API-level validation because they're client-state concerns. User spent 30+ minutes (19:29–20:07) debugging issues the automated suite never touched.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- E2E skill defines two coverage layers (Layer 1: API, Layer 2: client interaction)
- Sprint E2E validation is not declared complete until both layers are addressed
- If Layer 2 coverage is absent, skill surfaces explicit warning: "API validation complete. Client interaction coverage not performed. User manual testing required."
- Layer 2 scope includes: UI state transitions, context isolation between agents, end-to-end user flows via Maestro

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
