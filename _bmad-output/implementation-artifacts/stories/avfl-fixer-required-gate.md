---
title: AVFL Fixer Agent Required Alongside Validators — No Validation Without Fix Capability
story_key: avfl-fixer-required-gate
status: backlog
epic_slug: quality-enforcement
depends_on: []
touches: []
---

# AVFL Fixer Agent Required Alongside Validators — No Validation Without Fix Capability

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a AVFL orchestrator,
I want require a fixer agent to be present alongside every AVFL validator team — validation without fix path is disallowed,
so that findings don't pile up without resolution — every identified issue has an assigned fix path from the start.

## Description

AVFL validator agents run and produce findings but the fixer is optional. In practice, orchestrators forget to include the fixer, and findings accumulate without resolution. The fixer should be a mandatory team member in every AVFL invocation except scan-only profiles explicitly marked as discovery-only.

**Pain context:** Sprint-2026-04-06-2 (#3). AVFL team was composed without fixer twice in the same session. User had to micromanage team composition. The spawning-patterns.md rule helps but doesn't gate the AVFL invocation itself.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- AVFL workflow validates that a fixer agent is included unless profile is explicitly scan/discovery-only
- Missing fixer in non-scan context raises a composition error before spawning
- AVFL SKILL.md documents fixer-required contract
- Scan profile documentation explicitly notes it is the only profile that may omit fixer

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
