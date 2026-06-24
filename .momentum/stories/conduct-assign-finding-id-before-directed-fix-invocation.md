---
title: Conduct — assign finding_id before directed-fix invocation
story_key: conduct-assign-finding-id-before-directed-fix-invocation
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug: 
story_type: defect
priority: critical
depends_on: []
touches:
  - skills/momentum/skills/conductor/workflow.md
change_type:
  - skill-instruction
verification_method_advisory: skill-invoke
---

# Conduct — assign finding_id before directed-fix invocation

## Story

As a developer running a conduct sprint build,
I want the Conductor to assign a unique `finding_id` to every stage-2 finding before it invokes the directed fixer,
so that the directed-fix invocation contract is satisfied and every fix is correlated, retry-counted, and deduped by a stable key instead of by positional accident.

## Description

The Conductor invokes the directed fixer (`momentum:dev` in fix mode) at step 2.S3 Phase B (`skills/momentum/skills/conductor/workflow.md:956`) passing `{{stage2_findings}}` — findings that were never assigned a `finding_id`. Three things in the same step already presuppose that key exists:

1. The fix-loop entry binds the per-finding retry counter "keyed by finding ID" (`:939` — `Bind {{fix_attempts}} = {} — per-finding retry counter keyed by finding ID.`).
2. Every disposition CASE block (`fixed` :976/:995, `dismissed` :1003, `triaged-out` :1009, `escalated` :1016, `blocked` :1134) looks up the inbound finding by `F.finding_id` to recover descriptive fields and to emit ledger rows.
3. The ledger dedup guard keys on the tuple `(story_slug, event, finding_id)` (`:377`, `:404`).

But the canonical finding normalization that builds `{{qa_findings}}` (`:700-727`) does **not** list `finding_id` among the base fields it populates, and `{{cr_findings}}` (the bmad-code-review reviewer output bound at `:758` / `:778`) carries whatever the reviewer emitted — neither path guarantees a `finding_id`. Between the bind of `{{stage2_findings}}` (`:936`) and the fixer invocation (`:956`) there is no instruction that creates the key. So the fixer is invoked with findings lacking `finding_id`, in violation of the directed-fix invocation contract, which states (`skills/momentum/references/directed-fix-invocation-contract.md:40-48`):

> Each inbound finding carries a `finding_id` field assigned by the Conductor **before** the fix-mode is invoked. ... Assigned by: the Conductor (not by any reviewer, not by the fix-mode itself). Unique within: the findings array of a single fix-mode invocation. ... The fix-mode echoes `finding_id` in every returned disposition object so the Conductor can match dispositions to inbound findings without relying on positional ordering.

This is a genuine, critical contract violation in the live conduct build path, surfaced by the 2026-06-14 conduct sub-skills audit (`.momentum/handoffs/conduct-subskills-audit-2026-06-14.html`) — missed by the first audit, confirmed by the second, and flagged as the single genuine contract bug.

**Pain context:** Without a Conductor-assigned `finding_id`, the fixer cannot key/dedup inbound findings and cannot echo a stable correlation key in its returned dispositions. Disposition routing then falls back to positional ordering, retry counts collide or are lost, and the ledger dedup guard cannot fire — fixes can misroute or collide. The contract's stated purpose ("match dispositions to inbound findings without relying on positional ordering") is silently unmet.

## Acceptance Criteria

1. After `{{stage2_findings}}` is bound in step 2.S3 (`skills/momentum/skills/conductor/workflow.md:936`) and **before** the directed fixer is invoked in Phase B (`:956`), an explicit instruction iterates `{{stage2_findings}}` and assigns a `finding_id` to every finding that lacks one. Reading the step 2.S3 entry block top-to-bottom, the `finding_id`-assignment instruction is positioned after the `{{stage2_findings}}` bind and the `{{fix_attempts}}` bind and before Phase B's fixer invocation. (Contract: directed-fix-invocation-contract.md §"Finding Identification" — assigned by the Conductor, before the fix-mode is invoked.)

