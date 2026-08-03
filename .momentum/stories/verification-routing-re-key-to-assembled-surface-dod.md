---
title: Verification routing re-key to assembled surface + DoD reachability item
story_key: verification-routing-re-key-to-assembled-surface-dod
status: backlog
epic_slug: momentum-quality-gates-enforced
feature_slug:
story_type: practice
depends_on: []
touches: []
---

# Verification routing re-key to assembled surface + DoD reachability item

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the Method Routing Table in verification-standard.md re-keyed from `change_type`
(a property of the diff) to `assembled surface` (where a user actually meets the
behavior), and a new Definition of Done item requiring reachability from the
application's entry point,
so that user-facing conversational behavior stops being routed to API-only
verification just because its diff happened to touch backend code, and stories can
no longer be marked done while the capability they claim to deliver is unreachable
by an end user.

## Description

Re-key `verification-standard.md`'s Method Routing Table from `change_type` (a
property of the diff — e.g. backend→curl unconditionally) to `assembled surface`
(where a user meets the behavior): behavior a user meets in the chat UI is driven
through the chat UI regardless of its diff, or the story declares at plan time, out
loud, that it cannot be.

Add one Definition of Done item to the DoD template: "the capability is reachable
from the application's entry point by a user who has read no code."

Source: DEC-040 D7 (`_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`),
amending DEC-029.

**Pain context:** Nornspun discovery: backend→curl routing sent user-facing
conversational stories to API-only verification; all three adversarial council seats
independently converged on exactly this fix; the missing DoD item let a no-op
settings gear, an empty SurfaceType enum, and a heroes API with zero callers all
count as done.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Method Routing Table in verification-standard.md keys on assembled surface (where
  a user meets the behavior), not change_type (a property of the diff).
- Behavior a user meets in the chat UI is verified through the chat UI regardless of
  what the underlying diff touched (backend, frontend, or both).
- A story may declare, at plan time and out loud, that a capability cannot be
  verified through its assembled surface — this is an explicit, visible exception,
  not a silent default.
- DoD template gains one new item: "the capability is reachable from the
  application's entry point by a user who has read no code."
- Existing verification-standard.md routing logic (e.g. backend→curl) is superseded
  or explicitly reconciled with the new surface-based keying — no dangling
  contradictory routing rule left in place.

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

Source decision: DEC-040 D7 — `_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md` (amends DEC-029).

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
