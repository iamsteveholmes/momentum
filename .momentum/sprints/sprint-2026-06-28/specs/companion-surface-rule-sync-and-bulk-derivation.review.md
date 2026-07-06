# === VERIFICATION HEADER (Part A) ===
---
story_slug: companion-surface-rule-sync-and-bulk-derivation
verification_method: document-review
harness_profile: document-review
contract_path: .momentum/sprints/sprint-2026-06-28/specs/companion-surface-rule-sync-and-bulk-derivation.review.md
how_dev_self_checks: |
  Read the project-tier rule file .claude/rules/decision-grade-presentation.md and confirm it
  now carries the companion-surface obligation section, the presentation-form leg subsection, the
  companion-decision-surface budget row, the three added surface-schema rows, and the two added
  non-overridable cascade bullets — matching the canonical rule at
  skills/momentum/references/rules/decision-grade-presentation.md. Confirm no verbosity cap in the
  project rule is weaker (looser) than its canonical counterpart. The bulk-derivation wiring half
  (originally AC4/AC5) is out of scope for this story by a ratified plan-gate decision — the
  project rule sync is the whole delivered scope here.
coverage_disposition: dedicated-run
covered_by_scenario: null
acceptance_criteria_ref: .momentum/stories/companion-surface-rule-sync-and-bulk-derivation.md#acceptance-criteria
platforms: [host]
---

# companion-surface-rule-sync-and-bulk-derivation — Document Review Contract

**Harness Profile:** document-review

> **Method note (verification-standard §2 override, written justification).** The story's
> computed routing was `skill-invoke` because its declared change-types included a
> `skill-instruction` (intake) half. That half — the bulk-derivation wiring (AC4/AC5) — was
> **scoped out by a ratified decision at the `sprint-2026-06-28` plan gate** (intake has no
> over-budget review-document path today; the wiring is split to
> `companion-surface-bulk-derivation-wiring`). The delivered scope is therefore a normative
> **rule-document sync**, whose observable verification is reading/grepping the rule file — the
> textbook document-review case. Driver overridden to `document-review` accordingly.

## Document Under Review

`.claude/rules/decision-grade-presentation.md` (the project-tier copy of the decision-grade
presentation standard), compared against the canonical copy at
`skills/momentum/references/rules/decision-grade-presentation.md`.

## Required Claims

- [ ] The project rule contains a section titled "The Companion-Surface Obligation — Large Review Documents" (the companion-surface obligation).
- [ ] The project rule contains a subsection "Presentation form — the third leg (non-overridable)".
- [ ] The project rule's per-surface budget table contains a row whose first cell reads "Companion decision surface".
- [ ] The project rule's surface-schema table lists the rows "Companion decision surface", "Pre-sprint plan gate", and "Post-sprint results gate".
- [ ] The project rule's cascade-order "what cannot be overridden at any lower scope" list includes both the companion-surface obligation and the presentation-form leg, alongside the caps-vs-floor boundary, the three-required-fields, and the core-convention entries (≥ 5 non-overridable entries total).
- [ ] No verbosity cap value in the project rule is looser than its canonical counterpart (project scope may tighten a cap but never loosen one).

## Required Sections

- [ ] A companion-surface obligation section is present and self-sufficient (states the trigger, the collapse-to-one-line rule for verifiable claims, the ≤ 7 genuine-forks rule, the five required fork fields, and the depth-on-demand backing rule).
- [ ] The presentation-form leg is present and states: render as visual HTML, lead with a plain-language purpose hero, diagram the structure, link (not inline) source artifacts, and anti-rubber-stamp sign-off.
- [ ] The section numbering downstream of the added sections is internally consistent (no duplicate or skipped section numbers introduced by the sync).

## Pass Criteria

A reviewer reading `.claude/rules/decision-grade-presentation.md` can confirm every Required
Claim by inspection (e.g. `grep -c "Companion-Surface Obligation" .claude/rules/decision-grade-presentation.md`
returns ≥ 1; `grep -c "Presentation form — the third leg" …` returns ≥ 1; the budget and schema
rows are present), and a section-by-section comparison against the canonical rule shows the added
sections present and no cap loosened.

## Fail Criteria

The project rule is missing the companion-surface obligation, the presentation-form leg, the
budget row, or the schema rows; or its non-overridable list omits either added leg; or any cap in
the project rule is looser than the canonical rule's; or the sync introduced inconsistent section
numbering.

## Out of Scope (ratified at the plan gate)

The bulk-derivation wiring (original AC4/AC5 — emitting a paired companion surface from an
over-budget review document) is **not** part of this contract. It is recorded N/A and split to
`companion-surface-bulk-derivation-wiring`. This contract passes on the rule sync alone.
