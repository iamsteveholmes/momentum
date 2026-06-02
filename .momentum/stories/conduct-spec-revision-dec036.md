---
title: Revise the conduct spec to design to the DEC-036 stakes-and-timing exception
story_key: conduct-spec-revision-dec036
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: maintenance
change_type:
  - specification
verification_method: document-review
depends_on: []
touches:
  - _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
---

# Revise the conduct spec to design to the DEC-036 stakes-and-timing exception

## Story

As a developer building the conduct engine,
I want `sprint-dev-redesign-spec.md` revised so its design absorbs the DEC-036 stakes-and-timing exception,
so that the conduct build stories are not implemented against a spec that still contradicts the decision they are meant to realize.

## Description

**What:** Revise the conduct design spec — `_bmad-output/planning-artifacts/sprint-dev-redesign-spec.md` — so that four sections (§1 binding decisions, §4 fixer schema, §8 gate model, §9 report model) absorb the DEC-036 stakes-and-timing exception, and add a reconciliation note that ties each change back to its source decision.

**Why:** DEC-035 adopted conduct with an absolute "ONE human gate at the end / zero intermediate gates" stance and an absolute "legitimate findings are ALWAYS auto-fixed" stance. DEC-036 amends DEC-035 binding decision #1 narrowly: it permits a NARROW, high-bar, stakes-gated mid-flight escalation tier, requires the report to render dismissals, and adds an anti-rubber-stamp end-gate forcing function. The conduct spec still designs to the pre-amendment absolutism — §8 still says "zero intermediate gates" and §4 still says "ALWAYS auto-fixed." Every engine story in this sprint reads from this spec. If the spec is not revised first, the build agents would faithfully implement a design that contradicts the binding decision.

**Pain context:** No story in the original 52-item breakdown owned this revision — each per-leg breakdown agent saw only its slice of the spec, so none flagged the spec-revision-as-a-unit-of-work. Building the engine stories against a contradictory spec would have every build agent silently re-encode the very absolutism DEC-036 relaxed. This story is the PRE-BUILD GATE: it must land FIRST, before/alongside the schema-root story, so the schema and engine stories build against a reconciled spec.

**Source decisions:** DEC-035 (adopt conduct; one end-gate; no story-count cap; functionality-organized report; legible auto-fix loop) and DEC-036 (narrow stakes-gated mid-flight escalation tier; report renders dismissals; anti-rubber-stamp end-gate; routine findings stay always auto-fixed; anti-firehose intent preserved, only the absolutism relaxed). The DEC-036 Reconciliation table is the model for the reconciliation note this story adds.

## Acceptance Criteria

1. Section 1 (binding decisions) of `sprint-dev-redesign-spec.md` is revised so that the prior "zero intermediate gates / one human gate at the end" absolute is replaced by: a single human end-gate REMAINS the default, AND a narrow, high-bar, stakes-gated mid-flight escalation tier is permitted as the sole exception.

2. Section 1 states the mid-flight bar explicitly and narrowly: a finding may escalate mid-flight ONLY if it is irreversible-and-imminent OR build-invalidating. No other condition widens the mid-flight tier.

3. Section 1 states that routine findings are still ALWAYS auto-fixed silently, and that stakes-class legitimate findings are RAISED (surfaced/escalated), not silently auto-fixed.

4. Section 4 (fixer schema) no longer asserts that a legitimate finding is "ALWAYS auto-fixed (decision 1)"; the absolute is relaxed so that disposition depends on the finding's stakes class and timing tier.

5. Section 4 documents the stakes finding-classification: three stakes classes — (a) security / auth-isolation, (b) irreversible / destructive (migration, delete, force-push, prod deploy), (c) high-blast-radius / architecture — plus the default "routine" class for everything else.

6. Section 4 documents the full disposition set, including the NEW `escalated` disposition (raised, not silently fixed) alongside `fixed`, `dismissed`, and `triaged-out`.

7. Section 4 documents a timing-tier marker on each finding with two values: `end-gate-expanded` (the default) and `mid-flight` (the narrow exception).

8. Section 4 documents that when a finding's disposition is `dismissed`, a non-empty rationale is REQUIRED (an empty or missing dismissal rationale is invalid).

9. Section 8 (gate model) documents the narrow mid-flight escalation tier ALONGSIDE the single human end-gate, and states the narrow bar (irreversible-and-imminent OR build-invalidating only), making clear the end-gate is the default and the mid-flight tier is the rare exception and safety-net-by-end-gate-expansion is the norm.

10. Section 9 (report model) documents that dismissed findings are RENDERED in the report (the "D3" dismissed-rendering requirement), so the auto-fix loop is legible about what it dismissed and not only what it changed.

11. Section 9 documents the anti-rubber-stamp end-gate forcing function (the "D4" requirement) — the end-gate is structured so the human cannot trivially rubber-stamp it.

12. Section 9 documents the decision-grade presentation caps and the self-sufficiency floor (the "D5" requirement) — the report bounds how much is presented at the gate and guarantees enough context to decide without leaving the report.

13. A reconciliation note is added that ties EACH of the above changes back to DEC-035 binding decision #1 and to DEC-036, mirroring the structure of the DEC-036 Reconciliation table (each spec change mapped to the decision it satisfies).

