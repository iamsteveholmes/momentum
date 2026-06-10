---
title: covered-by-composition must defer only the dedicated QA run — adversarial code review still runs on every story
story_key: conduct-coverage-deferral-preserve-code-review
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: bug
change_type:
  - skill-instruction
verification_method_advisory: skill-invoke
depends_on:
  - conduct-coverage-disposition-branch
  - conduct-per-story-build-review-dispatch
touches:
  - skills/momentum/skills/conductor/workflow.md
---

# covered-by-composition must defer only the dedicated QA run — adversarial code review still runs on every story

## Story

As the Conductor running the autonomous build phase,
I want `covered-by-composition` routing to defer only REVIEWER A's dedicated QA verification run — while still dispatching REVIEWER B (`momentum:code-reviewer`) on the per-story diff,
so that no story ever merges to the sprint branch without adversarial code review, and the build log never shows a deceptively clean empty findings list for a story whose bug-hunt was silently deleted.

## Description

**Source.** Confirmed finding from the 2026-06-09 conductor effectiveness review — adversarially verified, high confidence, confirmed independently by two review lenses.

**The defect.** In `skills/momentum/skills/conductor/workflow.md`, the stage-2 coverage routing (lines ~375-378) reads:

> Apply coverage routing established at 2.1.5:
> - If `{{coverage_disposition}}[S.slug]` == "covered-by-composition": **skip stage-2 entirely**; bind `{{stage2_findings}}` = [] and advance directly to stage-3 with an empty findings list.
> - If `{{coverage_disposition}}[S.slug]` == "dedicated-run" (default): dispatch the fan-out below.

Stage-2 contains **two** reviewers (lines ~391-414):

- **REVIEWER A** — `qa-reviewer` agent (~line 393): verifies the story's frozen verification contract; returns per-AC classification (VERIFIED / PARTIAL / MISSING / BLOCKED). This is the *QA verification run* whose timing/venue the coverage disposition legitimately controls.
- **REVIEWER B** — `momentum:code-reviewer` skill (~line 404): adversarial bug-hunting code review (bmad-code-review adapter) on the per-story diff, report-only, normalized findings with `stakes_class` populated. This is **not** a QA verification run — it has nothing to do with `coverage_disposition`.

But step 2.C's own guarantee (~line 787) insists:

> "Choosing `covered-by-composition` changes only the timing and venue of the QA run; it never demotes, hides, silences, or auto-resolves any finding."

And the downstream discharge consumer (step 3.D, ~lines 1502-1511) runs only a **behavioral integration scenario** against the sprint branch — it observes acceptance behavior; it is not a code review and never inspects the per-story diff.

**Net effect (the bug).** A story planned as `covered-by-composition` merges to the sprint branch with zero QA verification at build time (intended) AND zero adversarial code review at any time (NOT intended), with `{{stage2_findings}} = []` making the build log look clean. The "skip stage-2 entirely" wiring over-implements the deferral: the disposition was designed to move *QA timing*, not to delete the *bug-hunt*.

**Why it matters.** This is the exact "silently produce bad code" failure mode the Conductor architecture exists to prevent — sanctioned on the happy path. Step 2.C's prose guarantee and the stage-2 wiring contradict each other; the wiring wins at execution time, and the guarantee is silently false for every covered-by-composition story.

**The fix.** Amend the stage-2 coverage routing so `covered-by-composition` stories STILL dispatch REVIEWER B on the per-story diff (canonical Scenario A diff range), and only REVIEWER A's dedicated QA verification run is deferred to the named integration scenario. `{{stage2_findings}}` = REVIEWER B's findings (normalized, severity-sorted); the stage-3 fix loop runs normally on them. Update step 2.C's notes so the prose guarantee and the wiring agree.

## Acceptance Criteria

