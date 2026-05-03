---
title: Validator Agent Definition — Abstract Base Role for AVFL/Distill Validation
story_key: validator-agent-definition
status: backlog
epic_slug: agent-team-model
feature_slug: momentum-composable-specialist-agents
story_type: feature
depends_on: []
touches: []
---

# Validator Agent Definition — Abstract Base Role for AVFL/Distill Validation

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a validator.md abstract base role body in the plugin's agents directory,
so that AVFL and distill validation roles have a canonical composable foundation and the two-tier agent taxonomy (DEC-016) has a root.

## Description

Create `skills/momentum/agents/validator.md` as the abstract base role body for the validator role type. The validator is the parent role for all Momentum validation agents (enumerator, adversary). It defines the validation stance, output format expectations, and composable interface that shipped custom agents (enumerator, adversary) inherit at spawn time. Following DEC-013's universal agent model and DEC-016's two-tier taxonomy (abstract base + shipped customs), this base establishes what every validator must do regardless of specialization.

**Pain context:** Per DEC-013, every agent role Momentum spawns needs a base body. Currently there is no base body for validation roles. DEC-016 formalizes the two-tier taxonomy where enumerator and adversary are Tier B shipped customs of the validator base — without the base, the taxonomy has no root and the override model is inconsistent.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- validator.md exists in skills/momentum/agents/
- The base body defines the validation stance, output format, and composable interface
- enumerator.md and adversary.md are consistent with the validator base contract
- A project can override validator.md to change validation behavior across all AVFL runs
- The file is referenced in the agents.md manifest for avfl and distill skills

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