14. The anti-firehose intent is preserved throughout: the revised spec keeps the bias toward narrowness — routine findings stay always auto-fixed, and the mid-flight tier is never widened beyond the two named conditions.

## Tasks / Subtasks

- [ ] Read the current `sprint-dev-redesign-spec.md` §1, §4, §8, §9 to locate the absolutist language to revise.
- [ ] Revise §1 (binding decisions): replace "zero intermediate gates / one human end-gate" absolute with "end-gate remains default + narrow stakes-gated mid-flight exception"; state the narrow bar (irreversible-and-imminent OR build-invalidating only); state routine-always-auto-fixed and stakes-raised-not-silently-fixed. (ACs 1–3)
- [ ] Revise §4 (fixer schema): relax "legitimate → ALWAYS auto-fixed (decision 1)"; document the 3 stakes classes + routine default; add the `escalated` disposition to the disposition set; add the timing-tier marker (`end-gate-expanded` default | `mid-flight`); require a non-empty rationale when disposition = `dismissed`. (ACs 4–8)
- [ ] Revise §8 (gate model): document the mid-flight escalation tier alongside the single end-gate; state the narrow bar; make clear end-gate is default and mid-flight is the rare exception. (AC 9)
- [ ] Revise §9 (report model): document dismissed rendering (D3), the anti-rubber-stamp end-gate forcing function (D4), and the decision-grade presentation caps + self-sufficiency floor (D5). (ACs 10–12)
- [ ] Add a reconciliation note mapping each spec change to DEC-035 binding decision #1 and DEC-036, mirroring the DEC-036 Reconciliation table. (AC 13)
- [ ] Re-read the four revised sections end-to-end to confirm the anti-firehose / narrow-bias intent is preserved and no language widens the mid-flight tier. (AC 14)

## Dev Notes

This is a specification-only revision. The deliverable is the edited markdown file `_bmad-output/planning-artifacts/sprint-dev-redesign-spec.md`; no skills, agents, or executable code change in this story. Verification is by document review of the revised spec.

**Sections to revise (cite by number, per the authoring brief — do not open the spec to renumber):**

- **§1 — binding decisions.** Currently encodes DEC-035's "one human gate at the end / zero intermediate gates" as an absolute. Revise to: end-gate-as-default + a narrow stakes-gated mid-flight exception; routine always auto-fixed; stakes-class legitimate findings raised, not silently fixed. (ACs 1–3)
- **§4 — fixer schema.** Currently asserts "legitimate → ALWAYS auto-fixed (decision 1)". Relax that absolute; add the stakes finding-classification (security/auth-isolation; irreversible/destructive; high-blast-radius/architecture; default routine), the new `escalated` disposition, the timing-tier marker (`end-gate-expanded` | `mid-flight`), and the required non-empty dismissal rationale. (ACs 4–8)
- **§8 — gate model.** Currently single end-gate, "zero intermediate gates." Add the narrow mid-flight escalation tier alongside the end-gate, stating the narrow bar (irreversible-and-imminent OR build-invalidating only). (AC 9)
- **§9 — report model.** Add dismissed rendering (D3), the anti-rubber-stamp end-gate forcing function (D4), and the decision-grade presentation caps + self-sufficiency floor (D5). (ACs 10–12)
- **Reconciliation note.** Mirror the DEC-036 Reconciliation table: map each spec change to DEC-035 binding decision #1 and DEC-036. (AC 13)

**Vocabulary to use consistently** (from the source decisions): stakes classes = security/auth-isolation, irreversible/destructive, high-blast-radius/architecture, default routine. Dispositions = fixed | dismissed (non-empty rationale required) | triaged-out | escalated (new). Timing tiers = end-gate-expanded (default) | mid-flight (narrow).

**Hard constraint — keep the mid-flight bar narrow.** DEC-036 relaxes only the absolutism, not the anti-firehose intent. The mid-flight tier admits exactly two conditions: irreversible-and-imminent OR build-invalidating. Do not introduce any third condition, and do not soften "routine findings are always auto-fixed." The end-gate-expanded tier is the safety net; bias every revision toward narrowness.

**Ordering note for the sprint.** This story is the PRE-BUILD GATE and lands first. The schema-root story and the engine stories read these four sections; revising them here prevents the build agents from re-encoding the pre-amendment absolutism.

### References

- Epic: `momentum-sprint-orchestration` — `_bmad-output/planning-artifacts/epics.json`.
- Decision: DEC-035 (adopt conduct; one human end-gate; no story-count cap; report organized by user-facing functionality; legible auto-fix loop showing what it changed AND dismissed) — `_bmad-output/planning-artifacts/decisions/`.
- Decision: DEC-036 (amends DEC-035 binding decision #1: narrow, high-bar, stakes-gated mid-flight escalation tier; report renders dismissals; anti-rubber-stamp end-gate; routine findings stay always auto-fixed; anti-firehose intent preserved) and its Reconciliation table — `_bmad-output/planning-artifacts/decisions/`.
- Target artifact: `_bmad-output/planning-artifacts/sprint-dev-redesign-spec.md` (§1, §4, §8, §9).
