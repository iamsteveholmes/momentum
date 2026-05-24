---
title: Triage consolidation phase — fan-out cluster analysis + merged-spec generation
story_key: triage-consolidation-phase
status: backlog
epic_slug: agent-team-model
feature_slug: 
story_type: practice
depends_on:
  - triage-dedup-phase
touches: []
---

# Triage consolidation phase — fan-out cluster analysis + merged-spec generation

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to add the consolidation analysis fan-out to `momentum:triage` so that merge-candidate clusters (flagged by the dedup phase) get analyzed by subagents that deep-read cluster members and return concrete merge/split/leave recommendations with draft merged-specs,
so that the second half of DEC-031 D5's mandate is satisfied — the backlog actively consolidates related work rather than just deduplicating duplicates.

## Description

Implements Phase 4 of the triage redesign plan approved 2026-05-24 (`~/.claude/plans/i-want-us-to-delightful-spindle.md`). Builds on the dedup gate (`triage-dedup-phase`) which surfaces merge candidates but defers full analysis.

**Scope:**

- **Phase 4 (new)** — consolidation analysis fan-out: for each merge-candidate cluster identified in Phase 3, spawn one subagent in parallel. Each agent deep-reads the full story files of its cluster members (not the compressed snapshot) and returns: `{cluster_id, recommendation: merge-into-one|merge-into-N|split|leave-as-is, target_slugs, merged_spec: "markdown body...", rationale}`.
- **Phase 5 (updated)** — approval UX merge-candidates section evolves from a flag list (Story A) to a real proposal panel with draft merged specs the developer can approve, edit, or reject.
- On approval, executor applies merges via `momentum-tools` (consume/supersede source stories, write merged story file via `momentum:intake` invocation, update index entries).
- Unit/behavioral tests for the consolidation agent (recommendation schema correctness, merged-spec drafting quality on a synthetic 3-story cluster).

**Pattern reused:** same parallel-fan-out skeleton as Phase 2 (Story A), but with full-file deep reads instead of prefiltered shortlists.

**Pain context:** Story A surfaces merge candidates but the developer still has to mentally merge them. Without Phase 4, the value of the dedup signal is bounded — the practice surfaces clusters but doesn't help close them. DEC-031 D5 explicitly mandates *both* dedup *and* consolidation.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- Triage workflow.md adds Phase 4 between Phase 3 (consolidation-candidate identification) and Phase 5 (approval UX).
- Phase 4 spawns one subagent per merge-candidate cluster, parallel, single message (mirrors retro Phase 4 fan-out pattern).
- Each consolidation agent receives the full story files of its cluster members (not the compressed snapshot).
- Each consolidation agent returns the documented JSON schema (`cluster_id`, `recommendation`, `target_slugs`, `merged_spec`, `rationale`).
- Recommendations include all four classes: `merge-into-one | merge-into-N | split | leave-as-is`.
- Approval UX merge-candidates section presents draft merged specs alongside member story slugs and rationale.
- Developer can approve, edit, or reject each consolidation proposal independently.
- On approval, executor consumes/supersedes source stories and creates the merged story via `momentum-tools` calls.
- Behavioral test on a synthetic 3-story cluster designed to merge: Phase 4 produces a `merge-into-one` recommendation with a coherent merged_spec.
- Behavioral test on a synthetic mixed cluster: Phase 4 produces a `split` or `merge-into-N` recommendation as appropriate.

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
