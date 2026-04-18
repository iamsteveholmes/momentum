---
title: e2e-validator and qa-reviewer — branch standalone vs teammate mode
story_key: e2e-and-qa-validator-prompts-branch-standalone-vs-team
status: backlog
epic_slug: agent-team-model
feature_slug: 
story_type: practice
depends_on: []
touches: []
---

# e2e-validator and qa-reviewer — branch standalone vs teammate mode

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want e2e-validator and qa-reviewer to detect whether they are running standalone or as a teammate and adjust their tool usage accordingly,
so that turns are not wasted on ToolSearch/SendMessage calls when these agents are spawned outside a team context.

## Description

Add conditional branch to e2e-validator.md and qa-reviewer.md prompt templates matching the team-communication.md pattern ('these rules apply ONLY when you are a teammate'). When spawned standalone, skip ToolSearch/SendMessage and use only return-value output. Touches: skills/momentum/agents/e2e-validator.md, skills/momentum/agents/qa-reviewer.md.

**Pain context:** auditor-execution E7 from nornspun sprint-2026-04-12 retro. ~20 turns wasted across two agents on ToolSearch/SendMessage attempts when they were running standalone, not as teammates. Signal type: Instruction. Source: triage — nornspun sprint-2026-04-12 retro handoff.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Both e2e-validator.md and qa-reviewer.md contain a conditional branch matching the team-communication.md pattern
- When spawned standalone (no team context), agents skip ToolSearch and SendMessage entirely
- When spawned as a teammate, existing team communication behavior is preserved
- No wasted turns on ToolSearch/SendMessage when agents run outside a team

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
