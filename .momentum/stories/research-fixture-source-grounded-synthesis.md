---
title: "research fixture: source-grounded synthesis"
story_key: research-fixture-source-grounded-synthesis
status: backlog
epic_slug: epic-5-trust-artifact-provenance
feature_slug: momentum-provenance-chain
story_type: practice
depends_on: []
touches: []
---

# research fixture: source-grounded synthesis

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a behavioral micro-eval fixture that verifies every synthesis claim in a research artifact traces back to a raw source file in the research bundle,
so that fabricated bridges (like the AA-Omniscience long-form risk profile from public benchmarks) cannot pass as grounded synthesis.

## Description

Build a behavioral micro-eval fixture that verifies every synthesis claim in a research artifact traces back to one of the raw source files in the research bundle. No source-less synthesis claims should pass. Catches fabricated bridges (the AA-Omniscience long-form risk profile from public benchmarks).

**Pain context:** Synthesis is where research goes off the rails — claims that "feel right" get bridged from sources that don't actually support them. The AA-Omniscience long-form risk profile fabricated from public benchmarks is the canonical example. Provenance chain integrity needs an executable assertion.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Fixture parses a research artifact's synthesis section and extracts each claim
- Fixture asserts that every claim has at least one citation pointing to a raw source file in the research bundle
- Fixture asserts that the cited source file actually supports the claim (or at minimum, that the citation resolves to extant text in the bundle)
- Fixture includes the AA-Omniscience case as a regression test — a synthesis that fabricates a long-form risk profile from non-supporting public benchmarks should fail
- Fixture follows the probabilistic-assertion / YAML-schema / lifecycle-states pattern
- Fixture fails with a list of unanchored claims and their best-match (or no-match) source candidates

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
