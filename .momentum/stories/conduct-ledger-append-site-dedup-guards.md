---
title: "Conduct — ledger append-site dedup guards"
story_key: conduct-ledger-append-site-dedup-guards
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug: ""
story_type: defect
priority: high
depends_on:
  - conduct-assign-finding-id-before-directed-fix-invocation
touches:
  - skills/momentum/skills/conductor/workflow.md
change_type:
  - skill-instruction
verification_method_advisory: skill-invoke
---

# Conduct — ledger append-site dedup guards

## Story

As a developer running a resumable `momentum:conduct` build,
I want the mandated `(story_slug, event, finding_id)` duplicate-prevention guard applied at **every** ledger append site that currently skips it — and the `:404` standing rule's dedup event-type list extended to cover the one event type it omits,
so that resuming a conduct build never double-appends finding rows, and finding counts, dedup logic, and governance guards stay correct across session death.

## Description

`skills/momentum/skills/conductor/workflow.md` step 2.0 (the `:404` DUPLICATE-PREVENTION standing rule) mandates that, before appending a `finding-disposition`, `stage3-escalation`, or `avfl-finding` row to the ledger during a live build, the Conductor checks the tuple `(story_slug, event, finding_id)` against `{{ledger_seen_events}}` and skips the append if the tuple is already present — then adds each newly appended tuple to `{{ledger_seen_events}}` so the check stays current throughout the build. This is the on-resume idempotency contract for the durable build ledger.

Only **one** append site actually implements the guard: the per-finding `avfl-finding` append at `:1797` (`Skip if (F.story_slug or "sprint-integration", "avfl-finding", F.finding_id) is already in {{ledger_seen_events}}` … `Add each newly appended tuple to {{ledger_seen_events}}`). Every other mandated site appends unconditionally:

- The **five `finding-disposition` append sites** in step 2.S3 — `:985` (scope-reverted), `:998` (fixed), `:1005` (dismissed), `:1010` (triaged-out), `:1017` (escalated) — all read "append per standing rule" but contain no skip-if-seen check and no add-after step.
- The **`stage3-escalation` append at `:1026`** (end-gate-expanded tier) — same omission.
- The **`stage3-mid-flight-escalation` append at `:1085`** — a count-level batch row that carries `finding_count` but **no `finding_id`**, so the `(story_slug, event, finding_id)` tuple as literally written does not key it. Two defects compound here: (1) this event type is **absent from the `:404` standing rule's dedup event-type list entirely** (the list names only `finding-disposition`, `stage3-escalation`, `avfl-finding`), and (2) even if added, the guard's key must be adapted for a row with no `finding_id`.

On resume, step 2.0 rehydrates `{{ledger_seen_events}}` from the durable ledger, but because these eight live-build append sites never consult it before appending (and the avfl-finding site is the only one that adds back to it), any story whose events survive from a prior session into the current session's ledger — and which is NOT re-run by the step 2.0 reconcile — can have its `finding-disposition` / `stage3-escalation` / `stage3-mid-flight-escalation` rows re-appended on the resume pass. That doubles ledger rows for the same finding, inflating `{{routine_auto_fixed_count}}`, the escalation accumulators, and the Phase 5 stakes-finding counts that drive the end-gate decision cards and governance guards.

From the 2026-06-14 conduct sub-skills audit (`.momentum/handoffs/conduct-subskills-audit-2026-06-14.html`).

**Pain context:** Resume idempotency defect in the live conduct build path. Without these guards every resume can double-append ledger rows, inflating finding counts and corrupting dedup/governance logic. Part of the idempotency cluster flagged by the 2026-06-14 conduct sub-skills audit.

## Acceptance Criteria

1. Each of the five `finding-disposition` append sites in step 2.S3 — `:985` (scope-reverted), `:998` (fixed), `:1005` (dismissed), `:1010` (triaged-out), `:1017` (escalated) — performs the `(story_slug, event, finding_id)` dedup check against `{{ledger_seen_events}}` **before** appending: if the tuple is already present, the append is skipped; otherwise the row is appended and the tuple is added to `{{ledger_seen_events}}` immediately after. The pattern mirrors the existing `avfl-finding` guard at `:1797` (skip-if-seen, then add-after).

2. The `stage3-escalation` append at `:1026` (end-gate-expanded tier) performs the same `(story_slug, "stage3-escalation", finding_id)` dedup check before appending and adds the tuple to `{{ledger_seen_events}}` after appending.

