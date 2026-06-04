---
title: Conductor Phase-1 pre-flight HALTs and non-interactive git reconcile
story_key: conduct-preflight-halts
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - skill-instruction
verification_method: skill-invoke
depends_on:
  - conduct-skill-scaffold-and-spine
touches:
  - skills/momentum/skills/conductor/workflow.md
---

# Conductor Phase-1 pre-flight HALTs and non-interactive git reconcile

## Story

As the developer running a conduct sprint,
I want the Conductor to perform every developer-facing cannot-start check during Phase 1 and to reconcile git state non-interactively before any build work,
so that the build phase only begins from a clean, validated starting point and I am never interrupted by a developer-facing HALT once building is underway — except the one narrow stakes-gated mid-flight escalation tier.

## Description

The Conductor is the top-level session orchestrator that owns the build phase, all git mutation, and the single human end-gate. This story defines **Phase 1 — pre-flight** — the only place left in the conduct flow where the Conductor surfaces developer-facing HALTs that prevent the sprint from starting, plus the non-interactive git reconcile-on-start that brings the working tree to a known-good state before any story is dispatched.

**What this builds.** Phase 1 of the Conductor `workflow.md` skill instructions: five cannot-start guards (H1–H5) that fire before any build work, and the reconcile-on-start procedure that auto-resets and re-dispatches stale in-progress stories without prompting the developer.

**The HALTs (H1–H5).** These are cannot-start guards: a missing sprint, a sprint that has not been activated, missing required approvals, and a stalled/inconsistent state. They are the *only* developer-facing HALTs that fire before build work begins. If any fires, the Conductor stops and reports the reason; the developer resolves it and re-invokes.

**Reconcile on start.** When Phase 1 passes the cannot-start guards, the Conductor reconciles git state non-interactively. There is no resume/cleanup prompt. A story left in an `in-progress` state from a prior, interrupted session is automatically reset to a clean dispatchable state and re-dispatched into the build phase. The developer is not asked to choose resume vs. cleanup — the reconcile decides and proceeds.

**Why this matters (pain context).** The legacy sprint-dev flow interrupted the developer repeatedly: a resume/cleanup prompt on every restart, plus a steady stream of mid-build questions. DEC-035 collapses the human touchpoints to a single end-gate and forbids developer-facing HALTs outside pre-flight, so the developer can leave the build running and return to one organized end-gate. The reconcile must therefore be silent and decisive: it picks up where a prior session left off without a question.

**The DEC-036 subtlety this story must encode.** DEC-035 binding decision #1 stated, as an invariant, that there is **no developer-facing HALT outside Phase 1**. The conduct breakdown already softened that invariant **once** — but that first carve-out was for the section-7 **Conductor-facing** freeze guard (an internal guard the Conductor itself observes, not the developer). DEC-036 amends DEC-035 #1 a second time, and this second carve-out is **developer-facing**: it permits a narrow, high-bar, stakes-gated **mid-flight escalation tier** that can pause the build and raise a stakes-class finding to the developer mid-build. So the invariant in this story must be re-softened to carve out **both** distinct exceptions: the Conductor-facing section-7 freeze guard **and** the developer-facing mid-flight escalation tier. The mid-flight tier stays narrow by construction — **irreversible-and-imminent OR build-invalidating only**. No other developer-facing HALT may exist outside Phase 1.

