---
title: "A4: Skill workflow updates — point retro/triage/sprint-planning/intake/decision/assessment/feature-breakdown at the new CLI"
story_key: a4-skill-workflow-updates-point-retro-triage-sprint
status: backlog
epic_slug: ad-hoc
feature_slug:
story_type: practice
depends_on: ["A1"]
touches: []
---

# A4: Skill workflow updates — point retro/triage/sprint-planning/intake/decision/assessment/feature-breakdown at the new CLI

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want every skill that currently invokes the intake-queue CLI to be updated to use the new practice-ledger CLI subcommand names (plus aligned evals and architecture authority rows),
so that the skill workflows remain consistent with the A1 ledger redesign and don't drift from the new CLI surface.

## Description

Update the workflow.md files for skills that invoke the intake-queue CLI to use the new practice-ledger CLI subcommand names. Affected skills (per AES-003 Agent E touchpoint audit): retro, triage, sprint-planning, intake, decision, assessment, feature-breakdown. Also update related evals (`eval-triage-queue-items-written-via-cli.md`, `eval-triage-resurfaces-open-queue-items.md`) for the schema changes (field renames where applicable). Update architecture.md Read/Write Authority rows to reflect the new CLI surface. Effort: 3–4 hours. Change type: skill-instruction. Verification: EDD eval per affected skill workflow (verify new CLI invocations work).

**Pain context:** Multi-skill update sweep per AES-003 Findings 6 and 9. Depends on A1's new CLI surface.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- All listed skill workflow.md files (retro, triage, sprint-planning, intake, decision, assessment, feature-breakdown) call the new practice-ledger CLI subcommand names instead of the old intake-queue CLI.
- Evals `eval-triage-queue-items-written-via-cli.md` and `eval-triage-resurfaces-open-queue-items.md` reflect the renamed schema fields where applicable.
- architecture.md Read/Write Authority rows are updated to reflect the new CLI surface.
- EDD eval per affected skill workflow passes (new CLI invocations work).
- Story is blocked on A1; do not start until A1's new CLI surface is shipped.

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

- Source: triage — handoff practice-ledger-and-epic-cascade-stories-2026-05-25
- AES-003 Findings 6 and 9
- Depends on: A1 (practice-ledger schema + CLI redesign)

## Dev Agent Record

<!-- DRAFT: This section is populated only during and after development. It is empty
     because this story has not been through create-story or development yet. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
