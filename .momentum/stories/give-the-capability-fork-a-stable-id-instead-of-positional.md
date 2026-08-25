---
title: Give the capability fork a stable id instead of positional addressing
story_key: give-the-capability-fork-a-stable-id-instead-of-positional
status: backlog
epic_slug: ad-hoc
feature_slug:
story_type: maintenance
depends_on: []
touches: []
---

# Give the capability fork a stable id instead of positional addressing

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want have the capability fork addressed by a stable id, matching how the coherence-fork mechanism already works,
so that sign-off parsing doesn't silently target the wrong fork when ordering shifts across M-cycle re-runs.

## Description

The capability fork is addressed positionally ('Fork 1') in workflow.md and plan-gate-renderer.md, while the coherence-fork mechanism uses stable ids specifically because fork order shifts across M-cycle re-runs. This is a real divergence between the two mechanisms, not a stylistic inconsistency — positional addressing under an M-cycle re-run risks a sign-off decision landing on the wrong fork. Reworking the sign-off parsing contract to use stable ids for the capability fork is a follow-up story.

**Pain context:** Surfaced by code-review triage during sprint-2026-08-03 build wave (goal-conditions story) as a real mechanism divergence, flagged for a follow-up story rather than in-scope fix.

**Source:** triage — Conductor build wave sprint-2026-08-03 (goal-conditions)

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- [ ] Capability fork gains a stable id assigned at creation, independent of display order
- [ ] workflow.md and plan-gate-renderer.md updated to address the capability fork by stable id
- [ ] Sign-off parsing updated to resolve by id, not position
- [ ] Behavior verified across an M-cycle re-run where fork order shifts

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
