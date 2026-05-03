---
title: Code Reviewer Agent Definition — Sprint-Dev Team Review Base Body
story_key: code-reviewer-agent-definition
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: feature
depends_on: []
touches: []
---

# Code Reviewer Agent Definition — Sprint-Dev Team Review Base Body

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a code-reviewer.md base body in the plugin's agents directory,
so that sprint-dev team review has a canonical spawnable agent definition for the code review role.

## Description

Create `skills/momentum/agents/code-reviewer.md` as the base role body for the code-reviewer agent used in sprint-dev Phase 4b (team review). The code reviewer is a read-only agent that audits merged code for quality issues, pattern violations, and AC compliance. Per DEC-013, this role needs a plugin base body. Note: `architecture-guard-implementation` (done) covered the momentum:architecture-guard SKILL — this story creates the separate base body for the code-reviewer spawnable role. A project can compose a project-specific code reviewer via build-guidelines to add stack-specific review patterns.

**Pain context:** No code-reviewer.md exists in the plugin's agents directory. Sprint-dev spawns the code-reviewer in team review using inline prompt injection. DEC-013 requires a plugin base body for every spawned role. The code-reviewer is distinct from the architect-guard — it focuses on code quality and AC compliance rather than architectural drift.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- code-reviewer.md exists in skills/momentum/agents/
- The base body defines the read-only review role, code quality focus, and structured findings output format
- sprint-dev Phase 4b references code-reviewer.md at spawn time
- A project can compose a project-specific code reviewer via build-guidelines

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