1. For a story whose `{{coverage_disposition}}[S.slug]` is `covered-by-composition`, stage-2 still computes `{{story_diff}}` using the canonical Scenario A diff range (per `references/per-story-review-diff-range.md`) and dispatches REVIEWER B (`momentum:code-reviewer`) on that diff with the same inputs and report-only constraint as the dedicated-run path. Only REVIEWER A (`qa-reviewer`) is not dispatched at build time — its dedicated QA verification run remains deferred to the named integration scenario at AVFL/merge.
2. For a `covered-by-composition` story, `{{stage2_findings}}` is bound to REVIEWER B's returned findings — normalized per the canonical finding schema (`finding-schema.md`), `stakes_class` populated, severity-sorted (critical → major → minor → low), source field `bmad-code-review`. `{{stage2_findings}}` is never unconditionally bound to `[]` by coverage routing.
3. The stage-3 fix loop (step 2.S3) runs normally on those findings: a `covered-by-composition` story with code-review findings enters the directed fix loop exactly as a dedicated-run story would; the empty-findings fast path in step 2.S3 applies only when REVIEWER B actually returns zero findings.
4. For a story whose disposition is `dedicated-run` (or defaulted to it), stage-2 behavior is unchanged: both reviewers dispatch concurrently, and `{{stage2_findings}}` remains the deduplicated, severity-sorted union of `{{qa_findings}}` and `{{cr_findings}}` per the existing merge/dedup rules.
5. Step 2.C's prose is reconciled with the wiring: the TIMING-AND-VENUE note (~line 787), the Path B action/notes (~lines 838-853), and the `coverage-disposition-deferred` build_log record state that the deferral covers ONLY the dedicated QA verification run (REVIEWER A / verifier dispatch), and that adversarial code review (REVIEWER B) still runs at build time on the per-story diff and is never deferred, demoted, or skipped by this disposition.
6. The step 2.1.5 routing prose ("Do NOT dispatch the verifier at build time for a story whose coverage_disposition is 'covered-by-composition'") is clarified so "the verifier" unambiguously means the dedicated QA verification run (REVIEWER A), not the stage-2 fan-out as a whole and not `momentum:code-reviewer`.
7. Existing step 2.C guardrails are preserved intact: no second dedicated QA verification run is introduced for a `covered-by-composition` story; the safe defaults (missing/unrecognized disposition → `dedicated-run`; missing `covered_by_scenario` → `dedicated-run`) are unchanged; the branch still never re-derives or overrides the frozen disposition; and dispatching REVIEWER B is not construed as a QA verification run anywhere in the amended text.
8. The downstream discharge consumer (step 3.D) is unchanged in behavior, and no amended prose implies the integration scenario performs or replaces code review — it discharges the deferred QA verification debt only.
9. All changes are confined to `skills/momentum/skills/conductor/workflow.md` (skill instruction file only — no scripts, schemas, rules, or other artifacts change).

## Tasks / Subtasks

- [ ] Task 1: Amend the stage-2 coverage routing block (`workflow.md` ~lines 373-378) (AC 1, 2, 4)
  - [ ] Replace the "skip stage-2 entirely; bind {{stage2_findings}} = []" branch with split routing: `covered-by-composition` → compute `{{story_diff}}` (Scenario A range, existing block at ~380-389) and dispatch REVIEWER B ONLY; `dedicated-run` → dispatch both reviewers (existing fan-out, unchanged).
  - [ ] For the covered-by-composition branch, bind `{{stage2_findings}}` = REVIEWER B's findings, normalized per finding-schema.md and severity-sorted (critical → major → minor → low). The dedup/merge rule remains applicable only to the two-reviewer path.
  - [ ] Keep the fan-out language accurate: on the covered-by-composition path a single agent is spawned (individual-agent fan-out semantics preserved; no TeamCreate).
- [ ] Task 2: Confirm stage-3 hand-off is unchanged (`workflow.md` ~lines 429-434 and step 2.S3 ~lines 535-600) (AC 3)
  - [ ] `{{stage2_findings}}` flows into step 2.S3 normally for both dispositions; the step 2.S3 empty-findings fast path (~line 586) fires only on a genuinely empty findings list.
  - [ ] No edits to step 2.S3 itself are expected — verify by read-through, not modification.
