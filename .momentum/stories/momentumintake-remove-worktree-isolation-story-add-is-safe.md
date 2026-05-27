---
title: "momentum:intake — remove worktree isolation, story-add is safe to run concurrently"
story_key: momentumintake-remove-worktree-isolation-story-add-is-safe
status: ready-for-dev
epic_slug: ad-hoc
feature_slug: ""
story_type: maintenance
change_type: skill-instruction
verification_method: EDD
harness_profile: default
depends_on: []
touches:
  - skills/momentum/skills/intake/SKILL.md
  - skills/momentum/skills/intake/workflow.md
  - skills/momentum/skills/intake/evals/eval-intake-runs-on-main-no-worktree.md
---

# momentum:intake — remove worktree isolation, story-add is safe to run concurrently

## Story

As a developer,
I want intake to always write its stub directly to the main working tree without any worktree isolation,
so that captured stubs land immediately in `.momentum/stories/` and are visible to every concurrent session without manual recovery steps.

## Description

The `momentum:intake` skill is a lightweight conversational capture step. The index mutation it performs is a `momentum-tools sprint story-add` call that writes a brand-new unique slug key — so there is no concurrent-write collision risk that worktree isolation would mitigate. Worktree isolation, when applied to intake (either by intake itself or by a caller wrapping intake), traps the stub file inside a feature branch instead of landing it on main. Recovery requires manually copying the stub out of the branch and re-running `story-add` against main.

Observed during the DEC-033 / DEC-034 cascade triage: 4 of 8 intake agents executed under worktree wrappers, leaving stub files orphaned in story branches; the triage orchestrator had to copy stub files out and re-register the index entries manually.

Audit of the current `intake/SKILL.md` and `intake/workflow.md` (commit `a5a1eb7` baseline) finds **no** `EnterWorktree` or `ExitWorktree` invocations — intake is already worktree-free by construction. The risk this story addresses is regression: a future edit or a caller wrapper silently re-introducing worktree isolation around intake. The fix is therefore (a) an explicit non-isolation contract documented in `SKILL.md` and `workflow.md`, and (b) an EDD eval that fails if any worktree-entry tool is invoked during an intake run or if the stub does not land on the main working tree.

**Pain context:** Captured during DEC-033/034 cascade triage. Recurrence: every batch intake run (8+ concurrent spawns) had a ~50% rate of stub orphaning. Workaround burden: manual copy + re-register per orphaned stub. Forgetting risk: each new orchestrator/caller may re-introduce isolation defensively without realizing intake's writes are non-colliding by design.

## Acceptance Criteria

AC1 — **No worktree-entry calls in intake skill files.** `skills/momentum/skills/intake/SKILL.md` and `skills/momentum/skills/intake/workflow.md` contain zero references to `EnterWorktree`, `ExitWorktree`, `git worktree add`, or any equivalent isolation mechanism. A literal grep for `worktree` (case-insensitive) over both files returns no matches outside of an explicit "MUST NOT use worktree isolation" prohibition statement.

AC2 — **Explicit non-isolation contract in workflow.md.** A `<critical>` directive in `intake/workflow.md` states that intake MUST run in the main working tree and MUST NOT invoke `EnterWorktree` or any worktree-creation command. The directive cites the rationale: `story-add` writes a new unique slug key — no collision risk exists.

AC3 — **Behavioral eval enforces main-tree execution.** A new eval file at `skills/momentum/skills/intake/evals/eval-intake-runs-on-main-no-worktree.md` defines a scenario where an intake skill run is observed; the eval's pass criteria explicitly require that no `EnterWorktree`/`ExitWorktree` tool calls appear in the run's tool sequence AND that the stub file at `.momentum/stories/<slug>.md` is visible from the main working tree (not a branch checkout) after the run completes.

AC4 — **Concurrent-spawn safety documented.** The workflow.md non-isolation directive states the safety guarantee for parallel callers: any number of concurrent intake invocations is safe because each generates a unique slug and `story-add` performs an atomic read-modify-write of `stories/index.json`. The directive explicitly tells caller skills they MUST NOT wrap intake in a worktree for collision protection.

AC5 — **EDD evals pass.** Running the EDD evals in `skills/momentum/skills/intake/evals/` (the new eval plus the two existing ones — `eval-intake-captures-context.md` and `eval-intake-routes-discovered-work-with-discovered-from.md`) all confirm expected behavior. The pre-existing capture-context eval still passes (no regression on B1–B8 from that eval).

AC6 — **No regression on stub registration.** A representative intake run still produces: (a) a stub file at `.momentum/stories/<slug>.md` with `status: backlog`, (b) an index entry registered via `momentum-tools sprint story-add` with the correct slug, title, epic, and priority. Both artifacts are present on the main working tree immediately after the run completes — no merge step required.

