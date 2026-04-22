---
title: "decision fixture: SDR cites source research"
story_key: decision-fixture-sdr-cites-source-research
status: backlog
epic_slug: epic-5-trust-artifact-provenance
feature_slug: momentum-assessment-decision-pipeline
story_type: practice
depends_on: []
touches: []
---

# decision fixture: SDR cites source research

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a behavioral micro-eval fixture that verifies every momentum:decision document includes a populated `source_research:` array in frontmatter referencing the document(s) that produced the recommendation,
so that no decision document is unanchored from the research it was supposed to be grounded in.

## Description

Build a behavioral micro-eval fixture that verifies every momentum:decision SDR includes a populated `source_research:` array in frontmatter referencing the document that produced the recommendation. Catches unanchored decisions.

(Note: per developer terminology preference, "decision document" is used in narrative; the `source_research` frontmatter key is the structured field being asserted on.)

**Pain context:** Decision documents that don't cite their source research are detached recommendations — there's no way to audit why the decision was made or to re-evaluate when the source research changes. Provenance chain integrity needs an executable assertion at the decision layer.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Fixture parses the frontmatter of every momentum:decision output document
- Fixture asserts the presence of a `source_research:` key in frontmatter
- Fixture asserts that `source_research:` is a non-empty array
- Fixture asserts each entry resolves to an existing research artifact path
- Fixture follows the probabilistic-assertion / YAML-schema / lifecycle-states pattern
- Fixture fails with a list of decision documents that lack populated source_research and the suggested research artifacts they could cite

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

No technical analysis has been performed. The following sub-sections are all stubs.

### Architecture Compliance

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- _bmad-output/research/forgecode-agentic-tools-eval-2026-04-21/analysis/retro-microeval-loop-analysis-2026-04-21.md
- Triage source: triage — conversation

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
