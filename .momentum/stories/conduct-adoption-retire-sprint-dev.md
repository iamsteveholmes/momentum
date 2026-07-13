---
title: Conduct completes its own sprint — port `sprint complete` into the end-gate approve sequence (Phase 0 of sprint-dev retirement)
story_key: conduct-adoption-retire-sprint-dev
status: ready-for-dev
epic_slug: momentum-conductor-core
feature_slug:
story_type: practice
priority: high
change_type:
  - skill-instruction
depends_on: []
touches:
  - skills/momentum/skills/conductor/workflow.md
  - skills/momentum/skills/conductor/evals/
verification_method_advisory: skill-invoke
---

# Conduct completes its own sprint — port `sprint complete` into the end-gate approve sequence (Phase 0 of sprint-dev retirement)

## Story

As the maintainer of the Momentum build practice,
I want the Conductor to run `momentum-tools sprint complete` as part of its Phase 5 end-gate approve sequence,
so that a conduct-built sprint moves itself into the completed list and `momentum:retro` picks it up with no manual step — closing a latent conduct bug that today leaves every conduct-built sprint un-completed.

**Scope note (developer-directed rescope, 2026-07-13).** This story is deliberately narrowed to **Phase 0 only** — the sprint-completion parity fix — carved out of the original full-retirement story. The slug is unchanged; the full retirement of `momentum:sprint-dev` (soft-deprecate, soak, hard-remove) is **deferred to a future story** and preserved verbatim under *Deferred scope* below. Nothing in this sprint removes, deprecates, or reroutes `momentum:sprint-dev`.

## Why this exists (audit basis, verified 2026-07-13)

`momentum-tools sprint complete` is the transition that moves the **active** sprint into `sprints/index.json` `completed[]`, sets its `status` to `done`, and sets `retro_run_at = null` (`skills/momentum/scripts/momentum-tools.py:290–309`). Two callers invoke it — the legacy builder `momentum:sprint-dev` (`skills/momentum/skills/sprint-dev/workflow.md:747`) and `momentum:retro`'s own sprint-closure step (`skills/momentum/skills/retro/workflow.md:695`). **The Conductor never calls it** — zero `sprint complete` occurrences in `skills/momentum/skills/conductor/workflow.md`.

The consequence is a latent conduct bug, independent of any deprecation work: `momentum:retro` Step 1 identifies the sprint to close by scanning `completed[]` for an entry with `retro_run_at == null` (`retro/workflow.md:55`) and **HALTs** with "No sprint is awaiting a retrospective" when none is found (`retro/workflow.md:57–63`). Retro's *own* `sprint complete` call lives downstream in its Phase 6 closure (`retro/workflow.md:695`) — unreachable, because Step 1 gates entry. So a sprint that conduct built and merged is never completed, and retro finds nothing to run.

**This is live and recurring, not theoretical.** The 2026-06-28 conduct sprint had to be marked complete **by hand** on 2026-07-06 (`.momentum/handoffs/sprint-2026-06-28-retro-handoff-2026-07-06.md:12` — "Sprint marked `completed` 2026-07-06 via `momentum-tools sprint complete`"), and the same retro handoff flags **three additional** conduct-built sprints left without `retro_run_at` — `sprint-2026-05-26`, `sprint-2026-06-05-conduct-runnable`, `sprint-2026-06-10` (`.momentum/handoffs/retro-sprint-2026-06-28-phase5-handoff-2026-07-06.md:56`). Every conduct build to date has required manual compensation for this gap.

## The fix (Phase 0)

Port `momentum-tools sprint complete` into the Conductor's **Phase 5 approve** branch (`conductor/workflow.md`, step `n="5"`, the `<check if="developer approves">` block). It runs **after** the sprint stories are transitioned to their terminal status (merged stories `review → verify → done`; stranded stories `→ closed-incomplete`, `conductor/workflow.md:2350–2359`) and **before** the push summary (`git log @{u}..HEAD --oneline`, `conductor/workflow.md:2387`). Because the tool exits non-zero with `"No active sprint to complete"` when the sprint was already completed (a resumed or re-approved run — `momentum-tools.py:296`), the ported step must treat that outcome as an expected, non-fatal no-op and let the approve sequence continue — exactly the convention `momentum:retro` already documents for its own call (`retro/workflow.md:698`).