## Tasks / Subtasks

- [ ] **Task 1 — Audit and verification of current state (skill-instruction).**
  - [ ] Grep `skills/momentum/skills/intake/` for `EnterWorktree`, `ExitWorktree`, and `worktree` (case-insensitive); record results.
  - [ ] Confirm baseline: zero pre-existing worktree references in intake skill files (matches AC1).
  - [ ] Record audit findings in the Dev Agent Record's Completion Notes.

- [ ] **Task 2 — Author EDD eval (skill-instruction, EDD).**
  - [ ] Create `skills/momentum/skills/intake/evals/eval-intake-runs-on-main-no-worktree.md`.
  - [ ] Eval scenario: a developer invokes `momentum:intake` mid-conversation; the eval runner observes the resulting tool-call sequence and the post-run filesystem state.
  - [ ] Eval pass criteria (B1): zero `EnterWorktree`, `ExitWorktree`, or `git worktree` tool invocations during the run.
  - [ ] Eval pass criteria (B2): stub file at `.momentum/stories/<slug>.md` exists on main working tree (not in a worktree branch checkout).
  - [ ] Eval pass criteria (B3): the `story-add` CLI call is the sole mutation of `.momentum/stories/index.json`.
  - [ ] Eval pass criteria (B4): zero manual recovery steps required after the run (no copy, no re-register).
  - [ ] Eval format follows existing intake eval conventions (see `eval-intake-captures-context.md`).

- [ ] **Task 3 — Add explicit non-isolation contract to workflow.md (skill-instruction).**
  - [ ] In `skills/momentum/skills/intake/workflow.md`, add a `<critical>` directive at the top of the `<workflow>` block (alongside the existing `<critical>` directives) prohibiting worktree isolation.
  - [ ] Directive text MUST state: (a) intake runs in the main working tree only, (b) `EnterWorktree`/`ExitWorktree`/`git worktree` MUST NOT be invoked, (c) caller skills MUST NOT wrap intake in a worktree, (d) the rationale: `story-add` writes a unique slug key, no collision risk exists.
  - [ ] Directive must be discoverable by grep — include the literal token `worktree` so a future audit (AC1's grep) finds the prohibition statement.

- [ ] **Task 4 — Update SKILL.md description if needed (skill-instruction).**
  - [ ] Verify `skills/momentum/skills/intake/SKILL.md` description (≤150 chars) still accurately summarizes the skill. The description need not mention worktree absence; it should remain concise.
  - [ ] If description is unchanged, document that in Completion Notes.
  - [ ] Confirm `model:` and `effort:` frontmatter fields are still present and appropriate (current: `effort: low`; `model:` may need to be added if missing).

- [ ] **Task 5 — Run EDD evals and verify (skill-instruction, EDD).**
  - [ ] Spawn a subagent per eval file in `skills/momentum/skills/intake/evals/`; give each subagent the eval scenario plus the intake `SKILL.md` and `workflow.md` contents as context.
  - [ ] Observe whether each subagent's behavior matches the eval's expected outcome.
  - [ ] All three evals must pass (the new no-worktree eval, plus the two pre-existing evals).
  - [ ] If any eval fails: diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing).
  - [ ] Document eval results in Dev Agent Record.

- [ ] **Task 6 — Final verification pass (skill-instruction).**
  - [ ] Re-run the AC1 grep audit on the final files; confirm zero `EnterWorktree`/`ExitWorktree` calls outside the prohibition statement.
  - [ ] Confirm the new eval file is present and well-formed.
  - [ ] Confirm SKILL.md is still ≤500 lines and description ≤150 chars.

## Dev Notes

### Architecture Compliance

This change touches a single Momentum skill (`momentum:intake`) and its evals. It does not alter any cross-skill contract beyond making explicit a guarantee that callers were already implicitly relying on: intake writes are safe to run concurrently without isolation.

The change is consistent with the orchestrator-purity model: intake is a lightweight, conversational capture skill (not an orchestrator), and adding worktree isolation would have been a mismatch with its purpose. The non-isolation contract codifies the existing design intent.

No architecture decision document needs updating. If DEC-033 / DEC-034 surface follow-on stories about caller-side wrapping behavior (e.g., `momentum:triage` or `momentum:dev` spawning intake under a worktree), those would be separate stories targeting the calling skills — out of scope here.

### Testing Requirements

Verification method per `skills/momentum/references/rules/verification-standard.md` § 1: `change_type: skill-instruction` routes to **EDD (Eval-Driven Development)** — adversarial eval scenarios authored independent of implementation.

