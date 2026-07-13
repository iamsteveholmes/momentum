---
title: Conduct — resume and rehydration idempotency hardening
story_key: conduct-resume-and-rehydration-idempotency-hardening
status: ready-for-dev
epic_slug: momentum-conductor-core
feature_slug: 
story_type: defect
priority: high
depends_on: []
touches:
  - skills/momentum/skills/conductor/workflow.md
  - skills/momentum/skills/conductor/references/build-ledger.md
change_type:
  - skill-instruction
verification_method_advisory: skill-invoke
---

# Conduct — resume and rehydration idempotency hardening

## Story

As a developer running an autonomous conduct build,
I want conduct's interrupt/resume and rehydration paths to be idempotent,
so that resuming a build after a session death or context compaction never re-dispatches a completed story, never duplicates or corrupts build-ledger rows, and never loses in-flight accumulator state — the resumed build produces the same end-gate report as an uninterrupted run (NFR23).

## Description

The 2026-06-14 conduct sub-skills audit (`.momentum/handoffs/conduct-subskills-audit-2026-06-14.html`) flagged four resume-path idempotency gaps in `skills/momentum/skills/conductor/workflow.md`. Since that audit, three hardening stories have landed — `conduct-build-state-persistence-and-resume` (built the rehydration replay block + `references/build-ledger.md`), `conduct-ledger-append-site-dedup-guards` (added the live-append `{{ledger_seen_events}}` guard), and `conduct-assign-finding-id-before-directed-fix-invocation` (single-site `finding_id` assignment). Those stories closed the live-append side and part of the rehydration side, so this story targets the **residuals that remain in the current source**, verified against the file on 2026-07-13.

### Original audit gaps (preserved evidence) and current-source reconciliation

1. **REHYDRATION EXEMPTION not restated inline (RESIDUAL — hardening).** The exemption that replayed rows must not trigger a second ledger append exists once, at the top of Step 2 (`workflow.md:217`), and names Step 2.0's replay loop explicitly. It is **not co-located** with the ~30 `Append R to {{build_log}}` instructions inside the replay loop (`:260-394`), where the LEDGER-APPEND STANDING RULE (`:209-217`) would otherwise imply a second ledger append. Restating the exemption at the point of use hardens the loop against a future edit re-introducing the double-append.

2. **Finding-accumulator rehydration lacks `finding_id` supersession (RESIDUAL — live defect).** The replay into `{{avfl_findings}}` (`:346-357`) and `{{e2e_findings}}` (`:359-375`) appends every matching ledger row with **no `finding_id` dedup or last-write-wins**. FR141 makes corrections **append-only override rows**, so the ledger legitimately holds more than one row per `finding_id`; and a re-run story (Step 2.0 reconcile resets `in-progress → ready-for-dev`, `:414-424`) leaves its prior-attempt rows in the ledger while `RE-RUN KEY CLEARING` only clears `{{ledger_seen_events}}` — it does not remove the prior entries already rehydrated into the accumulators. The SUPERSESSION RULE that fixes this at Phase 5 (`:2245`) covers only `finding-disposition` and `story-terminal` rows — **not** `avfl-finding` / `e2e-stakes-escalation` / `e2e-finding-auto-fixed`. Net effect: on resume, `{{avfl_findings}}`/`{{e2e_findings}}` double-count, inflating the MAJOR-RESIDUAL GOVERNANCE GUARD (`:2360`) and Phase 5 counts.

3. **No Phase 5 (end-gate) completion checkpoint (RESIDUAL — live defect).** The PHASE CHECKPOINT RULE (`:380-393`) has resume-skip checkpoints for AVFL (`avfl-on-merge-complete`) and E2E (`e2e-phase-complete`) but **none for Phase 5**, and `references/build-ledger.md` defines no `end-gate-phase-complete` event. Individual Phase-5 append sites are partly protected (the `scorecard-revert-reconciliation` override is `finding_id`-guarded at `:2277`), but the **approve-side mutations** — `git merge sprint/{slug}` then `git branch -d sprint/{slug}` (`:2344-2348`) and the per-story `verify→done` / `closed-incomplete` terminal transitions (`:2350-2358`) — have no completion checkpoint. On resume after a partial approve, Phase 5 re-executes and attempts to re-merge a deleted branch and re-transition already-`done` stories (both error against real state).

4. **`{{build_cross_artifact_notes}}` empty-init — OUT OF SCOPE (reconciled out).** The current source **annotates this as correct-by-design**: `workflow.md:243` states "no ledger event — empty-init every session start is correct." Any ledger-event treatment of cross-artifact notes is owned by the separate epic story `cross-artifact-note-ledger-event` (not in sprint-2026-07-13). This story does **not** modify `{{build_cross_artifact_notes}}`. See Dev Notes → Scope Boundary.

