---
title: "sprint-planning fixture: team composition matches story type mix"
story_key: sprint-planning-fixture-team-composition-matches-story-type-mix
status: backlog
epic_slug: epic-12-sprint-execution-workflow
feature_slug: momentum-sprint-planning-to-ready
story_type: practice
depends_on: []
touches: []
---

# sprint-planning fixture: team composition matches story type mix

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a behavioral micro-eval fixture that verifies momentum:sprint-planning composes the correct specialist dev team for a sprint given mixed story types,
so that the "dispatcher not inspecting story.tag" failure mode is caught automatically.

## Description

Build a behavioral micro-eval fixture that verifies momentum:sprint-planning composes the correct specialist dev team (frontend/build/skills mix) for a sprint given mixed story types. Catches the "dispatcher not inspecting story.tag" failure mode.

**Pain context:** If sprint-planning selects a homogeneous team regardless of story type mix, the wrong specialists get assigned and sprint execution degrades. This is a silent failure — the plan looks complete but the team is wrong. An executable fixture catches this before it affects a real sprint.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Given a sprint with a mix of frontend, build, and skills story types, the fixture verifies sprint-planning selects at least one specialist of each required type
- Fixture detects and fails when a homogeneous team is composed regardless of story type mix
- Fixture passes when team composition correctly reflects the story type distribution in the sprint
- Fixture follows ForgeCode-style YAML schema with probabilistic assertion, pinned temperature, and model-at-time-of-failure fields
- Fixture is placed in the appropriate evals/ directory under the sprint-planning skill

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

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
