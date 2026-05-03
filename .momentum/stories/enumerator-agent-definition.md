---
title: Enumerator Agent Definition — Shipped AVFL/Distill Validation Custom
story_key: enumerator-agent-definition
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: feature
depends_on: []
touches: []
---

# Enumerator Agent Definition — Shipped AVFL/Distill Validation Custom

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want an enumerator.md shipped custom agent definition in the plugin,
so that AVFL and distill have a concrete enumerator role that spans all lens types without project customization required.

## Description

Create `skills/momentum/agents/enumerator.md` as a shipped concrete agent definition for the enumerator role used by momentum:avfl and momentum:distill. The enumerator is a Tier B shipped custom per DEC-016 — Momentum's default concrete implementation of the validator base. It systematically enumerates issues, gaps, or items within a lens without adversarial challenge. Following DEC-013's universal agent model, it ships in the plugin so no project needs to create it, but projects can override the file if they need a domain-specific enumeration approach (e.g., security-focused enumeration, performance enumeration).

**Pain context:** Currently no enumerator.md exists in the plugin. AVFL and distill spawn enumerator agents without a base body, relying on inline system prompt injection instead of the composable file model established by DEC-013.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- enumerator.md exists in skills/momentum/agents/
- The file defines the enumeration stance, input/output format, and lens-agnostic behavior
- AVFL and distill reference enumerator.md at spawn time rather than inline prompt injection
- A project can override enumerator.md for domain-specific enumeration needs
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
