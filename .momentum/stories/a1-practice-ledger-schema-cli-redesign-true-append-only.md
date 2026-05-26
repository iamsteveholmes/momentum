---
title: "A1: Practice-ledger schema + CLI redesign — true append-only event log"
story_key: a1-practice-ledger-schema-cli-redesign-true-append-only
status: backlog
epic_slug: ad-hoc
feature_slug:
story_type: practice
depends_on: []
touches: []
---

# A1: Practice-ledger schema + CLI redesign — true append-only event log

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the practice-ledger to be a true append-only event log with a DuckDB-backed reader CLI and TTL closure,
so that practice state has immutable history, queryable views, and bounded growth per DEC-033.

## Description

Implement DEC-033 D1–D8 + D10. Rename `.momentum/intake-queue.jsonl` to `.momentum/practice-ledger.jsonl`. Rewrite the schema: `event_id` (immutable per row, unique), `entity_id` (repeats per logical thing), `ts`, `event_type` enum (`created`/`updated`/`consumed`/`rejected`/`closed_stale`/`reopened`/`custom`), `custom_event_type` (when custom), `source`, `actor`, `payload`. Implement append-only writer (`open('a')`, O_APPEND) for all writes — no whole-file rewrites. Implement DuckDB-backed reader CLI subcommands: `summary`, `open`, `history --entity`, `since`, `by-source`. Implement `close-stale --age-days <N>` CLI command for the TTL closure path. Set up Claude Code Routine (via CronCreate) to invoke close-stale daily. Hard-cut migration: freeze existing 88 entries as `.momentum/practice-ledger-pre-2026-05.jsonl`; new file starts empty under new schema. Update architecture.md (Decision 52 rewrite, Decision 1c amendment with pointer to DEC-033, State Layout, Read/Write Authority table). Update prd.md (FR115 rewrite; FR114/116/117 reference updates). Effort: 6–10 hours. Change types: script-code, specification, config-structure. Verification: EDD eval + execution test for migration.

**Pain context:** Foundation story for Cascade A. Blocks A2/A3/A4. Implements DEC-033 D1–D8 + D10.

**Source:** triage — handoff practice-ledger-and-epic-cascade-stories-2026-05-25

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- `.momentum/intake-queue.jsonl` renamed to `.momentum/practice-ledger.jsonl`
- New schema fields: `event_id`, `entity_id`, `ts`, `event_type` (enum), `custom_event_type`, `source`, `actor`, `payload`
- All writes use append-only `open('a')` / O_APPEND — no whole-file rewrites anywhere
- DuckDB-backed reader CLI exposes: `summary`, `open`, `history --entity`, `since`, `by-source`
- `close-stale --age-days <N>` CLI command implemented for TTL closure path
- Claude Code Routine registered via CronCreate to invoke close-stale daily
- Hard-cut migration: existing 88 entries frozen as `.momentum/practice-ledger-pre-2026-05.jsonl`; new file starts empty
- architecture.md updated: Decision 52 rewrite, Decision 1c amendment with DEC-033 pointer, State Layout, Read/Write Authority table
- prd.md updated: FR115 rewrite; FR114/116/117 reference updates
- Verification: EDD eval + execution test for migration passes

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

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

- DEC-033 — Practice-Ledger Event-Log Redesign

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
