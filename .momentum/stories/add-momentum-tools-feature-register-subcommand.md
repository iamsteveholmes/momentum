---
title: Add momentum-tools feature register so features can enter the registry via the sole-writer path
story_key: add-momentum-tools-feature-register-subcommand
status: backlog
epic_slug: ad-hoc
feature_slug:
story_type: feature
depends_on: []
touches: []
---

# Add momentum-tools feature register so features can enter the registry via the sole-writer path

<!-- INTAKE STUB: captured by momentum:intake. Not dev-ready; run momentum:create-story. -->

## Story

As a developer,
I want a feature register subcommand,
so that new features can legitimately enter .momentum/features.json while feature verify stays the sole verdict writer.

## Description

From sprint-2026-08-03 end-gate (Option A). The registry is a closed loop: feature verify refuses unknown slugs (cmd_feature_verify), feature --help shows only verify, FR146 forbids hand edits, and the greeting eval bars sprint-planning from placeholders. No new feature can enter, so every sprint routes to the maintenance fallback and the DEC-040 loop never engages. File: skills/momentum/scripts/momentum-tools.py (+ test-momentum-tools.py).

**Pain context:** Every sprint routes permanently to the maintenance fallback.

## Acceptance Criteria

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- feature register writes slug / name / acceptance_condition with status absent
- feature verify remains sole verdict writer
- Tests in test-momentum-tools.py

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._
