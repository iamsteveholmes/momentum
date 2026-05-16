---
title: analyst-base-body
story_key: analyst-base-body
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-agent-role-contracts
story_type: feature
depends_on: []
touches: []
---

# analyst-base-body

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a base body file for the analyst agent role (agents/analyst.md),
so that the Momentum plugin ships a universal unconditioned analyst agent that can be composed with project-specific context by the agent-composition-pipeline.

## Description

Create agents/analyst.md base body file — owns assessment records, analysis docs. Per DEC-020, analyst is one of the nine universal base bodies shipped in the Momentum plugin. Owns assessment documents, analysis artifacts, and business analysis deliverables. The base body defines the unconditioned analyst role; the agent-composition-pipeline adds project-specific context. BMAD role alignment: matches the analyst role. Document ownership: assessment records, analysis docs, requirements analysis.

**Pain context:** Per DEC-020, the nine universal base bodies are the foundation of the agent-team-model. Without this file the analyst role has no canonical definition and agent-composition-pipeline cannot produce a composed analyst agent for any project. Source: triage — handoff agent-architecture-triage-2026-05-16.md (DEC-020).

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- `agents/analyst.md` exists in the Momentum plugin module
- File defines the unconditioned analyst role (no project-specific context)
- Document ownership is declared: assessment records, analysis docs, requirements analysis
- BMAD role alignment to analyst role is documented in the file
- Agent-composition-pipeline can consume this base body to produce a project-specific composed analyst agent

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

- DEC-020: Agent taxonomy and universal base bodies
- handoff: agent-architecture-triage-2026-05-16.md

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
