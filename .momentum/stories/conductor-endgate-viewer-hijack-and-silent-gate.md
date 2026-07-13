---
title: Conductor end-gate — stop viewer pane hijack and silent gate turn-end
story_key: conductor-endgate-viewer-hijack-and-silent-gate
status: ready-for-dev
epic_slug: momentum-conductor-core
feature_slug:
story_type: defect
priority: critical
change_type:
  - skill-instruction
verification_method_advisory: skill-invoke
depends_on: []
touches:
  - skills/momentum/skills/conductor/workflow.md
  - skills/momentum/skills/conductor/references/endgate-report-renderer.md
---

# Conductor end-gate — stop viewer pane hijack and silent gate turn-end

## Story

As a developer,
I want the conductor to open gate reports without stealing focus or churning cmux panes, and to always present the end-gate approval ask after rendering,
so that my session view is never hijacked and a sprint never parks silently at an unpresented HITL gate.

## Description

Observed in the sprint-2026-06-28 conduct run (2026-07-06). Three compounding defects made the developer's session appear to "disappear," replaced by the End-Gate document, and left the sprint parked at an unanswered gate:

1. **Focus-steal against spec:** the end-gate open executed `cmux browser new … --focus true`, violating the skill's own instructions at `skills/momentum/skills/conductor/workflow.md:2337` and `:2610`, which both mandate `--focus false` ("keeps the developer in context").
2. **Stale placement assumption:** `workflow.md:2336` and `references/endgate-report-renderer.md` assume `cmux browser new` adds a tab to an existing viewer pane (`placement=reuse`). Verified false by live test 2026-07-06: it ALWAYS returns `placement=split` and creates a new structural pane — even when a browser viewer pane exists and is focused. Every gate open churns the layout. Fix: when a viewer browser surface already exists and its content is superseded (e.g. plan gate → end gate), navigate it in place with `cmux browser <surface> goto <url>`; use `browser new --focus false` only when no viewer surface exists.
3. **Silent gate:** the conductor ended its turn immediately after opening the report, WITHOUT presenting the `workflow.md:2341` end-gate ask ("approve to merge to main, or request changes"). The session transcript (83ea46d8) ends at 18:01:49Z with a turn_duration event and no ask — the developer's terminal showed nothing, and the sprint sat un-merged until manually rediscovered in a later session.

Fix all three in `skills/momentum/skills/conductor/workflow.md` and `references/endgate-report-renderer.md`; make the end-gate ask un-skippable (the turn must not end between report render and the ask).

**Pain context:** First occurrence, but on the highest-stakes surface in the practice — the single mandatory human gate of a sprint build. The developer lost their session view mid-review, believed the session had been destroyed, and the merge-to-main approval was delayed a full session cycle. Recurrence risk is every future conduct run until fixed.

## Acceptance Criteria

These ACs fall into two verification classes. **ACs 1, 3, 4, and 6 are grounded in observable end-gate runtime behavior** (Outsider Test) — a person watching a `/momentum:conduct` run reach Phase 5 can confirm or refute them without reading the skill internals (no focus steal, no extra viewer pane, a blocking approval prompt in the same turn as the render). **ACs 2, 5, and 7 are verified by static instruction review** — confirming that the required doctrine language is present at the named sites (`--focus false` framed as a MUST; no `placement=reuse` assertion remaining; an explicit "turn MUST NOT end between render and ask" directive at both ask sites). Both classes are checkable; they differ only in whether the check is a runtime observation or a read of the edited instruction files.

1. **No focus steal on end-gate open.** When the Conductor opens the end-gate report — at both the initial Phase 5 open and the request-changes re-render open — the developer's active focus stays on the main workspace pane; the report appears in the viewer pane without the view switching to it. The `cmux browser` open never uses `--focus true`. (Observable: after the open, the developer is still looking at / typing in the main pane, not the report.)

2. **`--focus false` is a hard requirement, not a hint.** In `workflow.md` at both open sites (Phase 5 initial open and the 5.RC.5 re-render open) and in `endgate-report-renderer.md`, `--focus false` is stated as a MUST with its rationale ("keeps the developer in context") — not as a bare command line and not as a parenthetical aside. (Observable: a reader of the instruction sees an explicit non-negotiable requirement, not an easily-skipped note. This is the root cause of leg 1 — the instruction already said `false`, but weak framing let the runtime deviate to `true`.)

