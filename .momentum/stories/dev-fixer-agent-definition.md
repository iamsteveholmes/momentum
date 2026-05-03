---
title: Dev Fixer Agent Definition — Sprint-Dev Fix Phase Base Body
story_key: dev-fixer-agent-definition
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: feature
depends_on: []
touches: []
---

# Dev Fixer Agent Definition — Sprint-Dev Fix Phase Base Body

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a dev-fixer.md base body in the plugin's agents directory,
so that the sprint-dev fix phase has a canonical spawnable agent definition for the fixer role, with support for multi-fixer configurations per DEC-016.

## Description

Create `skills/momentum/agents/dev-fixer.md` as the base role body for the dev-fixer agent used in sprint-dev Phase 4d (AVFL/code-review fix loop). The dev-fixer receives AVFL and code-review findings and implements targeted fixes. Per DEC-016, the dev-fixer slot supports N-instance cardinality — a project with backend and frontend can configure sprint-dev to spawn both a backend-fixer and client-fixer, each with different composed files. This base body is the default single-fixer implementation; project composition via build-guidelines enables multi-fixer topologies. The behavioral contract is critical: the fixer is a bounded executor that applies targeted fixes only — no scope expansion, no unsolicited refactoring.

**Pain context:** No dev-fixer.md exists. DEC-013 requires every spawned role to have a base body. The fixer role has emergent complexity in multi-stack projects and needs a well-defined behavioral contract (targeted executor, not autonomous developer) to prevent scope creep during fix passes.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- dev-fixer.md exists in skills/momentum/agents/
- The base body defines the fix-executor stance: targeted fixes only, no scope expansion
- sprint-dev Phase 4d references dev-fixer.md at spawn time
- The agents.md manifest for sprint-dev marks this slot as cardinality=N (project-configurable)
- A project with multiple stacks can configure stack-specific fixer variants via build-guidelines

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

No technical analysis has been performed. The following sub-sections are all stubs.

### Architecture Compliance

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

_DRAFT — requires rewrite via create-story before this story is dev-ready._

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
