---
title: "intake fixture: provenance capture"
story_key: intake-fixture-provenance-capture
status: backlog
epic_slug: epic-6-the-practice-compounds
feature_slug: momentum-retro-and-flywheel
story_type: practice
depends_on: []
touches: []
---

# intake fixture: provenance capture

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the momentum:intake skill to capture full provenance (source transcript reference + raw quote + classifier hint) when capturing a story idea mid-conversation,
so that the captured stub preserves the context that triggered it and doesn't lose the "why" that only exists in the originating conversation.

## Description

Build a behavioral micro-eval fixture that verifies the momentum:intake skill captures full provenance (source transcript reference + raw quote + classifier hint) when capturing a story idea mid-conversation, not just the bullet text. Catches the "shallow stub" failure mode where context is lost. Part of the ForgeCode-style retro→micro-eval feedback loop. See _bmad-output/research/forgecode-agentic-tools-eval-2026-04-21/analysis/retro-microeval-loop-analysis-2026-04-21.md for the fixture pattern (probabilistic assertion, YAML schema, lifecycle states).

**Pain context:** Recurring "shallow stub" failure mode where intake captures bullet text but loses the conversational context that triggered the capture, forcing re-derivation (or worse, unanchored rewriting) when the story is later enriched. Part of the ForgeCode-style retro→micro-eval feedback loop that turns retro findings into executable fixtures.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Fixture asserts that a captured stub (or its index entry) references the originating transcript / session location
- Fixture asserts that a raw quote from the conversation is preserved verbatim in the stub
- Fixture asserts that a classifier hint (triage class, ARTIFACT type, etc.) is captured
- Fixture uses the probabilistic-assertion / YAML-schema / lifecycle-states fixture pattern from retro-microeval-loop-analysis-2026-04-21.md
- Fixture fails when intake emits only bullet text with no source reference

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

- _bmad-output/research/forgecode-agentic-tools-eval-2026-04-21/analysis/retro-microeval-loop-analysis-2026-04-21.md
- Triage source: triage — conversation

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
