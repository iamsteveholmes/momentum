---
title: Re-benchmark AVFL model tiers on Claude 5.5 family
story_key: rebenchmark-avfl-model-tiers-on-claude-5-5-family
status: backlog
epic_slug: momentum-quality-gates-enforced
feature_slug: 
story_type: maintenance
depends_on: []
touches: []
---

# Re-benchmark AVFL model tiers on Claude 5.5 family

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want AVFL's model-tier guidance re-derived from a multi-trial benchmark on Haiku 5.5, Sonnet 5.5 and Opus 5.5,
so that orchestrators pick the cheapest model that actually holds quality for each AVFL role, instead of following 4.x-era guesses.

## Description

Plugin 0.35.0 (2026-11-07) removed all hard-coded model pins; orchestrators now choose models at spawn time, guided by tier hints in skills/avfl/SKILL.md and workflow-merge-review.md ("avoid the cheapest tier for enumerators", "avoid mid-tier for the adversary"). Those hints rest on a single-trial March 2026 benchmark (avfl-workspace phases: lens count, model per role, effort) on 4.x-era models (Haiku 4.5, Sonnet 4.6, Opus 4.6). Steve kept the hints for now but noted: "it's not clear that Haiku 5.5 isn't capable... we might find situations where it SHOULD use Haiku." Scope: re-run the AVFL benchmark phases on the 5.5 family with multiple trials per cell, then update the tier hints to match current evidence.

**Pain context:** Stale model guidance silently degraded AVFL before (4.x pins persisted into the 5.x era; latest two AVFL-on-merge runs NON_CONVERGENT). Single-trial evidence is weak; cost matters now that unpinned agents inherit the session model. Source: Momentum pivot audit session 2026-11-07.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- AVFL benchmark phases (lens count, model per role, effort) re-run on Haiku 5.5 / Sonnet 5.5 / Opus 5.5
- At least 3 trials per cell; report variance, not single scores
- Cost and time per configuration recorded alongside quality
- Tier hints in skills/avfl/SKILL.md and workflow-merge-review.md updated (or removed) to match results, citing the new benchmark
- Explicit answer to whether Haiku 5.5 is adequate for any AVFL role

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
