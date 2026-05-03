---
title: Documenter Agent Definition — Retro Synthesis Coordinator Base Body
story_key: documenter-agent-definition
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: feature
depends_on: []
touches: []
---

# Documenter Agent Definition — Retro Synthesis Coordinator Base Body

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a documenter.md base body in the plugin's agents directory,
so that momentum:retro has a canonical spawnable agent definition for the retrospective synthesis coordinator role.

## Description

Create `skills/momentum/agents/documenter.md` as the base role body for the documenter agent used in momentum:retro. The documenter receives auditor findings and synthesizes them into the retrospective report. Currently spawned without a base body file, relying on inline prompt injection. Per DEC-013, this role needs a plugin base body. Note: a related story (`retro-remove-teamcreate-documenter`) refactors the documenter away from TeamCreate topology — this story creates the base body regardless of spawning mechanism, so both stories can be developed independently.

**Pain context:** No documenter.md exists. DEC-013 requires every spawned role to have a base body. The documenter is a non-trivial synthesis role — it must transform structured auditor findings into actionable retrospective insights — and deserves a well-defined canonical definition rather than relying on inline prompt injection that drifts across workflow versions.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- documenter.md exists in skills/momentum/agents/
- The file defines the synthesis role, input format expectations (structured auditor findings), and retrospective report output format
- momentum:retro references documenter.md at spawn time rather than inline prompt injection
- A project can override documenter.md for custom retrospective report formats

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
