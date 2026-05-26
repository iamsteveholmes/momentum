---
title: "B1: Epic schema migration — define epics.json, migrate features and categorical epics, re-home unhomed stories"
story_key: b1-epic-schema-migration-define-epicsjson-migrate-features
status: backlog
epic_slug: ad-hoc
feature_slug:
story_type: practice
depends_on: []
touches: []
---

# B1: Epic schema migration — define epics.json, migrate features and categorical epics, re-home unhomed stories

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a unified epic schema with migrated features, evaluated categorical epics, and re-homed unhomed stories,
so that the epic layer becomes the single source of truth for work organization per DEC-034.

## Description

Implement DEC-034 D1–D5. Define new `epics.json` schema at `_bmad-output/planning-artifacts/epics.json` with the unified epic shape: `epic_slug`, `name`, `description`, `lifecycle: finite-lived | long-lived`, `audience: user | internal`, plus carried-forward feature fields (`value_analysis`, `system_context`, `acceptance_conditions`, `stories[]`, `stories_done`, `stories_remaining`, `last_verified`, `notes`). Migrate the 23 current features into the new shape (default `finite-lived` + `user`). Evaluate the 18 categorical epics one by one with the developer: dissolve into finite-lived epics where possible (re-home their stories accordingly) or convert to `long-lived` where genuinely warranted (e.g., `ad-hoc`). Best-effort re-home the 269 unhomed stories from `stories/index.json` into appropriate epics; `ad-hoc` accepts residue. Freeze `features.json` as `_bmad-output/planning-artifacts/archive/features-pre-2026-05.json`. Update architecture.md (Decisions 44–49 → historical; Read/Write Authority + Skills Deployment Classification). Update prd.md (FR102–FR113 superseded). Restructure `epics.md` (likely retire as narrative; the canvas becomes the human view). Effort: 6–10 hours. Change types: specification, config-structure, script-code. Verification: document review (developer + AVFL on new schema + migrated data).

**Pain context:** Foundation story for Cascade B. Blocks B2/B3/B4. Implements DEC-034 D1–D5. Heaviest single lift in cascade (269-story re-homing pass).

**Source:** triage — handoff practice-ledger-and-epic-cascade-stories-2026-05-25

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- New `epics.json` exists at `_bmad-output/planning-artifacts/epics.json` with unified schema (epic_slug, name, description, lifecycle, audience, value_analysis, system_context, acceptance_conditions, stories[], stories_done, stories_remaining, last_verified, notes)
- All 23 features migrated into new shape with `lifecycle: finite-lived` + `audience: user` defaults
- All 18 categorical epics evaluated with developer; each either dissolved (stories re-homed) or converted to `long-lived`
- 269 previously-unhomed stories from `stories/index.json` best-effort re-homed; residue lands in `ad-hoc`
- `features.json` frozen to `_bmad-output/planning-artifacts/archive/features-pre-2026-05.json`
- `architecture.md` updated: Decisions 44–49 marked historical; Read/Write Authority + Skills Deployment Classification sections updated
- `prd.md` updated: FR102–FR113 marked superseded
- `epics.md` restructured or retired (canvas becomes the human view)
- AVFL pass on new schema + migrated data passes
- Developer reviews and approves final state

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

<!-- DRAFT: No tasks have been analyzed or planned. -->

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

- DEC-034 (Epic-Layer Consolidation) — D1–D5
- AES-003 (Practice-Ledger Defects + Epic-Layer Consolidation)
- Handoff: `.momentum/handoffs/practice-ledger-and-epic-cascade-stories-2026-05-25.md`

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