**Source decisions.** DEC-035 (adopt conduct; one human gate at the end; no developer HALT outside pre-flight; anti-firehose auto-fix). DEC-036 (narrow stakes-and-timing mid-flight escalation tier amends DEC-035 #1).

## Acceptance Criteria

1. During Phase 1 — pre-flight, the Conductor evaluates five cannot-start guards (H1 no active sprint, H2 sprint not activated, H3 missing required approvals, H4/H5 stalled or inconsistent state) **before any build work begins**; if any guard condition holds, the Conductor stops, reports which guard fired and why, and does not dispatch any story.

2. When all five cannot-start guards pass, the Conductor proceeds to build; it does not re-evaluate H1–H5 or surface any new cannot-start guard after build work has started.

3. The git reconcile-on-start runs **non-interactively**: the developer is never shown a resume-vs-cleanup prompt and is never asked to choose how to handle prior state. The reconcile reaches its decision and proceeds on its own.

4. A story left in an `in-progress` state by a prior interrupted session is **automatically reset** to a clean, dispatchable state and **re-dispatched** into the build phase as part of reconcile-on-start — with no developer prompt.

5. After reconcile-on-start completes, the working tree and story states are in a known-good starting condition, and the build phase begins from there.

6. The Conductor's workflow states the invariant as: **no developer-facing HALT exists outside Phase 1, EXCEPT the stakes-and-timing mid-flight escalation tier** (the narrow, high-bar developer-facing pause).

7. The same invariant statement **also** explicitly carves out the section-7 **Conductor-facing** freeze guard as a distinct, separate exception — so the invariant names **both** carve-outs: (a) the Conductor-facing section-7 freeze guard, and (b) the developer-facing mid-flight escalation tier.

8. The carved-out developer-facing mid-flight escalation tier is constrained to **irreversible-and-imminent OR build-invalidating** triggers only; the workflow states this narrow bar and does not permit the tier to fire for routine or any broader class of finding.

9. Apart from the H1–H5 pre-flight cannot-start guards and the single carved-out mid-flight escalation tier, **no other developer-facing HALT exists anywhere in the conduct flow** — routine findings are never raised to the developer mid-build and there is no resume/cleanup prompt, no per-story confirmation, and no mid-build question outside the narrow tier.

## Tasks / Subtasks

- [ ] Add the **Phase 1 — pre-flight** section to `skills/momentum/skills/conductor/workflow.md` (AC 1, 2)
  - [ ] Define guard **H1** — no active sprint: condition, the stop message, and that no story is dispatched
  - [ ] Define guard **H2** — sprint not activated: condition, stop message, no dispatch
  - [ ] Define guard **H3** — missing required approvals: condition, stop message, no dispatch
  - [ ] Define guards **H4/H5** — stalled / inconsistent state: condition(s), stop message, no dispatch
  - [ ] State that H1–H5 are evaluated before any build work and are not re-evaluated once building has started
- [ ] Add the **reconcile-on-start** procedure to Phase 1 (AC 3, 4, 5)
  - [ ] Specify the reconcile runs non-interactively — explicitly forbid any resume/cleanup prompt or developer choice
  - [ ] Specify that an `in-progress` story from a prior interrupted session is auto-reset to a clean dispatchable state
  - [ ] Specify that the auto-reset story is re-dispatched into the build phase without a prompt
  - [ ] Specify the known-good end condition reconcile must reach before build begins
- [ ] Encode the **re-softened invariant** in the workflow (AC 6, 7, 8)
  - [ ] Write the invariant as "no developer-facing HALT outside Phase 1 EXCEPT the mid-flight escalation tier"
  - [ ] Explicitly name BOTH carve-outs: (a) Conductor-facing section-7 freeze guard, (b) developer-facing mid-flight escalation tier
  - [ ] State the narrow bar for the developer-facing tier: irreversible-and-imminent OR build-invalidating ONLY
- [ ] Add the **no-other-HALT** closure statement (AC 9)
  - [ ] State that no developer-facing HALT exists outside Phase 1 other than H1–H5 and the single mid-flight tier
  - [ ] State routine findings are never raised to the developer mid-build; no resume/cleanup prompt, no per-story confirmation, no other mid-build questions
- [ ] Self-check the workflow by invoking the Conductor against the cannot-start and reconcile scenarios and confirming observable behavior matches AC 1–9

## Dev Notes

This story implements **Phase 1 — pre-flight** of the Conductor skill. The Conductor writes no code itself; it is the orchestrator that owns the build phase, all git mutation, and the single human end-gate. Phase 1 runs before any story is dispatched.

**Governing spec sections (cited by number from the brief):**
- **Section 6 — "Git lifecycle"** (including "Reconcile on start"): the non-interactive git reconcile that auto-resets and re-dispatches stale `in-progress` stories without a resume/cleanup prompt, and the git-state handling for bringing the working tree to a known-good condition (AC 3, 4, 5).
- **Section 7**: the **Conductor-facing** freeze guard — the *first* carve-out from the DEC-035 #1 invariant. This story does not implement section 7; it references it so the invariant statement names it as carve-out (a) (AC 7).

**The two carve-outs, kept distinct.** DEC-035 #1 originally asserted a single, absolute invariant: no developer-facing HALT outside Phase 1. There are now two separate exceptions and the workflow must name both without conflating them:
- Carve-out (a) — **Conductor-facing** section-7 freeze guard. Internal to the Conductor; the developer does not see it. This was the breakdown's first softening of the invariant.
- Carve-out (b) — **developer-facing** mid-flight escalation tier (DEC-036). A narrow, high-bar, stakes-gated pause that *does* reach the developer mid-build. DEC-036 forces this second, distinct softening.

These are different in kind (who observes the HALT) and must be listed as two separate exceptions, not merged into one.

**Narrow bar discipline.** The developer-facing mid-flight tier fires only for **irreversible-and-imminent** (a stakes-class action about to happen that cannot be undone — e.g. destructive migration, delete, force-push, prod deploy) **OR build-invalidating** triggers. It is biased narrow on purpose: the default safety net is the end-gate-expanded tier (the single human end-gate at the end of the build), not a mid-flight pause. Routine findings stay on the silent auto-fix path and are never raised mid-build. The workflow must never widen this tier.

**Vocabulary to use consistently in the workflow text:**
- Stakes classes: security/auth-isolation; irreversible/destructive (migration, delete, force-push, prod deploy); high-blast-radius/architecture; default routine.
- Timing tiers: end-gate-expanded (default) | mid-flight (narrow).

**Black-box note for the implementer.** All of H1–H5 and the reconcile behavior are observable by invoking the Conductor and reading its outputs and git/story state — no source inspection is needed to confirm the behavior.

### References

- Epic **momentum-sprint-orchestration** — `_bmad-output/planning-artifacts/epics.json` (the conduct / sprint orchestration epic this story belongs to).
- **DEC-035** — adopt conduct; one human gate at the end; no developer-facing HALT outside pre-flight; report organized by user-facing functionality; legible anti-firehose auto-fix loop. (Binding decision #1 is the invariant amended here.) — `_bmad-output/planning-artifacts/decisions/`
- **DEC-036** — narrow, high-bar, stakes-and-timing mid-flight escalation tier amends DEC-035 #1; stakes-class findings leave the silent auto-fix path; anti-rubber-stamp end-gate; mid-flight bar stays narrow (irreversible-and-imminent OR build-invalidating only). — `_bmad-output/planning-artifacts/decisions/`
