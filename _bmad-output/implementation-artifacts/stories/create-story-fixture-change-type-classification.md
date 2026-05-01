---
title: "create-story fixture: change-type classification"
story_key: create-story-fixture-change-type-classification
status: backlog
epic_slug: epic-11-agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: practice
depends_on: []
touches: []
---

# create-story fixture: change-type classification

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a behavioral micro-eval fixture that verifies momentum:create-story picks the correct change-type (UI vs build vs skills vs general dev) for a given story,
so that sprint-dev dispatches the right specialist dev agent and the recurring "wrong subagent" failure class from nornspun retros is caught before it reaches dev.

## Description

Build a behavioral micro-eval fixture that verifies momentum:create-story picks the correct change-type (UI vs build vs skills vs general dev) so that sprint-dev dispatches the right specialist dev agent. Recurring failure class from nornspun retros — wrong subagent dispatch.

**Pain context:** Wrong change-type classification → wrong specialist dispatch → wasted dev cycles or worse, an inappropriate agent doing the work badly. This failure class has recurred across nornspun retros. An executable fixture turns a recurring retro finding into a permanent gate.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Fixture provides a labeled corpus of stories spanning all defined change-types (UI, build, skills, general dev — and any other current categories)
- Fixture asserts that create-story's chosen change-type matches the labeled type with target accuracy (e.g. >=85%)
- Fixture includes regression cases drawn from nornspun retros where the wrong specialist was dispatched
- Fixture follows the probabilistic-assertion / YAML-schema / lifecycle-states pattern
- Fixture fails with a confusion matrix and the specific stories that were misclassified

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
