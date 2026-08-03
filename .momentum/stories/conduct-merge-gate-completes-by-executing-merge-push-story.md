---
title: Conduct merge-gate completes by executing — merge + push + story transitions, never a report
story_key: conduct-merge-gate-completes-by-executing-merge-push-story
status: ready-for-dev
epic_slug: momentum-conductor-core
feature_slug:
story_type: practice
priority: high
change_type:
  - skill-instruction
verification_method_advisory: skill-invoke
depends_on: []
touches:
  - skills/momentum/skills/conductor/workflow.md
  - skills/momentum/skills/conductor/references/build-ledger.md
  - skills/momentum/skills/conductor/references/endgate-report-renderer.md
  - skills/momentum/skills/conductor/evals/
---

# Conduct merge-gate completes by executing — merge + push + story transitions, never a report

## Story

As a developer,
I want the tier-1 merge gate in `conductor/workflow.md` ("is this code something we are
comfortable keeping on trunk?") to complete only by executing the real state transition
— merge to main, push, and story status updates — and to FAIL loudly if it cannot execute
that transition,
so that an approval always has real, executed consequence instead of leaving finished
work stranded on a sprint branch behind a rendered report.

## Description

The Conductor's Phase 5 end-gate currently renders an HTML report, asks the developer to
approve, and then runs a merge sequence whose success is never checked and whose failure has
no recorded terminal state. On the approve path it prints "Sprint `X` complete. All stories
merged to main." unconditionally — including when the developer declines the separate push
prompt, in which case the commits sit on local `main` and origin has nothing. That sentence is
a report standing in for an executed transition, and it is the exact shape of the failure this
story removes.

This story rewrites the tier-1 merge gate so its terminal state is a **verified executed state
transition**: merge to `main` + push to origin + per-story status updates, each read back from
the system after execution rather than assumed from the fact that a command was issued. When
any part cannot execute, the gate reaches an explicit, loudly-surfaced FAILED outcome that says
which step failed and why. "Report rendered" and "developer said approve" are not terminal
states of this gate.

The report itself is not removed — it remains the review surface required by the
decision-grade-presentation standard. What changes is that the report is the *input* to the
gate's decision, never its *output*.

**Tier separation.** This story is tier 1 only. Sprint closure ("have the sprint goals been
met — do the named conditions verifiably work in the app?") is tier 2 and belongs to
`sprint-closure-refusal-recorded-human-verdicts-per-goal`. This story does not change sprint
closure semantics: the existing `momentum-tools sprint complete` call in the approve branch and
its retro-pickup behavior stay exactly as they are, and the regression eval that guards them
(`eval-phase5-completes-sprint-for-retro-pickup.md`) must still pass unchanged. The one new
constraint at that boundary is that a FAILED merge gate must never be masked by sprint closure
having succeeded.

**Pain context:** Nornspun discovery — 53 finished commits sat stranded on sprint branches for
11 days because the end-gate emitted HTML and nothing executed. An approval that leaves commits
stranded is an opinion, not an approval.

**Source:** DEC-040 D2 (`_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`),
amending DEC-035; `architecture.md` Decision 59 two-tier-gate paragraph documents the semantics.

## Acceptance Criteria

1. **The gate has exactly three recorded outcomes, and "report rendered" is not one of them.**
   The tier-1 merge gate resolves to `merged` (all three transitions executed and verified),
   `merge-gate-failed` (execution was attempted and could not complete), or `pending` (the
   developer has not yet decided). A rendered report, an acknowledged decision card, or a
   recorded "approve" with no executed transition is never a terminal state of this gate.

2. **Approval executes all three parts before any completion claim.** When the developer
   approves, the Conductor merges `sprint/{sprint-slug}` into `main`, pushes `main` to origin,
   and transitions every story to its terminal status (merged stories to `done`, non-merged
   stories to `closed-incomplete`). No output, ledger row, or summary states that the sprint
   merged until all three have executed and passed the verification in AC 3.

3. **Execution is verified by reading back from the system, not from the Conductor's own
   memory.** After executing, the Conductor confirms from git and the story index that: `main`
   contains the tip of the sprint branch; local `main` and `origin/main` point at the same
   commit; and every story it counted as merged reads back as `done` in
   `.momentum/stories/index.json`. Any check that does not hold makes the outcome
   `merge-gate-failed` — an issued command is not evidence that the transition happened.

4. **Failure is loud, specific, and never dressed as success.** When merge, push, or a status
   transition cannot complete — a conflict that survives the bounded autonomous resolution
   attempts, a rejected or unauthenticated push, a missing remote, a rejected state transition —
   the gate records `merge-gate-failed` naming the failing step and the actual error text,
   surfaces it to the developer in plain language with what is now stranded and where, and emits
   no message claiming the sprint merged or completed.

5. **Push is part of completing the gate, not an optional afterthought.** The gate's single
   approve control covers merge *and* push together, and the developer is shown the exact
   commits that will reach origin (`git log @{u}..HEAD --oneline`, mirrored in the report's §07
   preview) before they act — so approval remains an explicit, informed confirmation of the
   push. The standalone "Push to origin/main?" prompt that could be declined while the gate
   still reported completion is gone; an unpushed sprint is never reported as merged to main.

6. **Tier 1 and tier 2 stay separate.** The merge gate's outcome is determined solely by merge +
   push + story transitions and never by whether the sprint's goals were met. Sprint-closure
   behavior is unchanged by this story: the existing `momentum-tools sprint complete` call keeps
   its position and its "No active sprint to complete" idempotency note, and
   `eval-phase5-completes-sprint-for-retro-pickup.md` still passes. A `merge-gate-failed`
   outcome is surfaced to the developer even when sprint closure succeeded — closure never
   masks a failed merge gate.

7. **The outcome is durable in the build ledger.** The Conductor appends a row recording the
   gate outcome with its evidence — merge commit SHA, pushed head SHA, and per-story transition
   results on success, or the failing step and error text on failure. The row is documented in
   `references/build-ledger.md` alongside the existing event types.

8. **A resumed run neither re-executes nor re-claims a completed transition.** On resume, the
   Conductor reads the ledger: a gate already recorded as `merged` is not re-merged, re-pushed,
   or re-transitioned, and is not re-announced as if it just happened; a gate recorded as
   `merge-gate-failed` is re-surfaced rather than silently retried into a success claim.

9. **The report tells the truth about what approving does.** The end-gate report's §06 "what
   approving actually does" callout and its §07 merge-and-push preview state in plain terms that
   approving merges to `main`, pushes to origin, and moves stories to `done` — and that the
   sprint itself stays open until the separate closure decision. Neither section describes the
   push as an optional or deferred step.

10. **Evals prove the invariant, not just the happy path.** The conductor skill carries
    behavioral evals covering the executed-and-verified success path, the loud-failure path, and
    the core invariant that the gate cannot terminate in a non-executed state.

## Tasks / Subtasks

- [ ] **Task 1 — Write the evals first (EDD).** (AC 1, 4, 10)
  Add to `skills/momentum/skills/conductor/evals/`:
  - `eval-merge-gate-completes-by-executing.md` — approve leads to merge + push + terminal
    transitions, each read back and confirmed, before any completion output.
  - `eval-merge-gate-fails-loudly-when-transition-blocked.md` — a push that cannot land (or a
    conflict surviving the retry bound) yields `merge-gate-failed` naming the step and error, and
    no "merged to main" claim anywhere in the output.
  - `eval-merge-gate-never-terminates-in-a-report.md` — the invariant: no path through Phase 5
    reaches a terminal outcome whose only artifact is the rendered report or a recorded approval.
  Run them against the current workflow first and confirm they fail for the right reason.

- [ ] **Task 2 — Rewrite the Phase 5 approve branch as an execute-and-verify sequence.** (AC 1, 2)
  In `skills/momentum/skills/conductor/workflow.md` (step n="5", `<check if="developer
  approves">`), restructure the branch so it is explicitly an execution sequence with a bound
  outcome variable, and declare the three-value outcome enum for the gate. Preserve the existing
  `end-gate-phase-complete` checkpoint semantics and the MAJOR-RESIDUAL governance guard.

- [ ] **Task 3 — Add the bounded-failure path and the `merge-gate-failed` terminal state.** (AC 4)
  Give the existing "Conductor resolves conflicts and retries — never HALT" instruction an
  explicit bound (reuse `{{MAX_FIX_ATTEMPTS}}`, declared at step 2.S3) and a defined terminal
  state when the bound is exhausted. Add the same failure routing for push failures and rejected
  status transitions. Preserve the existing DEFENSIVE FALLBACK branches (already-merged branch
  ref, already-terminal story status) — those are resume cases, not failures.

- [ ] **Task 4 — Fold push into the gate's single approve control.** (AC 5)
  Move the `git log @{u}..HEAD --oneline` commit disclosure to before the gate ask (and into the
  §07 preview), make the approve control read as merge-and-push, and remove the standalone
  `<ask>Push to origin/main?</ask>` and its conditional branch. Update the final output so it
  reports the verified result rather than a fixed completion sentence.

- [ ] **Task 5 — Add post-execution read-back verification.** (AC 3)
  Before branch deletion, bind `{{sprint_tip_sha}}` = `git rev-parse sprint/{{sprint_slug}}`
  (matching the existing `{{S.launch_base_sha}}` capture pattern). After the execution
  sequence, verify from the system: `git merge-base --is-ancestor {{sprint_tip_sha}} main`,
  local `main` head equals `origin/main` head, and each merged story reads `done` in
  `.momentum/stories/index.json`. Route any failed check to the `merge-gate-failed` path
  from Task 3.

- [ ] **Task 6 — Record the outcome in the build ledger and make resume read it.** (AC 7, 8)
  Add the merge-gate outcome event to the controlled event set in
  `skills/momentum/skills/conductor/references/build-ledger.md` (payload: outcome, merge SHA,
  pushed head SHA, per-story transition results, failing step, error text), append it at the end
  of the execution sequence, and extend the step 2.0 resume rehydration so a recorded outcome
  suppresses re-execution and re-announcement.

- [ ] **Task 7 — Update the report's honesty and preview copy.** (AC 9)
  In `skills/momentum/skills/conductor/references/endgate-report-renderer.md`, update §9 (the
  §06 "So what does approving actually do?" callout) and the §07 row in the section table so the
  executed consequence — merge, push, stories to `done`, sprint stays open for the separate
  closure decision — is what the developer reads. Remove the "push is a separate confirmation"
  framing.

- [ ] **Task 8 — Run the EDD cycle and regression-check the existing Phase 5 evals.** (AC 6, 10)
  Re-run the three new evals to green. Then confirm the untouched-behavior evals still pass:
  `eval-phase5-completes-sprint-for-retro-pickup.md`, `eval-endgate-render-and-ask-are-atomic.md`,
  `eval-endgate-reuses-existing-viewer-surface.md`, `eval-endgate-open-never-steals-focus.md`,
  `eval-phase5-assembles-from-ledger.md`, and `eval-resume-after-approve-skips-merge.md`.

## Dev Notes

### Decision Authority

DEC-040 D2 is the source of truth and it amends DEC-035. Its operative sentence: the merge gate
"completes only by executing merge + push + story status transitions (it FAILS loudly rather
than emitting a report and stalling)." `architecture.md` Decision 59's two-tier-gate paragraph
restates it and marks the machinery **not yet implemented** — this story is that implementation
for tier 1. Where this story's wording and DEC-040 D2 differ, DEC-040 D2 wins.

### Current State of the Affected Files

`skills/momentum/skills/conductor/workflow.md` — step n="5" (Phase 5, ~line 2481 to end of file).
The approve branch already issues the right commands in roughly the right order: merge
(`git checkout main` / `git merge sprint/{{sprint_slug}}` / conflict resolution / `git branch -d`),
per-story terminal transitions via `momentum-tools sprint status-transition`, `momentum-tools
sprint complete`, the `end-gate-phase-complete` checkpoint, the MAJOR-RESIDUAL governance guard,
then a push summary, a `Push to origin/main?` ask, and `git push`. Four gaps make it a report
rather than an execution:

- Nothing verifies any of it afterward — success is inferred from having issued the command.
- Conflict handling says "resolves autonomously or fires a fixer, then retries — never HALT"
  with no bound and no defined outcome if resolution never succeeds.
- Declining the push still falls through to the unconditional output "Sprint `{{sprint_slug}}`
  complete. All stories merged to main." while origin has nothing — the stranded-commits shape.
- There is no third outcome. The `<ask>` has an approve branch and a request-changes branch;
  a session that ends without an answer leaves no record that the gate is unresolved.

`references/build-ledger.md` — controlled event-type set plus the Conductor-Level Events table
(events permitted to omit `story_slug`). The merge-gate outcome is sprint-scoped, so it belongs
in that table alongside `end-gate-phase-complete`.

`references/endgate-report-renderer.md` — §9 defines the §06 honesty callout; the section table
(~line 168) defines §07 as "Commits/diffstat; exact approve sequence; 'push is a separate
confirmation.'" That last clause is the copy this story contradicts.

### Architecture Compliance

- **Decision 59 (two-tier gate)** — implements tier 1 exactly; tier 2 is out of scope.
- **Single-mandatory-gate invariant** — Phase 5 remains the one mandatory human acceptance point.
  Folding push into the gate's approve control removes a second prompt; it does not add one.
- **Conductor is sole git-mutation authority** — all merge/push/transition commands stay in the
  Conductor's own turn. No spawned subagent gains git authority from this change.
- **Ledger is authoritative** — the outcome row is the durable record; in-context variables stay
  write-through caches (Decision 59 ledger-sourced end-gate/resume semantics).
- **`git push` approval rule** (`~/.claude/rules/git-discipline.md`) is preserved, not overridden:
  the developer still gives explicit confirmation and is still shown `git log @{u}..HEAD
  --oneline` before it runs. The change is that the confirmation is folded into the gate's one
  approve control instead of being a second, separately-declinable prompt — the disclosure the
  rule requires happens before the developer acts.

### Testing Requirements

Skill-instruction work — EDD, not TDD (see the Momentum Implementation Guide below). The three
new evals in Task 1 are written and confirmed failing before the workflow is edited. Because the
failure paths are hard to trigger live, the failure eval may be verified by inspection of the
workflow text plus a dry-run walkthrough with a subagent given a simulated push rejection — but
the success-path eval must be exercised against a real (fixture) sprint, not inspected.

The regression set in Task 8 is the guard against collateral damage in a 440-line phase.

### Project Structure Notes

All work is inside `skills/momentum/skills/conductor/`. No new skill directory, no new script,
no CLI change — `momentum-tools sprint status-transition` and `momentum-tools sprint complete`
are used as they exist today.

**Cross-story seam.** Two sibling stories in this sprint touch adjacent surfaces and must not
collide:
- `sprint-closure-refusal-recorded-human-verdicts-per-goal` (tier 2) will rework the
  `momentum-tools sprint complete` call this story deliberately leaves untouched. This story
  should leave that call clearly delimited so tier 2 has a clean insertion point.
- `conduct-resume-card-impetus-pending-gate-agenda-session` (DEC-040 D5) owns the resume card
  emitted when a gate is left pending. This story defines `pending` as a real, recorded outcome
  of the gate; it does not render the resume card.
- `consolidate-state-model-and-cross-skill-contract-tests` (same epic) is the intended home for a
  cross-skill contract test asserting the merge gate cannot terminate in a non-executed state.
  This story ships the equivalent assertion as a conductor eval; the sibling consolidates it
  later.

### References

- DEC-040 D2 — `_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`
  (amends DEC-035)
- `_bmad-output/planning-artifacts/architecture.md` — Decision 59, two-tier gate paragraph
  (DEC-040 D2/D3), marked implementation-pending
- `skills/momentum/skills/conductor/workflow.md` — step n="5", the tier-1 merge gate
- `skills/momentum/skills/conductor/references/build-ledger.md` — event-type set and
  Conductor-Level Events table
- `skills/momentum/skills/conductor/references/endgate-report-renderer.md` — §9 (§06 honesty
  callout), section table row for §07
- `_bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md` — canonical voice
  spec for gate output
- `~/.claude/rules/git-discipline.md` — push-approval and commit-disclosure requirements
- Sibling stories: `sprint-closure-refusal-recorded-human-verdicts-per-goal` (tier 2),
  `conduct-resume-card-impetus-pending-gate-agenda-session` (D5 resume card),
  `consolidate-state-model-and-cross-skill-contract-tests` (contract-test consolidation)
- Epic context: `momentum-conductor-core` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1–8 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic
LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write the behavioral evals in `skills/momentum/skills/conductor/evals/`:
   - One `.md` file per eval, named descriptively (Task 1 names all three)
   - Format each eval as: "Given [input and context], the skill should [observable behavior]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Modify `workflow.md` and the two `references/` files per Tasks 2–7

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it the eval's
   scenario as its task and load the skill by passing the SKILL.md and workflow.md contents as
   context. Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles;
   surface to the developer if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/`
  with clear load instructions (NFR3)
- Skill names use the `momentum:` namespace prefix (NFR12)

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 3 behavioral evals written in `skills/momentum/skills/conductor/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] Existing Phase 5 regression evals (Task 8 list) re-run and still passing
- [ ] SKILL.md description ≤150 characters confirmed (conductor SKILL.md is unmodified by this
      story — confirm it still holds after any incidental edit)
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically)

**Frozen verification contract.** A frozen verification contract exists for this sprint at
`.momentum/sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Read the Part-A header
(`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before
signaling done. Do not read the verifier body (Part B: scenarios, assertion scripts, Gherkin)
beyond the sections `how_dev_self_checks` explicitly references.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
