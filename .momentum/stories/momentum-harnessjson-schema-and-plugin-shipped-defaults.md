---
title: momentum/harness.json schema and plugin-shipped defaults
story_key: momentum-harnessjson-schema-and-plugin-shipped-defaults
status: backlog
epic_slug: bring-your-own-tools
feature_slug: momentum-protocol-based-integration
story_type: practice
depends_on: []
touches: []
---

# momentum/harness.json schema and plugin-shipped defaults

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want a harness.json schema plus plugin-shipped defaults that other workflows can consume,
so that verification is driven by declared harness config instead of hardcoded tool assumptions, and tooling is swappable per project.

## Description

Define the momentum/harness.json schema and ship a plugin default block, as a sibling to momentum/agents.json with the same defaults/project shape (JSON). It declares: environment startup + readiness probes; execution surface per change-type; driver binding (cmux / Skill / Maestro / Playwright / curl); platform/target matrix; human-review carve-outs; and a trivial-smoke escape hatch. It is written/maintained by agent-builder and agent-guidelines. (DEC-029 D3.)

**Pain context:** Source: DEC-029 (_bmad-output/planning-artifacts/decisions/dec-029-method-routed-acceptance-validation-pipeline-2026-05-17.md), decision D3. Phase 1 gated on routing-table-schema-and-implementation landing momentum/agents.json (DEC-029 Gate 1). The e2e-validator rewrite and the sprint-planning contract/coverage-plan stub both consume this harness.json.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- JSON schema mirroring agents.json defaults/project shape
- env startup + readiness probes declared in schema
- execution surface per change-type declared in schema
- driver binding for cmux/Skill/Maestro/Playwright/curl declared in schema
- platform/target matrix declared in schema
- human-review carve-outs declared in schema
- trivial-smoke escape hatch declared in schema
- authored/maintained by agent-builder and agent-guidelines

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