## Acceptance Criteria

1. In the Conductor Phase 5 approve branch (`skills/momentum/skills/conductor/workflow.md`, step `n="5"`, `<check if="developer approves">`), the workflow runs `momentum-tools sprint complete` **after** the sprint-story terminal-status transition action (the block ending at `conductor/workflow.md:2359`) and **before** the push summary action (`git log @{u}..HEAD --oneline`, `conductor/workflow.md:2387`). A conduct build therefore completes its own sprint with no hand-compensation step.

2. After a conduct build's approve sequence runs, the just-built sprint appears in `sprints/index.json` `completed[]` with `status == "done"` and `retro_run_at == null` — precisely the state `momentum:retro` Step 1 keys on (`retro/workflow.md:55`). Invoking `momentum:retro` against a conduct-completed sprint finds it (it does **not** HALT with "No sprint is awaiting a retrospective") with zero manual intervention.

3. The ported call is resume-safe: when the approve branch re-runs against an already-completed sprint (e.g., a rehydrated or re-approved end-gate), `momentum-tools sprint complete` returns `"No active sprint to complete"` and the Conductor treats it as an expected no-op — the approve sequence proceeds to the push summary without surfacing an error or aborting. The workflow text states this idempotency contract explicitly (mirroring `retro/workflow.md:698`).

## Tasks / Subtasks

- [ ] **Task 1 — Add the regression eval (AC 1, 2).** Author this eval FIRST, before the workflow edit (EDD). Add a behavioral eval under `skills/momentum/skills/conductor/evals/` (sibling of `eval-approve-path-routes-through-verify.md`) asserting that the Phase 5 approve sequence completes the sprint and that a conduct-completed sprint (`completed[]` entry with `retro_run_at == null`) satisfies the `momentum:retro` Step 1 precondition rather than HALTing. Follow the existing conductor-eval format (Surface under test / Scenario Given-When-Then / Pass Criteria / Fail Criteria).
- [ ] **Task 2 — Port the completion call (AC 1, 3).** In `skills/momentum/skills/conductor/workflow.md` Phase 5 approve branch, add an `<action>` that runs `momentum-tools sprint complete` immediately after the story terminal-status transition action (`:2350–2359`) and before the push summary (`:2387`). Add an adjacent `<note>` stating the "No active sprint to complete" return is an expected, non-fatal no-op on resumed/re-approved runs (cite the retro convention at `retro/workflow.md:698`). Do not alter the terminal-transition logic, the MAJOR-RESIDUAL governance guard, or the push/ask sequence.

## Deferred scope (future story)

**The following phases are explicitly OUT of scope for this sprint** and are preserved here (unedited in intent) so the full retirement is not lost. They belong to a follow-up story — do NOT implement them here, and they are intentionally absent from the Acceptance Criteria and Tasks above.

The larger goal these phases serve: retire `momentum:sprint-dev` (the legacy wave-loop builder) in sequenced phases — stop routing to it, let conduct soak as the sole engine, then delete the skill entirely — so there is exactly one build engine of record and the dead legacy path can no longer be invoked or drift against the live dev-agent contract. This is the downstream adoption step **DEC-037 named** (`conduct-adoption-retire-sprint-dev`). A four-surface deprecation audit (2026-06-12: routing, tooling/agents, decisions/docs, capability-parity) concluded conduct is a confirmed functional superset of sprint-dev — zero capability gap — and that keeping sprint-dev is itself a liability: sprint-dev is already broken against the current dev-agent contract (dev agents no longer commit per DEC-035; sprint-dev Phase 3 git-merges story branches with no staging step of its own, so a legacy run today would merge **empty** story branches). Phase 0 (this story) is the one hard prerequisite that audit surfaced; the phases below are the retirement proper.

