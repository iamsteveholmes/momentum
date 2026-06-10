---
title: Reconcile commit authority across the Conductor↔dev seam — one owner, effective write-scope guard
story_key: conduct-dev-commit-authority-reconciliation
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - skill-instruction
  - agent-definition
  - specification
verification_method_advisory: skill-invoke
depends_on: []
touches:
  - skills/momentum/agents/dev.md
  - skills/momentum/agents/dev-build.md
  - skills/momentum/agents/dev-frontend.md
  - skills/momentum/agents/dev-skills.md
  - skills/momentum/skills/dev/workflow.md
  - skills/momentum/references/directed-fix-invocation-contract.md
  - _bmad-output/planning-artifacts/sprint-dev-redesign-spec.md
---

# Reconcile commit authority across the Conductor↔dev seam — one owner, effective write-scope guard

## Story

As the maintainer of the Momentum build pipeline,
I want exactly one commit owner across the Conductor↔dev seam — the Conductor — with every artifact on both sides agreeing,
so that the Conductor's WRITE-SCOPE COMMIT GUARD actually fires on every story and out-of-scope edits can never ride into a merge unfiltered.

## Description

The Conductor and the dev agent contradict each other on who commits. The contradiction is live in shipped artifacts on both sides of the seam:

**Conductor side (subagents never commit):**
- `skills/momentum/skills/conductor/SKILL.md` Authority Invariant 1: "Sole git-mutation authority. … Spawned subagents do not mutate git. If a subagent produces output that would change the working tree (code, fixes, spec text), the Conductor reads that output and commits it — the subagent does not commit itself."
- `skills/momentum/skills/conductor/workflow.md` line ~339, spawn constraint passed to the dev agent: "Do not mutate git. Do not spawn build agents. Produce output only."
- `skills/momentum/skills/conductor/workflow.md` lines ~351–362, the Conductor's own commit sequence: `git -C .worktrees/story-{S.slug} add -u`, then the **WRITE-SCOPE COMMIT GUARD** (`git diff --name-only --cached`, unstage any path not in `writable_files` via `git restore --staged P`), then `git commit`. A parallel guard exists in the fix loop at line ~615.

**Dev side (dev commits itself):**
- `skills/momentum/agents/dev.md` line 36: "**Commit when done (green-field).** After implementation is complete, commit all changes with a conventional commit message…" plus the whole "### 4 (Green-field). Commit Changes" process step (lines ~170–176) and the frontmatter description ("delegates implementation to bmad-dev-story, commits, and returns…").
- `skills/momentum/agents/dev.md` line 38 ("Fix-mode commit discipline") and line ~77 (routine branch: "apply the fix by editing the affected file(s) and commit the change").
- `skills/momentum/skills/dev/workflow.md` Step 0.5 routine fix path (line ~67: "Commit the change with a conventional commit message"), and the Step 2 note (line ~148) which quotes "spec section 6 — 'Dev subagents write and commit inside their worktrees'".
- The three role variants the Conductor can bind as `{{dev_agent}}` (conductor/workflow.md line ~321) repeat the instruction verbatim: `agents/dev-build.md:79`, `agents/dev-frontend.md:95`, `agents/dev-skills.md:79` — "read the story, invoke bmad-dev-story, **commit changes**, return structured output".
- `skills/momentum/references/directed-fix-invocation-contract.md` attributes fix commits to the fixer: "the fix-mode applies a fix and returns `disposition: fixed` with the change committed" (line ~71) and "`fixed` — auto-fixed and committed" (line ~177).

**Why this is not cosmetic:** the dev agent receives BOTH instructions in conflict — its own definition says commit, the Conductor's spawn constraint says don't. If the dev obeys its own definition and commits in the worktree, the Conductor's `git add -u` stages nothing, the write-scope guard never fires, and out-of-scope edits ride into the merge unfiltered. The guard is silently neutralized — the failure mode leaves no error, just an unenforced scope boundary.

**Root cause:** `_bmad-output/planning-artifacts/sprint-dev-redesign-spec.md` §6 (line ~424) says "Dev subagents write and commit inside their worktrees; they never merge," and its file-touch table (line ~929) directed the prior story to "reduce to worktree-local commit + completion signal." The conduct build then placed commit authority in the Conductor instead (DEC-035 invariant: Conductor is sole git-mutation authority), but the dev-side artifacts were never reconciled. The prior story `dev-strip-merge-cleanup-authority` (done) stripped merge/cleanup/lock/crash-ask authority from dev but deliberately left commit instructions intact per the spec's wording — this story finishes that reconciliation.