- **New eval (mandatory):** `skills/momentum/skills/intake/evals/eval-intake-runs-on-main-no-worktree.md` per Task 2 above.
- **Regression evals (existing):** `eval-intake-captures-context.md` and `eval-intake-routes-discovered-work-with-discovered-from.md` must still pass.
- **Eval execution:** spawn one subagent per eval file via the Agent tool; pass the eval scenario + intake `SKILL.md`/`workflow.md` contents as context; observe whether behavior matches the expected outcome.
- **Harness profile:** `default` (per project default in `momentum/verification-harness.json` — no special harness needed; evals run as Agent-tool subagent spawns).
- **Adversarial guard (verification-standard § 4):** all eval pass criteria are stated in ordinary-user terms (observable tool-call sequence, observable filesystem state). No insider knowledge required.

### Implementation Guide

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4, 5, 6 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill change:**
1. Write the new behavioral eval in `skills/momentum/skills/intake/evals/eval-intake-runs-on-main-no-worktree.md`:
   - Format: "Given [intake invocation], the skill should [observable behavior — no worktree calls, stub lands on main, no manual recovery]"
   - Test observable behaviors, not exact output text.
   - The existing eval files (`eval-intake-captures-context.md`, `eval-intake-routes-discovered-work-with-discovered-from.md`) are the format/voice reference.

**Then implement:**
2. Add the `<critical>` non-isolation directive to `skills/momentum/skills/intake/workflow.md`. Place it among the existing `<critical>` blocks at the top of the `<workflow>` element (around lines 12–25 of the current file).
3. If `SKILL.md` needs any clarification, edit it — but keep `description` ≤150 chars and the file body minimal (it currently just delegates to `workflow.md`).

**Then verify:**
4. Run all three evals: for each `.md` file in `skills/momentum/skills/intake/evals/`, spawn an Agent-tool subagent. Pass it: (a) the eval scenario as its task, and (b) the intake `SKILL.md` and `workflow.md` contents as context. Observe whether the subagent's behavior matches the eval's expected outcome.
5. If all three evals pass → task complete.
6. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing).

**NFR compliance — mandatory for every skill-instruction task:**
- `SKILL.md` `description` field must be ≤150 characters — count precisely.
- `model:` and `effort:` frontmatter fields must be present.
- `SKILL.md` body must stay under 500 lines / 5000 tokens; overflow content goes in `references/`.
- Skill name uses `momentum:` namespace prefix — already satisfied (`name: intake` under `skills/momentum/skills/intake/`).

**Additional DoD items for this story:**
- [ ] New eval file written: `skills/momentum/skills/intake/evals/eval-intake-runs-on-main-no-worktree.md`.
- [ ] EDD cycle ran — all three eval behaviors confirmed (or failures documented with explanation).
- [ ] `SKILL.md` description ≤150 characters confirmed (count the actual characters).
- [ ] `model:` and `effort:` frontmatter present and correct.
- [ ] `SKILL.md` body ≤500 lines / 5000 tokens confirmed.
- [ ] AVFL checkpoint on produced artifacts documented (momentum:dev runs this automatically against story ACs).

### Project Structure Notes

Files touched live under the canonical Momentum skill path:

```
skills/momentum/skills/intake/
├── SKILL.md                                                # touched (verify/maybe-no-op)
├── workflow.md                                             # touched (add <critical> directive)
├── references/
│   └── stub-template.md                                    # untouched
└── evals/
    ├── eval-intake-captures-context.md                     # untouched (regression check only)
    ├── eval-intake-routes-discovered-work-with-discovered-from.md  # untouched
    └── eval-intake-runs-on-main-no-worktree.md             # NEW
```

This story does not introduce any new directories. The `evals/` directory already exists.

### References

- **Stub commit:** `a5a1eb7` — `docs(stories): intake stub — remove worktree isolation from momentum:intake` (baseline; documents the cascade-triage observation).
- **Verification routing:** `skills/momentum/references/rules/verification-standard.md` § 1 (skill-instruction → EDD) and § 3 (harness profile requirement).
- **Change-type template:** `skills/momentum/skills/create-story/references/change-types.md` (skill-instruction section).
- **Intake skill (under change):**
  - `skills/momentum/skills/intake/SKILL.md`
  - `skills/momentum/skills/intake/workflow.md`
- **Existing evals (regression baseline):**
  - `skills/momentum/skills/intake/evals/eval-intake-captures-context.md`
  - `skills/momentum/skills/intake/evals/eval-intake-routes-discovered-work-with-discovered-from.md`
- **Stub template (for context, not touched):** `skills/momentum/skills/intake/references/stub-template.md`
- **Dev skill (caller context, not touched):** `skills/momentum/skills/dev/workflow.md` (this is where worktree isolation legitimately lives, for code-change stories — not for intake).

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
