---
title: create-story validates dependency-delivered inputs exist
story_key: create-story-dependency-deliverable-check
status: backlog
epic_slug: momentum-sprint-planning-to-ready
feature_slug:
story_type: feature
depends_on: []
touches: []
---

# create-story validates dependency-delivered inputs exist

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want create-story to validate, when a story's ACs or tasks reference an externally-sourced input (e.g. "source the copy from the backend payload"), that the input is traceable to a concrete deliverable in an existing contract or in a `depends_on` story's ACs — and to flag an architecture gap when it isn't,
so that stories cannot be enriched to ready-for-dev while consuming artifacts that nothing in the system produces.

## Description

Root-caused from the nornspun campaign-init sprint (sprint-2026-05-30). create-story's
Step 7 only *extracts* `depends_on` slugs from the epic record into the index — no step
asks "does the depended-on story actually produce the artifact this story consumes?" The
offered-list client story said "source from the backend payload, not a hardcoded client
string" while its sole dependency edited a system prompt and delivered no payload, no
endpoint, no schema. The Step-8 AVFL checkpoint couldn't catch it either: it validates the
story against its own epic record, single-story, single-direction.

Faced with an AC naming a non-existent input, the dev agent silently substituted hardcoded
"fallback" constants and the sprint shipped a client-faked conversation.

Scope: a create-story step (likely between change-type classification and AVFL) that
extracts externally-sourced inputs from ACs/tasks, resolves each against (a) existing
contracts/code cited in references, or (b) the `depends_on` stories' ACs/deliverables, and
on failure either blocks enrichment or injects a loud, structured "UNRESOLVED INPUT —
architecture gap" marker the developer must resolve before ready-for-dev.

**Pain context:** This is the per-story half of the fix (the whole-sprint half is
`sprint-planning-cross-story-coherence-gate`); per-story matters because stories are often
created before any sprint exists, and the gap is invisible at every later gate. Discovered
during sprint-2026-05-30 root-cause analysis (2026-06-10).

## Acceptance Criteria

<!-- DRAFT: rough captures from conversation; create-story must rewrite. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- create-story extracts every externally-sourced input named in the enriched story's
  ACs/tasks (payloads, endpoints, signals, files, constants delivered by other work).
- Each input is resolved against existing artifacts/contracts in the story's references
  or against the ACs/deliverables of `depends_on` stories.
- An unresolvable input blocks the story from `ready-for-dev` or injects an explicit
  `UNRESOLVED INPUT — architecture gap` section naming what's missing and which story or
  contract should deliver it.
- The story's `depends_on` index entries are derived from these resolutions, not just
  copied from the epic record.
- Completion output surfaces resolved/unresolved input counts.

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

- Origin: nornspun sprint-2026-05-30 root-cause analysis — client story consumed a
  "backend payload" its dependency never delivered (AVFL held findings #6/#7).
- create-story workflow Step 7 (depends_on extraction without deliverable validation),
  Step 8 (AVFL scope = story vs own epic record only).
- Sibling whole-sprint gate: `sprint-planning-cross-story-coherence-gate`.

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
