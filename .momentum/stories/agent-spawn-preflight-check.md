---
title: Agent Spawn Pre-Flight Check — Validate Before Spawning
story_key: agent-spawn-preflight-check
status: backlog
epic_slug: agent-team-model
depends_on: []
touches: []
---

# Agent Spawn Pre-Flight Check — Validate Before Spawning

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a sprint orchestrator,
I want a pre-flight validation gate before spawning any agent,
so that agents are only created when they have a valid prompt, correct type, and no duplicate already running the same task.

## Description

Spawn workflows do not validate agent prompts or team composition before creating agents. Agents are created first, then given work — or not. No gate exists between "decide to spawn" and "actually spawn." This produces zero-turn agents that waste spawn overhead, context preparation, and JSONL manifest entries without producing any work.

The fix: a pre-flight validation step on all spawn workflows that checks prompt non-empty, team size within bounds, agent type matches required tools, and no duplicate task is already running. For TeamCreate specifically: propose composition to the developer first, receive approval, then spawn. This eliminates the oversized-team failure mode.

**Pain context:** D3 sprint (nornspun-2026-04-10-2-retro.md, Issue 3, High). 38 of 129 agents (29%) had zero assistant turns. Combined with the planning sprint's 54-agent fan-out, spawn-before-think is a recurring orchestration failure mode across sprint types. The oversized-team incident alone (messages 45–46, user ordered immediate shutdown) likely accounts for a portion of these, but 29% is too high to attribute to a single incident.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Before spawning any agent, verify: (1) prompt is non-empty, (2) team size ≤ 4 for TeamCreate, (3) agent type matches required tools (read-only task → Explore, not general-purpose), (4) no duplicate agent already running the same task
- For TeamCreate spawns: orchestrator proposes team composition to developer before spawning; spawn only after explicit approval
- Pre-flight failures produce a clear halt message — not a silent skip or best-effort spawn
- Zero-turn agent rate drops measurably in next sprint following fix

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

<!-- DRAFT: No tasks have been analyzed or planned. This section MUST be populated by
     create-story, which will break down the work based on architecture analysis and
     implementation guidance. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

<!-- DRAFT: Not yet populated. Run create-story to enrich with architecture analysis,
     implementation guide, technical requirements, and Momentum-specific guidance. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

No technical analysis has been performed. The following sub-sections are all stubs.

### Architecture Compliance

<!-- DRAFT: Architecture compliance has not been assessed for this story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

<!-- DRAFT: Testing requirements have not been defined for this story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

<!-- DRAFT: No implementation guide has been generated. Create-story will inject
     Momentum-specific guidance based on change-type classification. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

<!-- DRAFT: File paths, skill directories, and structural alignment have not been
     analyzed. Create-story will populate this based on the relevant epic and
     existing codebase structure. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

<!-- DRAFT: No references have been identified. Create-story will add source citations
     from architecture docs, PRD, and relevant code. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
