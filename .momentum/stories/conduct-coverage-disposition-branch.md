---
title: Conductor coverage-disposition branch (dedicated-run vs covered-by-composition)
story_key: conduct-coverage-disposition-branch
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - skill-instruction
verification_method: skill-invoke
depends_on:
  - conduct-build-phase-frontier
  - qa-reviewer-rescope-per-story-contract
touches:
  - skills/momentum/skills/conductor/workflow.md
---

# Conductor coverage-disposition branch (dedicated-run vs covered-by-composition)

## Story

As the Conductor running the autonomous build phase,
I want to branch each story on its frozen `coverage_disposition` so that a story marked `covered-by-composition` skips its dedicated build-time QA run and is instead discharged later by a named integration scenario at AVFL/merge,
so that we do not redundantly verify a story at build time when a composed integration scenario already covers it — without ever letting that routing change how findings are classified or how stakes-class findings are surfaced.

## Description

The Conductor owns the in-session build phase: for each story on the frontier it builds the change and decides whether a dedicated QA verification run happens during the build. This story adds the branch that reads each story's `coverage_disposition` field and routes accordingly:

- `dedicated-run` — the story gets its own dedicated QA verification run during the build phase.
- `covered-by-composition` — the story skips the dedicated build-time QA run; its verification debt is discharged later, at AVFL/merge, by the named integration scenario that composes it.

**What this adds.** A purely mechanical fork in the build phase. The Conductor reads the disposition from the frozen contract/assignment that was handed to it; it does not compute, infer, or override the disposition itself. When the disposition says `covered-by-composition`, the Conductor records that the dedicated run is deferred and names the integration scenario that will discharge it downstream.

**Why.** Some stories are best verified together as a composed integration scenario rather than each running an isolated QA pass at build time. Verifying such a story twice — once in isolation at build, once again in the composition at merge — is wasted work and can produce contradictory or noisy signals. The branch lets a planner mark a story `covered-by-composition` and trust that the build phase will honor that intent.

**Pain context.** In the current sprint-dev flow there is no first-class concept of a story whose verification is deferred to a composed scenario. Either every story runs its own verification at build time (redundant for composed work) or coverage gets dropped silently. This branch makes the deferral explicit and auditable: the build phase records *that* a dedicated run was skipped and *which* downstream scenario owns the discharge.

**Critical boundary — DEC-036 does not change this branch.** DEC-036 narrowly amends DEC-035 to permit a narrow, stakes-gated mid-flight escalation tier and to require legible dispositions and an anti-rubber-stamp end-gate. None of that touches *this* story. This branch decides **WHEN verification runs** (at build vs. deferred to AVFL/merge) — it does **NOT** decide **HOW findings are classified**. A stakes-class finding (security/auth-isolation; irreversible/destructive; high-blast-radius/architecture) that is discharged later by the composed integration scenario at AVFL/merge is *still* routed out of the silent auto-fix path — but that routing is done by the finding schema and the report, not by this coverage branch. Choosing `covered-by-composition` only changes the *timing and venue* of the QA run; it never demotes, hides, or silences a stakes-class finding.

**Source decisions.** DEC-035 (adopt conduct; single end-gate; report organized by user-facing functionality; legible auto-fix loop). DEC-036 (narrow stakes-gated mid-flight tier; legible dispositions; anti-rubber-stamp end-gate) — included here only to assert it does NOT alter this branch.

## Acceptance Criteria

1. When the Conductor processes a story whose frozen `coverage_disposition` is `dedicated-run`, that story gets a dedicated QA verification run during the build phase.
2. When the Conductor processes a story whose frozen `coverage_disposition` is `covered-by-composition`, that story does NOT get a dedicated QA verification run during the build phase; the dedicated run is skipped.
3. For a `covered-by-composition` story, the Conductor records that the dedicated build-time run was skipped and names the specific integration scenario that will discharge the story's verification later, at AVFL/merge.
4. The Conductor reads the `coverage_disposition` value from the frozen contract/assignment it was handed; it does not compute, infer, choose, or override the disposition, and it makes no verification decision of its own beyond honoring the value it read.
5. If a story's frozen `coverage_disposition` is missing or unrecognized, the Conductor treats the story as `dedicated-run` (the safe default that does not skip verification) rather than silently skipping the run.
6. Choosing `covered-by-composition` changes only the timing and venue of the QA run (build-time vs. deferred to AVFL/merge). It does not change how any finding is classified, and it does not demote, hide, silence, or auto-resolve any finding — including a stakes-class finding (security/auth-isolation; irreversible/destructive; high-blast-radius/architecture).
7. A stakes-class finding that surfaces when the deferred verification is discharged at AVFL/merge is still routed out of the silent auto-fix path and rendered in the report; this coverage branch neither performs nor suppresses that routing, and the deferral does not weaken it.
8. The branch never widens what runs at build time beyond what the disposition specifies, and never adds a second verification run for a story that was already marked `covered-by-composition`.

