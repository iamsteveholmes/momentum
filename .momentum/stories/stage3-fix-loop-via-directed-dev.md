---
title: Wire the per-story stage-3 fix loop to the directed fixer with escalation routing
story_key: stage3-fix-loop-via-directed-dev
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - skill-instruction
verification_method: skill-invoke
depends_on:
  - directed-fix-invocation-contract
  - dev-fix-mode-entry
  - conduct-stakes-timing-escalation-mechanism
touches:
  - skills/momentum/skills/conductor/workflow.md
---

# Wire the per-story stage-3 fix loop to the directed fixer with escalation routing

## Story

As a Conductor running the per-story build phase,
I want the stage-3 fix loop to drive routine findings through a bounded fix/re-check retry and route stakes-class escalated findings out of that loop onto the escalation channel,
so that ordinary issues get fixed autonomously without a human gate while genuinely high-stakes findings are surfaced (raised, never silently auto-fixed) at the right moment.

## Description

The Conductor owns the in-session, per-story, autonomous build phase. After a story's work product is produced, stage-3 is the per-story fix loop: it takes findings, applies fixes, re-checks, and loops — bounded — until the story is clean or exhausts its retries. Today this loop does not exist as part of the conduct rewrite; this story wires the loop's stage-3 leg to the directed fixer and threads escalation routing through it.

**What this story does.** It wires the per-story stage-3 fix loop (governing spec section 3, Phase B–D, and section 4) to the directed fixer with a retry bound of 3. For routine findings the mechanics are unchanged: fix → re-check → loop, up to 3 attempts, then mark BLOCKED and continue to the next story rather than halting the whole build. On top of that baseline, this story folds in the DEC-036 D1/D2 escalation behavior: an **escalated** finding is a distinct disposition — it is *neither* fixed-clean, *nor* remaining/unfixed-in-loop, *nor* BLOCKED. It is removed from the retry-bound-3 loop entirely and dispatched onto the **escalation channel**.

**Why.** DEC-035 adopted conduct with one human gate at the end and no story-count cap; the auto-fix loop must stay legible. DEC-036 narrowly amends DEC-035 binding decision #1: routine findings stay ALWAYS auto-fixed (silent), but a narrow, high-bar, stakes-gated tier of findings must leave the silent auto-fix path so they are raised, not silently changed. Without this routing, a stakes-class finding (e.g. an auth-isolation regression, an irreversible migration, a force-push) would be silently auto-fixed inside the loop with no human visibility — exactly the failure DEC-036 closes. This story is the stage-3 leg that makes the escaped path real.

**The escalation channel has two timing tiers.** By DEFAULT an escalated finding rides the **end-gate-expanded** tier (tier a): it is carried to the single human end-gate as a decision-card item. ONLY when the finding's timing flag marks it **irreversible-and-imminent** OR **build-invalidating** does it take the **mid-flight** tier (tier b), which invokes the escalation mechanism mid-build instead of waiting for the end. The mid-flight bar stays deliberately narrow; the end-gate-expanded tier is the safety net, so biasing toward the default is correct and intended.

**Pain context.** The "ALWAYS auto-fix" absolute appears in three places across the conduct spec: the schema comment, the dev executor, and this stage-3 branch. If any one of those three legs silently fixes a stakes-class finding, the DEC-036 guarantee is broken. This story threads the stage-3 leg specifically; the other two legs are threaded by their own stories.

**Source decisions:** DEC-035 (adopt conduct; one end gate; no story cap; legible auto-fix loop) and DEC-036 (narrow stakes-gated mid-flight escalation tier; escalated as a new disposition; routine findings stay always auto-fixed; anti-rubber-stamp end-gate).

## Acceptance Criteria

1. For a routine finding, the stage-3 loop applies a fix via the directed fixer, re-checks, and loops; if the re-check is clean the finding is resolved and the loop moves on.
2. The stage-3 retry loop is bounded at 3 attempts per finding. A routine finding that is still unresolved after the third attempt is marked BLOCKED, and the build continues to the next story rather than halting.
3. An escalated finding is recorded with the disposition `escalated` — distinct from `fixed`, from remaining/unresolved-in-loop, and from BLOCKED.
4. An escalated finding is removed from the retry-bound-3 loop: no further fix/re-check attempts are run against it inside the loop.
5. An escalated finding is dispatched onto the escalation channel. By default (when its timing flag is not set to a mid-flight condition) it rides the **end-gate-expanded** tier and is carried to the single human end-gate as a decision-card item.
6. An escalated finding whose timing flag marks it **irreversible-and-imminent** OR **build-invalidating** takes the **mid-flight** tier: it invokes the escalation mechanism mid-build instead of continuing the loop or waiting for the end-gate.
7. The mid-flight tier is entered ONLY for the two narrow conditions named in AC 6 (irreversible-and-imminent OR build-invalidating). Any escalated finding not meeting one of those two conditions stays on the default end-gate-expanded tier.
8. The stage-3 loop never silently auto-fixes a stakes-class finding (security/auth-isolation; irreversible/destructive such as migration, delete, force-push, or prod deploy; high-blast-radius/architecture). Such a finding is routed to the escalation channel, not fixed inside the loop.
9. Routine findings (default class) continue to be auto-fixed inside the loop without any human gate — the always-auto-fix behavior for routine findings is preserved unchanged.
10. The escalation routing is non-destructive to the routine path: introducing an escalated finding for one item does not stop routine findings on other items from completing their normal fix/re-check/bound-3 cycle.