**Decision taken by this story (Option A — Conductor owns commits):** the architecture default per DEC-035 stands. Strip every commit instruction from the dev side (green-field AND fix-mode, base agent AND all three role variants AND the dev skill workflow AND the directed-fix contract); the dev agent returns working-tree output + `file_list` only. The Conductor's existing write-scope commit guard remains the single staging/commit point, unchanged. The alternative (dev keeps worktree-local commits; guard moves to a pre-merge diff-range enforcement point) was considered and rejected — see Dev Notes for the rationale.

Source: confirmed finding from the 2026-06-09 conductor effectiveness review (adversarially verified, high confidence).

## Acceptance Criteria

1. **Single commit owner.** After this story, the Conductor is the only actor any build-path artifact instructs to stage or commit. No artifact under `skills/momentum/` instructs the dev agent — in any mode (green-field or fix-mode) or any variant (`dev`, `dev-build`, `dev-frontend`, `dev-skills`) — to run `git add`, `git commit`, or otherwise produce a commit.

2. **Green-field dev contract is output-only.** `skills/momentum/agents/dev.md` and `skills/momentum/skills/dev/workflow.md` contain no green-field commit instruction: the "Commit when done (green-field)" constraint, the "### 4 (Green-field). Commit Changes" process step, and the frontmatter description's "commits" clause are removed or rewritten so the terminal contract is implementation-complete + `file_list` (plus `part_a_self_check`, `test_results`, `cross_artifact_notes`) with all changes left uncommitted in the worktree for the Conductor to stage and commit.

3. **Fix-mode dev contract is output-only.** The routine-fixed path in both `agents/dev.md` and `skills/dev/workflow.md` edits the affected file(s) and returns `disposition: fixed` with `files_changed` populated — with no commit produced and no commit instruction remaining ("Fix-mode commit discipline" removed or rewritten to state the Conductor commits). The stakes-class no-edit guarantee (zero edits, zero commits for escalated/dismissed/triaged-out) is preserved verbatim in meaning.

4. **Stale spec quote replaced.** The Step 2 note in `skills/momentum/skills/dev/workflow.md` no longer quotes "Dev subagents write and commit inside their worktrees"; it states the as-built model (dev writes in the Conductor-provided worktree; the Conductor stages and commits). The Step 3 failed-variant guidance no longer tells dev to report "files committed before the failure" — it reports files changed in the worktree (e.g., via `git status`/`git diff --name-only`), since dev no longer produces commits.

5. **Role variants reconciled.** The base-process sentence in `agents/dev-build.md`, `agents/dev-frontend.md`, and `agents/dev-skills.md` no longer says "commit changes" — each reads (in substance): read the story, invoke bmad-dev-story, return structured output; the Conductor commits.

6. **Directed-fix contract reconciled.** `skills/momentum/references/directed-fix-invocation-contract.md` attributes all commit production to the Conductor: the `fixed` disposition means the fix was applied to the working tree and returned for the Conductor to stage (write-scope guard) and commit. No sentence in the contract states or implies the fixer commits.

7. **Write-scope guard remains the single enforcement point and its precondition now holds.** The Conductor's stage-1 commit sequence and WRITE-SCOPE COMMIT GUARD (`conductor/workflow.md` ~351–362) and the fix-loop guard (~615) are unchanged by this story. An audit of `conductor/SKILL.md` + `conductor/workflow.md` confirms no remaining text grants commit authority to any spawned dev/fixer agent. With dev no longer committing, the guard's operating precondition — uncommitted worktree changes present when the dev agent returns — holds on every story and every fix iteration.