- [ ] Task 3: Reconcile step 2.C prose with the new wiring (`workflow.md` step 2.C, ~lines 783-856) (AC 5, 7)
  - [ ] Amend the TIMING-AND-VENUE note (~line 787) to state explicitly: the deferral moves the dedicated QA verification run (REVIEWER A) to the named integration scenario; adversarial code review (REVIEWER B, `momentum:code-reviewer`) still runs at build time on the per-story diff and is never deferred by this disposition.
  - [ ] Amend Path B's action and notes (~lines 838-853): "Skip the dedicated QA verification run" language stays, plus an explicit statement that stage-2 still dispatches the code reviewer; update the `coverage-disposition-deferred` build_log record note so the log reflects that code review ran at build time.
  - [ ] Verify the NON-GOALS block (~lines 789-795) and no-second-run guardrail (~line 851) remain true under the new wiring; adjust wording only if the new REVIEWER-B dispatch could be misread as a second QA run.
- [ ] Task 4: Clarify the 2.1.5 routing prose (`workflow.md` ~lines 299-312) (AC 6)
  - [ ] Scope "Do NOT dispatch the verifier at build time..." to the dedicated QA verification run (REVIEWER A); make clear stage-2's code-review dispatch is unaffected by the disposition.
- [ ] Task 5: Sweep for stale cross-references (AC 5, 8)
  - [ ] Grep `workflow.md` for "skip stage-2", "stage2_findings", "covered-by-composition", and "stage-2" and reconcile any remaining prose that asserts stage-2 is skipped wholesale (e.g., step 2.S3 invocation-context note at ~line 541 describes stage-2 output as "qa-reviewer + bmad-code-review" — ensure it reads correctly when only code-review findings are present).
  - [ ] Confirm step 3.D prose (~lines 1440-1560) needs no change: it discharges QA verification debt only and must not be described as a code-review substitute.
- [ ] Task 6: Self-check via skill-invoke walkthrough (AC 1-9)
  - [ ] Read the amended stage-2 routing end-to-end twice — once simulating a `covered-by-composition` story, once a `dedicated-run` story — and confirm: REVIEWER B dispatches in both; REVIEWER A dispatches only for dedicated-run; `{{stage2_findings}}` is correctly bound in both; stage-3 receives findings in both; step 2.C prose makes no claim the wiring contradicts.

## Dev Notes

This story modifies only the Conductor workflow instruction at `skills/momentum/skills/conductor/workflow.md` (2136 lines). It is `change_type: skill-instruction`, verified by `skill-invoke` (read-through walkthrough of the amended routing — there is no app/UI/backend lane). It is a surgical consistency fix: the wiring is brought into agreement with the prose guarantee that already exists at step 2.C; no new mechanism, schema, or vocabulary is introduced.

### Current state of the file being modified (read before editing)

- **Stage-2 block (~373-427), inside step 2.1.3's per-story pipeline:** routing at ~375-378 skips the whole stage for covered-by-composition; diff-range computation at ~380-389 (Scenario A, materialized diff, authoritative pattern in `references/per-story-review-diff-range.md`); REVIEWER A spec at ~393-402 (qa-reviewer: story_slug, worktree_path, verification_contract, story_diff; read-only; per-AC classification; source `qa-reviewer`); REVIEWER B spec at ~404-414 (momentum:code-reviewer: story_slug, story_diff, worktree_path, optional review_depth pass-through for the DEEPER-REVIEW OPT-IN; report-only; canonical finding schema; source `bmad-code-review`); merge/dedup of both arrays into `{{stage2_findings}}` at ~416-427.
- **Stage-3 hand-off (~429-434):** invokes step 2.S3 with `{{stage2_findings}}`; step 2.S3 (~535+) binds the merged array at ~574 and short-circuits to merge on empty findings at ~586-587. This machinery needs no change — it already handles any findings array.
- **Step 2.C (~783-856):** READS-DOES-NOT-DECIDE note; TIMING-AND-VENUE note (~787) carrying the prose guarantee this story enforces; NON-GOALS guardrails (~789-795); safe-default checks (missing/unrecognized → dedicated-run at ~811-816; covered-by-composition with no named scenario → dedicated-run at ~826-836); Path A (~819-824); Path B (~838-854) with the `coverage-disposition-deferred` build_log record and the DOWNSTREAM DISCHARGE note pointing at step 3.D.
- **Step 2.1.5 (~299-312):** binds `{{coverage_disposition}}[S.slug]` from step 2.C's routing outcome; ends with "Do NOT dispatch the verifier at build time for a story whose coverage_disposition is 'covered-by-composition'" — this sentence is *consistent* with the intended fix if "the verifier" is read as the QA verifier, but the stage-2 wiring over-implemented it into skipping both reviewers. Clarify, don't restructure.
- **Step 3.D (~1440-1560):** discharge consumer; spawns an integration-scenario executor (behavioral; ran/passed/deferred_story_observed; stakes_findings pass-through channel). Unchanged by this story.