3. The `stage3-mid-flight-escalation` append at `:1085` performs a dedup check before appending and adds its key to `{{ledger_seen_events}}` after appending. Because this row is count-level and carries no per-finding `finding_id`, the guard uses a documented key adapted for this event type (e.g., `(story_slug, "stage3-mid-flight-escalation", null)` so the batch row is recorded at most once per story per session — consistent with how the existing `story-terminal` guard at `:422` keys a no-finding_id row as `(S.slug, "story-terminal", null)`). The chosen key is stated explicitly in the workflow text so a reader can reproduce the dedup semantics.

4. The `:404` DUPLICATE-PREVENTION standing rule's dedup event-type list is extended to include `stage3-mid-flight-escalation`. After the change, the standing rule enumerates all four guarded event types (`finding-disposition`, `stage3-escalation`, `avfl-finding`, `stage3-mid-flight-escalation`) and its prose remains internally consistent with how each site keys its tuple — including the explicit note that the `finding_id` component is `null` for the count-level `stage3-mid-flight-escalation` row.

5. No previously-guarded site loses its guard: the existing `avfl-finding` dedup at `:1797` (and the per-finding skip checks already present in the Phase 3 coverage-discharge / undischarged-deferral appends at `:1894`, `:1960`, `:1995`) remain intact and unmodified in behavior. The change is purely additive — it adds guards where they are missing; it does not remove or weaken any existing guard.

6. Each newly guarded append site's skip path is idempotent and silent on resume: when the tuple is already in `{{ledger_seen_events}}` (rehydrated from a prior session for a story that is NOT being re-run), the site skips the ledger append without erroring, without writing a duplicate row, and without altering the in-context accumulator state for that already-recorded event. The per-story re-run convention from step 2.0 (the reconcile resets in-progress stories to `ready-for-dev`) continues to determine which stories legitimately produce fresh events.

## Tasks / Subtasks

- [ ] **Task 1 — Guard the five `finding-disposition` append sites in step 2.S3.** (AC: 1, 6)
  - Edit `:985`, `:998`, `:1005`, `:1010`, `:1017` so each "LEDGER (phantom-store closure): append per standing rule …" instruction is preceded by a skip-if-seen check on `(story_slug, "finding-disposition", finding_id)` against `{{ledger_seen_events}}` and followed by an add-to-`{{ledger_seen_events}}` step on the appended tuple. Use the `:1797` avfl-finding guard as the canonical phrasing template so the four append sites are textually consistent.
  - Note: `:985` keys on `F.id`, `:998` on `F.id`, `:1005` on `F.id`, `:1010` on `F.finding_id`, `:1017` on `F.finding_id` — preserve each site's existing finding-id field name when forming the tuple; do not normalize the field references away.

- [ ] **Task 2 — Guard the `stage3-escalation` append at `:1026`.** (AC: 2, 6)
  - Add a skip-if-seen check on `(S.slug, "stage3-escalation", F.finding_id)` before the `:1026` append and an add-after step on the appended tuple, mirroring the avfl-finding guard at `:1797`.

- [ ] **Task 3 — Guard the `stage3-mid-flight-escalation` batch append at `:1085` with an adapted no-finding_id key.** (AC: 3, 6)
  - Add a skip-if-seen check before the `:1085` append and an add-after step. Because the row carries `finding_count` and no `finding_id`, key it as `(S.slug, "stage3-mid-flight-escalation", null)` (parallel to the `story-terminal` no-finding_id guard at `:422`). State the chosen key explicitly in the workflow text.

- [ ] **Task 4 — Extend the `:404` standing-rule dedup event-type list.** (AC: 4)
  - Add `stage3-mid-flight-escalation` to the list of guarded event types named in the `:404` DUPLICATE-PREVENTION note. Update the prose so it reads consistently with the four guarded event types and notes that the `finding_id` tuple component is `null` for the count-level `stage3-mid-flight-escalation` row.

- [ ] **Task 5 — Verify no existing guard regressed.** (AC: 5)
  - Confirm the `avfl-finding` guard at `:1797` and the Phase 3 coverage/deferral skip checks at `:1894`, `:1960`, `:1995` are unchanged in behavior. Confirm the change is purely additive across all touched lines.

- [ ] **Task 6 — EDD verification of resume idempotency.** (AC: 1, 2, 3, 5, 6)
  - Author and run behavioral evals (per the EDD guidance in the Momentum Implementation Guide below) that exercise the resume path: a ledger pre-seeded with prior-session `finding-disposition`, `stage3-escalation`, and `stage3-mid-flight-escalation` rows for a story that is NOT re-run, and confirm a second pass produces no duplicate rows.

## Dev Notes

### Decision Authority