3. **Existing viewer pane is reused, not churned.** When a viewer browser surface already exists in the workspace and its content is superseded (e.g. a plan-gate report is showing and the end-gate report replaces it), the Conductor navigates that surface in place with `cmux browser <surface> goto <url>` and does NOT run `cmux browser new`. (Observable: opening the end-gate report when a viewer pane already exists does not add a second viewer pane — the structural pane count is unchanged.)

4. **`cmux browser new` is used only for the first viewer open.** `cmux browser new --focus false` is used ONLY when no viewer browser surface yet exists this session. The instruction directs the Conductor to query existing surfaces first (e.g. `cmux list-panes` / `cmux list-pane-surfaces`) and branch on the result. (Observable: the new-vs-goto choice is conditioned on whether a viewer surface already exists, not issued unconditionally.)

5. **Stale placement doctrine corrected in both files.** The claim that `cmux browser new` "adds a tab to the existing viewer pane / does not create a new structural pane" is removed from `workflow.md` (the initial-open action, currently `:2336`) and from `endgate-report-renderer.md` (the open procedure at `:387–392` and the "as a tab" assertions at `:140` and `:558`). The replacement text states the verified behavior: `cmux browser new` ALWAYS creates a new structural pane (returns `placement=split`), so reuse requires `goto` on an existing surface. (Observable: neither file asserts `placement=reuse` for `cmux browser new`.)

