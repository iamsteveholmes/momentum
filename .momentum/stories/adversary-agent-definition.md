---
title: Adversary Agent Definition — Shipped AVFL/Distill Validation Custom
story_key: adversary-agent-definition
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: feature
depends_on: []
touches: []
---

# Adversary Agent Definition — Shipped AVFL/Distill Validation Custom

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want an adversary.md shipped custom agent definition in the plugin,
so that AVFL and distill have a concrete adversarial challenger role that works across all lens types without project customization required.

## Description

Create `skills/momentum/agents/adversary.md` as a shipped concrete agent definition for the adversary role used by momentum:avfl and momentum:distill. The adversary is a Tier B shipped custom per DEC-016 — Momentum's default concrete implementation of the validator base. It adversarially challenges enumerator findings, looking for false positives, missed edge cases, and weak evidence. Following DEC-013, it ships in the plugin so no project needs to create it, but projects can override for domain-specific adversarial patterns (e.g., a security-focused adversary that knows OWASP attack patterns).

**Pain context:** Currently no adversary.md exists in the plugin. AVFL and distill spawn adversary agents without a base body, relying on inline system prompt injection instead of the composable file model established by DEC-013.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- adversary.md exists in skills/momentum/agents/
- The file defines the adversarial stance, challenge patterns, and output format
- AVFL and distill reference adversary.md at spawn time rather than inline prompt injection
- A project can override adversary.md for domain-specific adversarial testing
- The file is consistent with the validator base contract (validator-agent-definition)

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