This story implements the on-resume idempotency contract already mandated by the `:404` DUPLICATE-PREVENTION standing rule in `skills/momentum/skills/conductor/workflow.md`. The standing rule is the authority; this story closes the gap between what the rule mandates and what the append sites actually do. No new design decision is introduced — the work makes the existing rule's coverage complete and the existing avfl-finding guard pattern (`:1797`) the uniform template across all guarded sites.

This is part of the conduct resume/rehydration idempotency cluster surfaced by the 2026-06-14 conduct sub-skills audit (`.momentum/handoffs/conduct-subskills-audit-2026-06-14.html`).

### Current State of Affected Files

**`skills/momentum/skills/conductor/workflow.md`** (the sole touched file):

- **`:404` standing rule** — DUPLICATE-PREVENTION USE OF `{{ledger_seen_events}}`. Names exactly three guarded event types: `finding-disposition`, `stage3-escalation`, `avfl-finding`. **Omits `stage3-mid-flight-escalation`.** Defines the dedup tuple as `(story_slug, event, finding_id)`.
- **`:422`** — existing precedent for a no-finding_id guard: the `story-terminal` site checks/keys `(S.slug, "story-terminal", null)`. This is the template for the count-level `stage3-mid-flight-escalation` key in AC 3 / Task 3.
- **`:985`, `:998`, `:1005`, `:1010`, `:1017`** — the five `finding-disposition` append sites in step 2.S3 (scope-reverted, fixed, dismissed, triaged-out, escalated). All say "append per standing rule" but **none implement the skip-if-seen / add-after guard.** Finding-id field names differ per site (`F.id` at `:985`/`:998`/`:1005`; `F.finding_id` at `:1010`/`:1017`) — preserve each.
- **`:1026`** — the `stage3-escalation` (end-gate-expanded) append in the CASE escalated block. No guard.
- **`:1085`** — the `stage3-mid-flight-escalation` batch append. Carries `finding_count`, no `finding_id`. No guard, and its event type is absent from the `:404` list.
- **`:1797`** — the **only** correctly guarded append: `avfl-finding`. Skip-if-`(F.story_slug or "sprint-integration", "avfl-finding", F.finding_id)`-seen, then add-after. **This is the canonical pattern to replicate.**
- **`:1894`, `:1960`, `:1995`** — Phase 3 coverage-discharge / undischarged-deferral appends. These already guard against in-context `{{avfl_findings}}` duplication (skip if an entry with a synthetic finding_id already exists). Leave their behavior intact (AC 5).
- **Rehydration routing (`:260`–`:304`)** — step 2.0 replays ledger rows into `{{ledger_seen_events}}` (bound at `:378`) and the accumulators. The rehydration side is correct; the defect is entirely on the live-build **append** side not consulting/maintaining `{{ledger_seen_events}}`.

### Architecture Compliance

- This is a `skill-instruction` change to a `workflow.md` — it edits an LLM-driven workflow contract, not executable code. Per `change-types.md`, follow EDD (eval-driven development), not TDD.
- The edits must preserve the existing "append per standing rule" / "build ledger per standing rule" staging convention (the staging primitive owned by `conduct-conductor-staging-and-ledger-append-safety`). The dedup guard wraps the append; it does not change how staging/append is performed.
- The dedup key must remain `(story_slug, event, finding_id)` for all sites that have a finding_id, and the documented `null`-finding_id variant `(story_slug, event, null)` only for the count-level `stage3-mid-flight-escalation` row — consistent with the existing `(S.slug, "story-terminal", null)` precedent at `:422`.
- Change is additive only. Removing or weakening any existing guard (especially `:1797`) is out of scope and a regression.

### Testing Requirements

- **Verification method (advisory):** `skill-invoke` — per the routing table in `skills/momentum/references/rules/verification-standard.md` Section 1, `skill-instruction` → `skill-invoke`. The routing key for the harness/conductor is derived from `change_type` at sprint-planning time; this field is an advisory hint.
- **EDD evals** must exercise the resume idempotency contract, not just the happy-path append:
  - Eval A: Given a build ledger pre-seeded with a prior-session `finding-disposition` row for story X (not re-run), the workflow's step 2.S3 disposition path skips re-appending that row on the current pass — no duplicate row, no error.
  - Eval B: Given a prior-session `stage3-escalation` row for story X (not re-run), the `:1026` site skips the re-append.
  - Eval C: Given a prior-session `stage3-mid-flight-escalation` batch row for story X (not re-run), the `:1085` site skips the re-append using the `(X, "stage3-mid-flight-escalation", null)` key.
  - Eval D: For a story that IS re-run (reset to ready-for-dev by the step 2.0 reconcile), fresh disposition/escalation events ARE appended (the guard does not suppress legitimately new events).
