---
title: Sprint-planning cross-story coherence gate for depends_on deliverables
story_key: sprint-planning-cross-story-coherence-gate
status: backlog
epic_slug: momentum-sprint-planning-to-ready
feature_slug:
story_type: feature
depends_on: []
touches: []
---

# Sprint-planning cross-story coherence gate for depends_on deliverables

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want sprint-planning (at contract-freeze time, when the full sprint story set is visible) to validate every `depends_on` edge — asserting that each input a consumer story names is actually delivered by the producer story's ACs/deliverables,
so that a sprint cannot freeze with two halves embodying contradictory architectures, where each story passes its own gates while the seam between them belongs to no one.

## Description

Root-caused from the nornspun campaign-init sprint (sprint-2026-05-30). The client story
`campaign-init-offered-suggestion-list-render-and-routes` instructed "source the copy from
the backend payload... not a hardcoded client string" with
`depends_on: backend-campaign-init-add-offered-suggestion-list-copy`. But that backend
story only edited the Urd **system prompt** — it delivered no payload, no endpoint, no
schema. The consumer's named input ("backend payload") did not exist on the producer side.

No gate could see this: create-story runs one story at a time, and its AVFL checkpoint
validates each story against its own epic record. The incoherence existed only *between*
stories. The result: backend stories all assumed the campaign-init conversation flowed
through Urd chat; client stories all assumed client-local rendering; no story owned the
wiring; the dev hardcoded "fallback" constants and the sprint shipped a scripted
client-side performance.

Sprint-planning is the altitude where all frozen contracts are visible together — the
cheapest, highest-leverage place for the check: for every `depends_on` edge in the sprint,
the consumer's referenced external inputs must map to a concrete deliverable (artifact,
endpoint, schema, constant, file) in the producer's contract. Unmatched edges block
activation or force an explicit wiring story.

**Pain context:** A 15-story sprint was internally consistent story-by-story and globally
incoherent; the gap cost a full build + end-gate cycle before live Phase-4 caught it.
Recurs on any sprint whose stories span a producer/consumer seam (client/backend,
skill/config, agent/harness). Discovered during sprint-2026-05-30 root-cause analysis
(2026-06-10).

## Acceptance Criteria

<!-- DRAFT: rough captures from conversation; create-story must rewrite. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- At contract-freeze, sprint-planning enumerates every `depends_on` edge in the sprint
  story set.
- For each edge, the consumer story's externally-sourced inputs (e.g. "backend payload",
  "signal from sibling story", "config produced by X") are extracted and matched against
  the producer story's ACs/deliverables.
- An edge whose named input has no matching producer deliverable is a coherence failure:
  reported with both story slugs, the missing deliverable, and a remediation choice
  (amend producer ACs, amend consumer, or add an owning wiring story).
- Sprint activation is blocked (or requires explicit developer override) while coherence
  failures are open.
- Edges to stories outside the sprint are checked against the dependency's recorded
  status/deliverables, not skipped silently.

> Note: rough captures only — create-story will replace with validated, testable ACs.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Architecture Compliance

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- Origin: nornspun sprint-2026-05-30 root-cause analysis — broken `depends_on`
  edge `campaign-init-offered-suggestion-list-render-and-routes` →
  `backend-campaign-init-add-offered-suggestion-list-copy` (AVFL held finding #7).
- Sibling per-story check: `create-story-dependency-deliverable-check` (this gate is the
  whole-sprint version run when all contracts are visible).

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
