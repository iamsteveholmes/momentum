---
title: Staleness detection mechanism for raw sources
story_key: staleness-detection-mechanism-for-raw-sources
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-practice-knowledge-base
story_type: feature
depends_on: []
touches: []
---

# Staleness detection mechanism for raw sources

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want kb-ingest to implement a staleness detection mechanism for raw sources,
so that stale vault content is surfaced before build-guidelines generates guidelines that cite outdated material.

## Description

Implement the staleness signal kb-ingest uses to surface stale vault content: lastVerified date, version pin, webhook trigger, or other mechanism. The acceptance condition implicitly requires guidelines cite current passages; without staleness detection the KB silently rots.

**Pain context:** Without staleness detection, the KB will degrade silently over time. build-guidelines citations may point to outdated vault pages with no signal to the agent or developer that the underlying source has changed. This is an invisible quality rot — the feature acceptance condition requires guidelines cite "current passages," which cannot be guaranteed without an active freshness signal.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- A staleness detection mechanism is implemented in kb-ingest (using lastVerified date, version pin, or equivalent signal)
- kb-ingest surfaces stale vault content to the developer when detected
- The mechanism is documented so that vault maintainers know how to keep content fresh
- build-guidelines can rely on the staleness signal when generating citations

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
