---
title: Install/Upgrade I/O Consolidation — Batch Sequential Bash Calls into Single Script Command
story_key: install-upgrade-io-consolidation
status: backlog
epic_slug: impetus-core
depends_on: []
touches: []
---

# Install/Upgrade I/O Consolidation — Batch Sequential Bash Calls into Single Script Command

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a Impetus install/upgrade workflow,
I want execute the full install or upgrade action set via a single momentum-tools.py command instead of 7+ sequential Bash calls,
so that install and upgrade paths are 800-1200 tokens cheaper and more reliable — LLM orchestration replaced with deterministic script execution.

## Description

Steps 3-4 of the Impetus install path perform 7+ sequential Bash calls: file copies, inline python3 one-liners for state file writes, and per-action shell execution. A single `session install-actions` command accepting an action list would return structured results. Also batch hash-drift resolution (manual file copy loop) and upgrade chain resolution (linked-list traversal by LLM). Extends the preflight script pattern to remaining deterministic operations. Source: PT-024.

**Pain context:** Identified in impetus-quality-analysis-20260406 (runs 142715 + 145856). Install/upgrade paths are infrequent but high token cost when hit (800-1200 tokens). The preflight architecture already proved the script pattern works — this extends it.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- `momentum-tools session install-actions` command accepts action list and returns structured JSON
- Single command replaces 7+ sequential Bash calls in install Steps 3-4
- Hash-drift resolution execution batched (not a manual copy loop)
- Upgrade chain resolution (linked-list traversal) moved to script
- Install/upgrade token cost reduced by estimated 800-1200 tokens
- Unit tests cover install-actions command

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
