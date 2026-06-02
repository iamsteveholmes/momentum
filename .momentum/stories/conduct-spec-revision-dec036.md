---
title: Revise the conduct spec to design to the DEC-036 stakes-and-timing exception
story_key: conduct-spec-revision-dec036
status: backlog
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: maintenance
depends_on: []
touches: []
---

# Revise the conduct spec to design to the DEC-036 stakes-and-timing exception

<!-- INTAKE STUB: captured by momentum:intake. NOT dev-ready. DRAFT sections require
     full rewrite by create-story before development. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want `sprint-dev-redesign-spec.md` revised to design to the DEC-036 stakes-and-timing exception,
so that the conduct build stories are not implemented against a spec that still contradicts the decision they are meant to realize.

## Description

DEC-036 Phase 2 prerequisite. The conduct spec still designs to DEC-035's absolutism: §8 says "zero intermediate gates" (lines 587-591) and §4 says "ALWAYS auto-fixed" (line 259). Revise §1 (binding decisions), §4 (fixer schema — relax the always-auto-fix absolute, add the stakes class + `escalated` disposition), §8 (gate model — add the narrow mid-flight tier), and §9 (report — dismissed rendering, anti-rubber-stamp, decision-grade caps) to absorb the DEC-036 stakes-and-timing exception, with a reconciliation note pointing at DEC-035 binding decision #1.

**Pain context:** No story in the 52-breakdown owns this — each per-leg agent saw only its slice of the spec, so none flagged the spec revision as a unit of work. Building the 18 stories against a contradictory spec would have the build agents contradict the decision they implement. This should land before/alongside the schema-root story (`directed-fix-finding-schema`). Source: DEC-036 Phase 2 / Reconciliation table (lines 95-99).

## Acceptance Criteria

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- §1 binding decisions reflect the DEC-036 amendment (intermediate gate removed EXCEPT the narrow stakes-gated mid-flight tier; routine findings always auto-fixed, stakes-class findings raised).
- §4 fixer schema relaxes the "ALWAYS auto-fixed" absolute and documents the stakes class + `escalated` disposition.
- §8 gate model documents the mid-flight escalation tier alongside the single end-gate.
- §9 report documents dismissed rendering, the anti-rubber-stamp forcing function, and the decision-grade presentation caps + self-sufficiency floor.
- A reconciliation note ties the changes back to DEC-035 binding decision #1 and DEC-036.

> Note: rough captures only. Create-story will replace with validated, testable ACs.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

Target: `_bmad-output/planning-artifacts/sprint-dev-redesign-spec.md` (§1, §4, §8, §9). Source decision: DEC-036 Phase 2.
