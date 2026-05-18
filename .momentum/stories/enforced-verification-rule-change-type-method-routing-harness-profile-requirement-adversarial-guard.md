---
title: "Enforced verification rule — change-type method-routing, harness-profile requirement, adversarial guard"
story_key: enforced-verification-rule-change-type-method-routing-harness-profile-requirement-adversarial-guard
status: backlog
epic_slug: quality-enforcement
feature_slug: momentum-quality-gates-enforced
story_type: practice
depends_on: []
touches: []
---

# Enforced verification rule — change-type method-routing, harness-profile requirement, adversarial guard

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a single enforced verification rule that routes verification method by change-type and requires a harness profile,
so that every change is verified by the right method with no insider-knowledge shortcut, and the retired standard is no longer an inert document.

## Description

Create the enforced verification rule that replaces the retired acceptance-testing-standard.md. It defines: change-type-driven verification method routing (DEC-029 D1); a hard requirement that every verified change declare a harness profile (D3); and an adversarial anti-insider-knowledge guard so verification cannot pass by reading implementation details (D6). The rule cascades global → project → path-scoped (D7). This replaces the 'process document' artifact class with an enforced rule (DEC-029 D7).

**Pain context:** Source: DEC-029 (_bmad-output/planning-artifacts/decisions/dec-029-method-routed-acceptance-validation-pipeline-2026-05-17.md), decisions D1/D3/D6/D7. Phase 1 build is gated on routing-table-schema-and-implementation landing momentum/agents.json (DEC-029 Gate 1). create-story method-selection (separate stub) routes off this rule.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- method routing table keyed by change-type
- harness-profile declaration is mandatory and validated
- adversarial anti-insider-knowledge guard defined
- cascade order global→project→path-scoped documented
- replaces acceptance-testing-standard.md (retired by D7)

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
