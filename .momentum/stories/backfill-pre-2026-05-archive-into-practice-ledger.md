---
title: "Backfill still-open pre-2026-05 archive entities into the practice-ledger schema"
story_key: backfill-pre-2026-05-archive-into-practice-ledger
status: backlog
epic_slug: ad-hoc
feature_slug: ""
story_type: maintenance
priority: critical
depends_on:
  - a1-practice-ledger-schema-cli-redesign-true-append-only
touches:
  - skills/momentum/scripts/momentum-tools.py
  - .momentum/practice-ledger.jsonl
---

# Backfill still-open pre-2026-05 archive entities into the practice-ledger schema

> **Stub** — captured at the close of sprint-2026-05-26. Flesh out at create-story / sprint-planning.

## Story

As a developer,
I want still-open entities from the frozen `practice-ledger-pre-2026-05.jsonl` archive projected into the new event schema,
so that `open` and `history` span the old→new migration boundary instead of silently dropping legacy entries.

## Background

DEC-033 (story a1) renamed the old `intake-queue.jsonl` to the archive `practice-ledger-pre-2026-05.jsonl` and started a fresh event-schema ledger. The reader **counts** archive entries (`summary` shows `archive_entries: N`) but **excludes** them from `open`/`history` derivation because the old schema (`id`/`status`/`kind`) is structurally incompatible with the event-fold model. Consequence: `history --entity <old-item>` shows only post-migration events (e.g. 1 instead of 2), and a legacy still-open item never appears in `open` unless it gets a new-schema event. The developer ratified leaving the archive frozen for the sprint and filing this backfill as **critical** follow-up.

## Acceptance Criteria (draft)

- AC1 — A one-time, idempotent backfill reads `practice-ledger-pre-2026-05.jsonl`, identifies entities whose last archived state is non-terminal (still "open"), and emits synthetic new-schema `created` events for them into `practice-ledger.jsonl` with `entity_id` preserved so chains reconcile.
- AC2 — After backfill, `open` includes the still-open legacy entities and `history --entity <id>` shows the full chain across the boundary.
- AC3 — Already-closed/terminal archive entities are NOT resurrected.
- AC4 — Idempotent: a second run appends zero events.

## Notes

Pairs with the deferred SQL-query command (`practice-ledger-duckdb-sql-query-command`). Verification method to be set at sprint-planning (likely `bash` execution test).
