---
title: Remove TeamCreate from Retro Documenter — Refactor to Fan-Out + Orchestrator Handoff
story_key: retro-remove-teamcreate-documenter
status: backlog
epic_slug: impetus-core
feature_slug: momentum-retro-and-flywheel
story_type: maintenance
depends_on: []
touches: []
---

# Remove TeamCreate from Retro Documenter — Refactor to Fan-Out + Orchestrator Handoff

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the retro workflow to spawn the documenter via direct orchestrator handoff instead of TeamCreate,
so that an unnecessary team topology is removed and the workflow follows the standard Momentum fan-out pattern.

## Description

Refactor momentum:retro to eliminate the TeamCreate/Shape-A topology for the documenter. Replace with: three parallel fan-out auditors (auditor-human, auditor-execution, auditor-review) return structured findings to the orchestrator; orchestrator then spawns the documenter directly with findings as context. No TeamCreate is needed — the documenter doesn't need to receive SendMessages from auditors mid-run; it needs their completed output. This simplification follows the standard Momentum fan-out pattern and removes a source of prior replication defects.

**Pain context:** TeamCreate was added to retro to allow the documenter to coordinate with auditors via SendMessage during the run. In practice the auditors run to completion and return findings — there is no mid-run coordination needed. TeamCreate is the wrong tool for a collect-and-synthesize pattern. Two prior stories (fix-retro-documenter-replication-defect, retro-team-singleton-guard) were both closed-incomplete due to complexity in the TeamCreate topology, confirming the pattern itself is the root cause.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- momentum:retro contains no TeamCreate call
- The three auditors run as parallel fan-out agents and return findings to the orchestrator
- The orchestrator passes combined auditor findings to a directly-spawned documenter
- No SendMessage calls remain in the retro workflow for auditor→documenter communication
- The retro workflow produces the same retrospective report output as before

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

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