8. **Spec drift annotated.** `_bmad-output/planning-artifacts/sprint-dev-redesign-spec.md` §6 carries a dated supersession note at the "Dev subagents write and commit inside their worktrees" sentence (line ~424; also covering the §6 "commit all work in the worktree" sentence at ~426 and the file-touch table's "worktree-local commit" at ~929) stating that as-built, the Conductor is the sole commit point per DEC-035 and the conductor skill's Authority Invariant 1 — so a future reader does not re-add commit authority to dev.

9. **Observable verification.** ACs 1–6 are verifiable by invoking `momentum:dev` (skill-invoke) on a representative green-field story and a representative routine-finding fix set, then inspecting terminal output and worktree state: edits present, `git log` shows no new dev-authored commit, structured output schemas (green-field and fix-mode) are otherwise unchanged. AC 7 is verifiable by grep over the conductor artifacts; AC 8 by inspection of the spec file.

## Tasks / Subtasks

- [ ] Task 1: Strip green-field commit authority from `skills/momentum/agents/dev.md` (AC 1, 2)
  - [ ] Rewrite frontmatter `description` to drop "commits" (e.g., "delegates implementation to bmad-dev-story and returns implementation-complete output with files changed").
  - [ ] Remove the "**Commit when done (green-field).**" constraint (line ~36); replace with a constraint stating dev produces working-tree changes only and the Conductor stages (under the write-scope guard) and commits.
  - [ ] Remove "### 4 (Green-field). Commit Changes" (lines ~170–176); fold any surviving intent (review modified files against `writable_files`) into the self-check/output steps; renumber step 5 accordingly.
  - [ ] Update Step 3 prose "skip this step and proceed to commit" (line ~166) to "skip this step and proceed to the completion signal".
  - [ ] Add a "What NOT to Do" bullet: **No commits (either mode)** — never run `git add`/`git commit`; the Conductor is the sole git-mutation authority (DEC-035; conductor SKILL.md Authority Invariant 1).
- [ ] Task 2: Strip fix-mode commit authority from `skills/momentum/agents/dev.md` (AC 1, 3)
  - [ ] Remove/rewrite "**Fix-mode commit discipline.**" (line ~38): fixes for `fixed` dispositions are applied to the working tree; the Conductor commits them after the fixer returns (matching conductor/workflow.md ~604).
  - [ ] Routine branch (line ~77): "apply the fix by editing the affected file(s) and commit the change" → "apply the fix by editing the affected file(s)"; disposition semantics unchanged.
  - [ ] Sweep fix-mode schema annotations: `files_changed: ["{{files_edited_and_committed}}"]` → files edited; "no edits made, no commits produced" phrasing may remain only where it describes the no-edit guarantee, not a dev commit duty.
- [ ] Task 3: Strip commit actions and stale citations from `skills/momentum/skills/dev/workflow.md` (AC 1, 2, 3, 4)
  - [ ] Step 0.5 routine fix path (line ~67): remove "Commit the change with a conventional commit message. Stage only the files changed by this fix — never git add -A." Dev edits files and reports; the Conductor commits under the fix-loop write-scope guard.
  - [ ] Step 2 note (line ~148): rewrite the full note — remove both the "spec section 6 — 'Dev subagents write and commit inside their worktrees'" quote AND the "bmad-dev-story writes and commits land in the Conductor-provided worktree automatically" phrasing; replace with the as-built model: dev writes in the Conductor-provided worktree; the Conductor stages and commits (conductor/workflow.md stage-1 sequence).
  - [ ] Step 3 failed-variant guidance (line ~196): "files committed before the failure (check git log in the worktree)" → files changed in the worktree before the failure (check `git status` / `git diff --name-only`).
  - [ ] Header/Role prose: confirm no remaining "commit" duty assigned to dev in either mode.
- [ ] Task 4: Reconcile the three role variants (AC 1, 5)
  - [ ] `agents/dev-build.md:79`, `agents/dev-frontend.md:95`, `agents/dev-skills.md:79`: remove "commit changes" from the base-process sentence; keep the structured-output requirement intact.
  - [ ] Inspect the "### Conventional Commits" section in `agents/dev-skills.md` (lines ~52–56): decide keep-with-annotation (if it only documents message format for the Conductor's benefit) vs. remove (if it instructs the agent to author commits), and record the decision explicitly in the Dev Agent Record.
- [ ] Task 5: Reconcile `skills/momentum/references/directed-fix-invocation-contract.md` (AC 1, 6)
  - [ ] Line ~71: "applies a fix and returns `disposition: fixed` with the change committed" → fix applied to the working tree; the Conductor stages and commits after the fixer returns.
  - [ ] Line ~177 (outcome table): "`fixed` — auto-fixed and committed" → "`fixed` — auto-fixed; committed by the Conductor".
  - [ ] Sweep the rest of the contract for any other sentence attributing commit production to the fixer (e.g., "producing a fix commit" phrasing is acceptable only where it describes what does NOT happen on escalation).
  - [ ] After the line ~71 edit, review the adjacent "This path is unchanged from prior behavior" claim — verify it still holds, and add a clarifying parenthetical if needed (unchanged = always-on, never escalates; the Conductor now produces the commit).
- [ ] Task 6: Audit the Conductor side — no edits expected (AC 7)
  - [ ] Grep `conductor/SKILL.md` and `conductor/workflow.md` for any text granting commit authority to spawned dev/fixer agents; confirm none exists; confirm the stage-1 guard (~351–362) and fix-loop guard (~615) are untouched by this story.
- [ ] Task 7: Annotate spec drift in `_bmad-output/planning-artifacts/sprint-dev-redesign-spec.md` (AC 8)
  - [ ] Add a dated supersession note at §6 line ~424 (covering ~426 and the table row at ~929): as-built, commit authority lives solely in the Conductor per DEC-035 / conductor Authority Invariant 1; dev returns uncommitted output. Do not rewrite the spec's history — annotate, don't erase.
- [ ] Task 8: Residual sweep + observable self-check (AC 1, 9)
  - [ ] `grep -rn "commit" skills/momentum/agents/dev*.md skills/momentum/skills/dev/ skills/momentum/references/directed-fix-invocation-contract.md` — confirm every remaining hit either assigns commit authority to the Conductor or describes the no-edit/no-commit guarantee.
  - [ ] Run the skill-invoke self-check per AC 9 (representative green-field story + representative routine fix set; observe uncommitted worktree changes and intact output schemas).

## Dev Notes

### Decision rationale — why Option A (Conductor commits), not Option B (dev commits)

- **DEC-035 already rules.** Conductor SKILL.md Authority Invariant 1 names the Conductor sole git-mutation authority including commits; DEC-036 D1 makes that relocation the precondition for Conductor-owned mid-flight escalation. The prior story `dev-strip-merge-cleanup-authority` (done) executed the merge/cleanup/lock/crash-ask half of this relocation for exactly this reason.
- **The as-built machinery assumes it.** The Conductor's stage-1 sequence (`git add -u` → guard → commit, workflow.md ~351–362), the fix-loop guard (~615, including the scope-revert paths that `git checkout -- P` / `restore --staged P` out-of-scope edits), the simplify-pass commit (~682–685), and the merge-conflict and AVFL fixer paths all operate on **uncommitted** subagent output. Option B would require relocating the guard to a pre-merge diff-range enforcement point and rebuilding the scope-revert machinery against committed history (revert/rewrite instead of unstage/discard) — strictly more work, more dangerous primitives, and it contradicts two ratified decisions.
- **The guard's silent-failure mode is the bug.** `git add -u` on a clean worktree stages nothing and `git commit` either no-ops or fails quietly in script context; no error surfaces. Choosing Option A converts the guard's precondition from "hope dev didn't commit" to "dev is forbidden to commit," which is checkable by grep and by skill-invoke observation.

### What the Conductor side already does (do not duplicate, do not modify)

- Spawn constraint at conductor/workflow.md ~339: "Do not mutate git. Do not spawn build agents. Produce output only." — already correct; it wins after this story because the dev-side artifacts stop contradicting it.
- Stage-1 commit: `git -C .worktrees/story-{S.slug} add -u` → WRITE-SCOPE COMMIT GUARD (`diff --name-only --cached`; `restore --staged` any path not in `writable_files`) → `commit -m "feat({S.slug}): implement {{S.title}}"`. The conventional-commit message duty lives here now (currently hardcoded as `feat`; change_type-aware formatting is a separate concern) — dev.md's removed step 4 must NOT be re-homed into dev output.
- Fix-loop: fixer returns dispositions; Conductor verifies stakes-class, runs the fix-loop guard, commits `fix({S.slug}): auto-fix {F.summary}` (~628). The contract reference (Task 5) must match this exactly.

### Current state of each touched file (read before editing)

- `agents/dev.md` (264 lines): dual-mode agent definition. Commit language at: frontmatter description (line 3), line 36 (green-field constraint), line 38 (fix-mode discipline), line 77 (routine branch), lines 119/132/135 (schema annotations), lines 170–176 (step 4), line 166 ("proceed to commit"). Everything else — Part-A contract rules, write-scope constraint, cross-artifact notes, escalation payloads, output schemas — is correct and must be preserved unchanged.
- `skills/dev/workflow.md` (218 lines): commit language at line 67 (Step 0.5 routine path), line 148 (Step 2 note with the stale spec §6 quote), line 196 (failed-variant "files committed"). The fix-mode disposition logic, Part-A self-check (Step 2.5), and output signals are correct otherwise.
- `agents/dev-build.md` / `dev-frontend.md` / `dev-skills.md`: one identical sentence each (lines 79/95/79). `dev-skills.md` also has a "### Conventional Commits" section (line ~52) — inspect it: if it instructs the agent to author commits, reconcile it the same way; if it only documents message format conventions for the Conductor's benefit, leave a one-line attribution note.
- `references/directed-fix-invocation-contract.md`: lines ~61 (escalated row — phrasing "instead of applying a fix or producing a fix commit" is about what escalation does NOT do; acceptable to keep), ~71, ~77 ("No fix is applied. No fix commit is produced." — acceptable, describes escalation), ~177–178 (outcome table).
- `skills/dev/SKILL.md`: already correct ("emits an implementation-complete + file_list signal") — no change expected; verify only.

### What must be preserved (regression guards)

- Dev's structured output schemas (green-field and fix-mode) — field names, AGENT_OUTPUT_START/END framing, disposition vocabulary, `timing_tier` nesting — are parsed by the Conductor. Do not change any schema shape; only the prose around commit duties.
- The stakes-class no-edit guarantee, the non-empty dismissal-rationale rule, the Part-A-only contract read surface, the writable_files write-scope constraint, and the cross-artifact-notes routing are all untouched by this story.
- `sprint-dev` (legacy wave-loop) still references the dev variants' structured output ("sprint-dev Phase 3 parses it"). Removing "commit changes" from the variant sentence does not change the parse contract. Note: under legacy sprint-dev the dev agent committing was load-bearing; legacy sprint-dev is no longer the primary build path (Impetus routes builds to momentum:conductor). If legacy compatibility text exists in those files, prefer a parenthetical ("under the Conductor, commits are the Conductor's") over deleting legacy context wholesale — but the binding instruction must be: do not commit.

### Previous story intelligence

`dev-strip-merge-cleanup-authority` (done) is the direct predecessor on the same two primary files. Its learnings: (a) it reduced dev to "implementation-complete + file_list" for merge concerns and the rewrite stuck — the same reduction pattern applies here for commit concerns; (b) it sourced its retained-commit wording from sprint-dev-redesign-spec.md §6/§file-touch-table — which is exactly the text this story annotates as superseded (root-cause closure, not just symptom edits); (c) its AC style ("observable purely from invoking momentum:dev and inspecting output + repository state") was effective and is reused in AC 9 here.

### Git intelligence

The conduct engine merged at `bc4ec4d` (conduct-runnable, 25 stories) with a post-merge AVFL reconcile at `351b36c` that fixed 9 cross-story drifts — this story is the same class of cross-story drift, found post-merge by the 2026-06-09 conductor effectiveness review. Conventional commit for this story: `fix(skills): ...` (it corrects shipped skill/agent instruction files; per the code-vs-docs rule, skill markdown is code; the spec annotation sub-change is `docs`-class but rides as a bullet).

### Web research

N/A — all artifacts are internal markdown skill/agent instruction files; no external libraries, frameworks, or version-sensitive APIs are involved.

### Project Structure Notes

- Agent definitions live in `skills/momentum/agents/*.md` (agent-definition change type); skill workflows in `skills/momentum/skills/{name}/workflow.md` and shared references in `skills/momentum/references/` (skill-instruction change type); planning artifacts in `_bmad-output/planning-artifacts/` (specification change type).
- Per `.claude/rules/dev-skills.md`, follow `skills/momentum/references/agent-skill-development-guide.md` conventions when modifying SKILL.md/workflow.md/agent definitions.
- No file moves or new files in this story except (optionally) EDD eval files under `skills/momentum/skills/dev/evals/`.

### References

- `skills/momentum/skills/conductor/SKILL.md` — Authority Invariant 1 (sole git-mutation authority; subagent does not commit itself).
- `skills/momentum/skills/conductor/workflow.md` — spawn constraint (~339); stage-1 commit sequence + WRITE-SCOPE COMMIT GUARD (~351–362); fix-loop guard and Conductor-commits-fixes (~596–628); `{{dev_agent}}` variant binding (~321).
- `skills/momentum/agents/dev.md`; `skills/momentum/skills/dev/workflow.md`; `skills/momentum/agents/dev-build.md` / `dev-frontend.md` / `dev-skills.md`; `skills/momentum/references/directed-fix-invocation-contract.md` — the dev-side surfaces carrying commit language (line anchors in Tasks).
- `_bmad-output/planning-artifacts/decisions/dec-035-conduct-execution-engine-in-session-workflows-2026-05-30.md` — DEC-035 (adopt conduct; Conductor owns build phase and git mutation; single end-gate).
- DEC-036 D1 (cited in dev.md and predecessor story) — relocating git-mutation authority out of dev is the precondition for Conductor-owned mid-flight escalation.
- `_bmad-output/planning-artifacts/sprint-dev-redesign-spec.md` — §6 line ~424, ~426; file-touch table line ~929 (the superseded dev-commits wording; Task 7 target).
- `.momentum/stories/dev-strip-merge-cleanup-authority.md` — predecessor story (done) on the same files.
- 2026-06-09 conductor effectiveness review — source finding (adversarially verified, high confidence).
- Epic context: `momentum-sprint-orchestration` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 4 → agent-definition (EDD via skill-invoke — agent definitions are LLM prompt files; same approach as skill-instruction)
- Tasks 3, 5 → skill-instruction (EDD)
- Tasks 6, 8 → verification sweep (no EDD)
- Task 7 → specification (direct authoring with cross-reference verification)

---

### skill-instruction + agent-definition Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md, workflow.md, or agent-definition files.** Skill instructions and agent definitions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the changes:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/dev/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-greenfield-returns-uncommitted-output.md`, `eval-fixmode-routine-fix-no-commit.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text. For this story the core behaviors are: (a) green-field dev completes implementation, leaves the worktree dirty (no new commit), and emits the unchanged structured output; (b) fix-mode dev applies a routine fix, produces no commit, returns `disposition: fixed` with `files_changed`; (c) no dev variant instruction text directs a commit.

**Then implement:**
2. Modify the agent definitions (`agents/dev.md`, `agents/dev-build.md`, `agents/dev-frontend.md`, `agents/dev-skills.md`), the dev skill workflow (`skills/dev/workflow.md`), and the shared reference (`references/directed-fix-invocation-contract.md`) per Tasks 1–5.

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) the modified agent/workflow contents as context. Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for skill-instruction tasks:**
- Any touched SKILL.md `description` field must remain ≤150 characters (NFR1) — count precisely (no SKILL.md description change is expected in this story; verify only)
- `model:` and `effort:` frontmatter fields must remain present (model routing per FR23)
- SKILL.md bodies must stay under 500 lines / 5000 tokens; overflow content goes in `references/` (NFR3)
- Skill names keep the `momentum:` namespace prefix (NFR12)

**Additional DoD items for skill-instruction/agent-definition tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/dev/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] Structured output schemas (green-field and fix-mode) byte-compatible for Conductor parsing — field names, AGENT_OUTPUT framing, disposition vocabulary, `timing_tier` nesting all unchanged
- [ ] `grep -rn -i "commit"` over the dev-side artifacts shows every remaining hit attributes commit authority to the Conductor or describes the no-edit/no-commit guarantee (Task 8 sweep)
- [ ] Conductor artifacts (`conductor/SKILL.md`, `conductor/workflow.md`) untouched — stage-1 guard (~351–362) and fix-loop guard (~615) byte-identical (Task 6 audit)

