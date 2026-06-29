---
title: "Companion surface — pre-sprint plan gate emitted by sprint-planning"
story_key: companion-surface-pre-sprint-plan-gate
status: backlog
epic_slug: momentum-impetus-experience
feature_slug:
story_type: practice
depends_on: []
touches:
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/sprint-planning/SKILL.md
---

# Companion surface — pre-sprint plan gate emitted by sprint-planning

<!-- DECOMPOSITION STUB: This story was decomposed from
     visual-hitl-gates-presentation-form-standard-leg (Part B). It is a planning
     stub, NOT a dev-ready story. Run momentum:create-story to enrich before dev. -->

_This story is a backlog stub decomposed from `visual-hitl-gates-presentation-form-standard-leg`.
Run `momentum:create-story` on it to make it dev-ready. Do NOT assign to a developer until
create-story has enriched it._

## Story

As the developer (the practice owner),
I want `momentum:sprint-planning` to emit a **visual, purpose-first pre-sprint plan gate**
(an HTML companion decision surface, sibling of `endgate-report.html`) as its final step,
so that at the single highest-leverage steering moment I can understand and shape a sprint in
seconds instead of skim-then-rubber-stamping an ad-hoc concatenation of full story specs.

## Description

The pre-sprint plan review is one of Momentum's two highest-leverage HITL gates. Today
`sprint-planning` selects, specs, and activates stories but **emits no human go/no-go surface** —
the human reviews by opening whatever they open (an unmeasured, ad-hoc path). For one 8-story
sprint that ad-hoc path was a ~37,500-word document — a log file, not a decision document.

The global decision-grade-presentation standard now **requires** this surface: §2.2 row 9
(Companion decision surface) names the "pre-sprint plan gate (`sprint-planning`, final step)" as a
mandatory instance (§6 surface schema), and §5.1 (presentation-form leg) requires it render as
visual HTML, lead with a plain-language purpose hero, and diagram the structure. A reusable
skeleton already ships at `skills/momentum/references/templates/companion-decision-surface.html`.
This story makes `sprint-planning` actually emit it.

**Decisions already ratified (honor in create-story):**
- Emitted as the **final step of `momentum:sprint-planning`** (Step 7 / developer-review), which
  already holds the selected-story set + wave/dep graph — generation is a synthesis step, not a
  new pipeline.
- Generation is **synthesis-now**: read and extract the fork callouts story authors already
  write; defer any `stakes:`/`value_line:`/`delta:` story-frontmatter contract on `create-story`
  until the gate's shape proves out over 2–3 sprints.
- The gate **links to** the canonical story `.md` files; it **never inlines or edits** them, so
  `momentum:dev` / `bmad-dev-story` keep their source-of-truth machine band intact.

**Parent / provenance:** `visual-hitl-gates-presentation-form-standard-leg` (Part B);
template `skills/momentum/references/templates/companion-decision-surface.html`;
sibling surface `endgate-report.html`; standard `skills/momentum/references/rules/decision-grade-presentation.md` §2.2 row 9 + §5 + §5.1.

## Acceptance Criteria

_DRAFT — captured from the parent story Part B; requires rewrite via create-story before dev-ready._

- `momentum:sprint-planning` emits a Layer-0 plan-gate surface as its final step — visual HTML, a sibling of `endgate-report.html`, opened in the viewer.
- Purpose-first hero: what the sprint accomplishes, in plain language a non-implementer reads in seconds, before any table or list.
- A dependency/wave diagram (inline SVG, not prose) marking any single-point-of-failure / critical-path story.
- A scannable story table (stakes · wave · dep · ★CALL-vs-✓batch verdict); as-specified/routine stories collapse to one line.
- A decision card per genuine fork only, with what / why-it-matters / evidence / recommendation fully inlined (no bare handles); ≤ 7 forks.
- Anti-rubber-stamp sign-off: forces a written one-line verdict + reason per genuine fork; a blanket "approve all" is insufficient.
- The gate links to canonical story files; it never inlines or edits them.
- Generation is synthesis-now (extract existing story fork-callouts); no story-frontmatter contract required for v1.

## Tasks / Subtasks

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation.

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._
