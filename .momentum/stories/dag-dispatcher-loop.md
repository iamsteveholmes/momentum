---
title: "DAG dispatcher loop — continuous claim from bd ready-set"
story_key: dag-dispatcher-loop
status: backlog
epic_slug: sprint-execution-workflow
feature_slug: momentum-sprint-orchestration
story_type: feature
depends_on: []
touches: []
---

# DAG dispatcher loop — continuous claim from bd ready-set

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to replace the wave-barrier fan-out in sprint-dev with a continuous bd-ready claim loop,
so that a slow story no longer blocks the entire sprint wave, and parallelism becomes structural not manual.

## Description

New sprint-dev execution model replacing barrier-synchronized wave fan-out. The in-session orchestrator continuously polls `bd ready ∩ frozen-sprint-set`, dispatches dev agents as beads become ready, unblocks dependents on completion, and never waits at a wave barrier. No wave-assignment field needed — dependency ordering is runtime-computed from the DAG. Sources: DEC-030 D1 (ratified Gate 1), dec-030-blast-radius-discovery-2026-05-17.md §3.

**Pain context:** Current wave-barrier fan-out freezes the entire sprint on a single slow story. DEC-030 D1 ratified in-session loop as the dispatch host. Urgency: blocks DAG-driven sprint model.

**Proposed dependency:** DEC-028 beads spike verdict (Gate 3 — bd ready predicate requires beads adoption or fallback)

**Source:** triage — DEC-030 blast-radius discovery

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- sprint-dev polls bd ready filtered to frozen sprint set
- each ready bead is atomically claimed before spawning a dev agent
- on agent completion, bd update closes the bead and dependents become ready
- no wave barrier exists — dispatch fires whenever bd ready is non-empty
- orchestrator crash recovery resumes from beads + worktree state without double-dispatch

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
