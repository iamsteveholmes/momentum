---
title: Auditor Execution Agent Definition — Shipped Retro Auditor for Agent Summaries
story_key: auditor-execution-agent-definition
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: feature
depends_on: []
touches: []
---

# Auditor Execution Agent Definition — Shipped Retro Auditor for Agent Summaries

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want an auditor-execution.md shipped custom agent definition in the plugin,
so that momentum:retro has a concrete agent for auditing execution agent behavior from the sprint transcript.

## Description

Create `skills/momentum/agents/auditor-execution.md` as a shipped concrete agent definition for the auditor-execution role used by momentum:retro. This Tier B shipped custom reads agent-summaries.jsonl from the sprint transcript to audit what execution agents (dev, build, etc.) did — tool calls, file writes, implementation choices, and behavioral deviations from the story spec. Following DEC-013, it ships as a default plugin agent. A project can override for custom transcript format handling.

**Pain context:** Currently no auditor-execution.md exists. DEC-013 requires every spawned role to have a plugin base body. The execution audit is a distinct analytical lens from the human and review audits — it warrants its own shipped definition.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- auditor-execution.md exists in skills/momentum/agents/
- The file specializes the retro-auditor base for agent-summaries.jsonl input analysis
- The file defines what execution signals to look for (tool calls, file writes, scope deviations)
- momentum:retro references auditor-execution.md at spawn time rather than inline prompt injection

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
