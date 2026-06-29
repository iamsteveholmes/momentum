---
title: "Companion surface — post-sprint results gate (conduct end-gate + retro digest, fused)"
story_key: companion-surface-post-sprint-results-gate
status: backlog
epic_slug: momentum-impetus-experience
feature_slug:
story_type: practice
depends_on: []
touches:
  - skills/momentum/skills/conductor/
  - skills/momentum/skills/retro/
---

# Companion surface — post-sprint results gate (conduct end-gate + retro digest, fused)

<!-- DECOMPOSITION STUB: This story was decomposed from
     visual-hitl-gates-presentation-form-standard-leg (Part C). It is a planning
     stub, NOT a dev-ready story. Run momentum:create-story to enrich before dev. -->

_This story is a backlog stub decomposed from `visual-hitl-gates-presentation-form-standard-leg`.
Run `momentum:create-story` on it to make it dev-ready. Do NOT assign to a developer until
create-story has enriched it._

## Story

As the developer (the practice owner),
I want the post-sprint review delivered as **one fused, results-first companion decision surface**
— `conduct`'s end-gate report extended with a RESULTS-first lead and `retro`'s ≤7 process digest
folded in beneath it —
so that results and process review live in a single moment instead of two disconnected surfaces.

## Description

The post-sprint results gate is the second of Momentum's two highest-leverage HITL gates, and the
standard names it as a Companion-decision-surface instance (§6: "post-sprint results gate
(`conduct` end-gate + `retro` digest, fused)"). The pieces largely exist already but live in two
separate moments: `conduct` emits `endgate-report.html` (results + ship gate) and `retro`'s
findings digest is already ≤7-capped (§2.2 row 6). This story reconciles them into one gate — it
is **not** a third surface.

**Decisions already ratified (honor in create-story):**
- Extend `conduct`'s `endgate-report.html` with a **RESULTS-first lead** (per-story ship status;
  incompletes get a force-close/investigate card).
- **Fold `retro`'s ≤7 process findings** (Keep/Stop/Change) beneath results in the **same** gate;
  one gate, per-decision checkboxes. No third surface.
- Presentation-form leg (§5.1) applies: visual HTML, purpose-first lead, diagram/structure where
  it aids the decision; anti-rubber-stamp sign-off per genuine fork.

**Parent / provenance:** `visual-hitl-gates-presentation-form-standard-leg` (Part C);
existing surfaces `endgate-report.html` (`conduct-endgate-decision-card-rendering`, done) and
`retro` findings digest; standard `skills/momentum/references/rules/decision-grade-presentation.md`
§2.2 row 9 + §5 + §5.1.

## Acceptance Criteria

_DRAFT — captured from the parent story Part C; requires rewrite via create-story before dev-ready._

- `conduct`'s `endgate-report.html` gains a RESULTS-first lead: per-story ship status leads the surface; incomplete stories surface a force-close / investigate decision card.
- `retro`'s ≤7 process findings (Keep / Stop / Change) are folded beneath results in the **same** gate — one fused surface, not a third.
- Per-decision checkboxes / sign-off on both the results section and the process section; anti-rubber-stamp (written reason per genuine fork).
- The fused gate honors the presentation-form leg (§5.1): visual HTML, plain-language lead, structure made scannable.
- The gate links to source artifacts (build ledger, story files, retro findings) as depth-on-demand; it does not inline or edit them.

## Tasks / Subtasks

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation.

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._
