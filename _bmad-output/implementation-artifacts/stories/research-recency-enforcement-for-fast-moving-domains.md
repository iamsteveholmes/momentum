---
title: Research recency enforcement for fast-moving domains
story_key: research-recency-enforcement-for-fast-moving-domains
status: backlog
epic_slug: research-knowledge
feature_slug: 
story_type: practice
depends_on: []
touches: []
---

# Research recency enforcement for fast-moving domains

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want research and AVFL corpus validation to enforce recency against live registries of truth for fast-moving domains (model catalogs, framework versions),
so that research outputs are provably current and I can trust the results without manually cross-referencing external sources.

## Description

Add a registry-of-truth pattern to momentum:research (openrouter.ai/models for model catalogs, official release feeds for framework versions). AVFL corpus validation must date-check entities in domains where a recency-of-truth URL exists. Touches: skills/momentum/skills/research/workflow.md, skills/momentum/skills/avfl/references/framework.json (corpus validators).

**Pain context:** auditor-human H16, H17 from nornspun sprint-2026-04-12 retro. Research returned 'GPT 4.1' when 5.4 is current and 'Gemini 2.5' when 3.1 is current. User: 'I find myself EXTREMELY skeptical of your results' and redirected to openrouter.ai/models as a live registry of truth. Signal type: Context. Source: triage — nornspun sprint-2026-04-12 retro handoff.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- When momentum:research runs in a domain with a registered recency-of-truth URL (e.g., model catalog), it fetches the live registry and cross-checks named entities (model names, versions) against it
- When AVFL corpus validation encounters named model or framework versions, it date-checks them against the registry-of-truth URL for that domain, if one exists
- A registry-of-truth index is maintained in skills/momentum/skills/avfl/references/framework.json (or equivalent) mapping domain → canonical URL
- openrouter.ai/models is registered as the canonical source of truth for AI model catalog
- Research outputs that cannot be verified against a live registry are flagged as unverified with explicit staleness risk noted
- The research workflow.md documents the registry-of-truth pattern and when it applies

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
