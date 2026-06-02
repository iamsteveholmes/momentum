---
title: Conductor contract-freeze check before per-story verification
story_key: conduct-contract-freeze-check
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - skill-instruction
verification_method: skill-invoke
depends_on:
  - conduct-build-phase-frontier
touches:
  - skills/momentum/skills/conductor/workflow.md
---

# Conductor contract-freeze check before per-story verification

## Story

As the developer running a conduct sprint,
I want the Conductor to confirm that each story's verification contract still matches the contract that was frozen at assignment time before it verifies the story,
so that no story is ever verified against a contract that drifted after it was frozen, and a mismatch is caught by the Conductor itself rather than silently passing or interrupting me.

## Description

The Conductor is the top-level session orchestrator that owns the build phase, all git mutation, and the single human end-gate. Each story carries a verification contract, and at assignment time the Conductor records a frozen fingerprint of that contract (`frozen_sha256`). This story defines the **contract-freeze check**: before the Conductor verifies a story, it re-computes the fingerprint of the contract file on disk and compares it to the recorded `frozen_sha256`. The check guarantees that verification always runs against the exact contract that was frozen at assignment — not a contract that was edited, regenerated, or otherwise drifted after freezing.

**What this builds.** A step in the Conductor `workflow.md` skill instructions, inside the per-story verification sequence: compute `sha256` of the contract file, compare it to the assignment's `frozen_sha256`, and branch on match vs. mismatch.

**Match path.** When the recomputed `sha256` equals `frozen_sha256`, the contract is unchanged and verification proceeds normally.

**Mismatch path.** When the two fingerprints differ, the contract has drifted since it was frozen. The Conductor does **not** silently re-verify against the changed contract — that would mean verifying a story against a moving target. Instead, the mismatch surfaces **to the Conductor** — this is a **Conductor-facing** integrity stop, the one sanctioned non-developer halt. It is not a developer-facing HALT and it is not a stakes-class escalation; it is the Conductor catching its own integrity violation before it can corrupt the verification result.

**Why this matters (pain context).** Conduct collapses the human touchpoints to a single end-gate (DEC-035): the developer leaves the build running and returns to one organized report. For that to be trustworthy, every verification result the report rests on must be sound. If a contract could silently change between freeze and verification, a story could "pass" against a contract nobody agreed to, or "fail" against one that was never assigned — and the end-gate would inherit a corrupted result. The freeze check is the integrity backstop that keeps the end-gate honest, and it is owned by the Conductor so it never needs to bother the developer.

**Why this is Conductor-facing, not developer-facing.** The conduct flow forbids developer-facing HALTs outside Phase 1 pre-flight, with two narrow carve-outs: the Conductor-facing section-7 freeze guard, and the developer-facing mid-flight escalation tier (DEC-036). This story implements that **first** carve-out — the Conductor-facing freeze guard from spec section 7, step 2. It is the integrity check the Conductor performs on itself; the developer is never paused by it.

**Source decisions.** DEC-035 (adopt conduct; one human gate at the end; soundness of per-story verification underpins the single end-gate). DEC-036 (narrow stakes-and-timing mid-flight escalation tier) — see Dev Notes for why DEC-036 leaves this story unchanged.

## Acceptance Criteria

1. Before a story is verified, the Conductor computes the `sha256` of that story's contract file and compares it to the `frozen_sha256` recorded for the story at assignment time.

2. When the recomputed `sha256` equals the assignment's `frozen_sha256`, verification proceeds normally and the build is not interrupted.

3. When the recomputed `sha256` does **not** equal the assignment's `frozen_sha256`, the Conductor does **not** silently re-verify the story against the changed contract — it stops short of producing a verification result from the drifted contract.

4. On a fingerprint mismatch, the integrity stop surfaces **to the Conductor** — it is a Conductor-facing stop, **not** a developer-facing HALT and **not** a stakes-class mid-flight escalation; the developer is not paused by it.

5. The contract-freeze check is performed **per story**, as the first step of that story's verification, so the comparison always reflects the specific story being verified and its own frozen fingerprint.

6. This freeze check is the **one sanctioned non-developer halt** in the verification path: a mismatch does not raise a stakes-class escalation, does not enter the silent auto-fix loop, and does not get dismissed — it is an integrity stop the Conductor owns and resolves before any verification result is recorded.

## Tasks / Subtasks

- [ ] Add the **contract-freeze check** step to the per-story verification sequence in `skills/momentum/skills/conductor/workflow.md` (AC 1, 5)
  - [ ] Specify computing `sha256` of the story's contract file at verification time
  - [ ] Specify comparing the computed `sha256` against the `frozen_sha256` recorded for that story at assignment
  - [ ] Specify the check runs as the first step of verifying each story, per story
