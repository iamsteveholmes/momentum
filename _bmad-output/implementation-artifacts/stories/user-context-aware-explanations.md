---
title: Context-Aware Explanations — Calibrate to User Role, Not System Architecture
story_key: user-context-aware-explanations
status: backlog
epic_slug: agent-team-model
depends_on: []
touches: []
---

# Context-Aware Explanations — Calibrate to User Role, Not System Architecture

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a lead agent communicating with a developer-user,
I want an explanation calibration rule that starts with the user's mental model before mapping to implementation,
so that technical architecture questions get user-level answers first, not implementation dumps that lose non-technical developers.

## Description

Momentum's lead agent prompts do not include instructions to calibrate explanation level to the user's role. When a non-technical user asks an architectural question, agents default to implementation-level answers (PostgreSQL, Docker, Alembic migration paths) when the user needed a conceptual explanation of where their data lives.

Explanation calibration rule:
1. Start with the user's mental model — what they experience, what they care about
2. Map to implementation only after the user-level concept is clear
3. Use concrete analogies from their domain (for a TTRPG app: campaign files, GM prep notes — not PostgreSQL tables, Docker volumes)
4. If the user says "I'm lost" or asks the same question twice: stop, restart from the user's perspective, not the system's

This is a general Momentum guidance capability gap. Skills should encode explanation-level awareness as a first-class concern, especially for products where the developer is also the primary user of what they're building.

**Pain context:** D3 sprint (nornspun-2026-04-10-2-retro.md, Issue 9, Medium). Messages 12–16: user asked "What does add persistent storage do?" and was given implementation layers (PostgreSQL, Docker, Alembic migrations). User: "Woof I'm getting lost. You keep talking very technical and I'm getting lost in the details." Then: "Where does all this get stored? When do we implement it?" — the same question rephrased. The agent was answering the system's perspective, not the user's question.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Lead agent prompts include an explanation calibration rule: start with user mental model, map to implementation second
- Rule specifies: use domain analogies (not system internals) for domain-focused users
- Rule specifies: if user says "I'm lost" or repeats the same question, restart from user perspective
- Rule is present in sprint-dev lead agent prompt, at minimum

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
