---
title: AVFL Cross-Story Integration Lens — Validate Stories Don't Break Each Other
story_key: avfl-cross-story-integration-lens
status: backlog
epic_slug: quality-enforcement
depends_on: []
touches: []
---

# AVFL Cross-Story Integration Lens — Validate Stories Don't Break Each Other

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a AVFL validation,
I want run a cross-story integration lens that checks for interface conflicts, shared-file mutations, and contract violations between merged stories,
so that sprint-level integration failures caught before merge, not after — the entire sprint doesn't fail because two stories stepped on each other.

## Description

AVFL currently validates each story independently. It has no lens that checks cross-story integration: does story A's output contract match story B's expected input? Do two stories both write to the same file? Did a rename in story A orphan a reference in story B? This lens runs after all stories are merged and validates the combined result.

**Pain context:** Sprint-2026-04-08 retro (#5). Cross-story integration failures were identified but AVFL had no lens to catch them. These failures are expensive — discovered at sprint merge time after individual story validation passed.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- AVFL framework.json includes cross-story integration lens definition
- Lens checks: shared-file write conflicts, interface contract matches, rename-orphan detection
- Lens runs in corpus mode across all sprint story files
- Critical findings on cross-story conflicts block merge
- Sprint-dev workflow invokes cross-story lens as part of Phase 5 AVFL pass

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
