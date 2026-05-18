---
title: "Epic+feature collapse — one closeable M:N value-grouping with acceptance_condition + discovered-from"
story_key: epic-feature-collapse-closeable-grouping
status: backlog
epic_slug: feature-orientation
feature_slug: momentum-feature-taxonomy-maintenance
story_type: feature
depends_on: []
touches: []
---

# Epic+feature collapse — one closeable M:N value-grouping with acceptance_condition + discovered-from

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to collapse the epic and feature taxonomy into a single closeable M:N value-grouping artifact with acceptance_condition and discovered-from,
so that value containers have explicit closure semantics and mid-sprint discovered work has traceable lineage back to its origin.

## Description

Collapse the current two-orthogonal-dimension epic/feature taxonomy into one closeable M:N value-grouping. Each grouping has: an acceptance_condition (when is this group done?), a discovered-from field (birth model for mid-sprint discovered work), and M:N relationship to stories (a story can belong to multiple groupings; a grouping can contain many stories). The two-dimensional model (epic as long-lived category × feature as capability) is replaced by one kind of artifact with explicit closure semantics. Value fields from the current feature model (value_analysis, system_context, acceptance_conditions) survive. Blast-radius: touches done stories feature-artifact-schema, feature-grooming, epic-grooming — a blast-radius review pass is required before this story enters sprint-planning. Source: DEC-030 D2.

**Pain context:** Two-dimensional taxonomy creates containers that never close — the sprint-dev frankenstein problem (6 stories → 20 story sprint scope creep). DEC-030 D2 adopts the single closeable value-grouping. Urgency: this is load-bearing for the DAG dispatch model.

**Proposed depends_on:** dag-dispatcher-loop (discovered-from origin captured at dispatch), sprint-manager-frozen-scope-enforcement (scope_guard uses frozen contract)

**Source:** triage — DEC-030 blast-radius discovery

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- (1) A single grouping artifact type replaces the epic/feature distinction
- (2) Each grouping has acceptance_condition (observable closure criteria) and discovered-from (nullable — set when born mid-sprint)
- (3) M:N: a story can belong to multiple groupings; a grouping can contain many stories
- (4) Existing value_analysis, system_context, acceptance_conditions fields survive in the new schema
- (5) features.json schema updated to reflect the new model
- (6) Blast-radius review of feature-artifact-schema, feature-grooming, epic-grooming done stories completed before sprint entry

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
