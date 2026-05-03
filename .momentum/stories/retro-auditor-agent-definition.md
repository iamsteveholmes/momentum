---
title: Retro Auditor Agent Definition — Abstract Base Role for Sprint Retrospective Auditors
story_key: retro-auditor-agent-definition
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: feature
depends_on: []
touches: []
---

# Retro Auditor Agent Definition — Abstract Base Role for Sprint Retrospective Auditors

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a retro-auditor.md abstract base role body in the plugin,
so that the three concrete retro auditor shipped customs (human, execution, review) have a canonical composable foundation with a consistent auditing contract.

## Description

Create `skills/momentum/agents/retro-auditor.md` as the abstract base role body for the retro auditor role type. The retro auditor is the parent role for auditor-human, auditor-execution, and auditor-review — Momentum's three shipped concrete auditors. The base defines the auditing stance, output format, and the interface that each concrete auditor inherits. Following DEC-016's two-tier taxonomy, this is the Tier A abstract base; the three concrete auditors are Tier B shipped customs. A project could override the base to change auditing behavior across all retro runs, or override an individual auditor for custom transcript format handling.

**Pain context:** Per DEC-013, every agent role needs a base body. No retro-auditor.md exists. The three shipped customs need a root so the taxonomy is coherent and overridable at the right level — overriding retro-auditor.md affects all three auditors, overriding auditor-human.md affects only that role.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- retro-auditor.md exists in skills/momentum/agents/
- The base body defines the auditing stance, transcript-reading approach, and output format contract
- auditor-human.md, auditor-execution.md, auditor-review.md are consistent with this base
- A project can override retro-auditor.md to change auditing behavior across all retro runs

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
