---
title: Dev Agent Executor Not Decider — Orchestrator Decides, Agent Implements
story_key: dev-agent-executor-not-decider
status: backlog
epic_slug: agent-team-model
depends_on: []
touches: []
---

# Dev Agent Executor Not Decider — Orchestrator Decides, Agent Implements

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a sprint orchestrator,
I want receive dev agents that execute a clearly defined specification without making architectural decisions or scope expansions,
so that scope creep and unexpected behavior from dev agents is eliminated — agents implement what they're told, nothing more.

## Description

Dev agents currently make implementation decisions that should belong to the orchestrator: adding features not in the story, choosing different patterns, expanding scope. The dev agent's role is pure executor: receive a spec, implement exactly what's specified, report done. Architectural choices belong to create-story and the orchestrator.

**Pain context:** Nornspun upstream #9 (Medium). Dev agents expanded scope without authorization on 3 occasions. User corrections were needed. The orchestrator purity principle covers the orchestrator side — this covers the dev agent side.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Dev agent definition explicitly states: 'implement what the story specifies — no additions, no interpretations'
- Dev agent definition includes examples of what NOT to do: adding error handling not in ACs, choosing patterns not in Dev Notes
- Dev agent raises a clarification question if spec is ambiguous rather than guessing
- Eval demonstrates agent implementing spec exactly as written without additions

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
