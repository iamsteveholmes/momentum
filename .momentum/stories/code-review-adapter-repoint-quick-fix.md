---
title: Repoint quick-fix code-review calls to the adapter
story_key: code-review-adapter-repoint-quick-fix
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - skill-instruction
verification_method: skill-invoke
depends_on:
  - code-review-adapter-retire-stub
touches:
  - skills/momentum/skills/quick-fix/workflow.md
---

# Repoint quick-fix code-review calls to the adapter

## Story

As the maintainer of the Momentum quick-fix flow,
I want the quick-fix code-review step to call the bmad-code-review adapter instead of the retired stub,
so that a single-story fix gets the same adapter-normalized findings the rest of the practice relies on, with no orphaned reference to the old code-review path.

## Description

The quick-fix workflow runs a code-review step as part of its streamlined define-specify-implement-validate-merge flow. Today that step still points at the old code-review stub. A prior story (`code-review-adapter-retire-stub`) retires that stub and stands up the bmad-code-review adapter as the canonical code-review entry point. Once the stub is gone, any caller still wired to it is a dangling reference: the quick-fix review either fails or runs against a path that no longer carries the normalized-findings contract.

This story closes that gap by repointing the quick-fix code-review step to the adapter. After this change, when a developer runs quick-fix and reaches the review step, the review goes through the bmad-code-review adapter and returns adapter-normalized findings — the same shape every other Momentum review consumer expects.

This is pure call-site wiring. The behavior of the review engine itself, the finding shape, the stakes-class taxonomy, dispositions, and the escalation tiers are all defined upstream by the adapter and the Conductor flow — this story only changes which thing quick-fix calls. Because it is wiring and not review semantics, this story is **unchanged by DEC-036**: the mid-flight escalation tier, dismissal rendering, and anti-rubber-stamp end-gate amendments are properties of the adapter and the Conductor, not of the quick-fix caller. Repointing the call inherits whatever the adapter provides without quick-fix needing to know about those mechanics.

Pain context: leaving quick-fix pointed at a retired stub produces a broken single-story flow — exactly the flow developers reach for when they want the fastest possible turnaround. A silent dangling reference here is worse than a loud failure, because it can surface as "review passed" when the review never actually ran.