## Tasks / Subtasks

- [ ] In `skills/momentum/skills/conductor/workflow.md`, add the coverage-disposition branch to the per-story build-phase step (AC 1, AC 2).
- [ ] Specify that the branch reads `coverage_disposition` from the frozen contract/assignment handed to the Conductor, and explicitly forbid the Conductor from computing, inferring, choosing, or overriding it (AC 4).
- [ ] For `dedicated-run`: instruct the Conductor to perform the dedicated QA verification run during the build (AC 1).
- [ ] For `covered-by-composition`: instruct the Conductor to skip the dedicated build-time run and instead record (a) that the run was skipped and (b) the named integration scenario that will discharge the story at AVFL/merge (AC 2, AC 3).
- [ ] Add the safe-default rule: missing or unrecognized `coverage_disposition` is treated as `dedicated-run` so verification is never silently skipped (AC 5).
- [ ] Add an explicit non-goal/guardrail block stating this branch routes WHEN verification runs, not HOW findings are classified; it must not demote, hide, silence, or auto-resolve any finding, including stakes-class findings (AC 6).
- [ ] State that a stakes-class finding raised when the deferred verification is discharged at AVFL/merge is still routed out of silent auto-fix and rendered in the report by the finding schema and report — not by this branch — and that the deferral does not weaken that routing (AC 7).
- [ ] Add a guard that prevents widening build-time verification beyond the disposition and prevents a duplicate run for a `covered-by-composition` story (AC 8).

## Dev Notes

This story modifies only the Conductor workflow instruction at `skills/momentum/skills/conductor/workflow.md`. It is `change_type: skill-instruction` and is verified by invoking the skill (`verification_method: skill-invoke`); it builds conduct as a skill-instruction edit — there is no app/UI/backend lane.

**Governing spec sections (cited by number from the brief).** Section 7 defines `coverage_disposition` and the `covered-by-composition` path that discharges a story's verification at AVFL/merge via a named integration scenario. Step 4 is the AVFL/merge discharge point where the named integration scenario actually runs and clears the deferred verification debt. The branch in this story is the build-phase fork that honors section 7 by either running the dedicated QA pass at build time (`dedicated-run`) or deferring to the step-4 discharge (`covered-by-composition`).

**Reads, does not decide.** The Conductor's job here is mechanical: read the frozen `coverage_disposition` and act on it. The disposition is set upstream (planning/contract freeze) and is immutable at build time. The Conductor must not re-derive it from story content, change it, or substitute its own judgment. The only judgment-shaped behavior allowed is the safe default for a missing/unrecognized value, and that default is the conservative one (`dedicated-run`, i.e., do not skip verification).

**DEC-036 explicitly does NOT change this branch — record this in the workflow.** DEC-036's amendments (narrow stakes-gated mid-flight escalation; legible `fixed | dismissed | triaged-out | escalated` dispositions with required non-empty rationale for dismissals; `end-gate-expanded` vs `mid-flight` timing tiers; anti-rubber-stamp end-gate) concern HOW findings are classified and WHEN stakes-class findings leave the silent auto-fix path. This coverage branch concerns only WHEN the verification *run* happens (build vs. AVFL/merge) and WHERE it runs. A stakes-class finding discharged at AVFL/merge is routed out of silent auto-fix by the finding schema + report, NOT by this branch. The deferral changes timing/venue only; it never demotes, hides, or silences a stakes-class finding, and never narrows or widens the stakes routing. The workflow text must state this boundary explicitly so a future reader does not mistake `covered-by-composition` for a way to bypass stakes handling.

**Dependencies.** `conduct-build-phase-frontier` establishes the per-story build-phase loop and frontier that this branch hooks into. `qa-reviewer-rescope-per-story-contract` establishes the frozen per-story contract (including `coverage_disposition`) that this branch reads — the branch consumes that frozen value and must not re-scope it.

### References

- Epic: `momentum-sprint-orchestration` — `_bmad-output/planning-artifacts/epics.json` (the conduct rewrite of momentum:sprint-dev: in-session, per-story, autonomous-build, single human end-gate).
- Decision: DEC-035 — adopt conduct; one human gate at the end; no story-count cap; report organized by user-facing functionality; legible auto-fix loop.
- Decision: DEC-036 — narrow, high-bar, stakes-gated mid-flight escalation tier; legible dispositions; anti-rubber-stamp end-gate (amends DEC-035 #1 narrowly; cited here to assert it does NOT alter this coverage-disposition branch).
- Governing spec: section 7 (coverage_disposition / covered-by-composition) + step 4 (AVFL/merge discharge by named integration scenario).