- Test behaviors and decisions (skip vs. append) and the resulting ledger row counts — not exact prose of the workflow instructions.

### Project Context Reference

- Source audit: `.momentum/handoffs/conduct-subskills-audit-2026-06-14.html` (idempotency cluster).
- Coupled story (same ledger region — sequence first): `conduct-assign-finding-id-before-directed-fix-invocation` ensures every finding carries a stable `finding_id` BEFORE the directed fixer runs. The `(story_slug, event, finding_id)` dedup key in THIS story depends on that `finding_id` being present on the `finding-disposition` and `stage3-escalation` rows. If finding_id is absent, the tuple key collapses and the dedup guard cannot distinguish findings — hence the `depends_on` edge.
- Sibling story (staging primitive this work wraps): `conduct-conductor-staging-and-ledger-append-safety` owns the "append per standing rule" ledger-append staging convention. These guards sit immediately around those append calls; coordinate to avoid edit conflicts in step 2.S3 and the AVFL/escalation append regions.
- Sibling story (same audit cluster): `conduct-resume-and-rehydration-idempotency-hardening` addresses other resume/rehydration gaps in the same workflow.md; both touch the same file.

### References

- `skills/momentum/skills/conductor/workflow.md:404` — DUPLICATE-PREVENTION standing rule (the authority; event-type list to extend).
- `skills/momentum/skills/conductor/workflow.md:1797` — canonical guarded append pattern (`avfl-finding`).
- `skills/momentum/skills/conductor/workflow.md:422` — no-finding_id guard precedent (`(S.slug, "story-terminal", null)`).
- `skills/momentum/skills/conductor/workflow.md:985,:998,:1005,:1010,:1017,:1026,:1085` — unguarded append sites this story fixes.
- `skills/momentum/references/rules/verification-standard.md` §1 — change_type → verification-method routing.
- `skills/momentum/skills/create-story/references/change-types.md` — skill-instruction EDD template.
- `.momentum/handoffs/conduct-subskills-audit-2026-06-14.html` — source audit.
- Epic context: `momentum-sprint-orchestration` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1–6 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the change:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/conductor/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-resume-skips-duplicate-finding-disposition.md`, `eval-mid-flight-batch-dedup-null-key.md`, `eval-rerun-story-still-appends-fresh-events.md`).
   - Format each eval as: "Given [a build ledger pre-seeded with prior-session rows for a story not being re-run], the Conductor workflow should [skip the duplicate append / append fresh events for a re-run story]."
   - Test the skip-vs-append decision and resulting ledger row counts, not the exact prose of the instructions.

**Then implement:**
2. Edit the eight append sites (`:985`, `:998`, `:1005`, `:1010`, `:1017`, `:1026`, `:1085`) to add the skip-if-seen / add-after guard, and extend the `:404` standing-rule event-type list. Use the `:1797` avfl-finding guard as the canonical phrasing template.

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it the eval's scenario as its task and load the conductor SKILL.md + workflow.md as context. Observe whether the subagent's behavior (skip vs. append) matches the eval's expected outcome.
4. If all evals match → tasks complete.
5. If any eval fails → diagnose the gap in the workflow instructions, revise, re-run (max 3 cycles; surface to the developer if still failing).

**NFR compliance — mandatory for skill-instruction tasks:**
- This story edits `workflow.md` only (not `SKILL.md`); the SKILL.md `description` ≤150 chars, `model:`/`effort:` frontmatter, and `momentum:` namespace constraints are unchanged — confirm they are not disturbed by the edit.
- Keep the `workflow.md` edits surgical and consistent with the surrounding step-2.S3 / AVFL-phase phrasing. Do not balloon the body; the guard text per site is short (skip-if-seen + add-after), mirroring `:1797`.

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/conductor/evals/`.
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation).
- [ ] Every one of the eight named append sites carries a skip-if-seen check AND an add-after step.
- [ ] The `:404` standing-rule event-type list names all four guarded events, including `stage3-mid-flight-escalation`, with the `null` finding_id note for the count-level row.
- [ ] No existing guard (`:1797`, `:1894`, `:1960`, `:1995`) regressed — change is additive only.
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically — validates the implemented workflow.md against story ACs).

**Frozen verification contract reminder:** A frozen verification contract exists for this sprint at `sprints/{sprint-slug}/specs/conduct-ledger-append-site-dedup-guards.{ext}`. As a self-check before signaling done, the dev reads only the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`). The dev never reads the verifier body (Part B: scenarios, assertion scripts, Gherkin) beyond sections explicitly referenced by `how_dev_self_checks`.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