- [ ] Specify the **match path** (AC 2)
  - [ ] State that an equal fingerprint means the contract is unchanged and verification proceeds without interruption
- [ ] Specify the **mismatch path** (AC 3, 4, 6)
  - [ ] State the Conductor must NOT silently re-verify against the changed contract
  - [ ] State the mismatch surfaces to the Conductor (Conductor-facing), not to the developer, and is not a HALT the developer sees
  - [ ] State the mismatch is NOT a stakes-class escalation, NOT routed to the silent auto-fix loop, and NOT a dismissable finding — it is an integrity stop the Conductor resolves
  - [ ] State no verification result is recorded for a story whose contract failed the freeze check
- [ ] Cross-reference the invariant carve-out (AC 4, 6)
  - [ ] Note this implements the Conductor-facing section-7 freeze guard — the first, distinct carve-out from the DEC-035 #1 invariant — so it is explicitly NOT a developer-facing pause
- [ ] Self-check by invoking the Conductor with (a) an unmodified contract and (b) a contract altered after its fingerprint was frozen, confirming observable behavior matches AC 1–6

## Dev Notes

This story implements the **contract-freeze check** that runs at the top of each story's verification in the Conductor skill. The Conductor writes no code itself; it is the orchestrator that owns the build phase, all git mutation, and the single human end-gate. The freeze check is an integrity gate the Conductor applies to itself before trusting a verification result.

**Governing spec section (cited by number from the brief):**
- **Section 7, step 2** — the contract-freeze check: assert `sha256(contract) == frozen_sha256` before per-story verification; on mismatch, surface to the Conductor (not the developer). This is the **one sanctioned non-developer halt** and the **first** carve-out from the DEC-035 #1 "no developer-facing HALT outside pre-flight" invariant (AC 1–6).

**Conductor-facing, by design.** The conduct invariant forbids developer-facing HALTs outside Phase 1 pre-flight, with exactly two narrow carve-outs: (a) the Conductor-facing section-7 freeze guard — this story — and (b) the developer-facing mid-flight escalation tier (DEC-036). The freeze check belongs to carve-out (a). A mismatch is observed and resolved by the Conductor; it never reaches the developer as a pause or prompt. Keeping it Conductor-facing is what lets the single end-gate stay the only developer touchpoint while still guaranteeing verification integrity.

**Why DEC-036 leaves this story UNCHANGED.** DEC-036 amends DEC-035 #1 to add a *developer-facing* mid-flight escalation tier for stakes-class findings (security/auth-isolation; irreversible/destructive; high-blast-radius/architecture). The contract-freeze check is **not** a stakes class and **not** a finding at all — it is a structural integrity assertion the Conductor makes about its own inputs. A fingerprint mismatch is not "a risky thing the build is about to do"; it is "the contract under verification is not the one that was frozen." Because it is neither a finding nor a stakes class, it does **not** enter the silent auto-fix path, it is **not** eligible for the mid-flight escalation tier, and it has **no** disposition of `fixed | dismissed | triaged-out | escalated`. DEC-036 therefore adds no escalation behavior here and changes nothing about this story. Do not add escalation logic, a stakes classification, or a developer-facing pause to the freeze check.

**Black-box note for the implementer.** The behavior is fully observable by invoking the Conductor: run it once with the contract file untouched (fingerprint matches the frozen value) and confirm verification proceeds; run it again after altering the contract file so its fingerprint no longer matches the frozen value, and confirm the Conductor stops short of verifying against the changed contract and surfaces the mismatch to itself rather than to the developer. No source inspection is needed to confirm the behavior.

**Vocabulary to use consistently in the workflow text:**
- Stakes classes: security/auth-isolation; irreversible/destructive (migration, delete, force-push, prod deploy); high-blast-radius/architecture; default routine. (The freeze check is none of these.)
- Dispositions: fixed | dismissed (required non-empty rationale) | triaged-out | escalated. (The freeze check produces none of these — it is an integrity stop, not a finding disposition.)
- Timing tiers: end-gate-expanded (default) | mid-flight (narrow). (The freeze check is neither — it is Conductor-facing.)

### References

- Epic **momentum-sprint-orchestration** — `_bmad-output/planning-artifacts/epics.json` (the conduct / sprint orchestration epic this story belongs to).
- **DEC-035** — adopt conduct; one human gate at the end; no developer-facing HALT outside pre-flight; report organized by user-facing functionality; legible anti-firehose auto-fix loop. Per-story verification soundness underpins the single end-gate. — `_bmad-output/planning-artifacts/decisions/`
- **DEC-036** — narrow, high-bar, stakes-and-timing mid-flight escalation tier amends DEC-035 #1. This story is **unchanged** by DEC-036: the freeze check is a Conductor-facing integrity stop, not a stakes class, and acquires no escalation behavior. — `_bmad-output/planning-artifacts/decisions/`
