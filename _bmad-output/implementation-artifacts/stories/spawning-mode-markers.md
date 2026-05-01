---
title: Sprint-Dev Team Composition, Phase Sequencing, and Spawning Mode Markers
story_key: spawning-mode-markers
status: backlog
epic_slug: impetus-epic-orchestrator
depends_on: []
touches: []
---

# Sprint-Dev Team Composition, Phase Sequencing, and Spawning Mode Markers

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a sprint orchestrator,
I want explicit team composition limits, phase sequencing constraints, and spawning mode annotations in every sprint-dev workflow step that creates agents,
so that code sprints use the correct team topology, phases execute in the right order, and orchestrators never guess individual vs TeamCreate.

## Description

Three related code-sprint orchestration failures, consolidated into one fix:

**1. Team composition rules (Critical, D3):** Sprint-dev created per-story agents (dev-d4-1, dev-d4-2, etc.) instead of shared role agents. The correct pattern: one backend-dev, one frontend-dev (if needed), one QA, one E2E — shared across all stories. Max team size 4 (lead excluded). No per-story team decomposition. The user discovered a "massive team" and ordered immediate shutdown. Six+ agents were created where 2–3 were appropriate.

**2. Phase sequencing (Medium, D3):** Sprint-dev used TeamCreate before AVFL validation and before individual dev agents finished their stories. Correct order: Phase 1 — individual dev fan-out (no TeamCreate); Phase 2 — AVFL; Phase 3 — TeamCreate for dev+QA+E2E iteration. TeamCreate is prohibited in Phase 1.

**3. Spawning mode markers (High, original):** Workflow steps don't declare whether they intend individual Agent calls or TeamCreate. Each spawn step should annotate: `spawning: individual` or `spawning: team`. Orchestrators currently infer this, leading to wrong topology.

All three are the same underlying fix: encode hard constraints in the sprint-dev workflow XML so orchestrators can't make the wrong choice.

**Pain context:** D3 sprint (nornspun-2026-04-10-2-retro.md, Issues 1 and 8, Critical/Medium). Per-story team decomposition produced 6+ agents where 2–3 were needed, contributing to 29% zero-turn agent waste. TeamCreate before AVFL required user intervention at message 54. The correct workflow sequence was user-specified mid-sprint. Original spawning-mode-markers pain: Sprint-2026-04-06-2 (#2, Critical) — wrong topology identified in spawning-patterns.md but never enforced at the workflow step level.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- All workflow steps with agent spawns include `spawning: individual` or `spawning: team` annotation
- Orchestrator reads annotation before spawning — no inference required
- spawning-patterns.md rule references the annotation format
- At least sprint-dev and sprint-planning workflows updated

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
