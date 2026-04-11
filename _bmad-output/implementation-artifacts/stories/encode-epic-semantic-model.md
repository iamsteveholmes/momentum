---
title: Encode Epic Semantic Model — Grooming and Refine Skills Know Epic Scope Boundaries
story_key: encode-epic-semantic-model
status: backlog
epic_slug: impetus-epic-orchestrator
depends_on: []
touches: []
---

# Encode Epic Semantic Model — Grooming and Refine Skills Know Epic Scope Boundaries

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a grooming/refine orchestrator,
I want find the epic semantic model (scope boundaries, purpose, what belongs vs what doesn't) encoded in grooming and refine skill references,
so that story assignment confusion and cross-epic misclassification are eliminated during grooming — agents know where things belong.

## Description

Epic grooming and backlog refine skills assign stories to epics but rely on LLM inference for scope boundaries. When epic scope is ambiguous (e.g., impetus-core vs impetus-epic-orchestrator), stories get misassigned. A canonical epic semantic model, loaded as a reference in grooming and refine workflows, would make assignment deterministic.

**Pain context:** Nornspun upstream #4 (High). Epic migration confusion during grooming. Developers spent time correcting misassignments. The taxonomy migration in this sprint exposed how fuzzy epic boundaries are without explicit scope definitions.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Epic semantic model document exists at references/epic-semantic-model.md
- Document describes each epic's purpose, what belongs, what explicitly doesn't
- Grooming and refine workflows load epic-semantic-model.md as a reference
- Epic assignment step cites the model when classifying stories
- At least 3 epics with historically ambiguous overlap are documented with disambiguation examples

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
