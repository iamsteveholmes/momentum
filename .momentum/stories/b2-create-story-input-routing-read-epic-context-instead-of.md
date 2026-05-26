---
title: "B2: create-story input-routing — read epic context instead of feature context"
story_key: b2-create-story-input-routing-read-epic-context-instead-of
status: backlog
epic_slug: ad-hoc
feature_slug:
story_type: practice
depends_on: ["B1"]
touches: []
---

# B2: create-story input-routing — read epic context instead of feature context

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want `momentum:create-story` to read epic context (from `epics.json`) instead of feature context (from the retired `features.json`),
so that story enrichment routes upstream context through the new epic-layer model defined in DEC-034.

## Description

Update `momentum:create-story` to read epic context (from new `epics.json`) instead of feature context (from retired `features.json`). The skill's input-routing logic for upstream context — currently looks up the story's feature_slug to find feature value_analysis/system_context/acceptance_conditions — needs to change to look up the story's epic_slug. The change_type-aware context injection that pulls from decisions/architecture/PRD for the right story type remains the same. Update SKILL.md + workflow.md. Effort: 2–3 hours. Change type: skill-instruction. Verification: EDD eval (run create-story against an epic-homed story stub; verify epic context is injected).

**Source:** triage — handoff practice-ledger-and-epic-cascade-stories-2026-05-25

**Pain context:** Skill update per DEC-034 D6. Depends on B1's new epics.json source.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- create-story reads epic context from `epics.json` keyed by the story's `epic_slug` (not feature context from `features.json`)
- Upstream context injected during enrichment includes the epic's value_analysis / system_context / acceptance_conditions equivalents from the epic record
- change_type-aware context injection (decisions / architecture / PRD by story type) is preserved unchanged
- Both `SKILL.md` and `workflow.md` for `momentum:create-story` are updated to reflect epic-based input routing
- EDD eval: run create-story against an epic-homed story stub and verify epic context is injected into the enriched story
- Depends on B1 landing first (the story that produces the new `epics.json` source)

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
