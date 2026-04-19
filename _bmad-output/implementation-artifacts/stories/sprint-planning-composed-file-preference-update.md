---
title: Sprint-planning composed-file preference update
story_key: sprint-planning-composed-file-preference-update
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: maintenance
depends_on: []
touches: []
---

# Sprint-planning composed-file preference update

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want sprint-planning's guidelines-verification-gate and specialist-assignment logic updated to reference composed files in .claude/guidelines/agents/,
so that planning correctly detects and routes to gen-2 composed specialists rather than pre-shipped plugin agents.

## Description

Update sprint-planning guidelines-verification-gate and specialist-assignment logic to reference composed files in .claude/guidelines/agents/ instead of the plugin agents directory. The gate must detect missing composed files (not missing rules/ entries) and the assignment logic must route to the composed specialist, not the pre-shipped one.

**Pain context:** sprint-planning currently verifies guidelines by checking rules/ entries (gen-1 model). After the gen-2 model is in place, the gate will pass even when no composed specialists exist in .claude/guidelines/agents/, because it's checking the wrong location. This means planning will proceed with incorrect specialist assignments.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- guidelines-verification-gate checks for composed files in .claude/guidelines/agents/ (not rules/ entries)
- When composed files are absent, the gate fires and surfaces a prompt to run build-guidelines
- Specialist-assignment logic routes to the composed file path (.claude/guidelines/agents/{role}-{domain}.md)
- Pre-shipped plugin agent files are NOT used as the specialist source during planning
- Sprint-planning workflow.md documents the updated gate and assignment logic

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
