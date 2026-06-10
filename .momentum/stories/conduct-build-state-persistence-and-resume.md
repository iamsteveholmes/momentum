---
title: Persist Conductor build state to an append-only ledger — end-gate and resume must survive session death and compaction
story_key: conduct-build-state-persistence-and-resume
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
priority: critical
change_type:
  - skill-instruction
verification_method_advisory: skill-invoke
depends_on: []
touches:
  - skills/momentum/skills/conductor/workflow.md
  - skills/momentum/skills/conductor/references/build-ledger.md
  - skills/momentum/references/build-results-ledger-schema.md
---

# Persist Conductor build state to an append-only ledger — end-gate and resume must survive session death and compaction

## Story

As a developer running a conduct build,
I want every state-bearing build event written to a durable append-only ledger the moment it happens,
so that the single human end-gate and partial-run resume survive session death and context compaction — instead of silently losing findings, dispositions, escalations, and quarantine records held only in volatile in-context variables.

## Description

Every input to the single human end-gate currently lives only in volatile in-context variables. Step 2.0 of `skills/momentum/skills/conductor/workflow.md` (lines 220–233) initializes ~12 Conductor-scoped in-memory collections — `{{build_log}}`, `{{escalations}}`, `{{end_gate_escalations}}`, `{{contract_integrity_stops}}`, `{{conductor_reverted_fixes}}`, `{{coverage_discharge_results}}`, `{{merged}}`, `{{blocked}}`, `{{retries}}`, `{{merge_attempts}}`, `{{frontier}}`, `{{running}}` — plus per-story state bound inside step 2.S3 (`{{fix_attempts}}`, `{{finding_dispositions}}`, `{{mid_flight_escalations}}`) and per-story `{{writable_files}}` (step 2.1). **No step anywhere writes any of them to disk** (verified by grep: zero persistence hits in the 2,136-line workflow).

Phase 5 reconstructs the entire end-gate report and all terminal status transitions from these accumulators (lines 1776–1814). Partial-run resume seeds only `{{merged}}` from story statuses (lines 235–241) — findings, dispositions, escalations, and quarantine records from a prior session are unrecoverable.

There is also a confirmed internal contradiction — the **"phantom store" defect**: per-story `{{finding_dispositions}}` is bound `= []` fresh for each story (line 577) and is never folded into `{{build_log}}` — the merged event at line 1153 appends only `findings_summary: S.leftover_findings` and merge-path escalations. Yet Phase 5's scorecard reconciliation (line 1797) instructs: "Scan all per-story `{{finding_dispositions}}` records in `{{build_log}}`" — records that were never put there. Even within a single uninterrupted session, the scorecard reconciliation reads a store that does not exist.

