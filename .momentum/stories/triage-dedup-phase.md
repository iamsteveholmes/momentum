---
title: Triage dedup phase — deterministic prefilter + cluster fan-out + per-theme findings
story_key: triage-dedup-phase
status: backlog
epic_slug: agent-team-model
feature_slug: 
story_type: practice
depends_on: []
touches: []
---

# Triage dedup phase — deterministic prefilter + cluster fan-out + per-theme findings

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want to implement the dedup gate in momentum:triage — a deterministic prefilter feeding cluster fan-out subagents that produce per-theme findings against the existing backlog,
so that every triage invocation (regardless of caller) deduplicates new items against the backlog before classification, ending the duplicate sprawl the backlog has been accreting.

## Description

Implements Phases 0–3 and 5 of the triage redesign plan approved 2026-05-24 (`~/.claude/plans/i-want-us-to-delightful-spindle.md`). Adds the dedup gate to `momentum:triage` as mandated by **DEC-031 D5**. Standalone value — ships backlog-hygiene gate even before consolidation analysis (Story B) lands.

**Scope:**

- **Phase 0 (new)** — `momentum-tools triage prefilter` subcommand. Pure-Python TF-IDF cosine on title + description, `touches`-path Jaccard overlap, epic/feature_slug boost, status filter (skip `done | dropped | closed-incomplete`). Output per item: top-K=10 candidate stories with score breakdowns, plus an intra-batch similarity matrix. Tuning target: recall ≥95% on real duplicates with K=10.
- **Phase 1 (new)** — inline batch clustering using Phase 0 similarity matrix (3–7 items/cluster; batches ≤5 skip clustering).
- **Phase 2 (new)** — dedup fan-out: one subagent per cluster, parallel single message, prefiltered shortlist only (~15–30 candidates, not full backlog). Returns per-theme JSON findings: `{source_item_id, theme, match_type: duplicate|supersedes|extends|unique, matched_story_slug, evidence, recommended_action, consolidation_hint}`.
- **Phase 3 (new)** — inline consolidation-candidate identification: orchestrator groups `consolidation_hint` fields by `target_slug_or_theme`; hint groups with 2+ members become merge candidates flagged for Story B.
- **Phase 5 (updated)** — approval UX gains three new sections: dedup actions, split candidates (multi-theme items), merge candidates flagged. Existing five-class classification reused for survivors.
- **Unit tests** for prefilter (recall on synthetic duplicates, status filter correctness, edge cases: empty backlog, single-item batch, all-identical batch).

**Pattern reused:** `retro/workflow.md` Phase 4 — pure fan-out (no TeamCreate, no SendMessage), parallel spawn in a single message, structured findings.

**Cost profile (with prefilter):** ~25–80K input tokens per triage run (vs ~200–320K under a full-snapshot design).

**Pain context:** The intake queue currently holds 33 open un-triaged items sitting next to ~250 non-terminal backlog stories. Sprint-planning bypasses the missing dedup gate by allowing raw handoff promotion via `handoff-N`, explicitly named as a defect in sprint-2026-05-17 retro handoff `iq-20260521002551-3a403aee`. Without this gate, every sprint cycle creates new duplicate stubs that compound the backlog hygiene problem; DEC-031 D5 ratified that dedup must become a mandatory triage gate to stop the accretion.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- `momentum-tools triage prefilter` subcommand exists and produces top-K=10 candidate shortlists per incoming item, with score breakdowns inspectable per (item, story) pair.
- Prefilter applies TF-IDF cosine on title + description, `touches` Jaccard, epic/feature_slug boost, and a status filter that excludes `done | dropped | closed-incomplete`.
- Prefilter outputs an intra-batch similarity matrix usable by Phase 1 clustering.
- Prefilter recall ≥95% on a synthetic duplicate fixture (validated by unit tests).
- Triage workflow.md adds Phase 0 (prefilter call), Phase 1 (cluster), Phase 2 (dedup fan-out), Phase 3 (consolidation candidate grouping) before existing classification.
- Phase 2 spawns one subagent per cluster in parallel via single-message fan-out (mirrors retro Phase 4 pattern, no TeamCreate).
- Each dedup agent receives only the prefiltered shortlist (not the full backlog snapshot).
- Each dedup agent returns per-theme JSON findings with the documented schema (`source_item_id`, `theme`, `match_type`, `matched_story_slug`, `evidence`, `recommended_action`, `consolidation_hint`).
- Multi-theme incoming items return multiple findings, surfacing a split candidate in the approval UX.
- Approval UX presents three new sections (dedup actions, split candidates, merge candidates) plus the existing classification of survivors.
- On approval, executor consumes duplicates, marks supersedes, and routes survivors to the existing five-class classification + executor paths.
- Unit tests cover prefilter recall, status filter correctness, empty-backlog edge case, single-item batch edge case.
- Run against the 33 open handoffs produces sensible dedup findings (at minimum: handoff-2 e2e service assumptions matched against `e2e-validator-black-box-hardening`; handoff-5 subagent context-tier matched against `agent-spawn-preflight-check`).

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
