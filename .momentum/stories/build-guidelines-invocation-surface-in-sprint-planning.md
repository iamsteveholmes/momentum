---
title: Build-guidelines invocation surface in sprint-planning
story_key: build-guidelines-invocation-surface-in-sprint-planning
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: feature
depends_on: []
touches: []
---

# Build-guidelines invocation surface in sprint-planning

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want sprint-planning's missing-guidelines prompt to offer /momentum:build-guidelines (gen-2) instead of /momentum:agent-guidelines (gen-1),
so that the planning phase drives developers to the correct skill when composed specialist files are absent.

## Description

Update sprint-planning's missing-guidelines prompt to offer /momentum:build-guidelines (gen-2) rather than /momentum:agent-guidelines (gen-1) when the verification gate fires. The planning phase is the natural trigger for build-guidelines; the prompt currently points at the wrong skill.

**Pain context:** When the guidelines-verification-gate fires during sprint-planning and alerts the developer that composed specialist files are missing, the prompt suggests /momentum:agent-guidelines — the gen-1 skill that generates rules/ entries rather than composed agent files. This sends developers down the wrong path and will not produce the .claude/guidelines/agents/ files that gen-2 requires.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- The missing-guidelines prompt in sprint-planning references /momentum:build-guidelines when composed files are absent
- /momentum:agent-guidelines is not offered or mentioned when the gen-2 gate fires
- The prompt clearly communicates what build-guidelines will produce and why it is needed
- Sprint-planning workflow.md documents the updated prompt language

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
