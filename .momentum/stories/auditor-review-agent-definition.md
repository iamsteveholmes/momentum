---
title: Auditor Review Agent Definition — Shipped Retro Auditor for Team Review Messages
story_key: auditor-review-agent-definition
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: feature
depends_on: []
touches: []
---

# Auditor Review Agent Definition — Shipped Retro Auditor for Team Review Messages

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want an auditor-review.md shipped custom agent definition in the plugin,
so that momentum:retro has a concrete agent for auditing review and QA agent outputs from the sprint transcript.

## Description

Create `skills/momentum/agents/auditor-review.md` as a shipped concrete agent definition for the auditor-review role used by momentum:retro. This Tier B shipped custom reads team-messages.jsonl from the sprint transcript to audit what review agents (QA reviewer, code reviewer, AVFL) found — findings reports, review comments, and quality signals raised during the sprint. Following DEC-013, it ships as a default plugin agent. A project can override for custom review signal analysis.

**Pain context:** Currently no auditor-review.md exists. DEC-013 requires every spawned role to have a plugin base body. The review audit lens is distinct from human and execution lenses — it focuses on quality findings rather than developer intent or implementation behavior.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- auditor-review.md exists in skills/momentum/agents/
- The file specializes the retro-auditor base for team-messages.jsonl input analysis
- The file defines what review signals to look for (AVFL findings, QA blocks, code review comments)
- momentum:retro references auditor-review.md at spawn time rather than inline prompt injection

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
