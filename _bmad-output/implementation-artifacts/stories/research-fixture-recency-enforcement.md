---
title: "research fixture: recency enforcement"
story_key: research-fixture-recency-enforcement
status: backlog
epic_slug: epic-9-performance-validation
feature_slug: momentum-deep-research-pipeline
story_type: practice
depends_on:
  - research-recency-enforcement-for-fast-moving-domains
touches: []
---

# research fixture: recency enforcement

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a behavioral micro-eval fixture that verifies momentum:research enforces date-bounded sources for fast-moving domain queries and rejects pre-cutoff hits,
so that stale recommendations (like the GLM-4.7-vs-5.1 oversight in this conversation) cannot leak into research artifacts.

## Description

Build a behavioral micro-eval fixture that verifies momentum:research enforces date-bounded sources for fast-moving domain queries (LLM models, agentic tools, etc.) and rejects pre-cutoff hits. Real failure mode: this conversation surfaced a GLM-4.7-vs-5.1 oversight where stale recommendations were emitted. Depends on (and validates) the existing story `research-recency-enforcement-for-fast-moving-domains`.

**Pain context:** Fast-moving domains (LLM models, agentic tools, frameworks) generate stale recommendations within months. The GLM-4.7-vs-5.1 oversight in this conversation is a concrete instance — a recency policy without an executable fixture is a guideline, not a gate. This fixture is the gate.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Fixture targets fast-moving-domain queries (LLM models, agentic tools, frameworks)
- Fixture asserts that all cited sources have a publication date within the configured recency window
- Fixture asserts that pre-cutoff hits are rejected (not just warned about)
- Fixture includes the GLM-4.7-vs-5.1 case as a regression test — a research run that should reject the stale GLM-4.7 source
- Fixture follows the probabilistic-assertion / YAML-schema / lifecycle-states pattern
- Fixture validates the implementation of the depended-on story (research-recency-enforcement-for-fast-moving-domains)

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
- Depends on: research-recency-enforcement-for-fast-moving-domains
- Triage source: triage — conversation

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
