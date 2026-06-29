---
title: "Companion surface — sync project rule + wire bulk-derivation paths to template"
story_key: companion-surface-rule-sync-and-bulk-derivation
status: backlog
epic_slug: momentum-impetus-experience
feature_slug:
story_type: practice
depends_on: []
touches:
  - .claude/rules/decision-grade-presentation.md
  - skills/momentum/skills/intake/
---

# Companion surface — sync project rule + wire bulk-derivation paths to template

<!-- DECOMPOSITION STUB: This story was decomposed from
     visual-hitl-gates-presentation-form-standard-leg (Part A remainder). It is a
     planning stub, NOT a dev-ready story. Run momentum:create-story to enrich before dev. -->

_This story is a backlog stub decomposed from `visual-hitl-gates-presentation-form-standard-leg`.
Run `momentum:create-story` on it to make it dev-ready. Do NOT assign to a developer until
create-story has enriched it._

## Story

As the developer (the practice owner),
I want the **project-tier** decision-grade-presentation rule brought up to the global/canonical
version (Companion-Surface Obligation + presentation-form leg), and the bulk-derivation paths
(`intake` / ad-hoc plan workflows) wired to emit the companion surface from the shipped template,
so that every tier enforces what the standard now mandates and no review-document path silently
escapes the companion-surface obligation.

## Description

Part A of the parent story (extend the standard) was **delivered** on branch
`feat/companion-decision-surface-standard` (commit `da70fed`): the canonical rule gained §5
(Companion-Surface Obligation), §5.1 (presentation-form leg), §2.2 row 9, and the
`companion-decision-surface.html` template. The **remainder** is propagation:

1. **Project-rule drift.** The project copy `.claude/rules/decision-grade-presentation.md` is
   **stale** — it stops at the 8-surface table and carries no Companion-Surface Obligation,
   no presentation-form leg, and no row 9. The project tier therefore silently under-enforces
   what global now requires. Sync it to the canonical version (project scope may tighten a cap but
   not loosen it, and cannot drop the non-overridable legs).
2. **Bulk-derivation wiring.** Wire the bulk-derivation paths (`intake` / ad-hoc plan workflows)
   that emit review documents to also emit the companion surface from
   `skills/momentum/references/templates/companion-decision-surface.html` — so a large review
   document is never handed over without its paired decision surface (the §5 defect this closes).

**Parent / provenance:** `visual-hitl-gates-presentation-form-standard-leg` (Part A remainder);
delivered foundation in `da70fed` (`skills/momentum/references/rules/decision-grade-presentation.md`
§5/§5.1, template); stale target `.claude/rules/decision-grade-presentation.md`.

## Acceptance Criteria

_DRAFT — captured from the parent story Part A remainder; requires rewrite via create-story before dev-ready._

- The project-tier rule `.claude/rules/decision-grade-presentation.md` carries the Companion-Surface Obligation (§5), the presentation-form leg (§5.1), and the §2.2 row-9 budget — consistent with the canonical/global version (no loosening of non-overridable legs).
- A grep for "Companion-Surface Obligation" (and "presentation form — the third leg") against the project rule returns a match (it currently returns zero).
- The bulk-derivation paths that emit a review document (e.g. `intake` / ad-hoc plan workflows) emit a paired companion decision surface derived from the shipped template.
- A review document produced by a wired bulk path is accompanied by its companion surface — emitting the large document alone is treated as a defect per §5.

## Tasks / Subtasks

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation.

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._
