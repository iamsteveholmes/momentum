---
title: track-errors-per-turn-as-decomposition-signal
story_key: track-errors-per-turn-as-decomposition-signal
status: backlog
epic_slug: impetus-sprint-orchestrator
feature_slug: momentum-sprint-retro
story_type: feature
depends_on: []
touches: []
---

# track-errors-per-turn-as-decomposition-signal

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want errors-per-turn ratio tracked per agent in retro DuckDB transcript analysis and surfaced as a decomposition recommendation when the threshold is exceeded,
so that sprint retrospectives automatically flag scope creep before it accumulates across future sprints.

## Description

Add errors-per-turn ratio as a decomposition signal in retro auditor-execution analysis. When an agent exceeds a threshold (suggested: >2 errors per 10 turns), the auditor should surface a decomposition recommendation in the retro findings. High error concentration in top-turn agents signals scope creep. In sprint-2026-05-03, high error concentration was observed.

The metric should be:
1. Computed per-agent in the retro DuckDB transcript analysis
2. Surfaced as a Tier 2 finding when threshold is exceeded
3. Included in the sprint efficiency summary

**Pain context:** sprint-2026-05-03 surfaced high error concentration in top-turn agents — a clear scope creep signal that the retro auditor did not automatically detect or recommend decomposition for. Without this metric, the pattern will recur unnoticed. Source: triage queue handoff sprint-2026-05-03.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- The retro DuckDB transcript analysis computes errors-per-turn ratio for each agent
- An agent with >2 errors per 10 turns triggers a Tier 2 decomposition recommendation in retro findings
- The decomposition recommendation names the specific agent and its error ratio
- The sprint efficiency summary section includes the errors-per-turn metric for all agents analyzed
- The threshold (>2 per 10 turns) is configurable or clearly documented

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
