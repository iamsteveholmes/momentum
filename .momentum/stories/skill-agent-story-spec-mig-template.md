---
title: skill-agent-story-spec-mig-template
story_key: skill-agent-story-spec-mig-template
status: backlog
epic_slug: impetus-sprint-orchestrator
feature_slug: momentum-sprint-orchestration
story_type: feature
depends_on: [change-type-routing-in-sprint-dev]
touches: []
---

# skill-agent-story-spec-mig-template

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want create-story to inject MIG (Momentum Injection Guidance) template context when a story has change_type: skill or change_type: agent,
so that skill-creator is pre-briefed with the right architectural context and doesn't start cold on architecture-sensitive work.

## Description

Add MIG (Momentum Injection Guidance) template injection for change_type: skill and change_type: agent in create-story. When a story has change_type: skill or change_type: agent, create-story distills relevant constitution context (skill architecture, SKILL.md format, agent base body conventions, workflow.md patterns) into the spec so skill-creator is pre-briefed with the right architectural context when dev routes to it. Per DEC-027 D3. This prevents skill-creator from starting cold on architecture-sensitive work.

**Pain context:** skill-creator currently receives no architectural context when picked up by sprint-dev for skill/agent stories. It must reconstruct conventions from scratch each time, risking drift from the Momentum constitution. MIG injection at create-story time ensures the spec carries distilled guidance before dev begins. Source: triage — handoff agent-architecture-triage-2026-05-16.md (DEC-027 D3).

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- When create-story processes a story with change_type: skill, it injects a MIG block containing: SKILL.md format conventions, skill architecture patterns, workflow.md structure guidelines
- When create-story processes a story with change_type: agent, it injects a MIG block containing: agent base body conventions, agent manifest format, routing table conventions
- The injected MIG block appears in the Dev Notes / Implementation Guide section of the story spec
- MIG injection does not occur for other change_types (feature, maintenance, defect, etc.)
- skill-creator, when reading a story spec with MIG injection, uses the injected context to align with Momentum constitution without requiring additional lookups

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

- DEC-027 D3 — agent-architecture-triage-2026-05-16.md

_DRAFT — create-story will expand with additional source citations._

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