2. The assigned `finding_id` is **unique within** the findings array of that single fix-mode invocation (one story's fix call), per the contract's uniqueness scope. The workflow text states an explicit, deterministic generation rule (for example `source` + `-` + zero-based array index, or an equivalent stable scheme) such that two findings in the same `{{stage2_findings}}` array can never receive the same `finding_id`.

3. The directed fixer at `:956` is **never** invoked with a finding that lacks `finding_id`. The Input description for the Phase B invocation reflects that every finding in `{{stage2_findings}}` (and any unresolved subset passed on later loop iterations) carries `finding_id`.

4. The canonical normalization that builds `{{qa_findings}}` (`:700-727`) either (a) lists `finding_id` among the populated base fields, or (b) the workflow text explicitly states that `finding_id` is assigned by the dedicated Conductor assignment step in AC-1 (single source of assignment) rather than by normalization. Whichever approach is chosen, there is no path by which a finding reaches `:956` without a `finding_id`, including the covered-by-composition path where only `{{cr_findings}}` (bmad-code-review) populates `{{stage2_findings}}` (`:778-779`).

5. The assignment is **idempotent within a build**: a finding that already carries a `finding_id` (for example, one re-presented on a later fix-loop iteration, or one rehydrated from the build ledger on resume) is not reassigned a new id. Re-running the assignment over the same `{{stage2_findings}}` array does not change any existing `finding_id`. (This preserves the `(story_slug, event, finding_id)` ledger dedup guard at `:377`/`:404` across resume and across loop iterations.)

6. The `finding_id` produced is consistent with every downstream consumer that already references it within step 2.S3: the `{{fix_attempts}}` retry counter (`:939`), each disposition CASE lookup of the inbound finding by `F.finding_id` (`:976`, `:982`, `:997`, `:1004`, `:1008`, `:1014`, `:1136`), and the ledger `finding-disposition` / `stage3-escalation` rows. No downstream reference to `finding_id` / `F.id` is left without a guaranteed source value.

7. The change is confined to instruction text in `skills/momentum/skills/conductor/workflow.md` (and, only if AC-4 option (a) is taken, the normalization field list in the same file). No other skill, reference, or contract file is modified. The directed-fix-invocation-contract.md remains the authoritative statement of the contract; this story makes the workflow comply with it, it does not amend the contract.

8. The precise diagnostic is preserved in the story record: the violated contract clause, the invocation site (`:956`), the presupposing-but-unprovisioning step (`:936-939`), and the normalization omission (`:700-727`) remain documented so the fix targets the real seam and not a symptom.

## Tasks / Subtasks

- [ ] **Task 1 — Add the Conductor `finding_id`-assignment instruction in step 2.S3 entry block** (AC 1, 2, 3, 5, 6)
  - In `skills/momentum/skills/conductor/workflow.md`, locate the step 2.S3 entry `<action>` block that binds `{{MAX_FIX_ATTEMPTS}}`, `{{stage2_findings}}`, and `{{fix_attempts}}` (`:933-947`).
  - After the `{{stage2_findings}}` bind and before Phase B (`:956`), add an explicit instruction: iterate `{{stage2_findings}}`; for each finding that lacks a `finding_id`, assign one using a deterministic, in-array-unique rule (e.g. `<finding.source>-<zero-based index>`, or a uuid — choose a scheme that survives a finding being a qa-reviewer+bmad-code-review merged record).
  - Make the assignment idempotent: skip any finding that already carries a non-empty `finding_id` (covers re-presented findings on later loop iterations and ledger-rehydrated findings on resume).
  - State that uniqueness is scoped to this single story's `{{stage2_findings}}` array (one fix-mode invocation), matching the contract.

- [ ] **Task 2 — Close the normalization gap so no path reaches the fixer without finding_id** (AC 4)
  - In the `{{qa_findings}}` canonical normalization (`:700-727`), either add `finding_id` to the enumerated base fields, or add a one-line note that `finding_id` is assigned by the step 2.S3 assignment instruction (Task 1) as the single source of assignment.
  - Confirm the covered-by-composition path (`:765-781`, where `{{stage2_findings}} = {{cr_findings}}` only) flows through the same Task-1 assignment instruction so bmad-code-review-only findings are also keyed.

- [ ] **Task 3 — Reconcile the Phase B Input description and downstream references** (AC 3, 6)
  - Update the Phase B invocation Input line (`:957`) so it reflects that every passed finding carries `finding_id`.
  - Walk the disposition CASE blocks and the `{{fix_attempts}}` counter to confirm every `F.finding_id` / `F.id` reference now has a guaranteed inbound source; adjust wording only where a reference still implies the key might be absent.

- [ ] **Task 4 — Verify via EDD eval (skill-invoke) that the invariant holds** (AC 1, 3, 5)
  - Add and run a behavioral eval that exercises step 2.S3 with a stage-2 findings array containing findings with no `finding_id`, and confirms the workflow assigns ids before the fixer is invoked, assigns unique ids, and does not reassign an already-present id. (See Momentum Implementation Guide for the EDD cycle.)

## Dev Notes

### Decision Authority

This story is a defect fix that makes the conductor workflow comply with an existing, authoritative contract. The contract — `skills/momentum/references/directed-fix-invocation-contract.md` §"Finding Identification" (`:40-48`) — is the decision of record: `finding_id` is **Conductor-assigned, before fixer invocation, unique within one fix-mode call**. This story does not change the contract; it provisions the workflow to honor it. If the implementer believes the contract itself is wrong, that is an escalation/upstream-fix, not a silent in-tree contract edit (AC-7).

### Current State of affected files

`skills/momentum/skills/conductor/workflow.md` (2601 lines) — step 2.S3 is the stage-3 directed fix-loop:
- `:700-727` — canonical normalization building `{{qa_findings}}` from the qa-reviewer report. Populates `story_slug, source, verdict, severity, stakes_class, type, location, summary, detail, evidence, ac_id, legitimate, suggested_fix`. **`finding_id` is absent from this list.**
- `:758` / `:778-779` — `{{cr_findings}}` bound from bmad-code-review reviewer output; merged (dedicated-run path) or assigned directly (covered-by-composition path) into `{{stage2_findings}}`.
- `:936-939` — entry block binds `{{stage2_findings}}` and `{{fix_attempts}}` ("keyed by finding ID"). **No `finding_id` assignment exists between this bind and the fixer call.**
- `:956-968` — Phase B: invokes the directed fixer with `{{stage2_findings}}` as Input. This is the contract-violating call site.
- `:976`–`:1136` — disposition CASE blocks, each looking up the inbound finding by `F.finding_id` and each emitting ledger rows keyed by `finding_id`.
- `:377` / `:404` — ledger dedup guard keyed on `(story_slug, event, finding_id)`.

The fix is localized: add one assignment instruction in the entry block (Task 1), close the normalization gap (Task 2), and reconcile wording (Task 3). No script, config, or other skill changes.

### Architecture Compliance

- The `finding_id` is a **Conductor-internal correlation key**, not a member of the Canonical Normalized Finding Schema (`finding-schema.md`) — per the contract's closing note (`directed-fix-invocation-contract.md:48`). Do not add it to finding-schema.md; add it only as a Conductor-assigned field in the workflow.
- Assignment ownership is exclusive to the Conductor: not the reviewer (qa-reviewer / bmad-code-review), not the fix-mode. The single assignment site must live in the Conductor's step 2.S3, before Phase B.
- Idempotence is required because the build ledger's dedup guard relies on a stable `finding_id` across sessions (resume rehydration at step 2.0) — reassigning ids on a re-run would defeat the `(story_slug, event, finding_id)` dedup tuple. This is the seam shared with `conduct-ledger-append-site-dedup-guards` (see depends_on rationale below).

### depends_on rationale

`conduct-ledger-append-site-dedup-guards` operates on the same ledger/finding region: it hardens the append sites that emit `finding-disposition` / `stage3-escalation` rows keyed by `finding_id`. The dedup guards it adds presuppose a stable, Conductor-assigned `finding_id` — the exact key this story provisions. They must be reconciled so both stories agree on where `finding_id` originates and on the idempotence guarantee that keeps the dedup tuple stable across resume. Implement/merge this story's assignment instruction in a way consistent with the coupled story's append-site guards; if both are in the same sprint, coordinate the shared edits in step 2.S3 to avoid conflicting wording at `:976-1136`.

### Testing Requirements

Verification method: **skill-invoke** (advisory) — `change_type: skill-instruction` routes to `skill-invoke` per `skills/momentum/references/rules/verification-standard.md` §1. The workflow is a non-deterministic LLM instruction file, so verification is behavioral, not unit-test-based:
- Exercise step 2.S3 with a representative `{{stage2_findings}}` array whose findings have no `finding_id`. Observe that the workflow assigns ids before the fixer invocation, that ids are unique within the array, and that the fixer Input never contains a finding missing the key.
- Idempotence check: present an array where one finding already carries a `finding_id`; observe it is not reassigned.
- Covered-by-composition check: with a `{{cr_findings}}`-only `{{stage2_findings}}`, observe ids are still assigned.

### Project Context Reference

This story is part of the conduct (in-session sprint build orchestrator) hardening surfaced by the 2026-06-14 conduct sub-skills audit. It is one of a cluster of contract/idempotency defects in `skills/momentum/skills/conductor/workflow.md`; this one is the single genuine *contract* violation (others address resume idempotency and ledger dedup). The conductor is the load-bearing center of the Momentum cycle (see epic `momentum-sprint-orchestration`), so a correlation-key bug in the fix loop affects every story that produces findings.

### References

- Violated contract: `skills/momentum/references/directed-fix-invocation-contract.md:40-48` (§"Finding Identification") — Conductor assigns `finding_id` before fix-mode invocation; unique within one fix call; echoed in every disposition.
- Invocation site (the bug): `skills/momentum/skills/conductor/workflow.md:956` (step 2.S3 Phase B).
- Presupposing-but-unprovisioning entry block: `skills/momentum/skills/conductor/workflow.md:936-939`.
- Normalization omission: `skills/momentum/skills/conductor/workflow.md:700-727` (`{{qa_findings}}` base fields).
- Covered-by-composition path: `skills/momentum/skills/conductor/workflow.md:765-781`.
- Ledger dedup guard keyed on finding_id: `skills/momentum/skills/conductor/workflow.md:377`, `:404`.
- Audit source: `.momentum/handoffs/conduct-subskills-audit-2026-06-14.html` (second audit; flagged as the single genuine contract bug).
- Coupled story (same ledger/finding region): `conduct-ledger-append-site-dedup-guards`.
- Verification routing: `skills/momentum/references/rules/verification-standard.md` §1 (`skill-instruction → skill-invoke`).
- Epic context: `momentum-sprint-orchestration` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing the fix:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/conductor/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-assigns-finding-id-before-fixer.md`, `eval-finding-id-idempotent-on-rerun.md`, `eval-covered-by-composition-findings-keyed.md`).
   - Format each eval as: "Given [a `{{stage2_findings}}` array with/without pre-existing `finding_id`s], the conductor step 2.S3 should [assign unique ids before the Phase B fixer invocation / not reassign an existing id / key the bmad-code-review-only path]."
   - Test the observable behavior (every finding has a unique `finding_id` before `:956`; existing ids preserved), not exact wording.

**Then implement:**
2. Edit `skills/momentum/skills/conductor/workflow.md` per Tasks 1–3: add the assignment instruction in the step 2.S3 entry block, close the normalization gap, reconcile the Phase B Input and downstream references.

**Then verify:**
3. Run evals: for each eval file, spawn a subagent with the eval scenario as its task and the relevant step 2.S3 slice of workflow.md as context. Observe whether its behavior matches the expected outcome (ids assigned before fixer invocation; uniqueness; idempotence; covered-by-composition coverage).
4. If all evals match → task complete.
5. If any eval fails → diagnose the gap in the instruction text, revise, re-run (max 3 cycles; surface to developer if still failing).

**NFR compliance — this story edits an existing workflow.md, no new SKILL.md:**
- Do not bloat the step: the assignment is one tight instruction. Keep the conductor workflow's existing structure and vocabulary (it is already large — additive, surgical edits only).
- Preserve the established `{{var}}` binding style and the LEDGER/CASE block conventions already in step 2.S3.

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/conductor/evals/`.
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation).
- [ ] `finding_id` is assigned exactly once, by the Conductor, before the Phase B fixer invocation, and is unique within the story's `{{stage2_findings}}` array.
- [ ] Idempotence confirmed: re-running the assignment over an array with existing ids changes nothing.
- [ ] Covered-by-composition path confirmed to flow through the same assignment.
- [ ] No edits outside `skills/momentum/skills/conductor/workflow.md`; the contract file is unchanged (AC-7).
- [ ] Reconciled with `conduct-ledger-append-site-dedup-guards` where the same step 2.S3 region is touched.
- [ ] AVFL checkpoint on the produced workflow.md slice documented (momentum:dev runs this automatically — validates the edit against story ACs).

**Frozen verification contract reminder:** A frozen verification contract exists for this sprint at `.momentum/sprints/{sprint-slug}/specs/conduct-assign-finding-id-before-directed-fix-invocation.{ext}`. Before signaling done, read the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check. Do not read the verifier body (Part B: scenarios, assertion scripts, Gherkin) beyond sections explicitly referenced by `how_dev_self_checks`.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