### specification Tasks: Direct Authoring with Cross-Reference Verification

Specification changes (Task 7 — the `sprint-dev-redesign-spec.md` supersession annotation) are validated by AVFL against their upstream source — not by tests or evals. Write directly and verify by inspection:

1. **Write the annotation** per AC 8: a dated supersession note at §6 line ~424 (covering ~426 and the file-touch table row at ~929) — annotate, don't erase or rewrite the spec's history
2. **Verify cross-references:** the note must cite DEC-035 and the conductor skill's Authority Invariant 1 by their real paths/identifiers; check both resolve
3. **Verify format compliance:** match the spec's existing annotation/editorial conventions if any exist
4. **Document** what was written in the Dev Agent Record

**Additional DoD items for specification tasks:**
- [ ] All cross-references in the annotation resolve correctly
- [ ] Annotation is additive — no original spec sentence deleted or reworded
- [ ] AVFL checkpoint result documented (momentum:dev runs this automatically)

### Frozen verification contract reminder

A frozen verification contract exists for this story's sprint at `sprints/{sprint-slug}/specs/conduct-dev-commit-authority-reconciliation.{ext}` (created at sprint-planning time). Dev reads the **Part-A header only** (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before signaling done. Dev never reads the verifier body (Part B: scenarios, assertion scripts, Gherkin) beyond sections explicitly referenced by `how_dev_self_checks`. If no contract exists yet (story not yet assigned to a sprint), proceed against the plain-English ACs above.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