Source decisions: DEC-035 (adopt conduct; one human gate; report organized by user-facing functionality; legible auto-fix loop) and DEC-036 (narrow stakes-gated mid-flight escalation tier amends DEC-035 #1; routine findings stay always auto-fixed; report renders dismissals; anti-rubber-stamp end-gate). Governing spec: section 12.

## Acceptance Criteria

1. When the quick-fix flow reaches its code-review step, the step invokes the bmad-code-review adapter as the code-review entry point.
2. The quick-fix code-review step does NOT invoke the retired code-review stub, and no reference to the retired stub remains in the quick-fix flow.
3. Running the quick-fix review end-to-end produces code-review findings in the adapter-normalized form (the same normalized finding shape the adapter emits for any caller), not in the old stub's raw form.
4. The repointed quick-fix review preserves the behaviors the adapter provides without quick-fix re-implementing them — in particular, routine findings remain on the always-auto-fixed path (DEC-036), so quick-fix does not introduce its own gate or suppress the adapter's handling of routine findings.
5. The repointed quick-fix review inherits the adapter's rendering of dismissed findings with their required non-empty rationale (DEC-036), so a dismissed finding surfaced during a quick-fix review is visible with its rationale and is not silently dropped by the quick-fix caller.
6. The repointed quick-fix review inherits the adapter's escalation behavior (DEC-036): if the adapter raises an escalated (raised, not silently fixed) finding, quick-fix surfaces it rather than swallowing or auto-resolving it, and quick-fix does not widen the escalation criteria on its own.
7. The change is confined to the quick-fix call site; it does not alter the adapter's review semantics, finding shape, stakes-class taxonomy, dispositions, or timing tiers.

## Tasks / Subtasks

- [ ] Locate the code-review step in `skills/momentum/skills/quick-fix/workflow.md`.
- [ ] Replace the reference to the retired code-review stub with an invocation of the bmad-code-review adapter as the code-review entry point (AC1, AC2).
- [ ] Remove any remaining mention, fallback, or comment that points the quick-fix flow at the retired stub (AC2).
- [ ] Ensure the repointed step consumes and surfaces the adapter's normalized findings unchanged — do not transform, re-shape, or re-summarize the adapter output in the quick-fix caller (AC3, AC7).
- [ ] Verify the quick-fix caller adds no gate, filter, or suppression around routine findings — routine findings must stay on the adapter's always-auto-fixed path (AC4).
- [ ] Verify the quick-fix caller passes through dismissed findings (with rationale) and escalated findings from the adapter without dropping or auto-resolving them, and without widening escalation criteria (AC5, AC6).
- [ ] Run the quick-fix flow to its review step and confirm the review runs through the adapter and returns adapter-normalized findings (AC1, AC3).
- [ ] Confirm no broken or dangling reference to the retired stub remains anywhere in the quick-fix flow (AC2).

## Dev Notes

This is a call-site repoint only. The work lives entirely in `skills/momentum/skills/quick-fix/workflow.md`, at the code-review step. The change_type is `skill-instruction` because it edits workflow instruction text (which skill the step calls), not an agent body or a tool. Verification is `skill-invoke`: run the quick-fix flow and observe that its review step goes through the adapter and yields normalized findings.

Dependency: `code-review-adapter-retire-stub` must land first. That story retires the old stub and establishes the bmad-code-review adapter as the canonical entry point with its normalized-findings contract. This story assumes the adapter exists and is the thing to call; it must not recreate or wrap the stub.

Governing spec section: **12** (code-review adapter call-site wiring). Per the brief, this story is the quick-fix caller repoint described in section 12.

**Unchanged by DEC-036.** This is call-site wiring. The DEC-036 amendments — the narrow stakes-gated mid-flight escalation tier (irreversible-and-imminent OR build-invalidating ONLY), report rendering of dismissals with required non-empty rationale, and the anti-rubber-stamp end-gate — are all properties of the bmad-code-review adapter and the Conductor flow, not of the quick-fix caller. By repointing quick-fix at the adapter, the quick-fix review inherits those behaviors for free. The quick-fix caller must NOT re-implement, narrow, or widen any of them: routine findings stay always auto-fixed (DEC-036), dismissals and their rationale render through, and escalated findings are surfaced, not swallowed. The ACs encode these as pass-through obligations on the caller (AC4–AC6) precisely so the wiring does not accidentally change adapter semantics (AC7).

Vocabulary anchors (defined upstream, inherited here): stakes classes = security/auth-isolation; irreversible/destructive; high-blast-radius/architecture; default routine. Dispositions = fixed | dismissed (required non-empty rationale) | triaged-out | escalated (raised, not silently fixed). Timing tiers = end-gate-expanded (default) | mid-flight (narrow). Quick-fix does not define any of these — it consumes the adapter's output that carries them.

### References

- Epic: `momentum-sprint-orchestration` — `_bmad-output/planning-artifacts/epics.json`.
- DEC-035 — adopt conduct; one human end-gate; no story-count cap; report organized by user-facing functionality; legible auto-fix loop (records what it changed AND dismissed).
- DEC-036 — amends DEC-035 #1: narrow, high-bar, stakes-gated mid-flight escalation tier permitted; stakes-class findings leave the silent auto-fix path; report renders dismissals; anti-rubber-stamp end-gate; routine findings stay always auto-fixed; mid-flight bar stays narrow (irreversible-and-imminent OR build-invalidating ONLY).
- Governing spec section 12 — code-review adapter call-site wiring (quick-fix caller repoint).
