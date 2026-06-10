---
title: Conductor creates story worktrees and branches — close the unexecutable first step of the per-story pipeline
story_key: conduct-worktree-and-branch-creation
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
story_type: defect
priority: high
depends_on: []
change_type: skill-instruction
verification_method_advisory: skill-invoke
---

# Conductor creates story worktrees and branches — close the unexecutable first step of the per-story pipeline

Status: ready-for-dev

## Story

As the Conductor (in-session sprint build orchestrator),
I want an explicit story-branch + worktree creation action in the step 2.1 story launch sequence — fork `story/{S.slug}` from the current tip of `sprint/{{sprint_slug}}`, then `git worktree add .worktrees/story-{S.slug}` — executed before the stage-1 dev spawn,
so that every dev spawn targets a worktree that actually exists, the branch base is never improvised, and the merge-base diff math in per-story reviews stays correctly scoped.

## Why this exists

Confirmed finding from the 2026-06-09 conductor effectiveness review (adversarially verified, high confidence, confirmed independently by two review lenses):

- `skills/momentum/skills/conductor/workflow.md` line 336 passes `worktree_path: .worktrees/story-{S.slug}` to the stage-1 dev agent, but the only `git worktree` commands anywhere in the file are **removals** (pre-flight reconcile, lines ~157–169; post-merge cleanup, line ~1144). There is no `git worktree add` and no story-branch creation step anywhere (verified by grep at story-creation time).
- The dev agent explicitly disclaims the job: `skills/momentum/skills/dev/workflow.md` line ~148 — "The dev agent neither creates nor enters/exits worktrees" — and line 7 lists worktree creation/lifecycle as Conductor responsibilities (spec sections 3 and 6; DEC-035, DEC-036 D1).
- The branch base for `story/{slug}` is never specified anywhere. On a fresh sprint, every stage-1 dev spawn targets a worktree that does not exist, forcing the orchestrating model to improvise the most isolation-critical git operation in the build. If it forks from `main` instead of the sprint branch tip, the story builds on a base that silently omits prior merged sprint work, and — whenever `main` has diverged from the sprint fork point — the merge-base form in `references/per-story-review-diff-range.md` over-scopes the review diff and drags non-sprint commits into every merge.

## Acceptance Criteria

