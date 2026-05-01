---
title: Load Impetus persona on happy path so voice is in context every session
story_key: load-impetus-persona-on-happy-path-so-voice-is-in-context
status: backlog
epic_slug: impetus-ux-redesign
feature_slug:
story_type: feature
depends_on: []
touches: []
---

# Load Impetus persona on happy path so voice is in context every session

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the Impetus persona to be loaded on every entry path so his identity is in context on every session,
so that Impetus speaks as himself on the happy path, not as a template substituter.

## Description

The Impetus happy-path greeting (SKILL.md lines 29–51) substitutes pre-rendered
narrative/menu/closer strings from the Python preflight
(`momentum-tools session startup-preflight`). The rich persona file at
`skills/momentum/references/session-greeting.md` (Optimus Prime + KITT register,
"a guardian who kneels to listen") is only loaded on the rare open-threads path
(`workflow.md` step 11). SKILL.md's inline `## Voice & Input` section carries voice
rules but NOT the full persona.

Result: on every happy-path session, Impetus speaks as a template substituter, not
as a character — which is exactly why the developer reports "no warmth, no
personality, no reason to want to work with him."

This is the lowest-risk first bite of the Epic 2a UX redesign: make the persona
available on every entry path without yet restructuring the rendering contract with
Python (that's a separate story — `preflight-context-envelope`).

**Pain context:** Over a month of daily sessions feeling like meeting a teleprompter wearing a guardian's name. Quality analysis (bmad-agent-builder, 2026-04-19, finding H1) rated this HIGH severity — it's the architectural root of the agent feeling uninformed and lifeless on the happy path.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- SKILL.md Startup block loads the persona content from `references/session-greeting.md` before rendering the greeting (or includes it by reference so voice rules + identity are always in context)
- Happy-path output uses the persona voice — the existing pre-rendered `greeting.narrative` is one input among several, not the entire output
- Open-threads path (Step 11) still works; no regression there
- Voice Guidelines section of `session-greeting.md` becomes the single source of truth for identity/voice (cross-referenced from SKILL.md instead of duplicated)
- Existing evals still pass: `eval-first-install-personality-and-identity`, `eval-session-menu-voice-and-upgrade-voice`, `eval-2item-menu-first-time-user-orientation-unaffected`
- New eval added asserting identity/persona language is present in greeting output
- Preflight Python script is NOT changed in this story (separate story: `preflight-context-envelope`)

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

Origin: bmad-agent-builder quality analysis report, `_bmad-output/reports/impetus/quality-analysis/2026-04-19-141047/quality-report.md`, opportunity H1 "Persona starved at runtime — the architectural root of 'no warmth, no personality'."

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
