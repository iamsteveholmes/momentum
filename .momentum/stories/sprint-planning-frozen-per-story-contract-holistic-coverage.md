---
title: "sprint-planning: frozen per-story contract, holistic coverage plan, adversarial guard"
story_key: sprint-planning-frozen-per-story-contract-holistic-coverage
status: backlog
epic_slug: sprint-dev-workflow
feature_slug: momentum-sprint-planning-to-ready
story_type: practice
depends_on: []
touches: []
---

# sprint-planning: frozen per-story contract, holistic coverage plan, adversarial guard

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want sprint-planning that freezes a per-story verification contract, builds a sprint-wide coverage plan, and adversarially guards the contracts,
so that each story has an immutable spec-of-done and the sprint has non-redundant transitive E2E coverage that cannot be gamed by insider knowledge.

## Description

Extend momentum:sprint-planning to author (a) the frozen method-polymorphic per-story contract written to .momentum/sprints/{slug}/specs/ as the spec-of-done, AND (b) the per-sprint holistic E2E coverage plan (scenario → story/file span map, transitive coverage, anti-redundancy), AND (c) run the adversarial anti-insider-knowledge guard over the authored contracts. (DEC-029 D2/D6/D8.)

**Pain context:** Source: DEC-029 (_bmad-output/planning-artifacts/decisions/dec-029-method-routed-acceptance-validation-pipeline-2026-05-17.md), decisions D2/D6/D8. Consumes the enforced verification rule and momentum/harness.json. Phase 1 gated on routing-table-schema-and-implementation landing momentum/agents.json (DEC-029 Gate 1).

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- frozen method-polymorphic per-story contract written to .momentum/sprints/{slug}/specs/
- per-sprint coverage plan mapping scenario→story/file span with transitive coverage and anti-redundancy
- adversarial anti-insider-knowledge guard runs over authored contracts
- contract is the spec-of-done

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
