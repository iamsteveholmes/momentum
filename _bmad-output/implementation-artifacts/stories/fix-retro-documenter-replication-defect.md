---
title: Fix retro documenter replication defect (AC4 regression)
story_key: fix-retro-documenter-replication-defect
status: backlog
epic_slug: impetus-core
feature_slug:
story_type: defect
depends_on: []
touches: []
---

# Fix retro documenter replication defect (AC4 regression)

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the retro skill to spawn exactly one documenter and N distinct auditors (not N× duplicate documenters),
so that retro runs match AC4 of retro-workflow-rewrite and produce coherent, non-replicated audit output.

## Description

Defect report against retro-workflow-rewrite (status: review). Despite AC4 specifying 3 auditors + 1 documenter via TeamCreate, actual runs produce N× duplicate documenters. Three-retro escalating pattern: sprint-04-08 retro = 10 agents; sprint-04-10 retro = 17 agents. Identical tool_use_id across 10 documenter transcripts confirms replication from a single API call rather than distinct spawns. Replace TeamCreate-with-retro-lead topology with single orchestrator + single documenter + N distinct auditors. Retro-lead must not fan out per-instance. Verify by dry-running retro skill on a prior sprint and counting spawned agents. Touches: skills/momentum/skills/retro/workflow.md. Cites: retro-workflow-rewrite story.

**Pain context:** auditor-execution E14, E15 from nornspun sprint-2026-04-12 retro. Prior retro flagged this and it went unactioned. Signal type: Workflow defect.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Replace the TeamCreate-with-retro-lead topology in `skills/momentum/skills/retro/workflow.md` with a single-orchestrator topology: 1 orchestrator + 1 documenter + N distinct auditors.
- Retro-lead (or equivalent) must not fan out per-instance — no topology path that causes the documenter API call to replicate.
- Dry-run verification: running the retro skill on a prior sprint spawns exactly 1 documenter and the intended auditor count (no duplicate tool_use_ids across documenter transcripts).
- Regression check against prior escalation data: sprint-04-08-style run produces <= intended agent count (not 10); sprint-04-10-style run produces <= intended agent count (not 17).
- Cites and respects AC4 of the retro-workflow-rewrite story; closes the workflow defect flagged in auditor-execution E14/E15 from nornspun sprint-2026-04-12 retro.

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
