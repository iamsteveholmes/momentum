---
title: Conduct — assign finding_id before directed-fix invocation
story_key: conduct-assign-finding-id-before-directed-fix-invocation
status: backlog
epic_slug: momentum-sprint-orchestration
feature_slug: 
story_type: defect
depends_on: []
touches: []
---

# Conduct — assign finding_id before directed-fix invocation

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the Conductor to assign a unique finding_id to every finding before it invokes the directed fixer,
so that the directed-fix contract is satisfied and fixes are routed/deduped by a stable key.

## Description

The Conductor invokes the directed fixer at step 2.S3 (skills/momentum/skills/conductor/workflow.md:956) with {{stage2_findings}} that were never assigned a finding_id. The normalization section at :700-727 that builds {{qa_findings}} omits finding_id from the canonical base fields, yet the directed-fix-invocation-contract (skills/momentum/references/directed-fix-invocation-contract.md:40-48) requires that "Each inbound finding carries a finding_id field assigned by the Conductor before the fix-mode is invoked." Step 2.S3 (:933-939) presupposes finding_id exists ("keyed by finding ID") but provides no instruction to create it. This is a genuine, critical contract violation surfaced by the 2026-06-14 conduct sub-skills audit (.momentum/handoffs/conduct-subskills-audit-2026-06-14.html) — missed by the first audit, confirmed by the second.

**Pain context:** Critical contract violation in the live conduct build path. Without a finding_id, the directed fixer cannot key/dedup inbound findings; fixes can misroute or collide. Found in the 2026-06-14 conduct sub-skills audit; flagged as the single genuine contract bug.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Before Phase B of step 2.S3 (before :956), an explicit action iterates {{stage2_findings}} and assigns a unique finding_id to each finding that lacks one (unique within the story's findings array — e.g. source + '-' + index, or a uuid).
- The directed fixer is never invoked with a finding missing finding_id.
- The normalization at :700-727 lists finding_id among canonical base fields (or the assignment step guarantees presence downstream).

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
