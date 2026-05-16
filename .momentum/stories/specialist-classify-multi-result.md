---
title: specialist-classify-multi-result
story_key: specialist-classify-multi-result
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-agent-composition-pipeline
story_type: maintenance
depends_on: [routing-table-schema-and-implementation]
touches: []
---

# specialist-classify-multi-result

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the specialist-classify command to return an array of `{slug, agent_path, file_scope}` objects instead of a single string,
so that routing-table-driven resolution can correctly handle files that touch multiple agents with overlapping scopes.

## Description

Rework the `momentum-tools specialist-classify` command to return an array of `{slug, agent_path, file_scope}` instead of a single string. Required for routing-table-driven resolution where a single file touch may involve multiple agents with overlapping scopes. Per DEC-023. The current single-string return value cannot represent multi-agent matches. Update all callers that consume the `specialist-classify` output to handle the array result.

**Pain context:** The current single-string return from `specialist-classify` is a blocking limitation for the routing-table redesign (DEC-023). Without multi-result support, the routing table cannot correctly dispatch stories that span agent boundaries — any multi-agent file overlap silently drops all but one agent match. This was identified during the agent architecture triage (2026-05-16) as a prerequisite for the full agent-team-model epic to function correctly.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- `specialist-classify` returns an array (not a string) even when only one agent matches
- Each array element has the shape `{slug, agent_path, file_scope}`
- When a file matches multiple agent scopes, all matching agents are returned
- All callers of `specialist-classify` are updated to consume the array result without breaking
- Existing single-agent routing behavior is preserved (no regression)
- Depends on `routing-table-schema-and-implementation` being merged first (DEC-023 routing table schema must be in place)

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

- Source: triage — handoff `agent-architecture-triage-2026-05-16.md` (DEC-023)

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