A session death or context compaction at story 20 of a 25-story build silently corrupts the one human gate the whole design leans on (DEC-035's single end-gate).

**Precedent:** both hand-run rehearsal sprints (conduct-core, conduct-runnable) wrote incremental `.momentum/*-build-results.jsonl` ledgers — the humans did by instinct what the skill never instructs. A stable row schema already exists (`skills/momentum/references/build-results-ledger-schema.md`, v1.0, 2026-06-07) and a controlled-enum finding schema shipped in conduct-runnable (`skills/momentum/references/finding-schema.md`, v1.1).

**The fix:** mandate an append-only JSONL build ledger at `.momentum/sprints/{{sprint_slug}}/build-ledger.jsonl`, written by the Conductor at every state-bearing event. Phase 5 assembles `{{stakes_findings}}` and all supporting report variables from the LEDGER, not from in-context memory. Step 2.0 resume rehydrates all accumulators from the ledger when one exists for the active sprint. The row vocabulary aligns with the existing build-results-ledger-schema.md and finding-schema.md controlled enums — no new parallel shape.

**Source:** confirmed finding from the 2026-06-09 conductor effectiveness review — adversarially verified, high confidence, confirmed independently by three review lenses.

## Acceptance Criteria

1. **Ledger exists and is sprint-scoped.** When a conduct build starts (or resumes) for a sprint, the Conductor maintains an append-only JSONL build ledger at `.momentum/sprints/{{sprint_slug}}/build-ledger.jsonl`, creating the file on first write if it does not exist. One ledger per sprint; rows are only ever appended.
2. **Every state-bearing event is appended at event time.** The workflow instructs a ledger append at the moment each of the following occurs (not batched at phase end): story launch (pipeline spawn), per-story stage transitions (stage-1 → stage-2 → stage-3), each finding disposition (per finding: fixed / dismissed / triaged-out / escalated / blocked / scope-reverted), per-story terminal signals (merged | failed), merge and quarantine outcomes, escalations on both tiers (mid-flight and end-gate-expanded), coverage deferrals and coverage discharges, contract-integrity stops, scope-reverted fixes, and end-gate change-request fixer events. A crash at any point loses at most the event in flight — never previously recorded state.
3. **Row vocabulary aligns with existing schemas — no new shape.** Ledger rows carry a real story slug as the join key (field name consistent with the canonical-join-key rule), an `event` field drawn from a controlled event-type set, and reuse the existing controlled enums verbatim: `disposition` (finding-schema §Disposition plus the documented `blocked`/`scope-reverted` extensions from workflow step 2.S3), `severity`, `type`, `stakes_class`, and `timing_tier` from finding-schema.md v1.1. No `key` field. No prose-label rows. No enum values invented outside the existing vocabulary.
4. **The phantom store is eliminated.** Every per-story `{{finding_dispositions}}` record is durably appended to the ledger before that story's pipeline emits its terminal signal, and Phase 5's scorecard reconciliation reads disposition records from the ledger — not from a per-story in-context variable that was reset between stories. The reconciliation instruction at Phase 5 no longer references disposition records "in `{{build_log}}`" that no step ever placed there.
5. **Phase 5 assembles the end-gate from the ledger.** `{{stakes_findings}}` (all three sources) and every supporting report variable — `{{routine_auto_fixed_count}}`, `{{dismissed_findings}}`, `{{stories_built_count}}`, `{{blocked_stories}}`, `{{quarantined_stories}}`, `{{contract_integrity_stops}}`, `{{mid_flight_escalations}}`, `{{high_risk_divergences}}`, `{{undischarged_deferrals}}`, and the conductor-revert reconciliation inputs — are assembled by reading the ledger. In-context accumulators may remain as a write-through convenience, but the ledger is the authoritative source at end-gate assembly, and the workflow says so explicitly.
6. **Resume rehydrates from the ledger.** At step 2.0, when a build ledger already exists for the active sprint, the Conductor rehydrates all Conductor-scoped accumulators from it — finding dispositions, escalations (both tiers), quarantine records, integrity stops, reverted fixes, coverage deferrals/discharge results, retries, and build-log events — before computing the frontier. The existing status-based `{{merged}}` seeding and in-progress reconcile are retained and cross-checked against the ledger rather than replaced.
7. **Interrupted-then-resumed equals uninterrupted.** A build interrupted after any number of stories and resumed in a fresh session produces an end-gate report containing the same findings, dispositions, escalations, quarantine records, and scorecard counts for the pre-interruption stories as an uninterrupted run would have — no silent loss, no double-counting on re-append after resume (rehydration plus idempotent-append guidance prevents duplicate rows for already-recorded events).
8. **Append-only corrections.** The Conductor never rewrites or deletes existing ledger rows. Corrections and overrides (e.g., the Phase 5 scorecard-revert-reconciliation disposition override from `fixed` to `scope-reverted`) are expressed as new override rows, preserving the original record — consistent with the existing "do NOT mutate the raw `{{build_log}}`" rule.
9. **Behavioral evals exist and pass.** Per EDD, behavioral evals in `skills/momentum/skills/conductor/evals/` demonstrate at minimum: (a) state-bearing events produce ledger appends at event time, (b) step 2.0 rehydrates accumulators from an existing ledger on resume, and (c) Phase 5 assembles end-gate variables from the ledger rather than in-context memory.

## Tasks / Subtasks

- [ ] Task 1 — EDD first: write behavioral evals (AC: 9)
  - [ ] In `skills/momentum/skills/conductor/evals/`, add 3 evals before touching the workflow: ledger-append-at-state-bearing-events, resume-rehydrates-from-ledger, phase5-assembles-from-ledger. Format: "Given [context], the skill should [observable behavior]". Test behavior, not exact row text.
- [ ] Task 2 — Define the build-ledger event row schema (AC: 1, 3, 8)
  - [ ] Author `skills/momentum/skills/conductor/references/build-ledger.md`: ledger path (`.momentum/sprints/{{sprint_slug}}/build-ledger.jsonl`), append-only rules, the controlled event-type set (derive from the event names already used in `{{build_log}}` appends — e.g., `story-launched`, `stage-transition`, `finding-disposition`, `stage3-fix-scope-reverted`, `stage3-escalation`, `stage3-mid-flight-escalation`, `stage3-finding-blocked`, `merged`, `retry`, `blocked`, `quarantined`, `mid-flight-escalation`, `coverage-disposition-deferred`, `coverage-deferral-discharged`, `coverage-deferral-undischarged`, `contract-integrity-stop`, `e2e-*`, `endgate-*`, `scorecard-revert-reconciliation` — keep existing names; do not rename established events), per-event required fields, the join-key rule, idempotent re-append guidance for resume, and the override-row pattern for corrections. Note the existing `{{build_log}}` rows are heterogeneous — some carry `event:` (e.g., `retry`, line 1195) while terminal rows carry `outcome:` (e.g., `merged`, line 1153): the reference must define one normalization (recommended: every ledger row has an `event` field; terminal rows use an event like `story-terminal` with `outcome` as a payload field) and state it explicitly so producers never mix the two.
  - [ ] Reuse enum vocabulary by reference (link to `finding-schema.md` v1.1 and `build-results-ledger-schema.md` v1.0) — do not restate or fork the enums.
  - [ ] In `skills/momentum/references/build-results-ledger-schema.md`, add a short cross-reference note: the story-level build-results row is derivable from the event-level build ledger; the two are companion schemas joined on the story slug. Do not change the v1.0 row shape.
- [ ] Task 3 — Step 2.0: ledger init + rehydration (AC: 1, 6, 7)
  - [ ] In `workflow.md` step 2.0, add ledger initialization (bind `{{ledger_path}}`; create on first append) and a rehydration pass: when the ledger exists, replay rows to rebuild all Conductor-scoped accumulators before the `{{merged}}` status-seed and in-progress reconcile run; cross-check ledger-derived state against story statuses and prefer the richer ledger record for findings/dispositions/escalations.
  - [ ] Specify duplicate-prevention on resume: events already present in the ledger are not re-appended when their stories are not re-run.
- [ ] Task 4 — Wire appends at every state-bearing event site (AC: 2, 4, 8)
  - [ ] Convert every existing `{{build_log}}` append instruction into "append to `{{build_log}}` AND append the same row to the ledger" (sites include ~lines 623, 653, 686–687, 711, 756, 768, 813, 830, 844, 1153, 1195, 1204, 1215, 1285–1305, 1440, 1483, 1532, 1565, 1587, 1676, 1687, 1691, 1800, 1891, 1940, 2049, 2052, 2078, 2106 — re-locate by content, line numbers drift).
  - [ ] Add ledger appends for state-bearing events that currently never reach `{{build_log}}` at all: story launch (step 2.1 pipeline spawn), stage transitions (2.1 → stage-2 ~line 371, → stage-3 ~line 427), every `{{finding_dispositions}}` record (step 2.S3 lines 629, 634, 638, 644, 755 — this closes the phantom store), quarantine outcomes (step 2.2.M.5), contract-integrity stops (step 2.V path ~line 497), and end-gate escalation accumulation (`{{end_gate_escalations}}` writes in step 2.2).
  - [ ] Keep append mechanics simple and tool-free: a single-line `Bash` append of one JSON object per event (`printf '%s\n' '<row>' >> {{ledger_path}}`); no new script, no momentum-tools change.
- [ ] Task 5 — Phase 5: assemble from the ledger (AC: 4, 5, 8)
  - [ ] Rewrite the Phase 5 assembly instructions (lines 1776–1814) to source `{{stakes_findings}}` Sources 1–3 and all supporting report variables from ledger rows; keep the existing dedup, reconciliation, and exclusion logic intact but pointed at the ledger.
  - [ ] Fix the scorecard-revert-reconciliation instruction to scan ledger `finding-disposition` rows (not "per-story `{{finding_dispositions}}` records in `{{build_log}}`"); express the disposition override as an appended override row plus the existing assembled-view-only override.
- [ ] Task 6 — Run evals and self-check (AC: 7, 9)
  - [ ] Run the 3 evals via subagent per EDD; fix instruction gaps; max 3 cycles.
  - [ ] Self-check AC 7 by walking the interrupted-at-story-N scenario through the revised step 2.0 + Phase 5 text and confirming every accumulator consumed in Phase 5 is recoverable from ledger rows alone.

## Dev Notes

### Current state of the files being modified (read before editing)

**`skills/momentum/skills/conductor/workflow.md`** (UPDATE — 2,136 lines). Structure: Phase 1 pre-flight (step 1, ~58–199, single ask), Phase 2 build (step 2: 2.0 init ~213–274; 2.1 launch + freeze gate + coverage branch ~276–860; 2.V integrity gate ~449–533; 2.S3 fix loop ~534–860; 2.2 heartbeat/signals ~862–1317; 2.F escalation hook), Phase 3 AVFL-on-merge (~1318–1605), Phase 4 E2E (~1606–1770), Phase 5 end-gate (~1771–2136 incl. request-changes redispatch loop with `endgate-*` events).

- **What it does today:** all build state is in-context only. Step 2.0 initializes the 12 Conductor-scoped collections (220–233); resume seeds only `{{merged}}` from story statuses (235–241) and reconciles in-progress stories (243–255). Per-story state binds fresh inside 2.S3 (`{{fix_attempts}}`, `{{finding_dispositions}}`, `{{mid_flight_escalations}}` — lines 573–583) and 2.1 (`{{writable_files}}` ~line 322). `{{build_log}}` accumulates event objects in memory at ~30 sites (see Task 4 list). Phase 5 (1776–1814) assembles everything from these accumulators.
- **What this story changes:** adds disk persistence (ledger init/rehydrate in 2.0; appends at every state-bearing site; Phase 5 re-sourced to the ledger) and closes the phantom store.
- **What must be preserved — do not break:**
  - The **event vocabulary already in `{{build_log}}`** (e.g., `stage3-fix-scope-reverted`, `coverage-deferral-discharged`, `scorecard-revert-reconciliation`, `endgate-change-workflow-pass`). Ledger rows reuse these names; renaming breaks the end-gate renderer's expectations and retro tooling.
  - The **"do NOT mutate the raw `{{build_log}}`" rule** (line 1799): overrides are applied only to the assembled report view. The ledger extends this to disk: corrections are new rows, never edits.
  - The **conductor-scoped vs per-story-transient distinction** (line 1811): Phase 5 must source mid-flight escalations from the Conductor-scoped accumulator/ledger, never the per-story transient that resets each story. Rehydration restores the Conductor-scoped collections.
  - The **quarantine convention**: blocked/stranded stories keep non-terminal status until Phase 5 approve performs the single terminal transition (lines 1203–1204). Ledger rows record the outcome; they do not trigger status transitions.
  - The **single-ask invariant** (DEC-035): no new developer prompts anywhere — ledger writes are silent Conductor mechanics.
  - The **anti-firehose / narrow mid-flight bar** (DEC-036): persistence must not change escalation behavior, only record it.
  - Status transitions remain exclusively via `momentum-tools sprint status-transition` — the ledger is an additional record, not a replacement state machine, and `stories/index.json` stays owned by sprint-manager.

**`skills/momentum/references/build-results-ledger-schema.md`** (UPDATE — 106 lines, v1.0 stable 2026-06-07). Story-level: one row per story per run; `slug` is the canonical join key; `key` is banned. **This story does not change the v1.0 row shape** — it adds only a companion-schema cross-reference note. The event-level build ledger and the story-level build-results row are different granularities; a build-results row is derivable by folding a story's ledger events.

**`skills/momentum/skills/conductor/references/build-ledger.md`** (NEW). Follows the pattern of the existing conductor references (`escalation.md`, `endgate-report-renderer.md`, `per-story-review-diff-range.md`): a behavioral specification the workflow cites by name, not duplicated inline.

### The phantom store defect — exact evidence

- Line 577: `Bind {{finding_dispositions}} = []` — fresh per story inside 2.S3.
- Lines 629/634/638/644/755: disposition records written to `{{finding_dispositions}}` only.
- Line 1153 (merged event): appends `findings_summary: S.leftover_findings` + merge-path escalations to `{{build_log}}` — dispositions are NOT folded in.
- Line 1797 (Phase 5): "Scan all per-story `{{finding_dispositions}}` records in `{{build_log}}`" — reads a store no step populated. The ledger's per-finding `finding-disposition` rows become the real store this instruction needs.

### Schema alignment — controlled vocabulary, no forks

- Join key: every ledger row carries a real story slug (`story_slug`, matching finding-schema's canonical-join-key rule; build-results uses `slug` — the build-ledger reference must state which field name event rows use and keep it consistent across all rows). Conductor-level events not tied to a story (e.g., `endgate-report-re-rendered`) are the only permitted exception and must be explicitly enumerated in the reference — no prose-label keys (the conduct-core retro found exactly this drift).
- Enums by reference: `severity` (critical|major|minor|low), `type` (10-value closed set), `stakes_class` (4 values, default routine), `timing_tier` (end-gate-expanded|mid-flight), `disposition` (fixed|dismissed|triaged-out|escalated, plus workflow-documented `blocked` and `scope-reverted` extensions per step 2.S3 line 577–580 — the reference should note `scope-reverted` maps to `triaged-out` for schema consumers, as the workflow already states).
- `dismissed` rows must carry non-empty `dismissal_rationale` (Required-Rationale Rule) — the ledger inherits this invariant.

### Why event-time appends, not phase-end snapshots

The failure mode is session death/compaction mid-build. A snapshot written at phase boundaries still loses everything since the last boundary — at story 20 of 25 that can be hours of dispositions. JSONL append-per-event bounds the loss to one in-flight event and is exactly what both rehearsal sprints did by hand (`.momentum/conduct-core-build-results.jsonl` incrementally grown across rounds).

### Previous story intelligence

- **conduct-runnable sprint (25 stories, merged 2026-06-07/08):** post-merge AVFL required a 9-drift cross-story reconciliation pass (`fix(conduct)` commit 351b36c) — when editing many sites in this one large file, keep terminology identical across phases or AVFL will flag drift. Use one canonical phrase for the ledger ("the build ledger at `{{ledger_path}}`") everywhere.
- **conduct-state-machine-defects-shipped-unfixed:** MAJOR findings that lack a durable record get silently dropped — the same class of failure this story fixes at the persistence layer. Also: verify current line positions before editing; convergence commits have already shifted content (~lines cited here drift).
- **Retro finding (conduct-core):** build-results schema drifted mid-build (structured rows vs prose rows). The countermeasure is the same here: one stable event-row shape declared up front in a reference, no improvised fields.
- **Established pattern:** conductor behavior specs live in `references/` and the workflow cites them (escalation.md precedent from conduct-stakes-timing-escalation-mechanism). Follow it — keep workflow.md edits surgical, put the schema in the reference.

### Git intelligence

Recent commits (bcbb452..8195e75): conduct-runnable just merged; plugin at 0.28.0; the ledger schemas (`build-results-ledger-schema.md`, `finding-schema.md` v1.1) landed 2026-06-07 and are stable — align with them, do not version-bump them for this change (the build ledger is a new companion artifact, not a revision of either).

### Implementation guardrails

- This is a `skill-instruction` change: EDD, not TDD. No new scripts — appends are one-line Bash instructions inside workflow actions.
- `workflow.md` has no line-count NFR (the 500-line cap applies to SKILL.md, which this story does not touch). Still: prefer citing `references/build-ledger.md` over restating schema rules inline at 30 sites — a single "append to the ledger per references/build-ledger.md" clause keeps the diff small.
- Do not introduce any new `<ask>`: the ledger is invisible to the developer except as better end-gate fidelity and working resume.
- `.momentum/sprints/{{sprint_slug}}/` already holds per-sprint build artifacts (`contract-freeze-baseline.sha256`, `coverage-plan.md`, `specs/`) — `build-ledger.jsonl` belongs beside them.

### Project Structure Notes

- New file: `skills/momentum/skills/conductor/references/build-ledger.md` (conductor-scoped reference — conductor is the only writer of this ledger).
- Runtime artifact path: `.momentum/sprints/{{sprint_slug}}/build-ledger.jsonl` (gitignored or committed per sprint convention — the rehearsal ledgers at `.momentum/*.jsonl` are currently untracked; follow whatever the sprint dir already does for `coverage-plan.md`, which is committed).
- No changes to `momentum-tools`, `stories/index.json` ownership, or the sprint state machine.

### References

- Epic context: `momentum-sprint-orchestration` (from _bmad-output/planning-artifacts/epics.json)
- Conductor workflow (primary UPDATE target): `skills/momentum/skills/conductor/workflow.md` — step 2.0 init 220–233, resume seed 235–241, per-story binds 573–583, disposition writes 629–755, merged event 1153, Phase 5 assembly 1776–1814, endgate fixer events 1891–2106.
- Row-schema precedent: `skills/momentum/references/build-results-ledger-schema.md` (v1.0 — story-level companion; `slug` join key; `key` banned).
- Controlled enums: `skills/momentum/references/finding-schema.md` (v1.1 — severity/type closed sets, stakes_class, disposition, timing_tier, Required-Rationale Rule, canonical join key `story_slug`).
- Decisions: **DEC-035** (one human end-gate; legible auto-fix loop — the gate this story makes durable) and **DEC-036** (`_bmad-output/planning-artifacts/decisions/dec-036-conduct-hitl-calibration-2026-06-01.md` — stakes/timing tiers the ledger must record, bar must not be widened).
- Hand-run precedent ledgers: `.momentum/conduct-core-build-results.jsonl`, `.momentum/conduct-core-finding-cards-by-story.json`; sprint artifact dirs `.momentum/sprints/sprint-2026-06-05-conduct-runnable/`.
- Source finding: 2026-06-09 conductor effectiveness review (adversarially verified, high confidence, three independent lenses; conversation-level review — no committed artifact file).

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1–6 → skill-instruction (EDD)

All tasks modify markdown instruction files under `skills/momentum/` (conductor workflow, conductor references, shared schema references, conductor evals) — a single change type governs the whole story.

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for workflow.md or reference files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill changes:**
1. Write the 3 behavioral evals in `skills/momentum/skills/conductor/evals/` (Task 1 — the directory already exists):
   - One `.md` file per eval, named descriptively (e.g., `eval-ledger-append-at-state-bearing-events.md`, `eval-resume-rehydrates-from-ledger.md`, `eval-phase5-assembles-from-ledger.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text — do not pin evals to exact ledger row JSON or specific line numbers

**Then implement:**
2. Author `references/build-ledger.md`, then modify `workflow.md` (Tasks 2–5), then the cross-reference note in `build-results-ledger-schema.md`

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) the conductor SKILL.md + workflow.md (+ build-ledger.md) contents as context. Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- This story does NOT modify `skills/momentum/skills/conductor/SKILL.md` — if you find yourself editing it, stop and re-read the tasks. The ≤150-char description, `model:`/`effort:` frontmatter, and ≤500-line body NFRs apply to SKILL.md and are already satisfied; do not regress them.
- `workflow.md` has no line cap, but keep the diff surgical: cite `references/build-ledger.md` for schema rules instead of restating them at each of the ~30 append sites.
- Skill names keep the `momentum:` namespace (no new skills are created by this story).

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 3 behavioral evals written in `skills/momentum/skills/conductor/evals/` before implementation began
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] Conductor SKILL.md untouched (verify with `git diff --stat`)
- [ ] `build-results-ledger-schema.md` v1.0 row shape unchanged (cross-reference note only)
- [ ] No new `<ask>` introduced anywhere in workflow.md (single-ask invariant preserved)
- [ ] Event names in ledger rows match the existing `{{build_log}}` event vocabulary (no renames)
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically — validates the implemented changes against story ACs)

**Frozen verification contract reminder:** when this story enters a sprint, a frozen verification contract will exist at `sprints/{sprint-slug}/specs/conduct-build-state-persistence-and-resume.{ext}`. Dev reads the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before signaling done. Dev never reads the verifier body (Part B: scenarios, assertion scripts, Gherkin) beyond sections explicitly referenced by `how_dev_self_checks`.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
