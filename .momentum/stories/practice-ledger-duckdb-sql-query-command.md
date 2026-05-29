---
title: "Add a DuckDB-backed practice-ledger query command for arbitrary SQL over ledger records"
story_key: practice-ledger-duckdb-sql-query-command
status: backlog
epic_slug: ad-hoc
feature_slug: ""
story_type: feature
priority: high
depends_on:
  - a1-practice-ledger-schema-cli-redesign-true-append-only
touches:
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
---

# Add a DuckDB-backed practice-ledger query command for arbitrary SQL over ledger records

> **Stub** — captured at the close of sprint-2026-05-26. Flesh out at create-story / sprint-planning.

## Story

As a developer,
I want a `practice-ledger query "<SQL>"` command that runs arbitrary SQL over the ledger JSONL and returns records,
so that I can ask any question of the practice ledger — not just the five pre-baked reads (`summary`/`open`/`history`/`since`/`by-source`).

## Background

This captures the **actual value DuckDB was for** in DEC-033 / AC15: arbitrary SQL queries that return records over the sorted JSONL. Story a1 shipped a pure-Python reader with only the five fixed subcommands — which answers neither arbitrary queries nor SQL syntax (grep only word-matches). The developer's reasoning at the sprint-2026-05-26 close: the JSONL is a sorted set of records, so SQL-over-records is exactly the capability worth having; defer it to this dedicated story rather than bolt it on at sprint-close. The misleading `_load_duckdb_events` name and AC15 wording were corrected in a1 to reflect that the SQL-query interface is deferred here.

## Acceptance Criteria (draft)

- AC1 — `practice-ledger query "<SQL>"` runs the SQL via DuckDB over `read_json('practice-ledger*.jsonl')` (both live + archive) and returns matching records.
- AC2 — Full SQL syntax supported (SELECT/WHERE/GROUP BY/ORDER BY/joins on the JSON fields); output as JSON records by default, `--format text` optional.
- AC3 — Read-only: the command never mutates the ledger.
- AC4 — Adds the `duckdb` dependency cleanly (documented; `uv`-managed) and degrades with a clear error if unavailable.
- AC5 — Does not change the existing five fixed subcommands.

## Notes

The fixed subcommands stay as ergonomic shortcuts; this adds the open-ended escape hatch. Verification method to be set at sprint-planning (likely `bash` execution test). Pairs with `backfill-pre-2026-05-archive-into-practice-ledger`.