### Deferred Phase 1 — soft-deprecate (stop routing, mark legacy, keep file as redirect stub)
- No live routing surface dispatches a build to `momentum:sprint-dev`: `impetus/references/dispatch.md` "legacy wave-loop" row removed or repointed; `.claude/rules/impetus.md` legacy line flipped to deprecated; `references/session-greeting.md:157–166` menu strings ("Run the sprint" / "Continue the sprint" / "Activate sprint") repointed to `momentum:conductor`.
- `commands/sprint-dev.md` becomes a redirect stub: invoking `/momentum:sprint-dev` prints a deprecation notice pointing at `/momentum:conduct`; it does not run the legacy wave-loop.
- `skills/momentum/skills/sprint-dev/SKILL.md` carries a `DEPRECATED` marker in description and body; the workflow body is reduced to a deprecation-halt redirect (the `momentum:feature-status` stub pattern — registry entry retained, body halts with a pointer). The skill is inert but present.
- sprint-planning Step 5.5 prose (the team-composition gate) reworded so its rationale cites conduct's per-story-pipeline role requirements rather than sprint-dev's `<team-composition>` block; the gate continues to validate the same agent files (dev roles, qa-reviewer, e2e-validator, architecture-guard), which conduct also needs — so the gate stays valid, only the citation changes.
- The impetus eval `eval-dispatch-uses-agent-not-skill.md` (uses sprint-dev as its worked example) and the 5+ `skills/momentum/skills/sprint-dev/evals/` files are marked deprecated or dropped so CI/eval runs do not assert against a dead target.
- Soft cosmetic sweep: `retro/workflow.md`, dev-agent definition lineage notes, and any remaining prose that says "sprint-dev Phase N parses it" reworded to conduct (descriptive, not load-bearing — the `AGENT_OUTPUT_START/END` parse contract is mandated for conduct regardless).

### Deferred Phase 2 — soak / safety gate (define the bar for deletion)
- A documented soak condition gates Phase 3: at least **N consecutive successful conduct sprints** (recommend N=3) completed with no fallback to sprint-dev, AND confirmation that sprint-planning no longer emits or depends on wave-model artifacts (`wave_count`, wave-derived ordering) that only sprint-dev consumed. The soak bar is recorded in the deferred story (or a linked decision) so Phase 3 is not executed prematurely.

### Deferred Phase 3 — hard removal (final retirement: delete the skill)
- **`skills/momentum/skills/sprint-dev/` is deleted in full** — SKILL.md, workflow.md, references, evals — once the Phase 2 soak condition is met.
- `commands/sprint-dev.md` is deleted (redirect stub removed; `/momentum:sprint-dev` no longer resolves).
- The dispatch.md legacy row and any remaining skill-registry/marketplace entry for sprint-dev are removed; orphaned sprint-dev eval coverage is deleted (or still-relevant assertions migrated to conduct evals).
- PRD requirements that defined sprint-dev (FR62, FR63, FR74, and the FR139/FR140 coexistence clauses) are marked retired/removed in `prd.md`, and `architecture.md`'s sprint-dev-specific sections (e.g. Decision 31 team-review contrast) are annotated as historical.
- A final repo-wide grep confirms **no live reference resolves to the deleted skill**: `grep -rn "sprint-dev" skills/ commands/ .claude/` returns only archival/comment matches. Archival mentions under `.momentum/stories/`, `_bmad-output/`, and retros are left intact as the audit trail.
- The plugin version is bumped (minor) on the soft-deprecate release and again on the hard-removal release, per the version-on-release rule.

**Deferred-scope sequencing note (for the future story):** Phase 1 before Phase 2 before Phase 3 — delete the safety net last. The soft-deprecate phases (1) should ship together so the dead path stops being reachable promptly; Phase 3 may be its own story after the soak. The ~240 archival mentions need no edits in any phase — they are the audit trail. Because sprint-dev is already broken against the dev no-commit contract, leaving it reachable is an active risk (an accidental `/momentum:sprint-dev` run merges empty branches); Phase 1 closes that risk, Phase 3 eliminates it. This story (Phase 0) is the blocking prerequisite for all of the above: until conduct completes its own sprints, sprint-dev cannot be pulled.

