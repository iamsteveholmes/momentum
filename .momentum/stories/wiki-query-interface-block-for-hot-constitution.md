---
title: Wiki-Query Interface Block for Hot Constitution
story_key: wiki-query-interface-block-for-hot-constitution
status: backlog
epic_slug: agent-team-model
feature_slug: 
story_type: feature
depends_on: []
touches: []
---

# Wiki-Query Interface Block for Hot Constitution

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the hot constitution (constitution.md) to include a wiki-query interface block documenting both invocation modes with exact agent syntax and prescriptive trigger scenarios,
so that every agent always knows when and how to query the KB without relying on memory or inference.

## Description

The constitution (constitution.md) is Tier 1 hot context — it is always loaded for every agent in every session. Adding a wiki-query interface block here guarantees that KB query behavior is universally available and consistently applied across all agents.

The block must document both wiki-query modes:
- **Normal mode:** `wiki-query [question]` — tiered retrieval (index scan → section grep → full page read), returns cited answers with wikilinks
- **Fast/index-only mode:** `wiki-query quick answer: [question]` — index-only, no page bodies, cheaper and faster. Also triggered by prefix variants: "just scan:", "don't read the pages:", "fast lookup:"

The block must also include **prescriptive trigger language** — not permissive "if you need" phrasing, but specific named scenarios where KB lookup is required before proceeding. The goal is deterministic agent behavior: agents don't decide whether to query, they follow a trigger list.

This is DEC-018 Phase 2. Phase 1 established the wiki-skills architecture; Phase 2 ensures agents actually use it via Tier 1 hot context injection.

**Source decision:** DEC-018 — `dec-018-wiki-skills-replace-kb-stories-query-interface-2026-05-03.md`

**Related stories:** `build-guidelines-skill`, `constitutionmd-generation-acceptance-criteria`

**Pain context:** Without this block in the constitution, agents rely on their own judgment about when and how to query the KB. This produces inconsistent behavior — some agents query, some don't; normal vs fast mode is chosen arbitrarily. Placing the interface spec in Tier 1 hot context eliminates the judgment call and makes KB usage deterministic and auditable.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- constitution.md contains a dedicated wiki-query interface block
- Block documents normal mode: `wiki-query [question]` with description of tiered retrieval (index scan → section grep → full page read) and cited wikilink output
- Block documents fast mode: `wiki-query quick answer: [question]` with description of index-only behavior, cost advantage, and all trigger prefixes ("just scan:", "don't read the pages:", "fast lookup:")
- Block includes prescriptive trigger language — specific named scenarios where KB lookup is required before proceeding (not "if you need" phrasing)
- Trigger scenarios are written as imperatives, not suggestions
- Block is placed in constitution.md such that it is loaded as Tier 1 hot context for every agent
- Existing constitutionmd-generation-acceptance-criteria story ACs remain consistent with this addition (no conflict)

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

- Source decision: `_bmad-output/planning-artifacts/decisions/dec-018-wiki-skills-replace-kb-stories-query-interface-2026-05-03.md`
- Related: `.momentum/stories/build-guidelines-skill.md`
- Related: `.momentum/stories/constitutionmd-generation-acceptance-criteria.md`

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