6. **The end-gate ask is presented in the same turn as the render.** After rendering and opening the end-gate report, the Conductor presents the end-gate approval ask ("approve to merge to main, or request changes") in the SAME turn — the turn does not end between opening the report and presenting the ask. (Observable: the developer's terminal shows the blocking approval prompt immediately after the report opens; the sprint never parks with the report open and no ask on screen. This is verified across BOTH ask sites — the initial gate and the request-changes redispatch.)

7. **Render-then-ask atomicity is stated as un-skippable at both ask sites.** At the initial Phase 5 ask (`workflow.md:2341`) and the request-changes redispatch ask (`workflow.md:2628`), the instruction explicitly forbids ending the turn between opening the report and presenting the ask. (Observable: the instruction contains an explicit "the turn MUST NOT end between render and ask" directive — the render and the ask are bound as one atomic unit — at both sites.)

## Tasks / Subtasks

- [ ] **Task 1 — Write behavioral evals first (EDD).** (AC1, AC3, AC6) Before editing any instruction, create `skills/momentum/skills/conductor/evals/` if absent and write 2–3 behavioral evals that a subagent can run against the conductor Phase 5 instructions:
  - `eval-endgate-open-never-steals-focus.md` — given the Phase 5 end-gate open step, the Conductor issues the open with `--focus false` (or a `goto`) and never `--focus true`. (AC1, AC2)
  - `eval-endgate-reuses-existing-viewer-surface.md` — given a workspace where a viewer browser surface already exists and its content is superseded, the Conductor navigates it via `cmux browser <surface> goto <url>` rather than `cmux browser new`. (AC3, AC4)
  - `eval-endgate-render-and-ask-are-atomic.md` — given the Phase 5 render step, the Conductor presents the approval ask in the same turn as the report open and does not end the turn between them. (AC6, AC7)
- [ ] **Task 2 — Harden the initial end-gate open.** (AC1, AC2, AC4, AC5) In `workflow.md` at the Phase 5 initial-open action (currently `:2336–2339`): replace the bare `Run:` line and the "does not create a new structural pane" claim with a MUST-framed procedure — (a) query existing viewer surfaces; (b) if a viewer surface exists and its content is superseded, `cmux browser <surface> goto <url>`; (c) else `cmux browser new … --focus false`; state `--focus false` as a hard MUST with rationale; state that `cmux browser new` always splits a new structural pane.
- [ ] **Task 3 — Harden the request-changes re-render open.** (AC1, AC2, AC4, AC5) Apply the identical hardened procedure at the 5.RC.5 re-render open action (currently `:2609–2612`), replacing the parenthetical `--focus false` note with the same MUST framing and new-vs-goto branch.
- [ ] **Task 4 — Correct the renderer open procedure and tab assumptions.** (AC3, AC4, AC5) In `endgate-report-renderer.md`: fix the open procedure (`:387–392`) to the reuse-via-`goto` / `browser new`-only-when-absent pattern with `--focus false` as a MUST; correct the "does not create a new structural pane" line (`:392`); and correct the "as a browser tab" / "as a tab, per §8" assumptions at `:140` and `:558` so the renderer no longer claims `cmux browser new` reuses an existing pane.
- [ ] **Task 5 — Bind render + ask atomically (kill the silent gate).** (AC6, AC7) At both end-gate ask sites (`workflow.md:2341` initial ask and `:2628` redispatch ask): add an explicit, un-skippable instruction that the Conductor MUST present the end-gate ask in the same turn as the report open, and MUST NOT end the turn between rendering/opening the report and presenting the ask. Frame render+ask as a single atomic unit so no turn can end with the report open and no ask on screen.
- [ ] **Task 6 — Run the evals and confirm behavior (EDD verify).** (AC1–AC7) Run the Task 1 evals against the edited instructions via subagents; confirm each behavior fires. If any eval fails, diagnose the instruction gap, revise, and re-run (max 3 cycles). Document results in the Dev Agent Record.

## Dev Notes

### Decision Authority

The end-gate is the **single mandatory human acceptance point** of a conduct build (DEC-035: one end-gate, no second mandatory acceptance gate). A silent turn-end at that gate does not merely inconvenience the developer — it **defeats the only gate in the spine**, leaving the sprint un-merged and the developer unaware a decision is pending. This story restores the gate's invariant that render and ask are inseparable.

The end-gate is also an anti-rubber-stamp surface (DEC-036 D4) and a self-sufficiency-floor surface (DEC-036 D5 / the decision-grade-presentation rule §5.1): it renders as a visual HTML companion surface in the viewer pane. That form requirement is exactly why the open must land in the viewer pane **without** hijacking focus — the developer reads the HTML while staying in their working context.

### Current State of Affected Files

**`skills/momentum/skills/conductor/workflow.md` (2633 lines).** Both end-gate open sites already carry `--focus false` in the file today — leg 1 is NOT "the file says `true`." The runtime deviated to `--focus true` despite the file, because the instruction is weak: `:2337` is a bare `Run:` command line and `:2611` is a parenthetical. The fix strengthens the framing to an un-skippable MUST, not a value change.
- `:2336–2339` — initial Phase 5 open action; contains the stale "does not create a new structural pane" claim and the bare `Run: cmux browser new … --focus false`.
- `:2341` — initial end-gate `<ask>` (exists, but not bound to the render).
- `:2609–2612` — 5.RC.5 re-render open action; parenthetical `--focus false` note.
- `:2628` — redispatch `<ask>` (exists, but not bound to the render).

**`skills/momentum/skills/conductor/references/endgate-report-renderer.md` (33 KB).**
- `:140` — "Open it in the cmux viewer pane (right pane, as a browser tab)…" (tab assumption).
- `:387–392` — open procedure using `cmux browser new … --focus false`, ending with the stale line "(Adds a tab to the existing viewer pane; does not create a new structural pane.)".
- `:558` — "It opens the updated file in the cmux viewer pane (as a tab, per §8)." (tab assumption).

Line numbers are current-as-of-authoring anchors; the dev must re-locate by content (the edits are content-addressed, not line-addressed) since earlier tasks shift later line numbers.

### Architecture Compliance

- **DEC-035** — one end-gate, the only mandatory human acceptance point; the silent-gate leg violates this decision's core guarantee.
- **DEC-036 D4/D5** — anti-rubber-stamp end-gate; self-sufficiency floor. The gate must be *presented* for acknowledgment to mean anything.
- **decision-grade-presentation rule §5.1** — the end-gate is a visual HTML companion surface opened in the viewer pane; focus must stay with the developer.
- **Verified cmux behavior** — `cmux browser new` always returns `placement=split` (never `placement=reuse`); reuse requires `goto` on an existing surface. This is the load-bearing fact behind AC3–AC5.

### Testing Requirements

Verification method (advisory): **`skill-invoke`** — this is a pure skill-instruction story (both touched files are skill-instruction files), and `skill-instruction` routes to `skill-invoke` per `skills/momentum/references/rules/verification-standard.md` §1. Verification is behavioral: drive (or subagent-simulate) the Conductor's Phase 5 end-gate and observe the three behaviors — no focus steal (AC1), reuse-via-`goto` when a viewer surface exists (AC3), and a blocking approval ask emitted in the same turn as the render (AC6). Static instruction review confirms AC2, AC5, and AC7 (the framing/doctrine/atomicity language is present at the named sites).

### Project Structure Notes

**Cross-artifact tension — the global cmux rule carries the same stale assumption (flag for the developer, out of this story's scope).** `~/.claude/rules/cmux.md` (a global user rule) still asserts under "Opening an HTML doc as a viewer tab" that `cmux browser new` "Returns `placement=reuse` — adds a tab to the existing viewer pane and does NOT create a new structural pane," and Rule 6 contrasts `markdown open` (always splits) against `browser new` (additive tab). That is the same doctrine this story corrects in the conductor files, and it is contradicted by the 2026-07-06 live test and by the standing project-memory note `reference_cmux_browser_new_always_splits`. Correcting a global user rule is **outside this story's declared `touches`** (the two conductor files) and is a scope-widening the developer should ratify separately. Risk if left: the conductor doctrine will (correctly) say "always splits" while the global rule still says "reuse," until the global rule is also corrected. Recommend a follow-up story/observation to reconcile `~/.claude/rules/cmux.md`; do not silently edit the global rule from this story.

### Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1–6 → skill-instruction (EDD)

---

#### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/conductor/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-endgate-render-and-ask-are-atomic.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Modify the workflow.md end-gate open/ask actions and the endgate-report-renderer.md open procedure per Tasks 2–5.

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the relevant conductor Phase 5 instructions as context. Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete.
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to the developer if still failing).

**NFR compliance — mandatory for every skill-instruction task:**
- No new SKILL.md is created here (this edits an existing workflow.md + reference), so the ≤150-char description NFR and the `model:`/`effort:` frontmatter NFR apply only if the conductor `SKILL.md` frontmatter is touched — it is not in scope, so leave it unchanged.
- NFR3's 500-line / 5000-token cap applies to the conductor `SKILL.md` BODY only — which is out of scope here (the SKILL.md is unchanged). `workflow.md` and `endgate-report-renderer.md` are instruction/reference bodies and carry NO NFR3 line cap; `references/` is exactly where overflow is meant to land (`endgate-report-renderer.md` is already ~565 lines, which is fine). Keep the edits additive and surgical, and keep the two files coherent with each other.
- Skill remains under the `momentum:` namespace (unchanged).

**Additional DoD items for skill-instruction tasks (added to the standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/conductor/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] Both open sites (workflow.md) and the renderer open procedure use the reuse-via-`goto` / `browser new`-only-when-absent pattern with `--focus false` as a MUST
- [ ] Both ask sites (workflow.md) bind render + ask atomically with an explicit "turn MUST NOT end between render and ask" directive
- [ ] The stale `placement=reuse` / "does not create a new structural pane" language is gone from both files
- [ ] AVFL checkpoint on the produced artifact documented (momentum:dev runs this automatically — validates the edited instructions against story ACs)

**Frozen verification contract reminder:** a frozen verification contract exists for this sprint at `sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Dev reads the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before signaling done. Dev never reads the verifier body (Part B: scenarios, assertion scripts, Gherkin) beyond sections explicitly referenced by `how_dev_self_checks`.

### References

- Incident transcript: session `83ea46d8`, sprint-2026-06-28 conduct run, 2026-07-06 (turn ends 18:01:49Z with a `turn_duration` event and no end-gate ask).
- Live test 2026-07-06: `cmux browser new` returns `placement=split` (never `reuse`) even when a focused viewer pane exists.
- Project memory: `reference_cmux_browser_new_always_splits` — verified always-splits behavior; use `goto` on an existing surface to avoid pane churn.
- Affected instructions: `skills/momentum/skills/conductor/workflow.md` (`:2336–2341`, `:2609–2628`) and `skills/momentum/skills/conductor/references/endgate-report-renderer.md` (`:140`, `:387–392`, `:558`).
- Governing decisions/rules: DEC-035 (single end-gate), DEC-036 D4/D5 (anti-rubber-stamp; self-sufficiency floor), decision-grade-presentation rule §5.1 (visual companion surface in the viewer).
- Epic context: `momentum-conductor-core` (from _bmad-output/planning-artifacts/epics.json)

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
