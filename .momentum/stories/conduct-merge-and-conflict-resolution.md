---
title: Conductor per-story merge, conflict resolution, quarantine, and escalation hook
story_key: conduct-merge-and-conflict-resolution
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - skill-instruction
verification_method: skill-invoke
depends_on:
  - conduct-build-phase-frontier
  - conduct-stakes-timing-escalation-mechanism
touches:
  - skills/momentum/skills/conductor/workflow.md
---

# Conductor per-story merge, conflict resolution, quarantine, and escalation hook

## Story

As the developer running a conduct sprint,
I want the Conductor to own every per-story merge — rebasing and merging each completed story's work, resolving conflicts autonomously where it safely can, quarantining anything it cannot, and escalating only the narrow set of resolutions that carry real stakes,
so that one bad merge never halts the whole sprint, my history stays clean, and I am pulled in mid-flight only when a conflict resolution would silently change something irreversible or build-invalidating.

## Description

The Conductor is the top-level session orchestrator that owns the build phase and **all** git mutation for a conduct sprint. No subagent touches git history; the Conductor is the single writer. This story specifies the per-story integration machinery: how each completed story's branch is rebased and merged into the sprint integration branch, how conflicts are detected and resolved, what happens when a story cannot be merged, and how the merge machinery participates in the mid-flight escalation mechanism.

**What it does.** For each story that finishes its build, the Conductor performs a rebase followed by a merge into the sprint integration branch. Both the rebase step and the merge step are conflict-guarded. When a conflict is **trivial** (mechanically resolvable — non-overlapping hunks, additive-only collisions, generated index/lockfile churn the machinery can reconcile deterministically), the Conductor auto-resolves it and continues. When a conflict is **semantic** (the resolution requires understanding intent — overlapping logic, contradictory edits to the same construct), the Conductor fires a directed fixer to produce a correct resolution, then retries the rebase/merge. Resolution attempts are bounded at **3**. A story that still cannot be integrated after 3 attempts is **quarantined**: its work is preserved on its own branch, the conflict detail is recorded, and the remaining stories continue to integrate. Quarantine-and-continue replaces any HALT — a single unmergeable story never stops the sprint.

