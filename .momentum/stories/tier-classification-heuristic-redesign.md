---
title: Tier Classification Heuristic Redesign — Well-Understood+Reversible vs Novel+Load-Bearing
story_key: tier-classification-heuristic-redesign
status: backlog
epic_slug: impetus-core
depends_on: []
touches:
  - _bmad-output/planning-artifacts/prd.md
  - skills/momentum/skills/distill/workflow.md
  - skills/momentum/skills/retro/workflow.md
  - skills/momentum/skills/distill/evals/eval-tier-classification.md
derives_from: distill Tier 2 escalation (self-referential distill session 2026-04-14)
---

# Tier Classification Heuristic Redesign — Well-Understood+Reversible vs Novel+Load-Bearing

<!-- INTAKE STUB: This story was captured by momentum:distill's Tier 2 escalation path. It is a
     backlog stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a practice maintainer,
I want the Tier 1 / Tier 2 classification in `momentum:distill` (and its downstream consumers) to key on **well-understood + reversible vs novel + load-bearing** rather than file count or sentence length,
so that distill accepts multi-file well-understood changes as Tier 1 and only escalates truly novel, load-bearing changes to Tier 2 — removing the over-rigor that currently causes distill to be underused.

## Description

The current Tier 1 / Tier 2 definitions across the practice are wrong. They key on file count and sentence length:

- Current Tier 1: "single-file, single-section, single-sentence-ish addition"
- Current Tier 2: "multi-file change, new skill, workflow redesign, or anything requiring spec-level deliberation"

This produced a recent incorrect escalation: a three-file addition of Flow D to `momentum:decision` (workflow + SDR template + eval) was classified as Tier 2 on file-count grounds, despite being well-understood (mirrored existing Flows A/B/C) and reversible. The developer overrode the escalation and the change landed as a distill.

The correct axis: **well-understood + reversible** vs **novel + load-bearing**. Multi-file changes can be Tier 1 if the pattern is well-understood. Structural redesigns stay Tier 2. File count alone is not the signal.

**Why this is Tier 2 itself (and why it needs a story, not an immediate distill):**
1. **Spec source-of-truth** — `prd.md` FR97 canonically defines both tiers; changing the workflow without updating the PRD creates spec/code drift.
2. **Cross-skill routing coupling** — `retro/workflow.md` Phase 5 embeds the old heuristic inline for routing findings to distill. Changing distill alone silently breaks retro's routing.
3. **Reconciliation algorithm break** — distill Phase 1 uses `max(enumerator_tier, adversary_challenge)` with "adversary escalates only." That monotonic rule is wrong under the new axis — a well-understood multi-file change that an Enumerator over-flags must be *de-escalated* by the Adversary, which the current rule forbids.

**Pain context:** Distill is being underused (this session surfaced it explicitly). The current heuristic produces false Tier 2 escalations, which forces work into sprint-lifecycle rigor that should have landed in minutes. Until this redesign lands, every distill session is at risk of incorrect classification.

## Acceptance Criteria

<!-- DRAFT: Rough ACs captured from conversation. Require refinement via create-story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from the distill discovery pass that escalated this story:

- **FR97 in `prd.md` updated** to define Tier 1 as "well-understood + reversible" and Tier 2 as "novel + load-bearing" — not by file count or sentence length. Examples in the FR illustrate well-understood multi-file Tier 1 cases and novel single-file Tier 2 cases.
- **`distill/workflow.md` Enumerator prompt** (lines ~63–67) updated to instruct classification by the new axis; includes concrete examples of well-understood multi-file Tier 1 patterns (flow branches mirroring existing flows, reference entries in established format) and novel Tier 2 patterns (new concept introduction, classification-logic rewires).
- **`distill/workflow.md` Adversary prompt** (lines ~98–102) updated to challenge classifications using the new axis; tier-challenge rule changed from "escalate only" to "adjust either direction — escalate when novel+load-bearing, de-escalate when well-understood+reversible and Enumerator over-classified."
- **`distill/workflow.md` Phase 1 reconciliation** (lines ~121–127) redesigned to handle non-monotonic tier relationships. Not `max(enumerator, adversary)` — instead, Adversary's tier assessment takes precedence when it's grounded in the new heuristic (well-understood AND reversible → Tier 1 regardless of Enumerator).
- **`retro/workflow.md` Phase 5** (lines ~431–453) updated to use the new heuristic text when routing findings to distill. Any routing examples that reference the old "single-sentence" framing replaced.
- **`distill/evals/eval-tier-classification.md`** updated: scenarios reframed around the new axis; at least one new scenario covering well-understood multi-file → Tier 1 and at least one covering novel single-file → Tier 2.
- Self-test: this very story, if run through the updated distill pipeline, should correctly classify as Tier 2 under the new heuristic (novel reframing of classification logic + load-bearing across distill/retro/PRD).
- Backward compatibility note in `distill/workflow.md` explaining the change and why old-style classifications (file-count-based) should be re-evaluated.

> Note: The ACs above are rough captures. Create-story will replace them with validated, testable criteria.

## Tasks / Subtasks

<!-- DRAFT: No tasks analyzed or planned. Populate via create-story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

<!-- DRAFT: Not yet populated. Run create-story to enrich with architecture analysis,
     implementation guide, technical requirements, and Momentum-specific guidance. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Architecture Compliance

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

_DRAFT — requires rewrite via create-story before this story is dev-ready._

Must include: eval scenario covering well-understood multi-file (Tier 1) case; eval scenario covering novel single-file (Tier 2) case; a self-test confirming reconciliation correctly handles Adversary de-escalation.

### Implementation Guide

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- Distill workflow source: `skills/momentum/skills/distill/workflow.md` (lines 63–67 Enumerator tier definition; 98–102 Adversary tier challenge; 121–127 Phase 1 reconciliation)
- Retro Phase 5 routing: `skills/momentum/skills/retro/workflow.md` (lines 431–453 old heuristic embedded inline)
- PRD canonical Tier definition: `_bmad-output/planning-artifacts/prd.md` FR97 (lines 857–874)
- Current eval: `skills/momentum/skills/distill/evals/eval-tier-classification.md` (lines 19–27, 41–43 Tier 2 scenario tied to old axis)
- Distill skill description: `skills/momentum/skills/distill/SKILL.md` (line 3 references retro Tier 1 finding — retains correct spirit under new axis)
- Triggering distill session: 2026-04-14 self-referential distill escalation by Adversary agent

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
