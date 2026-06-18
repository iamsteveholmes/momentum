---
title: "Conduct — ledger append-site dedup guards"
story_key: conduct-ledger-append-site-dedup-guards
status: backlog
epic_slug: momentum-sprint-orchestration
feature_slug: ""
story_type: defect
depends_on: []
touches: []
---

# Conduct — ledger append-site dedup guards

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want add the mandated (story_slug, event, finding_id) duplicate-prevention guard at every ledger append site that currently skips it,
so that resuming a conduct build never double-appends finding rows, so finding counts and governance guards stay correct.

## Description

`skills/momentum/skills/conductor/workflow.md:404` mandates that before appending a finding-disposition, stage3-escalation, or avfl-finding row during a live build, the Conductor checks the `(story_slug, event, finding_id)` tuple against `{{ledger_seen_events}}` and skips if already present, adding new tuples afterward. Only the avfl-finding append at `:1797` implements this. The five finding-disposition append sites (`:985`, `:998`, `:1005`, `:1010`, `:1017`), the stage3-escalation append (`:1026`), and the stage3-mid-flight-escalation append all skip the guard. Additionally, `:404`'s dedup event-type list omits `stage3-mid-flight-escalation` entirely. On resume this risks duplicate findings and ledger doubling. From the 2026-06-14 conduct sub-skills audit (`.momentum/handoffs/conduct-subskills-audit-2026-06-14.html`).

**Pain context:** Resume idempotency defect in the live conduct build path. Without these guards every resume can double-append ledger rows, inflating finding counts and corrupting dedup/governance logic. Part of the idempotency cluster flagged by the 2026-06-14 conduct sub-skills audit.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Each finding-disposition append site (:985/:998/:1005/:1010/:1017) performs the (story_slug, event, finding_id) dedup check before appending and adds the tuple to {{ledger_seen_events}} after — following the :1797 avfl-finding pattern.
- The stage3-escalation (:1026) and stage3-mid-flight-escalation append sites perform the same guard.
- The :404 standing rule's dedup event-type list includes stage3-mid-flight-escalation.

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
