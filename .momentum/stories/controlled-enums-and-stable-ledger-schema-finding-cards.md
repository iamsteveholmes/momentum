---
title: Controlled enums + stable schema for finding-cards / build-results ledgers
story_key: controlled-enums-and-stable-ledger-schema-finding-cards
status: backlog
epic_slug: momentum-sprint-orchestration
story_type: feature
priority: medium
depends_on: []
---

# Controlled enums + stable schema for finding-cards / build-results ledgers

## Story
The conduct finding-cards and build-results ledgers need controlled enums and one stable schema so a consumer can join them on a canonical key without losing stories.

## Why this exists
Retro finding (sprint-2026-06-02-conduct-core): 20+ free-text `type` strings across 105 cards (near-duplicates like `internal-contradiction` vs `internal-contradiction / AC-violation`); the build-results schema drifted mid-build (3 structured "gates" rows vs 18 prose "key" rows); two real stories have no card key while two non-story prose keys exist. This made the retro's own join across the two ledgers lossy.

## What's needed
- `type` and `severity` are controlled enums.
- build-results uses one stable schema across all rounds.
- Both ledgers join on a single canonical key (story slug).
- A consumer joining the card and build-results ledgers loses no stories.

## References
- Retro findings (v2): `.momentum/sprints/sprint-2026-06-02-conduct-core/retro-transcript-audit.md`
- Source: `conduct-core-finding-cards-by-story.json`, `conduct-core-build-results.jsonl`
- Related (different ledger — cross-ref only): `a1-practice-ledger-schema-cli-redesign-true-append-only` (the practice ledger, not conduct's build ledgers)
