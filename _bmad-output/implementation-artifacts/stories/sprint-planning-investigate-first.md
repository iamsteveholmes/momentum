---
title: Sprint Planning Investigate-First — Look Before Asking Diagnostic Questions
story_key: sprint-planning-investigate-first
status: backlog
epic_slug: quality-enforcement
depends_on: []
touches: []
---

# Sprint Planning Investigate-First — Look Before Asking Diagnostic Questions

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer using sprint planning,
I want the planning skill to search the codebase before presenting diagnostic questions about code state,
so that my time is spent on decisions, not on answering questions the agent could answer itself by reading the code.

## Description

During sprint-04-10 planning, the agent asked the user to choose among multiple-choice options about API stub status — questions the agent could have answered by grepping NornApiClient.kt for TODO or stub markers. The user had to say they didn't know, prompting the agent to look for itself. This is the "ask-before-looking" anti-pattern applied to the sprint-planning skill.

The user's response ("I hate when you ask me this without doing a bit of research") and the fact that the answer was "it just returns a scripted speech every time" (observable behavior, not architectural knowledge) illustrate that a simple grep would have resolved the question before it reached the user.

**Pain context:** HF-02 in sprint-04-10 planning (2026-04-11T05:41). The user explicitly named the anti-pattern. Recurs whenever planning encounters ambiguous code state: API implementation status, platform coverage gaps, feature flag state. Sprint-planning is the session where these questions arise most — it's the wrong time to be blocked on code lookups.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- sprint-planning skill prompt includes an explicit rule: before presenting any diagnostic question about code state or existing implementation, grep/read the relevant files first
- Only escalate to the user if the answer is genuinely ambiguous after reading
- Never present "is it A or B or C?" to the user without first searching for A, B, and C in the code
- When planning must escalate a question, it includes what it searched and what it found (or didn't find) before asking

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
