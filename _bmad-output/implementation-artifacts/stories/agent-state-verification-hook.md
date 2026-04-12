---
title: Agent State Verification — Require Post-Action System State Check Before Claiming Changes Live
story_key: agent-state-verification-hook
status: backlog
epic_slug: agent-team-model
depends_on: []
touches: []
---

# Agent State Verification — Require Post-Action System State Check Before Claiming Changes Live

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a dev/E2E agent,
I want to verify actual system state after making changes (kill+relaunch, APK reinstall, process verification) rather than asserting claimed state from my execution trace,
so that agents never declare a change "live" when the running system hasn't picked it up.

## Description

Dev and E2E agents repeatedly declared app or build state without verifying the running system reflected the change. UI changes were declared "live" without relaunching the app. Desktop launch failures went unnoticed because the agent didn't check. Android was declared "showing the new UI" without reinstalling the APK. E2E validation was claimed complete without a visible cmux surface.

The `cmux.md` "Visible to the Developer" principle and GUI-launch checklist already encode the correct behavior. This is a compliance gap in dev/E2E skill prompts, not a knowledge gap in the rules.

**Pain context:** Nornspun sprint-04-08/04-10 execution. Multiple user interventions:
- HF-04 (2026-04-09T19:47): "Where is the E2E? I didn't see the cmux pane/surface" — E2E claimed success without running in a visible pane
- HF-06 (2026-04-09T21:37): "IT LOOKS LIKE DESktop failed?" — caps-lock frustration; desktop launch failed silently
- HF-07 (2026-04-09T22:14–22:40): "I think you need to shut it off and restart" / "I didn't see the android re-launch" — said three times before the agent acted
- HF-19 (2026-04-09T21:27–21:29): "I'm seeing Verdandi coming soon when I click. Is that the latest?" — agent's model of the running app diverged from the user's live observation

This pattern recurs every code sprint involving desktop or Android. The cmux rules exist but carry no enforcement weight in skill prompts.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- E2E skill: Output must include a surface reference (surface:N) — if absent, the step is not complete; sprint-dev review phase enforces this as a hard validation
- Desktop launch: After any build or UI change, agents must kill + relaunch + verify via pgrep or cmux capture-pane with a version marker or visible indicator before declaring the change live
- Android: After APK build, installDebug is required before claiming "Android has the new UI"; dev-frontend skill explicitly calls this out for any Android-affecting story
- Dev/E2E skill prompts include a post-action verification checklist referencing cmux.md GUI-launch protocol
- Zero occurrences of agents declaring state live without an observed process-level verification step

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