1. `skills/momentum/skills/conductor/workflow.md` step 2.1 contains an explicit branch-and-worktree creation action that executes within the story launch sequence **before the stage-1 dev spawn**, so that a launched story never reaches its dev spawn without `.worktrees/story-{S.slug}` existing and checked out on branch `story/{S.slug}`.
2. The branch base is stated explicitly in the action's command(s) — `story/{S.slug}` is created from the **current tip of `sprint/{{sprint_slug}}`** — never from `main`, never from an unspecified default, and never left to the executing model to infer.
3. The creation action is idempotent-safe alongside the Phase 1 pre-flight reconcile: if a stale `story/{S.slug}` branch or `.worktrees/story-{S.slug}` worktree still exists at launch time, the action specifies deterministic handling (remove-and-recreate using the same removal semantics the reconcile uses) instead of failing into improvisation.
4. The creation action is performed by the Conductor itself inside the launch loop, preserving the sole-git-mutation-authority invariant. No part of branch or worktree creation is delegated to the dev agent, and the existing disclaimers in `skills/momentum/skills/dev/workflow.md` (Conductor owns worktree lifecycle; dev neither creates nor enters/exits worktrees) remain true. A clarifying note in dev/workflow.md is permitted; a responsibility transfer is not.
5. The creation action is consistent with the merge-base diff doctrine: forking from the sprint branch tip preserves Scenario A of `skills/momentum/skills/conductor/references/per-story-review-diff-range.md` (pre-merge review: `merge-base sprint/{{sprint_slug}} story/{{S.slug}}` isolates exactly the story's own commits). The new action cites that reference (or states the fork-point rationale inline) so the base choice is traceable, not re-derivable.
6. Behavioral evals exist under `skills/momentum/skills/conductor/evals/` covering at least: (a) fresh launch — branch created from sprint tip and worktree added before dev spawn; (b) stale collision at launch — deterministic remove-and-recreate, no prompt, no improvisation.

## Tasks / Subtasks

- [ ] Task 1: Write behavioral evals first (EDD red phase) (AC: 6)
  - [ ] 1.1 Add an eval to `skills/momentum/skills/conductor/evals/` for the fresh-launch path: given a story entering step 2.1 with no existing branch/worktree, the Conductor creates `story/{S.slug}` from the current tip of `sprint/{{sprint_slug}}` and adds `.worktrees/story-{S.slug}` before spawning the stage-1 dev agent
  - [ ] 1.2 Add an eval for the stale-collision path: given a leftover `story/{S.slug}` branch or `.worktrees/story-{S.slug}` worktree at launch, the Conductor removes and recreates them deterministically (no developer prompt, no improvised base)
- [ ] Task 2: Insert the branch+worktree creation action into step 2.1 of `skills/momentum/skills/conductor/workflow.md` (AC: 1, 2, 4, 5)
  - [ ] 2.1 Place the action inside the launch loop, after the launch gates (2.1.4 contract-freeze / 2.1.5 coverage-disposition) resolve and before the stage-1 dev spawn fires — recommended position: first action of the STAGE-1 DEV SPAWN block, per Dev Notes "Placement" (which also explains the gating consideration)
  - [ ] 2.2 State the base explicitly in the commands, e.g. `git branch story/{S.slug} sprint/{{sprint_slug}}` then `git worktree add .worktrees/story-{S.slug} story/{S.slug}` (or the single-command equivalent `git worktree add -b story/{S.slug} .worktrees/story-{S.slug} sprint/{{sprint_slug}}` — either form is acceptable; the base ref must appear literally)
  - [ ] 2.3 Add a one-line rationale citing `references/per-story-review-diff-range.md` Scenario A (fork from sprint tip keeps the merge-base diff exactly story-scoped)
  - [ ] 2.4 Confirm the action is Conductor-executed (no delegation into the dev spawn prompt) and that the existing dev-spawn constraint text ("Do not mutate git...") is unchanged
- [ ] Task 3: Specify idempotent collision handling consistent with the pre-flight reconcile (AC: 3)
  - [ ] 3.1 Before creating: if `.worktrees/story-{S.slug}` exists, `git worktree remove --force .worktrees/story-{S.slug}`; if `story/{S.slug}` exists, `git branch -D story/{S.slug}` — mirroring the reconcile's removal commands (workflow.md ~157–169)
  - [ ] 3.2 Verify the reconcile end-condition note (workflow.md ~line 173) and the Phase 1 notes remain accurate after the change (worktree creation happens in Phase 2, so the "only main + sprint worktree after reconcile" claim still holds — adjust wording only if it now reads as contradicted)
- [ ] Task 4: Add a clarifying note to `skills/momentum/skills/dev/workflow.md` (AC: 4)
  - [ ] 4.1 Extend the existing working-directory note in step 2 (the "Conductor spawns this agent already scoped to the story worktree" note, ~line 148) to state that the Conductor creates the story branch and worktree at story launch (conductor workflow step 2.1) — clarification only, no responsibility change
- [ ] Task 5: Run EDD evals and verify NFR compliance (AC: 1–6)
  - [ ] 5.1 Run the Task 1 evals against the updated workflow instructions; revise until behaviors match (max 3 cycles)
  - [ ] 5.2 Confirm conductor SKILL.md frontmatter untouched and workflow.md stays internally consistent (no second freeze gate added, no new developer prompts on the routine path)

## Dev Notes

### Current state of files being modified (verified at story-creation time)

**`skills/momentum/skills/conductor/workflow.md`** (~2000+ lines):

- Step 2.1 ("Launch every story in the frontier concurrently — no story-count cap", line ~276) launches all frontier stories simultaneously. Sub-step ordering inside the launch loop is intentionally non-sequential: 2.1.1 (frontier→running), 2.1.2 (transition to in-progress), 2.1.4 (contract-freeze gate), 2.1.5 (coverage-disposition branch), then 2.1.3 (the stage-1→2→3 pipeline, fired "after 2.1.4/2.1.5 resolve"). Do NOT renumber existing sub-steps; insert the new action without disturbing this ordering.
- STAGE-1 DEV SPAWN (line ~322 onward) resolves the agent, derives `{{writable_files}}`, and spawns with `worktree_path: .worktrees/story-{S.slug}` (line ~336). This is the consumer of the worktree this story makes real.
- Pre-flight reconcile (lines ~150–173) removes stale story branches/worktrees for `in-progress` stories: `git worktree remove --force .worktrees/story-{slug}`, `git branch -D story/{slug}`, then `git worktree prune` and orphan `worktree-agent-*` removal. The new launch-time collision handling must reuse these exact removal semantics.
- H5 guard + reconcile verify `sprint/{{sprint_slug}}` exists and is checked out before Phase 2 — the new action may assume the sprint branch exists (guarded upstream); it must NOT re-verify or halt.
- Post-merge cleanup at step 2.2.M.6 (line ~1144): `git worktree remove --force .worktrees/story-{S.slug}` + `git branch -d story/{S.slug}`. The lifecycle this story completes: create at launch (NEW) → commit/fix in worktree → merge → remove at 2.2.M.6.
- The 2.1.4 placement note explicitly forbids adding a second contract-freeze gate later in the pipeline — do not touch the gate logic while inserting the creation action.

**`skills/momentum/skills/dev/workflow.md`**:

- Line 7: "Conductor owns everything else. Worktree creation/lifecycle, lockfile handling, git mutation... are all Conductor responsibilities (spec sections 3 and 6)."
- Step 2 note (~line 148): "the Conductor spawns this agent already scoped to the story worktree (spec section 6...). The dev agent neither creates nor enters/exits worktrees." Both statements remain true after this story; Task 4 only adds where/when the Conductor performs the creation.

**`skills/momentum/skills/conductor/references/per-story-review-diff-range.md`**:

- Single named source-of-record for review diff ranges. Scenario A (pre-merge, conduct's case) assumes `story/{slug}` diverged from `sprint/{{sprint_slug}}` — the merge-base form isolates exactly the story's commits *only if* the story branch forked from the sprint branch. This story's explicit base (sprint tip) is what makes that assumption hold. Do not modify this reference; cite it.

### What must be preserved

- Sole-git-mutation-authority: only the Conductor runs git commands (DEC-035, DEC-036 D1; dev/workflow.md line 7). The creation action is Conductor-executed inside the launch loop.
- Concurrent launch invariant: all frontier stories launch in a single turn, no story-count cap (DEC-035 D4). Per-story creation commands run within each story's launch iteration and must not serialize or block the loop beyond the commands themselves.
- Non-interactive routine path: no new developer prompts. Collision handling is deterministic remove-and-recreate, mirroring the reconcile's "no resume/cleanup prompt" doctrine.
- Existing dev-spawn constraint text, write-scope guards, and the 2.1.4/2.1.5 gate ordering — untouched.

### Placement consideration (implementer decides within AC 1)

Recommended placement: first action of the STAGE-1 DEV SPAWN block (inside 2.1.3, before agent resolve). Rationale: 2.1.2 transitions the story to `in-progress` before the gates, so a story stopped at 2.1.4 (contract integrity stop) would acquire an orphan worktree if creation ran earlier. Creating immediately before the dev spawn means only stories that actually build get worktrees. Either way, the pre-flight reconcile already cleans up `in-progress` stories' worktrees on the next session, so this is a tidiness choice, not a correctness one — but state the choice explicitly in the inserted action.

### Git mechanics (for the inserted instructions)

- `git branch story/{S.slug} sprint/{{sprint_slug}}` creates the branch at the sprint tip without checking it out — works even though `sprint/{{sprint_slug}}` is checked out in the main worktree.
- `git worktree add .worktrees/story-{S.slug} story/{S.slug}` checks the new branch out into the worktree. It fails if the path already exists or if the branch is checked out in another worktree — hence the Task 3 pre-removal.
- Single-command equivalent: `git worktree add -b story/{S.slug} .worktrees/story-{S.slug} sprint/{{sprint_slug}}` (use `-B` only if intentionally resetting an existing branch; the explicit remove-then-create form is preferred for legibility in instructions).
- `.worktrees/` is gitignored (`.gitignore` lines 76–78), so worktree directories never pollute the tree.

### Previous story intelligence

- `extract-shared-diff-range-helper-for-per-story-review` (done, this epic) established `per-story-review-diff-range.md` as the single source-of-record after a retro found the same merge-boundary diff bug independently re-authored three times. Lesson applied here: cite the doctrine, never re-derive git range logic inline; and validate instructions against the workflow's concrete merge mechanics (rebase-then-ff at 2.2.M), not the abstract git model.
- `tighten-dev-fixer-write-scope-stop-story-spec-edits` (done): dev/fixer agents get enumerated writable files. This story's writable set is exactly the two workflow.md files plus new eval files — keep edits inside it.
- Recent conductor commits (351b36c, 28d4693, 9249c3e) show active hardening of conductor/workflow.md; re-grep line numbers before editing — the line references above are anchors, not contracts.

### Architecture and convention compliance

- Follow `skills/momentum/references/agent-skill-development-guide.md` for workflow.md editing conventions (project dev-skills rule — authoritative for skill instruction structure).
- This change is skill-instruction only: no scripts, no hooks, no config. Verification is by skill behavior (EDD evals + skill-invoke), not unit tests.

### Project Structure Notes

- Files to modify: `skills/momentum/skills/conductor/workflow.md` (primary), `skills/momentum/skills/dev/workflow.md` (clarifying note only).
- Files to create: 2 eval files under `skills/momentum/skills/conductor/evals/` (existing examples: `eval-approve-path-routes-through-verify.md`, `eval-escalation-machinery-end-to-end.md` — match their given/should format).
- No changes to `per-story-review-diff-range.md`, SKILL.md frontmatter, or any `.momentum/` state files.

### References

- Conductor launch sequence: `skills/momentum/skills/conductor/workflow.md` step 2.1 (line ~276), stage-1 spawn (~322–365), reconcile (~150–173), post-merge cleanup (~1144)
- Dev agent worktree disclaimers: `skills/momentum/skills/dev/workflow.md` (line 7, step 2 note ~148)
- Diff-range doctrine: `skills/momentum/skills/conductor/references/per-story-review-diff-range.md` (Scenario A)
- Verification routing: `skills/momentum/references/rules/verification-standard.md` §1 (skill-instruction → skill-invoke)
- Source finding: 2026-06-09 conductor effectiveness review (adversarially verified, two independent lenses)
- Epic context: `momentum-sprint-orchestration` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 (behavioral evals in `skills/momentum/skills/conductor/evals/`) → skill-instruction (EDD)
- Task 2 (insert branch+worktree creation action in `conductor/workflow.md`) → skill-instruction (EDD)
- Task 3 (idempotent collision handling in `conductor/workflow.md`) → skill-instruction (EDD)
- Task 4 (clarifying note in `dev/workflow.md`) → skill-instruction (EDD)
- Task 5 (run EDD evals + NFR verification) → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/conductor/evals/` (the directory already exists — match the format of `eval-approve-path-routes-through-verify.md`):
   - One `.md` file per eval, named descriptively (e.g., `eval-launch-creates-worktree-from-sprint-tip.md`, `eval-launch-stale-collision-remove-recreate.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text (e.g., "creates the story branch with the sprint branch stated as base, before the stage-1 dev spawn" — not a literal command-string match)

**Then implement:**
2. Modify `skills/momentum/skills/conductor/workflow.md` (Tasks 2–3) and `skills/momentum/skills/dev/workflow.md` (Task 4)

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context (or invoke the skill via its Agent Skills name if installed). Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- This story modifies existing skills (conductor, dev) — it must not regress their NFR posture:
- SKILL.md `description` field must remain ≤150 characters (NFR1) — do not touch SKILL.md unless required; if touched, count precisely
- `model:` and `effort:` frontmatter fields must remain present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; workflow.md is the correct home for the new action — do not add it to SKILL.md (NFR3)
- Skill names keep the `momentum:` namespace prefix (NFR12)

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/conductor/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] Conductor and dev SKILL.md descriptions still ≤150 characters (only if SKILL.md was touched)
- [ ] `model:` and `effort:` frontmatter still present and correct on both skills
- [ ] No SKILL.md body overflow introduced (changes land in workflow.md / references/)
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically — validates the modified workflow.md against story ACs)

**Implementation approach for this story specifically:**
- Tasks 2–3 are instruction-insertion edits inside conductor workflow.md step 2.1. Re-grep anchors before editing (line numbers in Dev Notes are anchors, not contracts). Preserve the existing 2.1.x sub-step numbering and the 2.1.4 placement note verbatim.
- Task 4 extends one existing `<note>` in dev/workflow.md step 2 — a clarification, not a behavior change. The dev agent's disclaimers must read identically in meaning afterward.
- Follow `skills/momentum/references/agent-skill-development-guide.md` conventions for all workflow.md edits (project dev-skills rule).

**Frozen verification contract reminder:** a frozen verification contract will exist for this story's sprint at `sprints/{sprint-slug}/specs/conduct-worktree-and-branch-creation.{ext}`. Dev reads the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before signaling done. Dev never reads the verifier body (Part B: scenarios, assertion scripts, Gherkin) beyond sections explicitly referenced by `how_dev_self_checks`.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
