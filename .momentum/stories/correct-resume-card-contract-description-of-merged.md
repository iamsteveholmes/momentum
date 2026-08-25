---
title: Correct resume-card contract description of merged/blocked count source
story_key: correct-resume-card-contract-description-of-merged
status: backlog
epic_slug: ad-hoc
feature_slug:
story_type: maintenance
depends_on: []
touches: []
---

# Correct resume-card contract description of merged/blocked count source

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want have resume-card.md's contract text accurately describe where merged/blocked counts come from,
so that a future implementer doesn't read the contract literally and add a redundant, wasteful re-read of the build ledger.

## Description

skills/momentum/skills/conductor/references/resume-card.md's contract text says merged/blocked counts come "from the build ledger... never an in-context accumulator," but every actual write site uses the rehydrated {{merged}}/{{blocked}} accumulators. The contract description is imprecise/inaccurate and could mislead an implementer into adding a redundant ledger re-read that doesn't match current behavior. Fix the prose to describe the actual accumulator-based mechanism (or, if the ledger-sourcing language reflects an intended-but-unimplemented invariant, reconcile the two explicitly).

**Pain context:** Surfaced by code-review triage during sprint-2026-08-03 build wave (resume-card story) as a documentation-accuracy gap, not a behavioral bug.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- [ ] resume-card.md contract prose reviewed against actual write-site implementation
- [ ] Prose corrected to match implementation (rehydrated accumulators), or implementation/contract intentionally reconciled with a documented rationale
- [ ] No behavior change to resume-card write sites unless the reconciliation calls for it

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
