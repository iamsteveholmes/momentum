---
title: bulk-approve-ux-split-prompt
story_key: bulk-approve-ux-split-prompt
status: backlog
epic_slug: impetus-sprint-orchestrator
feature_slug: momentum-backlog-refinement
story_type: feature
depends_on: []
touches: []
---

# bulk-approve-ux-split-prompt

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the bulk-approve flow to prompt me to split large batches before presenting the A=all option,
so that I don't accidentally approve a heterogeneous batch blindly and have to reverse the decision.

## Description

Add a split-first prompt when bulk-approve flow presents batches above N items. In sprint-2026-05-03, the developer reversed a bulk A&A&A approval to insist on splitting the batch first. The prompt should fire before offering the A=all option when item count exceeds a threshold (suggested: N=8). Applies to: triage, refine, and any other skill with bulk-approve patterns. The prompt should suggest natural split points (by class, feature, epic) before the developer approves blindly.

**Pain context:** Developer was burned in sprint-2026-05-03 by bulk-approving a large mixed batch — had to reverse the approval. Without a gate, the A=all shortcut encourages approving batches that should be split for safety and reviewability. Recurrence risk is high since bulk-approve is a common pattern across triage, refine, and other orchestration skills.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- When item count exceeds threshold N (suggested: 8), the bulk-approve flow emits a split-first prompt before displaying the A=all option
- The prompt suggests natural split points: by class, by feature, by epic
- Developer can choose to proceed with the full batch (override) or split before approving
- The split-first behavior applies consistently across triage, refine, and any other skill that uses the bulk-approve pattern
- Threshold N is configurable or at minimum documented as a tunable constant

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
