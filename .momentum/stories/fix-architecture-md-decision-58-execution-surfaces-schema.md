---
title: Fix architecture.md Decision 58 — execution_surfaces schema lists 5 entries but implementation ships 10
story_key: fix-architecture-md-decision-58-execution-surfaces-schema
status: backlog
epic_slug: quality-enforcement
feature_slug: momentum-quality-gates-enforced
story_type: maintenance
depends_on: []
touches: []
---

# Fix architecture.md Decision 58 — execution_surfaces schema lists 5 entries but implementation ships 10

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want architecture.md Decision 58 to accurately document all 10 execution_surfaces,
so that the architecture document matches the shipped implementation and doesn't mislead future readers.

## Description

Decision 58 in `_bmad-output/planning-artifacts/architecture.md` documents the verification-harness.json schema but lists only 5 execution_surfaces keys (from early design). The shipped implementation in `momentum/verification-harness.json` correctly has all 10 entries — one per change_type in the routing table: skill-instruction, agent-definition, rule-hook, script-code, script-cli, backend, app-ui, research-spike, specification, config-structure.

The architecture doc is a protected planning artifact ("modify via refine workflow only"). The fix requires running `momentum:refine` on architecture.md to amend Decision 58's execution_surfaces documentation to match the implementation.

**Pain context:** Flagged as Architecture Guard finding H4 during sprint-2026-05-17 Phase 5 review. The document divergence could mislead developers designing new change types or reading the architecture for context on the harness schema.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:
- Decision 58 in architecture.md lists all 10 execution_surfaces keys matching momentum/verification-harness.json
- The 5 missing entries added: agent-definition, rule-hook, script-cli, backend, app-ui, research-spike (net: the 5 that were absent from the early design spec)
- No other Decision 58 content is altered

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

- `_bmad-output/planning-artifacts/architecture.md` — Decision 58 (the target section)
- `momentum/verification-harness.json` — authoritative implementation with all 10 entries
- Sprint-2026-05-17 Architecture Guard finding H4

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
