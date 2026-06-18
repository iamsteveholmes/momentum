---
title: Conduct — resume and rehydration idempotency hardening
story_key: conduct-resume-and-rehydration-idempotency-hardening
status: backlog
epic_slug: momentum-sprint-orchestration
feature_slug: 
story_type: defect
depends_on: []
touches: []
---

# Conduct — resume and rehydration idempotency hardening

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to close the four resume/rehydration idempotency gaps in the Conductor workflow,
so that resuming a conduct build never re-executes phases or re-appends rows, keeping end-gate assembly and finding accumulators correct.

## Description

The 2026-06-14 conduct sub-skills audit (`.momentum/handoffs/conduct-subskills-audit-2026-06-14.html`) found four resume-path idempotency gaps in `skills/momentum/skills/conductor/workflow.md`:

1. The rehydration block (`:260-394`) does not restate the REHYDRATION EXEMPTION (`:217`) inline, risking double-append on every resume.
2. The `{{avfl_findings}}`/`{{e2e_findings}}` rehydration (`:346-375`) has no `finding_id` dedup for mixed qa-reviewer+code-reviewer sources, unlike the live-build append (`:1797`) and step 3.D (`:1894`/`:1960`) which both dedup.
3. Phase 5 (the end-gate) has no phase-completion checkpoint in the PHASE CHECKPOINT RULE (`:380-393`) and no `end-gate-phase-complete` event in the ledger schema, so Phase 5 can re-execute on resume and append duplicate rows (e.g. `endgate-report-re-rendered`, `scorecard-revert-reconciliation`), corrupting end-gate assembly.
4. `{{build_cross_artifact_notes}}` is emptied every session with no ledger event, risking silent loss if resume happens mid-collection.

**Pain context:** Resume idempotency defects in the live conduct build path; these corrupt end-gate report assembly and finding accumulators when a build resumes. Part of the idempotency cluster flagged by the 2026-06-14 conduct sub-skills audit.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- The rehydration block restates the REHYDRATION EXEMPTION (`:217`) inline so resume does not re-append exempted rows.
- avfl/e2e rehydration dedups by `finding_id` before appending to `{{avfl_findings}}`/`{{e2e_findings}}`.
- Phase 5 gains a phase-completion checkpoint plus an `end-gate-phase-complete` ledger event so it does not re-execute on resume.
- The `{{build_cross_artifact_notes}}` accumulator re-init is guarded (ledger event or checkpoint) against mid-collection resume loss.

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
