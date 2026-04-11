---
title: Fan-Out Agent Prompt Fix — Return Report as Final Response, Not SendMessage
story_key: fan-out-agent-prompt-fix
status: backlog
epic_slug: agent-team-model
depends_on: []
touches: []
---

# Fan-Out Agent Prompt Fix — Return Report as Final Response, Not SendMessage

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a sprint orchestrator,
I want receive agent findings as the final response message, not via SendMessage, in fan-out spawning contexts,
so that 2-4 wasted turns per validator eliminated — agents don't burn a turn trying to use SendMessage before discovering they should just return.

## Description

Fan-out agents (individual Agent spawns, no TeamCreate) frequently emit SendMessage calls that fail or are ignored, then recover and return their result as the final response. The spawn prompt should explicitly say 'return your findings as the final response — do not use SendMessage' for fan-out contexts.

**Pain context:** Sprint-2026-04-08 retro (#8), sprint-2026-04-06-2 (#7). Recurring 1-2 wasted turns per agent in every fan-out wave. At 10-20 agents per sprint, this compounds.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Fan-out spawn prompts include explicit instruction: 'return findings as final response — SendMessage is not available'
- spawning-patterns.md documents this requirement in the fan-out section
- E2E validator and QA reviewer spawn prompts updated
- Zero SendMessage calls from fan-out agents in eval runs

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