### What must be preserved (do not break)

- **Step 2.C is timing-and-venue only.** It must keep reading the frozen disposition, never re-derive it, and never classify findings. This story narrows what "deferral" covers; it must not turn 2.C into a dispatcher.
- **No second dedicated QA run** for covered-by-composition stories (NON-GOAL 4, guardrail ~851). REVIEWER B's dispatch is a code review, not a QA verification run — say so explicitly so the no-second-run guard isn't misread as forbidding it.
- **Safe defaults unchanged:** missing/unrecognized disposition → dedicated-run; named-scenario precondition for Path B → otherwise dedicated-run.
- **Finding classification machinery untouched:** stakes classes, dispositions, timing tiers, the step 2.F mid-flight hook, dedup rules, and the finding schema are all out of scope. REVIEWER B findings on the covered-by-composition path flow through the *existing* stage-3/2.S3 machinery without any new routing.
- **DEEPER-REVIEW OPT-IN:** the `review_depth` pass-through to REVIEWER B (~409-411) must work identically on the covered-by-composition path.
- **Concurrency model:** individual-agent fan-out, never TeamCreate; the pipeline language ("Spawn the following two agents CONCURRENTLY") needs adjusting where only one agent spawns.
- **Conductor as sole git-mutation authority** and all WRITE-SCOPE rules — untouched.

### Implementation shape (suggested, not binding)

In the stage-2 block, replace the two-bullet routing with three-part logic: (a) always compute `{{story_diff}}` (Scenario A); (b) `dedicated-run` → existing two-reviewer concurrent fan-out + merge/dedup (verbatim); (c) `covered-by-composition` → dispatch REVIEWER B only; bind `{{qa_findings}}` = [] conceptually absent (do not fabricate an empty QA result — the QA run is deferred, not empty) and `{{stage2_findings}}` = REVIEWER B's normalized, severity-sorted findings. Keep the deferral record emission where it is (step 2.C Path B); only its note text changes to mention that code review still runs.

### Anti-patterns to avoid

- Do not "fix" this by making step 3.D run a code review — the fix direction is explicit: REVIEWER B runs at build time on the per-story diff.
- Do not introduce a new coverage_disposition value or a new finding source string; `bmad-code-review` remains the source for REVIEWER B findings.
- Do not relax or delete the prose guarantee at ~787 to match the broken wiring — the wiring moves to match the guarantee, not the reverse.
- Do not touch `references/per-story-review-diff-range.md`, `finding-schema.md`, the qa-reviewer agent, or `momentum:code-reviewer` — the contract surfaces of both reviewers are unchanged.

### Previous story intelligence

