---
title: Sprint-dev composed-file spawn wiring
story_key: sprint-dev-composed-file-spawn-wiring
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: feature
depends_on: []
touches: []
---

# Sprint-dev composed-file spawn wiring

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want sprint-dev Phase 2 to spawn subagents from .claude/guidelines/agents/{role}-{domain}.md with documented fallback behavior,
so that composed specialist agents are actually used during sprint execution.

## Description

Update sprint-dev Phase 2 to spawn subagents from .claude/guidelines/agents/{role}-{domain}.md (gen-2 composed path) with documented fallback behavior when a composed file is absent. Core integration point that makes composed agents actually reach sprint execution.

**Pain context:** sprint-dev currently spawns subagents from the plugin agents directory (gen-1 path). Without wiring it to the gen-2 composed path, composed specialists built by build-guidelines will never be used — they exist on disk but are never loaded during sprint execution. This is the critical integration point.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- sprint-dev Phase 2 resolves subagent bodies from .claude/guidelines/agents/{role}-{domain}.md
- When a composed file exists, it is used as the subagent body for that role+domain
- When a composed file is absent, fallback behavior is documented and implemented (e.g., fall back to plugin base body or warn and skip)
- The fallback behavior is logged/surfaced so the developer knows composition is incomplete
- sprint-dev workflow.md documents the gen-2 spawn path and fallback

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
