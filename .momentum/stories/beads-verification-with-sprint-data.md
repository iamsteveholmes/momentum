---
title: "Beads dual-write: verify activation scenarios with real sprint execution"
story_key: beads-verification-with-sprint-data
status: backlog
epic_slug: agent-team-model
feature_slug: ""
story_type: exploration
depends_on: []
touches: []
---

# Beads dual-write: verify activation scenarios with real sprint execution

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to verify the beads dual-write integration scenarios that require real sprint activation data,
so that I can confirm the shadow layer works end-to-end before committing to the full beads integration.

## Description

The beads-dual-write-spike sprint (2026-05-16) established the infrastructure and produced a research artifact, but three Gherkin scenarios could not be verified because `beads-id-map.json` was empty — no sprint was actually activated with `bd ready --claim` during that sprint.

Scenarios blocked:
- S3: Story creation via sprint commands mirrors a bead into the shadow layer
- S4: Bead created for a story links back to its spec file (spec_id field)
- S7: Discovered work captured via intake includes a beads shadow entry

This story is a follow-up to execute the next sprint with beads active and verify these scenarios against real data.

**Pain context:** The spike proved the infrastructure is present and the CLI works, but the go/no-go recommendation was marked INCOMPLETE because no sprint data existed. This story closes the loop.

## Acceptance Criteria

<!-- DRAFT -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Run a sprint activation with beads active (bd ready --claim invoked)
- Verify `.momentum/beads-id-map.json` is populated with story slug → bead ID entries
- Verify `bd show {bead-id}` displays the story title and exits 0
- Verify the `spec_id` field in `bd show` output points to the correct `.momentum/stories/{slug}.md` file
- Verify an intake-captured story produces a beads shadow entry and a discovered-from relationship
- Update the research artifact go/no-go from INCOMPLETE to a definitive recommendation

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- `docs/research/beads-dual-write-spike-findings-2026-05-16.md` — research artifact with go/no-go criteria
- `beads-dual-write-spike.feature` in sprint-2026-05-16 specs — Scenarios 3, 4, 7
- `.momentum/beads-id-map.json` — currently empty `{}`

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
