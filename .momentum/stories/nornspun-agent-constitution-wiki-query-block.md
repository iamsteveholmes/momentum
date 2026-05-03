---
title: "Add Wiki-Query Interface Block to Nornspun Agent Constitution (Tier 1)"
story_key: nornspun-agent-constitution-wiki-query-block
status: backlog
epic_slug: agent-team-model
feature_slug: ""
story_type: feature
depends_on: []
touches: []
---

# Add Wiki-Query Interface Block to Nornspun Agent Constitution (Tier 1)

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the nornspun agent constitution to include the canonical wiki-query interface block (both modes, exact syntax) as part of its Tier 1 hot-context delivery,
so that every nornspun agent has cold KB access baked in from the moment the constitution is built.

## Description

The existing backlog story `nornspun-agent-constitution` ("Build Nornspun Agent Constitution (Tier 1 Hot Context)") needs its scope extended: when the nornspun agent constitution is authored, it must include the canonical wiki-query interface block — the same block that DEC-018 Phase 2 adds to the Momentum constitution — verbatim, not a nornspun-specific variant.

The block must cover both modes (fast index-only and full-body query) with exact syntax, so that nornspun agents can query the cold KB without leaving hot context.

Source decision: DEC-018 (`dec-018-wiki-skills-replace-kb-stories-query-interface-2026-05-03.md`).

**Pain context:** Without this, the nornspun agent constitution would be built without KB access baked in, requiring a follow-up patch after DEC-018 Phase 2 is merged. Including it in Tier 1 delivery avoids drift and ensures nornspun agents ship with complete cold-KB access from day one. The wiki-query block is already being canonicalized by DEC-018 for the Momentum constitution — it is low-effort to include the identical block in the nornspun constitution at build time.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- The nornspun agent constitution includes the wiki-query interface block at Tier 1 (hot context)
- The block is identical to the canonical block added to the Momentum constitution by DEC-018 Phase 2 — not a nornspun-specific variant
- Both query modes are present: fast index-only mode and full-body query mode, with exact syntax
- The constitution build story (`nornspun-agent-constitution`) references or supersedes this story so the two are not implemented in isolation
- The wiki-query block is placed in the constitution such that every nornspun agent receives it in their loaded hot context

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

- Source decision: DEC-018 — `_bmad-output/planning-artifacts/decisions/dec-018-wiki-skills-replace-kb-stories-query-interface-2026-05-03.md`
- Related story: `nornspun-agent-constitution` (the parent story this extends)

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
