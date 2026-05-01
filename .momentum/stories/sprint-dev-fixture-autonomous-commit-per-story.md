---
title: "sprint-dev fixture: autonomous commit per story"
story_key: sprint-dev-fixture-autonomous-commit-per-story
status: backlog
epic_slug: epic-12-sprint-execution-workflow
feature_slug: momentum-sprint-orchestration
story_type: practice
depends_on: []
touches: []
---

# sprint-dev fixture: autonomous commit per story

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a behavioral micro-eval fixture that verifies momentum:sprint-dev produces an autonomous commit per merged story without prompting the developer,
so that the `feedback_autonomous_commits_enforced` memory is encoded as a durable, executable regression test.

## Description

Build a behavioral micro-eval fixture that verifies momentum:sprint-dev produces an autonomous commit per merged story without prompting the developer. Encodes the `feedback_autonomous_commits_enforced` memory as an executable test.

**Pain context:** The autonomous_commits_enforced feedback has been recorded as a user memory item — sprint-dev was asking for commit approval instead of committing autonomously. Without an executable fixture, this regression can silently recur. The fixture makes the expectation machine-verifiable.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Given a completed story merge, the fixture verifies sprint-dev performs a git commit without requesting developer approval
- Fixture detects and fails if sprint-dev emits any approval-seeking language around commits (e.g., "Should I commit?", "Do you want me to commit?")
- Fixture passes when sprint-dev commits autonomously and reports the commit reference
- Fixture follows ForgeCode-style YAML schema with probabilistic assertion, pinned temperature, and model-at-time-of-failure fields
- Fixture is placed in the appropriate evals/ directory under the sprint-dev skill

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
