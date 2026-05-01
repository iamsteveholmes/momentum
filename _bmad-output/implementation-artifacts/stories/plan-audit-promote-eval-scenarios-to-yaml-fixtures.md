---
title: "plan-audit: promote existing eval scenarios to executable YAML fixtures"
story_key: plan-audit-promote-eval-scenarios-to-yaml-fixtures
status: backlog
epic_slug: epic-9-performance-validation
feature_slug: momentum-quality-gates-enforced
story_type: maintenance
depends_on: []
touches: []
---

# plan-audit: promote existing eval scenarios to executable YAML fixtures

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the existing plan-audit eval scenario files converted into executable YAML fixtures,
so that mature, high-leverage scenarios become part of the durable micro-eval library and regressions are caught automatically.

## Description

Convert the existing eval-substantive-spec-audit.md and eval-trivial-classification.md scenario files in skills/momentum/skills/plan-audit/evals/ into executable YAML fixtures following the ForgeCode-style schema (probabilistic assertion, pinned temperature, model-at-time-of-failure). These existing scenarios are mature and high-leverage starting candidates for the micro-eval library.

**Pain context:** The scenario files already encode hard-won behavioral expectations for plan-audit. Converting them to executable fixtures stops regression risk from accumulating silently as the skill evolves.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- eval-substantive-spec-audit.md scenarios are converted to YAML fixtures in the evals/ directory
- eval-trivial-classification.md scenarios are converted to YAML fixtures in the evals/ directory
- Each fixture includes: probabilistic assertion (pass threshold), pinned temperature, and model-at-time-of-failure fields per ForgeCode-style schema
- All converted fixtures pass when run against the current plan-audit skill implementation
- Original markdown scenario files are retained or archived (not deleted) to preserve provenance

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
