---
title: "Companion surface — wire over-budget bulk-derivation paths (triage batch / ad-hoc plan) to emit paired surface"
story_key: companion-surface-bulk-derivation-wiring
status: backlog
epic_slug: momentum-impetus-experience
feature_slug:
story_type: practice
depends_on: []
touches: []
---

# Companion surface — wire over-budget bulk-derivation paths to emit a paired companion surface

<!-- SPLIT STUB: Split from companion-surface-rule-sync-and-bulk-derivation at the
     sprint-2026-06-28 plan gate (developer chose resolution C — scope intake out).
     This is a backlog stub, NOT dev-ready. Run momentum:create-story before dev. -->

_Backlog stub. Run `momentum:create-story` before assigning to a developer._

## Story

As the developer (the practice owner),
I want the bulk / ad-hoc-plan derivation paths that emit a review document exceeding the
Decision-card budget to also emit the paired companion decision surface from the shipped template,
so that no over-budget review document is ever handed to a human without its decision surface (the
§5 defect the standard names).

## Description

Split from `companion-surface-rule-sync-and-bulk-derivation` (AC4/AC5) at the `sprint-2026-06-28`
plan gate. That story's enrichment established that **`momentum:intake` has no over-budget review
path** (single-stub capture only, well under the Decision-card budget), so the intake-wiring half
was scoped out (recorded N/A) and the project-rule sync shipped alone.

The genuine over-budget emitters — the paths that DO produce a large review document a human must
evaluate — are more likely:
- **`momentum:triage`** batch intake (classifies many observations at once → a large digest), and/or
- the **sprint-planning pre-sprint plan gate** itself (handled by `companion-surface-pre-sprint-plan-gate`).

This story identifies the real over-budget bulk-derivation emitter(s) and wires each to emit a paired
companion decision surface from `skills/momentum/references/templates/companion-decision-surface.html`,
per the §5 Companion-Surface Obligation. create-story should first confirm which path(s) actually
exceed the Decision-card budget before committing scope.

**Provenance:** parent `companion-surface-rule-sync-and-bulk-derivation`; standard
`skills/momentum/references/rules/decision-grade-presentation.md` §5 + §5.1 + §2.2 row 9; template
`skills/momentum/references/templates/companion-decision-surface.html`.

## Acceptance Criteria

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Identify the bulk-derivation path(s) that emit a review document exceeding the Decision-card budget (confirm, don't assume — the parent found intake does NOT qualify).
- Each qualifying path emits a paired companion decision surface derived from the template; the large document is linked as depth-on-demand, never inlined.
- Emitting the review document without its companion surface is treated as a defect ("has not finished"), per §5.

## Tasks / Subtasks

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation.

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._
