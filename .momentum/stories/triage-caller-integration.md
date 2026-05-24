---
title: Triage caller integration — wire retro, assessment, and decision through triage
story_key: triage-caller-integration
status: backlog
epic_slug: agent-team-model
feature_slug: 
story_type: practice
depends_on:
  - triage-dedup-phase
touches: []
---

# Triage caller integration — wire retro, assessment, and decision through triage

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want `momentum:retro`, `momentum:assessment`, and `momentum:decision` to invoke `momentum:triage` on their generated handoff items at the moment of generation, rather than writing raw `kind: handoff` events into the intake queue,
so that the backlog-hygiene gate fires automatically at every upstream source — fulfilling the DEC-031 D5 mandate that *every* caller inherits dedup + consolidation behavior, and retiring the `kind: handoff` escape hatch entirely.

## Description

Implements the "caller integration" half of the triage redesign plan approved 2026-05-24 (`~/.claude/plans/i-want-us-to-delightful-spindle.md`). Depends on Story A's invocation contract being frozen (not full ship — can start mid-Story-A once the contract is agreed).

**Scope:**

- `momentum:retro` Phase 5 invokes `momentum:triage` directly on its findings list instead of writing `kind: handoff` events to `intake-queue.jsonl`. Retro outputs become triage-classified results (story stubs created, decisions routed, etc.) before retro completes.
- `momentum:assessment` handoff disposition invokes `momentum:triage` similarly.
- `momentum:decision` handoff disposition invokes `momentum:triage` similarly.
- Remove the `handoff-N` shortcut in `sprint-planning/workflow.md` Step 2 — sprint-planning reads the *triaged* backlog only; raw handoffs no longer appear in selection.
- Update `sprint-planning/workflow.md` Step 1 Phase A.6 — the open-handoff-items read is retired (handoffs no longer exist by design).
- Retire (or repurpose) the `kind: handoff` queue-entry kind once all callers route through triage.
- Documentation updates: PRD FR114, FR116, FR117 reflect the new flow (sprint-planning spec impact pass).

**Pain context:** Even with Stories A and B shipped, the intake queue keeps accreting `kind: handoff` entries from retro/assessment/decision unless those callers are explicitly wired to invoke triage at the point of generation. The current "write handoff and hope someone runs triage later" pattern is exactly what DEC-031 D5 was decided to end. This story closes the loop.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- `momentum:retro` Phase 5 no longer writes `kind: handoff` events to `intake-queue.jsonl`; instead it invokes `momentum:triage` on its findings list and consumes the triage outputs.
- `momentum:assessment` handoff disposition follows the same pattern.
- `momentum:decision` handoff disposition follows the same pattern.
- After a retro completes, no `source: retro, kind: handoff, status: open` events exist for that sprint — all findings are either triaged stubs, decisions, or recorded SHAPING/DEFER/REJECT items.
- `sprint-planning/workflow.md` Step 2 no longer accepts `handoff-N` references; the option is removed from the prompt text.
- `sprint-planning/workflow.md` Step 1 Phase A.6 (handoff-items surfacing) is retired.
- PRD spec impact pass updates FR114 (triage taxonomy reflects post-dedup behavior), FR116 (retro disposition no longer includes raw handoff), FR117 (sprint-planning no longer reads raw handoff entries).
- Behavioral test: run a retro that produces ≥5 findings → triage runs inline → no raw handoff events remain in the queue after retro completes.
- Behavioral test: run an assessment that produces handoffs → same expected behavior.

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
