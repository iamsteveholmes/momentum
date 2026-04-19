---
title: Enforce parallel spawning for independent subagents
story_key: enforce-parallel-spawning-for-independent-subagents
status: backlog
epic_slug: agent-team-model
feature_slug:
story_type: practice
depends_on: []
touches: []
---

# Enforce parallel spawning for independent subagents

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want Momentum workflows to enforce parallel spawning when multiple independent subagents are invoked,
so that workflows don't degrade into slow sequential subagent runs when the spawning-patterns rule clearly calls for fan-out.

## Description

Add an explicit check in dev/research skills: before spawning N independent subagents, confirm parallel invocation (single message with N tool calls); log or warn on sequential fallback. Consider a pre-flight validation in momentum:avfl and momentum:research that enforces this. Touches: skills/momentum/skills/research/workflow.md, skills/momentum/skills/avfl/SKILL.md, skills/momentum/skills/dev/workflow.md, potentially skills/momentum/rules/spawning-patterns.md.

**Pain context:** auditor-human H29 ('Please fire up 9 subagents ALL AT ONCE IN PARALLEL.') from nornspun sprint-2026-04-12 retro. Signal type: Workflow.

Source: triage — nornspun sprint-2026-04-12 retro handoff.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Workflows that spawn N independent subagents (AVFL lenses, research queries, dev waves) contain an explicit pre-flight check that the spawn will occur as a single message with N parallel tool calls.
- Sequential subagent invocation for independent work is either prevented or produces a visible warning/log entry the developer can see.
- `momentum:avfl` and `momentum:research` enforce parallel fan-out at the pre-flight/spawn step.
- Relevant workflow files updated: `skills/momentum/skills/research/workflow.md`, `skills/momentum/skills/avfl/SKILL.md`, `skills/momentum/skills/dev/workflow.md`.
- `skills/momentum/rules/spawning-patterns.md` updated if enforcement language needs to tighten from "expected" to "required with check".
- Retro auditor pattern of requesting "ALL AT ONCE IN PARALLEL" for 9+ subagents no longer recurs in subsequent sprint retros.

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
