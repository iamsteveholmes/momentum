---
title: Architect Guard Agent Definition — Sprint-Dev Team Review Architecture Body
story_key: architect-guard-agent-definition
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: feature
depends_on: []
touches: []
---

# Architect Guard Agent Definition — Sprint-Dev Team Review Architecture Body

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want an architect-guard.md base body in the plugin's agents directory,
so that sprint-dev team review has a canonical spawnable agent definition for the architecture guard role.

## Description

Create `skills/momentum/agents/architect-guard.md` as the base role body for the architect-guard agent spawned in sprint-dev Phase 5 (team review). The architect-guard is distinct from the momentum:architecture-guard SKILL — it is the spawnable agent role that validates merged code against architectural decisions during sprint team review. The `architecture-guard-implementation` story (done) implemented the skill; this story creates the base body for the spawnable agent the skill invokes. Per DEC-013, every spawned role needs a plugin base body. A project can compose a project-specific architect-guard via build-guidelines.

**Pain context:** No architect-guard.md exists in the plugin's agents directory even though architecture-guard-implementation is done. That story implemented the SKILL — the agent base body is a separate artifact. DEC-013 requires both. Without the base body, the architect-guard spawn relies on inline prompt injection that cannot be project-composed.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- architect-guard.md exists in skills/momentum/agents/
- The base body defines architecture-focused read-only review, ADR validation, and drift detection patterns
- sprint-dev team review references architect-guard.md at spawn time
- A project can compose a project-specific architect-guard via build-guidelines

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