**Why it matters (pain context).** The legacy sprint-dev model treated a merge conflict as a stop-the-world event: the human was pulled in to hand-resolve, the sprint stalled, and momentum died. Worse, the absolutist anti-firehose posture (DEC-035 binding decision #1) said *every* conflict resolution should be silently auto-resolved and the sprint should just keep going — which is right for the common case but dangerous when a semantic resolution silently rewrites an authentication boundary or breaks the build for every downstream story. The Conductor needs a path that is autonomous by default yet refuses to silently swallow a high-stakes resolution.

**What changes here (DEC-036 scope nuance).** DEC-036 amends DEC-035 #1 narrowly. It does **not** make the terminal sprint→main merge a new mid-flight escalation trigger — that merge already lives inside the developer-gated APPROVE sequence at the end-gate, so it is already guarded and is out of scope for this story's mid-flight tier. What changes **here** is narrower and specific to the per-story conflict path: (a) when a semantic conflict resolution would touch a **stakes class** (security/auth-isolation; irreversible/destructive; high-blast-radius/architecture) **or** is **build-invalidating**, the Conductor must **escalate** that resolution via the escalation mechanism instead of silently auto-resolving and continuing; and (b) the merge machinery must **expose the escalation hook** that the mechanism calls, so the stakes/timing logic from the dependency story has a concrete integration point inside the merge path. Trivial conflict auto-resolution and ordinary quarantine-and-continue stay fully autonomous — the narrow mid-flight bar is **irreversible-and-imminent OR build-invalidating only**, and it must never widen.

**Source decisions.** DEC-035 (adopt conduct; single human end-gate; no story-count cap; legible auto-fix loop). DEC-036 (narrow, high-bar, stakes-gated mid-flight escalation tier amending DEC-035 #1; `escalated` becomes a first-class disposition meaning *raised, not silently fixed*).

## Acceptance Criteria

1. For each completed story, the Conductor performs a **rebase step followed by a merge step** into the sprint integration branch, and **both** steps are conflict-guarded (a conflict surfacing in either step is detected and handled, not left unresolved).
2. A **trivial** conflict (mechanically resolvable without understanding intent) is **auto-resolved** by the Conductor and integration continues, with no human involvement.
3. A **semantic** conflict (resolution requires understanding intent) causes the Conductor to **fire a directed fixer** to produce the resolution, after which the rebase/merge is **retried**.
4. Conflict-resolution attempts for a single story are **bounded at 3**; the Conductor does not retry indefinitely.
5. A story that **cannot be merged after 3 attempts is quarantined**: its work is preserved (not discarded), the conflict detail is recorded, and the **remaining stories continue** to integrate.
6. Quarantine is **never a HALT** — a single unmergeable story does not stop the sprint or pull the human in mid-flight; the sprint proceeds and the quarantined story is surfaced at the end-gate.
7. When a **semantic conflict resolution would touch a stakes class** (security/auth-isolation; irreversible/destructive such as migration, delete, force-push, or prod deploy; high-blast-radius/architecture), the Conductor **escalates that resolution via the escalation mechanism** instead of silently auto-resolving and continuing.
8. When a semantic conflict resolution is **build-invalidating** (it would break the build for the sprint or downstream stories), the Conductor **escalates via the escalation mechanism** instead of silently auto-resolving and continuing.
9. The Conductor **only** escalates from the merge path on the narrow bar of clause 7 or clause 8 (a stakes-class-touching resolution **or** a build-invalidating resolution); a routine semantic resolution that touches **no** stakes class and is **not** build-invalidating is auto-resolved-and-continued without escalation.
10. The merge machinery **exposes an escalation hook** that the escalation mechanism calls — the per-story merge path has a defined, documented integration point where the stakes/timing logic raises an escalation.
11. The **terminal sprint→main merge is NOT** treated as a mid-flight escalation trigger by this machinery — it remains inside the developer-gated end-gate APPROVE sequence and is out of scope for the per-story mid-flight path.
12. An escalation raised from the merge path is recorded with the disposition **`escalated`** (raised, not silently fixed) — distinct from `fixed` (auto-resolved) and from a quarantine record — so the end-gate report can render it.

## Tasks / Subtasks

- [ ] **Define the per-story integration sequence in the Conductor workflow** (AC: 1)
  - [ ] Specify rebase-then-merge ordering for integrating a completed story's branch into the sprint integration branch.
  - [ ] State that both the rebase step and the merge step are conflict-guarded, and that the Conductor is the sole git writer for these operations.
- [ ] **Specify conflict classification: trivial vs. semantic** (AC: 2, 3)
  - [ ] Define what makes a conflict *trivial* (mechanically resolvable: non-overlapping hunks, additive-only collisions, deterministic index/lockfile reconciliation).
  - [ ] Define what makes a conflict *semantic* (resolution requires understanding intent: overlapping logic, contradictory edits to the same construct).
- [ ] **Specify the trivial auto-resolution path** (AC: 2)
  - [ ] Document that trivial conflicts are auto-resolved and integration continues with no human involvement.
- [ ] **Specify the semantic resolution path via directed fixer + bounded retry** (AC: 3, 4)
  - [ ] Document firing the directed fixer to produce a semantic resolution.
  - [ ] Document the retry of rebase/merge after a fix, with the attempt bound fixed at 3.
- [ ] **Specify quarantine-not-HALT** (AC: 5, 6)
  - [ ] Document that after 3 failed attempts a story is quarantined: work preserved, conflict detail recorded.
  - [ ] Document that remaining stories continue and that quarantine never halts the sprint or pulls the human in mid-flight.
  - [ ] Document that quarantined stories are surfaced at the end-gate.
- [ ] **Specify the narrow stakes/build-invalidating escalation in the merge path** (AC: 7, 8, 9)
  - [ ] Document that a semantic resolution touching a stakes class escalates via the mechanism rather than silently continuing.
  - [ ] Document that a build-invalidating semantic resolution escalates via the mechanism rather than silently continuing.
  - [ ] Document the narrow bar explicitly: escalate ONLY on stakes-class-touching OR build-invalidating; routine semantic resolutions are auto-resolved-and-continued. State that the bar must never widen.
- [ ] **Expose the escalation hook for the mechanism** (AC: 10)
  - [ ] Document the integration point in the merge path where the escalation mechanism is invoked, so the dependency story's stakes/timing logic has a concrete call site.
- [ ] **Scope out the terminal sprint→main merge** (AC: 11)
  - [ ] State explicitly that the terminal sprint→main merge stays inside the developer-gated end-gate APPROVE sequence and is not a mid-flight trigger here.
- [ ] **Record escalations with the `escalated` disposition** (AC: 12)
  - [ ] Document that merge-path escalations are recorded as `escalated` (raised, not silently fixed), distinct from `fixed` and from quarantine, so the end-gate report can render them.

## Dev Notes

This story instructs the Conductor (`skills/momentum/skills/conductor/workflow.md`) and is `change_type: skill-instruction`, verified by `skill-invoke`. It builds on two dependencies: `conduct-build-phase-frontier` (which establishes that the Conductor owns the build phase and how completed stories arrive at integration) and `conduct-stakes-timing-escalation-mechanism` (which defines the stakes classes, timing tiers, and the escalation mechanism this story's merge path calls and exposes a hook for).

**Governing spec sections (by number, from the brief).**
- **Section 6** — the Conductor owns ALL git mutation: per-story rebase + merge, conflict detection, trivial auto-resolution, directed-fixer-driven semantic resolution with retry bound 3, and quarantine-not-HALT. This story implements that section's per-story integration machinery and is the single-git-writer locus.

**Conduct vocabulary (use consistently).**
- **Stakes classes**: security/auth-isolation; irreversible/destructive (migration, delete, force-push, prod deploy); high-blast-radius/architecture; default routine.
- **Dispositions**: `fixed` | `dismissed` (requires non-empty rationale) | `triaged-out` | `escalated` (NEW — raised, not silently fixed). Merge-path escalations use `escalated`.
- **Timing tiers**: `end-gate-expanded` (default) | `mid-flight` (narrow). The merge-path escalation is the `mid-flight` tier and must stay narrow: **irreversible-and-imminent OR build-invalidating ONLY**.

**Design guardrails.**
- The mid-flight bar here is deliberately narrow. Trivial auto-resolution and ordinary quarantine-and-continue are autonomous and silent. Only a semantic resolution that **touches a stakes class** or is **build-invalidating** leaves the silent path and escalates. The end-gate-expanded tier is the safety net for everything else; never widen the mid-flight bar to catch routine resolutions.
- The Conductor is the sole git writer. The directed fixer produces a *resolution* (content), but the Conductor performs the actual rebase/merge/commit operations — fixers never mutate git history directly.
- The escalation **hook** is a structural seam: the merge machinery exposes it; the stakes/timing **mechanism** (dependency story) decides when to fire it. This story owns the hook's existence and call site, not the stakes-classification logic itself.
- DEC-036 scope nuance is load-bearing: the terminal sprint→main merge is already gated by the human end-gate APPROVE sequence and is explicitly out of scope for the mid-flight tier. Do not turn it into a new D1 trigger.

### References

- Epic: **momentum-sprint-orchestration** — `_bmad-output/planning-artifacts/epics.json`
- Decision: **DEC-035** — adopt conduct; single human end-gate; no story-count cap; legible auto-fix loop (organized by user-facing functionality; reports what it changed AND dismissed) — `_bmad-output/planning-artifacts/decisions/`
- Decision: **DEC-036** — narrow, high-bar, stakes-gated mid-flight escalation tier amending DEC-035 binding decision #1; `escalated` as a first-class disposition; anti-rubber-stamp end-gate — `_bmad-output/planning-artifacts/decisions/`
