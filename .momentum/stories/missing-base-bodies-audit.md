---
title: Missing Base Bodies Audit — Verify Universal Agent Model Coverage Post-DEC-013
story_key: missing-base-bodies-audit
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: exploration
depends_on: []
touches: []
---

# Missing Base Bodies Audit — Verify Universal Agent Model Coverage Post-DEC-013

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a one-time audit that enumerates every agent role spawned across all Momentum skills and confirms each has an agent definition file in the plugin,
so that I can verify DEC-013 universal agent model compliance with zero untracked gaps.

## Description

Run a systematic audit of all Momentum workflow.md files to enumerate every named agent role spawn point. Cross-reference against the agents/ directory to identify missing definition files. Produce a gap report. This story closes when all gaps are either resolved (definition file exists) or tracked as open stories with known slugs. This is an exploration/audit story — it produces a report, not a file. It can be run before or after `agents-md-manifest-format` ships, but benefits from that story's machine-parseable manifest if available.

**Pain context:** DEC-013 mandates universal agent definition coverage but was adopted 2026-05-02, mid-sprint, after the last grooming pass. The grooming pass on 2026-05-02/2026-05-03 identified the known gaps and created stories for them. This audit confirms no gaps were missed and closes the loop — it's the verification step after all the agent-definition stories have been implemented.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Every workflow.md in skills/momentum/skills/ has been read and all named spawn roles enumerated
- Each role is cross-referenced against skills/momentum/agents/
- A gap report is produced listing covered vs. missing roles
- All missing roles are either: (a) now covered (file exists), or (b) tracked as a backlog story
- The audit story closes once the gap count reaches zero untracked gaps

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
