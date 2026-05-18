---
title: "sprint-manager frozen-scope enforcement — subtract-only + scope_guard"
story_key: sprint-manager-frozen-scope-enforcement
status: backlog
epic_slug: impetus-sprint-orchestrator
feature_slug: momentum-sprint-orchestration
story_type: feature
depends_on: []
touches: []
---

# sprint-manager frozen-scope enforcement — subtract-only + scope_guard

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to add subtract-only scope_guard to sprint-manager that enforces the frozen-scope invariant at every status transition,
so that sprint scope cannot silently expand mid-sprint, and ambiguous changes drop cleanly to next planning cycle without human interruption.

## Description

At sprint_activate, sprint-manager captures a frozen-scope manifest (per-story AC hash, contract hash, change_type, touches_root) into sprints/index.json. During the active sprint: (1) sprint_plan add is unconditionally rejected — adds are forbidden; (2) any status_transition on a member story runs scope_guard first — recomputes AC hash / change_type / touches against the frozen manifest; if the frozen contract no longer verifies byte-identically, the transition is rejected and the story drops from the sprint (subtract is always allowed). Fail-closed: no mid-sprint human escalation — ambiguous cases drop and re-enter the next planning cycle via discovered-from lineage. Source: DEC-030 D3, Gate 2 ratified and amended (dec-030-blast-radius-discovery-2026-05-17.md §4).

**Pain context:** Without scope enforcement, sprints silently expand mid-execution. DEC-030 D3 defines the subtract-only invariant. Gate 2 ratified with amendment: no mid-sprint human-in-the-loop. Critical for frozen-scope sprint model.

**Proposed depends_on:** sprint_activate must support writing the frozen manifest (may require sprint-planning changes).

**Source:** triage — DEC-030 blast-radius discovery

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- sprint_activate writes frozen manifest to sprints/index.json for each member story
- sprint_plan add on an active sprint returns an error with no side effects
- scope_guard at status_transition recomputes AC hash and compares to frozen manifest
- byte-identical verification → MODIFY accepted; hash change → story dropped from sprint (subtract always allowed)
- no developer escalation — fail-closed deterministic
- dropped story carries discovered-from lineage for next planning cycle

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