## Tasks / Subtasks

- [ ] Locate the stage-3 fix-loop leg in the conductor workflow (the per-story Phase B–D fix loop, governing spec section 3 + section 4) and confirm it is the leg that drives fix → re-check → loop with a retry bound.
- [ ] Wire the loop's fix step to the directed fixer using the directed-fix invocation contract (dependency: directed-fix-invocation-contract) operating in fix mode (dependency: dev-fix-mode-entry).
- [ ] Encode the retry bound as 3: per-finding attempts cap at 3, after which the finding is marked BLOCKED and the build continues to the next story (no whole-build halt).
- [ ] Add the `escalated` disposition as a first-class outcome of stage-3, distinct from `fixed`, from remaining/unresolved, and from BLOCKED.
- [ ] Add the branch that removes an escalated finding from the retry-bound-3 loop (no further fix/re-check attempts inside the loop).
- [ ] Add the escalation-channel dispatch: default route is the end-gate-expanded tier (carry the finding to the single human end-gate as a decision-card item).
- [ ] Add the mid-flight branch: when the finding's timing flag marks it irreversible-and-imminent OR build-invalidating, invoke the escalation mechanism (dependency: conduct-stakes-timing-escalation-mechanism) mid-build instead of waiting for the end-gate.
- [ ] Constrain the mid-flight branch to ONLY those two narrow conditions; everything else stays on the default end-gate-expanded tier.
- [ ] Add the guard that prevents any silent auto-fix of a stakes-class finding inside the loop (security/auth-isolation; irreversible/destructive; high-blast-radius/architecture) — such findings route to the escalation channel.
- [ ] Confirm routine findings still auto-fix inside the loop with no human gate (preserve the always-auto-fix behavior for the default class).
- [ ] Confirm the escalation routing on one item does not interrupt routine fix/re-check/bound-3 cycles on other items.

## Dev Notes

This story modifies a skill-instruction artifact: `skills/momentum/skills/conductor/workflow.md`. The Conductor is the top-level session orchestrator that owns the build phase and the single human end-gate; it spawns subagents and writes no code itself. The stage-3 fix loop is one leg of the per-story build phase.

**Governing spec sections (cite by number):**
- Section 3, Phase B–D — the per-story fix loop (fix → re-check → loop) that this story's stage-3 leg implements.
- Section 4 — the fix-loop mechanics, including the retry bound and BLOCKED-then-continue behavior.

**Routine-path mechanics (unchanged baseline).** Fix → re-check → loop; retry bound 3; on exhaustion mark BLOCKED and continue to the next story (never halt the whole build). The fix step is delegated to the directed fixer via the directed-fix invocation contract, operating in fix mode.

**Escalation routing (DEC-036 D1/D2).** An escalated finding is a distinct disposition — neither fixed-clean, nor remaining, nor BLOCKED. It is routed OUT of the retry-bound-3 loop onto the escalation channel:
- **Tier a (default): end-gate-expanded.** The finding is carried to the single human end-gate as a decision-card item. This is the safety net and should be the common case.
- **Tier b (narrow): mid-flight.** ONLY when the timing flag marks the finding irreversible-and-imminent OR build-invalidating does it invoke the escalation mechanism mid-build. Bias narrow — never widen these two conditions.

**Vocabulary (use consistently across the workflow text):**
- Stakes classes: security/auth-isolation; irreversible/destructive (migration, delete, force-push, prod deploy); high-blast-radius/architecture; default routine.
- Dispositions: `fixed` | `dismissed` (requires a non-empty rationale) | `triaged-out` | `escalated` (new — raised, not silently fixed).
- Timing tiers: end-gate-expanded (default) | mid-flight (narrow).

**Three-place absolute.** The "ALWAYS auto-fix" absolute appears in three places in the conduct spec: the schema comment, the dev executor, and this stage-3 branch. This story threads only the stage-3 leg; the guard that stakes-class findings are never silently auto-fixed must be honored here even though the other two legs are threaded elsewhere.

**Dependencies.** This story consumes the directed-fix invocation contract (`directed-fix-invocation-contract`), the fixer's fix-mode entry (`dev-fix-mode-entry`), and the stakes/timing escalation mechanism (`conduct-stakes-timing-escalation-mechanism`) that the mid-flight tier invokes. Those are separate stories; this one wires them together at the stage-3 leg.

### References

- Epic: `momentum-sprint-orchestration` — see `_bmad-output/planning-artifacts/epics.json`.
- Decision: DEC-035 — adopt conduct; one human gate at the end; no story-count cap; report organized by user-facing functionality; auto-fix loop must be legible.
- Decision: DEC-036 — narrow, high-bar, stakes-gated mid-flight escalation tier; `escalated` as a new disposition; stakes-class findings leave the silent auto-fix path; routine findings stay always auto-fixed; anti-rubber-stamp end-gate. Amends DEC-035 binding decision #1.
