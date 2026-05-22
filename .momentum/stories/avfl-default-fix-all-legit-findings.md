---
title: "AVFL default: always fix all legit findings, retire fix/defer gate"
story_key: avfl-default-fix-all-legit-findings
status: backlog
epic_slug: epic-3
feature_slug: momentum-quality-gates-enforced
story_type: feature
depends_on: []
touches: []
---

# AVFL default: always fix all legit findings, retire fix/defer gate

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the AVFL loop to fix all confirmed-legit findings by default without a per-finding fix/defer decision gate,
so that the loop runs to completion without friction and I don't have to make per-finding deferral calls for things already classified as legit.

## Description

Sprint-dev Phase 4c AVFL pass should default to fixing all confirmed-legit findings without a per-finding fix/defer decision gate. The current gate asks the developer (or orchestrator) to choose fix vs defer per finding — this is friction that slows the loop. Behavioral change: once AVFL confirms a finding is legit, fix it. Defer is no longer a valid verdict for a legit finding in the AVFL loop.

**Pain context:** Developer-stated preference; reduces per-finding gate friction in sprint-dev AVFL loop. Source: triage — conversation.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- When AVFL confirms a finding as legit, the loop proceeds to fix it without asking
- No per-finding fix/defer gate fires in Phase 4c of sprint-dev
- A legit finding always results in a fix attempt; defer is not a valid outcome for legit findings
- The behavioral change is reflected in the AVFL workflow/skill

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