- `conduct-coverage-disposition-branch` (done) built step 2.C and its guarantees; its AC 6/7 are the prose this story now makes true in the wiring. Its dev notes stress the DEC-036 boundary — reuse that vocabulary verbatim when amending notes.
- `conduct-per-story-build-review-dispatch` (done) wired the stage-2 two-reviewer fan-out and the normalized-findings contract; the Scenario A diff-range rule itself is documented authoritatively in `references/per-story-review-diff-range.md`.
- `conduct-coverage-disposition-discharge-consumer` (done) built step 3.D; its stakes-findings pass-through (commit c3a56a9) shows the established pattern for not silently dropping findings — this story applies the same principle one stage earlier.
- Recent git history on this file is all surgical XML-step edits with `fix(conductor):`/`feat(conductor):` conventional commits; post-merge AVFL reconciliation passes (351b36c) catch cross-step drift — minimize drift by keeping edits tightly scoped to the blocks named in the tasks.

### Project Structure Notes

- Single-file change: `skills/momentum/skills/conductor/workflow.md`. The conductor skill directory also holds `SKILL.md` and `references/` — none of those change.
- Story file lives at `.momentum/stories/conduct-coverage-deferral-preserve-code-review.md`; index entry in `.momentum/stories/index.json` keyed by the slug.
- Verification: `skill-invoke` (per the verification-standard routing for `skill-instruction`). Self-check = the Task 6 dual-disposition walkthrough; a frozen verification contract will exist for this story in `sprints/{sprint-slug}/specs/` at sprint time — read only the Part-A header (how_dev_self_checks, verification_method, harness_profile) before signaling done.

### References

- Target file: `skills/momentum/skills/conductor/workflow.md` — stage-2 routing [~373-427], step 2.1.5 [~299-312], step 2.C [~783-856], step 2.S3 [~535-600], step 3.D [~1440-1560].
- [Source: skills/momentum/skills/conductor/references/per-story-review-diff-range.md] — canonical Scenario A pre-merge diff range.
- [Source: skills/momentum/references/finding-schema.md] — canonical finding record shape REVIEWER B already emits.
- Decision: DEC-035 — adopt conduct; single end-gate; legible auto-fix loop.
- Decision: DEC-036 — stakes-gated mid-flight tier; legible dispositions; anti-rubber-stamp end-gate (does not alter coverage routing; cited to keep the boundary language consistent).
- Finding provenance: 2026-06-09 conductor effectiveness review — adversarially verified, confirmed by two independent review lenses.
- Epic context: `momentum-sprint-orchestration` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1–6 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/conductor/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-covered-by-composition-still-dispatches-code-reviewer.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text
   - Suggested evals for this story: (a) Given a story whose frozen `coverage_disposition` is `covered-by-composition`, the Conductor should dispatch REVIEWER B (momentum:code-reviewer) on the per-story Scenario A diff and bind `{{stage2_findings}}` to its normalized, severity-sorted findings — and should NOT dispatch REVIEWER A; (b) Given a story whose disposition is `dedicated-run`, the Conductor should dispatch both reviewers concurrently and merge/dedup findings exactly as before; (c) Given a covered-by-composition story whose code review returns findings, the stage-3 fix loop should run on them rather than short-circuiting to merge.

**Then implement:**
2. Modify `skills/momentum/skills/conductor/workflow.md` per Tasks 1–5

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the relevant workflow.md sections as context (or invoke the skill via its Agent Skills name if installed). Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely. (This story does not modify the conductor SKILL.md; this item applies only if SKILL.md is touched, which would exceed scope — it must not be.)
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23) — unchanged by this story; do not regress.
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3). workflow.md is the overflow document and has no hard cap, but keep the edit surgical — no wholesale restructuring.
- Skill names use `momentum:` namespace prefix (NFR12) — unchanged.

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/conductor/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] No SKILL.md changes (out of scope for this story — workflow.md only); frontmatter NFRs not regressed
- [ ] Dual-disposition walkthrough (Task 6) completed and documented in Dev Agent Record
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically — validates the amended workflow.md against story ACs)

**Frozen verification contract reminder:** a frozen verification contract exists for this sprint at `sprints/{sprint-slug}/specs/conduct-coverage-deferral-preserve-code-review.{ext}`. Dev reads the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before signaling done. Dev never reads the verifier body (Part B: scenarios, assertion scripts, Gherkin) beyond sections explicitly referenced by `how_dev_self_checks`.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
