---
title: "distill fixture: correct layer targeting"
story_key: distill-fixture-correct-layer-targeting
status: backlog
epic_slug: epic-9-performance-validation
feature_slug: momentum-practice-distillation
story_type: practice
depends_on: []
touches: []
---

# distill fixture: correct layer targeting

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a behavioral micro-eval fixture that verifies momentum:distill patches the correct artifact layer for a given finding,
so that agent-level findings patch the agent definition (not a rule file) and rule-level findings patch the rule (not the agent), preventing wrong-layer fixes that miss scope.

## Description

Build a behavioral micro-eval fixture that verifies momentum:distill patches the correct artifact layer — agent-level findings patch the agent definition file, not the rule file (and vice versa). Catches wrong-layer fixes that miss scope.

**Pain context:** Wrong-layer fixes are insidious — the patch lands, the test passes, but the actual scope of the failure is missed (agent-only fix when it should be a global rule, or vice versa). Distill needs an executable assertion that layer targeting is correct.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Fixture provides labeled findings tagged with their correct target layer (rule / agent / skill / template / hook)
- Fixture asserts that distill's chosen patch target matches the labeled layer for each finding
- Fixture covers at least the rule-vs-agent confusion case explicitly (the most common wrong-layer failure)
- Fixture follows the probabilistic-assertion / YAML-schema / lifecycle-states pattern
- Fixture fails with a diff showing chosen layer vs. expected layer

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