## Dev Notes

### Decision Authority
- **DEC-035** — conduct is the execution engine of record; the Conductor is sole git-mutation authority; one end-gate. Completing the sprint at the end-gate is the Conductor's responsibility because it owns the terminal sprint→main merge and terminal story transitions.
- **DEC-037** — names `conduct-adoption-retire-sprint-dev` and the coexistence-then-retire sequencing; establishes Phase 0 (this story) as the hard prerequisite before any sprint-dev removal.
- The sprint-completion transition itself is owned by `momentum-tools` (never hand-edit `sprints/index.json`); the Conductor's job is only to *call* the tool at the right point.

### Current State of affected files
- `skills/momentum/skills/conductor/workflow.md` (2633 lines) — Phase 5 is step `n="5"` (~`:2238`). The approve branch `<check if="developer approves">` (`:2343`) currently: (1) merges sprint→main and deletes the sprint branch (`:2344–2349`); (2) transitions each story to terminal status — `review→verify→done` for merged, `→closed-incomplete` for stranded (`:2350–2359`); (3) runs the MAJOR-RESIDUAL governance guard (`:2360–2386`); (4) shows the push summary and asks to push (`:2387–2391`). **No `sprint complete` call exists anywhere in the file.** The new call belongs between (2) and (4).
- `skills/momentum/skills/conductor/evals/` — existing conductor evals (e.g. `eval-approve-path-routes-through-verify.md`, `eval-phase5-assembles-from-ledger.md`) are the format template for Task 1's new eval.
- Reference-only (do not edit): `momentum-tools.py:290–309` (`cmd_sprint_complete` behavior); `retro/workflow.md:55,57–63,695,698` (retro precondition, HALT, own closure call, idempotency note); `sprint-dev/workflow.md:747` (legacy caller — untouched this sprint).

### Architecture Compliance
- The Conductor remains sole git/state authority — this change adds one tool invocation inside the already-developer-gated approve branch; it introduces no new developer HALT and no new git-mutation site.
- Ordering is load-bearing: `sprint complete` must follow the terminal story transitions (so the sprint is genuinely done before it is archived) and precede the push summary (so the completed state is on disk before the push preview). It may be placed before or after the MAJOR-RESIDUAL guard — either satisfies the AC-1 ordering; placing it immediately after the terminal transitions is the most direct reading of "after done transitions."
- Idempotency is mandatory: the tool exits code 1 on "No active sprint to complete" (`momentum-tools.py:296` via `error_result`). The workflow step and its note must make clear a non-zero "no active sprint" return is expected on resume/re-approval and must not abort the sequence.

### Testing Requirements
- Verification method (advisory): **`skill-invoke`** — the primary deliverable is a `workflow.md` edit (change_type `skill-instruction`), which the routing table maps to `skill-invoke`: exercise the Conductor's Phase 5 approve path and observe that the sprint is completed and retro can pick it up. Single change type → routing is unambiguous (no precedence tiebreak needed).
- EDD (see Implementation Guide): author the Task 1 eval *before* editing the workflow, then confirm the observable behavior. A minimal live check: seed an active sprint with all stories at `done`, run `momentum-tools sprint complete`, then assert `sprints/index.json` shows the sprint in `completed[]` with `retro_run_at == null`; a second `sprint complete` returns "No active sprint to complete" without corrupting state.

