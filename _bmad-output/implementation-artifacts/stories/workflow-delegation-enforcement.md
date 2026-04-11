---
title: Workflow Delegation Enforcement — Runtime Detection When Spawn Steps Are Bypassed
story_key: workflow-delegation-enforcement
status: backlog
epic_slug: quality-enforcement
depends_on: []
touches: []
---

# Workflow Delegation Enforcement — Runtime Detection When Spawn Steps Are Bypassed

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a orchestrator skill,
I want detect when a workflow step marked 'spawn' is executed directly instead of delegated, and halt with a correction,
so that the workflow-fidelity rule is machine-enforced not just documented — delegation bypass becomes impossible without an explicit override.

## Description

The workflow-fidelity rule (done) says spawn steps must spawn. But the rule is only advisory — orchestrators can and do bypass it. This story adds runtime enforcement: a mechanism that detects when an orchestrator is about to write files or execute logic that should have been delegated, and raises a compliance error.

**Pain context:** Recurring across sprint-2026-04-08 retro (#4), sprint-2026-04-06 (#2). Documented 3 sprints in a row. The rule alone is insufficient — agents rationalize bypasses ('I already have context'). Enforcement must be structural.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Workflow steps with delegation intent are annotated (e.g., `delegate: true`)
- At runtime, if a delegated step proceeds without spawning, an audit log entry is written
- Sprint retro reports delegation bypass count as a metric
- At least one eval demonstrates detection of a bypass scenario

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
