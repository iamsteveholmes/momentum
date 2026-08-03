---
title: Intake owner-priority validator — owner-sourced app observations enter critical with a feature link
story_key: intake-owner-priority-validator-owner-sourced-app
status: backlog
epic_slug: momentum-backlog-refinement
feature_slug:
story_type: practice
depends_on: []
touches: []
---

# Intake owner-priority validator — owner-sourced app observations enter critical with a feature link

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a validator rule in intake and triage that forces any observation whose source is the product owner driving the app to enter at critical priority with a mandatory feature link, verified on the surface where the owner met the behavior,
so that the system's most expensive input signal — direct owner-reported defects — is never mechanically discounted at the door (no more priority:low, feature:null, or curl-only verification).

## Description

Validator rule in intake and triage: any observation whose source is the product owner driving the app enters at critical priority with a mandatory feature link (feature_slug against .momentum/features.json), verified on the surface where the owner met the behavior — never priority:low / feature:null / curl. Source: DEC-040 D6 (_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md).

**Pain context:** Nornspun discovery specimen: the owner's twice-reported top defect (campaign context) entered the sprint as priority low, position #10, unattached to any feature, routed to curl verification — the system's most expensive input signal was mechanically discounted at the door.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Any observation whose source field indicates the product owner driving the app (i.e., the owner directly encountered the behavior in the running application, not a report relayed secondhand) is force-set to `priority: critical` at intake/triage time, overriding any lower priority suggested elsewhere or by the reporter.
- The observation must carry a non-null `feature_slug` that resolves against `.momentum/features.json`; if no match exists, the validator halts and flags for manual resolution rather than defaulting to `feature: null`.
- The verification method assigned to such an observation must reflect the surface where the owner encountered the behavior (e.g., UI-driven verification when the owner drove the app UI) — never silently defaulted to curl/API-only verification.
- The validator applies at both entry points: `momentum:intake` and `momentum:triage`.
- Reference: DEC-040 D6 (`_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`).

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

- DEC-040 D6 — `_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