### Project Context Reference
- First-live-run proof that conduct is runnable end-to-end (satisfies DEC-037's gate for this work): sprint-2026-06-10 build ledger + end-gate report under `.momentum/sprints/sprint-2026-06-10/` and `.momentum/handoffs/`. The recurring manual-completion evidence is the 2026-06-28 retro handoffs cited above.

### References
- DEC-037 (`_bmad-output/planning-artifacts/decisions/dec-037-conduct-invocation-model-standalone-skill-2026-06-04.md`) — names this step and the coexistence-then-retire sequencing.
- DEC-035 / DEC-036 — adopt conduct; Conductor sole git authority; behavioral changes that intentionally retire the wave-loop/stop-gate model.
- Prerequisite evidence: `conductor/workflow.md` (zero `sprint complete` calls; approve branch `:2343–2392`); `sprint-dev/workflow.md:747` (legacy caller); `retro/workflow.md:55,695,698` (precondition + idempotency convention); `momentum-tools.py:290–309` (`sprint complete` behavior).
- Recurring-gap evidence: `.momentum/handoffs/sprint-2026-06-28-retro-handoff-2026-07-06.md:12`; `.momentum/handoffs/retro-sprint-2026-06-28-phase5-handoff-2026-07-06.md:56`.
- Deprecation audit, 2026-06-12 — four-surface analysis behind the deferred retirement phases.
- Epic context: `momentum-conductor-core` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for `workflow.md`.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD, adapted to this surgical edit of an existing skill:

**Before editing the workflow:**
1. Write the Task 1 behavioral eval in `skills/momentum/skills/conductor/evals/` (the directory already exists). Name it descriptively (e.g., `eval-phase5-completes-sprint-for-retro-pickup.md`). Format it as the existing conductor evals do — Surface under test / Scenario (Given-When-Then) / Pass Criteria / Fail Criteria — asserting: (a) the Phase 5 approve sequence prescribes a `momentum-tools sprint complete` call positioned after the terminal story transitions and before the push summary; (b) a conduct-completed sprint (`completed[]` with `retro_run_at == null`) satisfies the `momentum:retro` Step 1 precondition instead of HALTing.

**Then implement:**
2. Make the surgical edit to `conductor/workflow.md` Phase 5 approve branch (Task 2). This is a targeted insertion into an existing 2633-line workflow — do not restructure surrounding steps.

**Then verify:**
3. Run the eval by spawning a subagent: give it the eval scenario and the edited `conductor/workflow.md` Phase 5 section as context, and observe whether the described approve sequence completes the sprint and whether a conduct-completed sprint clears retro's precondition. Complement with the live `momentum-tools` check in Testing Requirements above.
4. If the eval behavior matches → task complete. If not → diagnose the gap in the workflow text, revise, re-run (max 3 cycles; surface to the developer if still failing).

**NFR notes for this story (adapted — no new SKILL.md is authored):**
- This story edits `workflow.md` and adds an eval; it does **not** create or modify a `SKILL.md`, so the ≤150-char description NFR and the ≤500-line SKILL.md-body NFR are **not triggered** (the 500-line cap governs SKILL.md bodies, not the pre-existing large workflow file). Keep the insertion minimal.
- Model routing frontmatter on `conductor/SKILL.md` is unchanged — do not touch it.

**Additional DoD items for this story (added to standard bmad-dev-story DoD):**
- [ ] Task 1 eval written in `skills/momentum/skills/conductor/evals/` before the workflow edit
- [ ] EDD cycle ran — approve-sequence completion behavior and retro-pickup behavior confirmed (or failures documented)
- [ ] `momentum-tools sprint complete` call inserted after terminal story transitions and before the push summary in the Phase 5 approve branch
- [ ] Idempotency note present in the workflow ("No active sprint to complete" = expected no-op on resume/re-approval)
- [ ] Live check performed: seeded/active sprint → `sprint complete` → `completed[]` entry with `retro_run_at == null`; second call is a safe no-op
- [ ] No changes to terminal-transition logic, the MAJOR-RESIDUAL guard, the push/ask sequence, or any sprint-dev file
- [ ] AVFL checkpoint on the produced artifact documented (momentum:dev runs this automatically)

**Frozen verification contract reminder:** a frozen verification contract exists for this sprint at `sprints/{sprint-slug}/specs/conduct-adoption-retire-sprint-dev.{ext}`. Read only the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before signaling done. Do NOT read the verifier body (Part B: scenarios, assertion scripts, Gherkin) beyond sections `how_dev_self_checks` explicitly references.

## Dev Agent Record