**Pain context:** Resume idempotency defects in the live conduct build path corrupt end-gate report assembly and finding accumulators when a build resumes. This story maps directly to the `momentum-conductor-core` acceptance condition: "A developer can interrupt and resume a conduct run and observe the build continue from persisted state without duplicated or lost story work."

## Acceptance Criteria

1. **NFR23 resume-equivalence invariant holds.** Killing a conduct session mid-build (or after context compaction) and re-invoking `/momentum:conduct` on the same activated sprint yields an end-gate report identical in content to an uninterrupted run over the same stories: no already-merged story is re-dispatched, no build-ledger row is duplicated, and no in-flight accumulator is lost. (Source: PRD NFR23; epic `momentum-conductor-core` acceptance condition #2.)

2. **REHYDRATION EXEMPTION is restated inline in the replay loop.** The Step 2.0 replay action (`workflow.md:260-394`) states, at the point where it appends replayed rows into `{{build_log}}`, that these replay appends do NOT trigger a second ledger append — so a resume never doubles the ledger. Observable: after a resume, the ledger's line count equals its pre-interrupt count plus only genuinely new live-event rows; no replayed row is re-appended. (Source: `workflow.md:217` REHYDRATION EXEMPTION, `:209-217` LEDGER-APPEND STANDING RULE, `:260-394` replay loop.)

3. **Finding accumulators are collapsed by `finding_id` on rehydration.** When the ledger holds more than one row for the same `finding_id` — an append-only correction/override row (FR141) or both prior-attempt and current-attempt rows for a re-run story — rehydration of `{{avfl_findings}}` and `{{e2e_findings}}` keeps exactly one entry per `finding_id` using last-write-wins by `ts`; and when Step 2.0 reconcile resets a story to `ready-for-dev`, that story's prior entries are removed from `{{avfl_findings}}`/`{{e2e_findings}}` (mirroring the existing `RE-RUN KEY CLEARING` of `{{ledger_seen_events}}`) so a fresh re-run does not double-count. Observable: after a resume over a ledger containing an override row (or a re-run story), the MAJOR-RESIDUAL GOVERNANCE GUARD and Phase 5 counts reflect one entry per finding, not duplicates. (Source: `workflow.md:346-375` rehydration, `:414-424` re-run reconcile + key clearing, `:2245` SUPERSESSION RULE scope, `:2360` guard; FR141 append-only override rows.)

4. **Phase 5 gains a resume-skip completion checkpoint.** `references/build-ledger.md` defines an `end-gate-phase-complete` event in its controlled event-type set; the Conductor appends it when the Phase 5 approve sequence has completed (sprint→main merge done and all per-story terminal transitions applied); and the PHASE CHECKPOINT RULE (`workflow.md:380-393`) skips the approve-side mutations on resume when that event is present. Observable: killing a session after approval (sprint merged, `sprint/{slug}` branch deleted, stories transitioned) and re-invoking does NOT attempt to re-merge the deleted branch or re-transition already-`done` stories — the build recognizes completion and re-renders the same end-gate report from the ledger. (Source: `workflow.md:380-393` checkpoint rule, `:2343-2358` approve branch; `build-ledger.md` event vocabulary + Phase 5 summary-row table `:124-127`.)

5. **All guards preserve the append-only ledger contract.** Every change is additive: no guard rewrites or deletes an existing ledger row, corrections remain append-only override rows, and the only new vocabulary is the single `end-gate-phase-complete` event — no parallel event set is introduced. Observable: after any number of resume cycles, `build-ledger.jsonl` remains valid append-only JSONL with every row carrying `event`, `story_slug`, and `ts`. (Source: FR141; `build-ledger.md:34-40` Row Shape + normalization rule, `:136` enum-reuse.)

## Tasks / Subtasks

- [ ] **Task 1 — Restate the REHYDRATION EXEMPTION inline in the replay loop** (AC 2, AC 1)
  - [ ] In `workflow.md` Step 2.0 replay action (`:260-394`), add an inline restatement, adjacent to the `Append R to {{build_log}}` routing, that replay appends are a REBUILD only and do NOT re-append to the ledger (cross-reference `:217`).
  - [ ] Confirm no wording implies the standing rule's implicit ledger append applies inside the replay loop.

- [ ] **Task 2 — Add `finding_id` supersession to finding-accumulator rehydration** (AC 3, AC 1)
  - [ ] In the `avfl-finding`, `e2e-stakes-escalation`, and `e2e-finding-auto-fixed` rehydration clauses (`:346-375`), collapse rows by `finding_id` using last-write-wins by `ts` so each accumulator holds one entry per `finding_id` (aligning with the Phase 5 SUPERSESSION RULE at `:2245`).
  - [ ] In the Step 2.0 re-run reconcile / `RE-RUN KEY CLEARING` block (`:414-424`), also remove the reset story's prior entries from `{{avfl_findings}}` and `{{e2e_findings}}` so the fresh re-run's live appends do not double-count.
  - [ ] Verify the MAJOR-RESIDUAL GOVERNANCE GUARD (`:2360`, source (a)/(c)) and Phase 5 Sources 2–3 observe one entry per finding after resume.

- [ ] **Task 3 — Define and wire the `end-gate-phase-complete` checkpoint** (AC 4, AC 5, AC 1)
  - [ ] Add `end-gate-phase-complete` to the controlled event-type set and the Phase 5 summary-row table in `references/build-ledger.md` (`:104`/`:124-127` pattern; fields e.g. `stories_merged`, `stories_closed_incomplete`, `pushed`).
  - [ ] Append the event in `workflow.md` Phase 5 approve branch after the sprint→main merge and per-story terminal transitions complete (after `:2358`).
  - [ ] Extend the PHASE CHECKPOINT RULE (`:380-393`) so that on resume, if an `end-gate-phase-complete` row exists, the approve-side mutations (merge, `git branch -d`, terminal transitions) are skipped and the report is re-rendered from the ledger; the existing per-finding `scorecard-revert-reconciliation` guard (`:2277`) is left intact (not duplicated).
  - [ ] Route `end-gate-phase-complete` through the Step 2.0 replay generic `build_log` clause (`:264-274`) so rehydration recognizes it.

- [ ] **Task 4 — EDD verification of resume idempotency** (AC 1–5)
  - [ ] Author 2–3 behavioral evals under `skills/momentum/skills/conductor/evals/` exercising: (a) resume over a ledger with a duplicate/override `finding_id` yields no accumulator double-count; (b) resume after a completed approve does not re-merge/re-transition; (c) resume never re-appends a replayed row to the ledger.
  - [ ] Run the EDD cycle; record results in the Dev Agent Record.

## Dev Notes

### Decision Authority

- **NFR23 (Conduct Build State Durability)** and **FR141 (Conduct Build Ledger and Resume)** are the governing requirements. FR141 mandates: end-gate assembled from the ledger; in-context accumulators are write-through convenience only; re-invocation rehydrates all accumulators before computing the frontier; corrections are **append-only override rows** (never rewritten/deleted); row vocabulary reuses `finding-schema.md` v1.1 and `build-results-ledger-schema.md` v1.0 enums verbatim.
- **DEC-035** — one human end-gate; the gate this ledger makes durable (`build-ledger.md:173`).
- This is a **defect-hardening** story on the live build path. All edits are additive; none may weaken existing guards (`{{ledger_seen_events}}`, `scorecard-revert-reconciliation` idempotency guard, SUPERSESSION RULE).

### Current State of Affected Files

- `skills/momentum/skills/conductor/workflow.md` (2633 lines): LEDGER-APPEND STANDING RULE + REHYDRATION EXEMPTION (`:209-217`); Step 2.0 init (`:230-246`) + rehydration replay (`:257-397`); DUPLICATE-PREVENTION `{{ledger_seen_events}}` note (`:404`); re-run reconcile + RE-RUN KEY CLEARING (`:414-424`); PHASE CHECKPOINT RULE (`:380-393`); Phase 5 end-gate (`:2238-2392`), including AUTHORITATIVE SOURCE (`:2243`), SUPERSESSION RULE (`:2245`), `scorecard-revert-reconciliation` idempotency guard (`:2277`), approve branch merge + transitions (`:2343-2358`), MAJOR-RESIDUAL GOVERNANCE GUARD (`:2360`).
- `skills/momentum/skills/conductor/references/build-ledger.md` (175 lines): Row Shape table requiring `event`/`story_slug`/`ts` (`:34-40`); Controlled Event-Type Set + phase-summary tables (`:57`, `:94-127`); enum-reuse and every-row-has-`event` normalization rule (`:136`, `:175`). Currently has `avfl-on-merge-complete` and `e2e-phase-complete` summary events but **no** `end-gate-phase-complete`.

### Architecture Compliance

- The ledger is the durable source of truth; in-context accumulators are write-through caches rehydrated on resume (`workflow.md:2243`). Fixes must keep that invariant — never make an accumulator authoritative over the ledger.
- Reuse existing enum vocabulary verbatim (FR141); the only new token permitted is the `end-gate-phase-complete` event (AC 5).
- Idempotency guards follow the established pattern: check-before-append keyed on `finding_id` / `(story_slug, event, finding_id)` tuples, and phase-completion checkpoints keyed on the presence of a summary-row event.

### Scope Boundary (reconciliation of audit gap #4)

- **Out of scope:** `{{build_cross_artifact_notes}}` re-init. The current source (`workflow.md:243`) annotates empty-init-per-session as **correct by design**; any ledger-event treatment is owned by the separate epic story `cross-artifact-note-ledger-event`. Do not modify that accumulator in this story. This reconciliation follows the verify-before-acting principle — the 2026-06-14 audit predates the current annotation and the dedicated story.
- **Co-touch note:** the sibling story `conduct-conductor-staging-and-ledger-append-safety` (also in sprint-2026-07-13) touches the same `workflow.md`; both scopes are distinct (this = resume/rehydration idempotency; that = staging/append safety). The Conductor's merge/rebase machinery reconciles concurrent worktree edits; no `depends_on` edge is warranted.

### Testing Requirements

- **Verification method (advisory): `skill-invoke`.** Both touch targets are skill-instruction files (`conductor/workflow.md`, `references/build-ledger.md`), which route to `skill-invoke` per `skills/momentum/references/rules/verification-standard.md` §1. A **harness-profile** reference must be declared before verification (verification-standard §3); the `skill-invoke` driver in `momentum/verification-harness.json` governs it.
- These are non-deterministic LLM-prompt instructions — use **EDD**, not TDD (see Momentum Implementation Guide). Evals must exercise observable resume behavior, framed in ordinary-user terms (verification-standard §4): interrupt a build, re-invoke, observe no duplication / no re-dispatch / no lost state — not internal variable names as the assertion surface.
- The end-to-end proof of NFR23 (AC 1) is exercised most fully by the sibling `conduct-live-run-against-fixture-sprint` story; the evals here target the specific residual behaviors (AC 2–4) at the unit-of-behavior level.

### Project Context Reference

- Frozen verification contract: a per-sprint contract for this story is emitted at `.momentum/sprints/{sprint-slug}/specs/conduct-resume-and-rehydration-idempotency-hardening.{ext}`. The dev agent reads only the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before signaling done, and does **not** read the Part-B verifier body (scenarios / assertion scripts) beyond sections `how_dev_self_checks` explicitly references.

### References

- Epic context: `momentum-conductor-core` (from _bmad-output/planning-artifacts/epics.json)
- Audit evidence: `.momentum/handoffs/conduct-subskills-audit-2026-06-14.html` — the four original resume/rehydration idempotency gaps.
- PRD FR141 (Conduct Build Ledger and Resume) and NFR23 (Conduct Build State Durability) — `_bmad-output/planning-artifacts/prd.md`.
- Prior landed hardening (context, all `done`): `conduct-build-state-persistence-and-resume`, `conduct-ledger-append-site-dedup-guards`, `conduct-assign-finding-id-before-directed-fix-invocation`.
- Ledger spec: `skills/momentum/skills/conductor/references/build-ledger.md`.

### Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1–4 → skill-instruction (EDD) — edits to `conductor/workflow.md` and `references/build-ledger.md`

---

#### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for workflow.md / references files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the change:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/conductor/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-resume-does-not-double-count-avfl-findings.md`, `eval-resume-after-approve-skips-merge.md`, `eval-replay-does-not-re-append-ledger.md`).
   - Format: "Given [a build ledger / session state], the Conductor on resume should [observable behavior]."
   - Test behaviors and decisions (no double-count, no re-dispatch, no re-append), not exact instruction text.

**Then implement:**
2. Modify `workflow.md` (Tasks 1–3) and `references/build-ledger.md` (Task 3) per the ACs.

**Then verify:**
3. Run evals: for each eval, spawn a subagent, give it the eval scenario and the relevant skill contents (or invoke `/momentum:conduct` against a fixture ledger), and observe whether behavior matches.
4. All evals match → task complete. Any fail → diagnose the gap in the instructions, revise, re-run (max 3 cycles; surface if still failing).

**NFR compliance — mandatory for every skill-instruction task:**
- `conductor/workflow.md` has no SKILL.md frontmatter of its own, but the conductor SKILL.md `description` must stay ≤150 chars (NFR1) and `model:`/`effort:` present (FR23) — do not regress them if touched.
- Keep SKILL.md body ≤500 lines / 5000 tokens; overflow goes to `references/` (NFR3). `workflow.md` and `build-ledger.md` are the reference/instruction bodies — edits stay additive and minimal.
- `momentum:` namespace prefix preserved (NFR12).

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/conductor/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] No regression to conductor SKILL.md `description` (≤150 chars) or `model:`/`effort:` frontmatter if touched
- [ ] `build-ledger.md` change reuses existing enum vocabulary; only `end-gate-phase-complete` added (AC 5)
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically)
- [ ] A frozen verification contract exists for this sprint at `sprints/{sprint-slug}/specs/conduct-resume-and-rehydration-idempotency-hardening.{ext}`; dev reads the Part-A header only as a self-check before signaling done.

## Dev Agent Record

<!-- This section is populated only during and after development. -->

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
