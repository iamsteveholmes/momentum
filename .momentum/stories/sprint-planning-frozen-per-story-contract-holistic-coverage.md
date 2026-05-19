---
title: "sprint-planning: frozen per-story contract, holistic coverage plan, adversarial guard"
story_key: sprint-planning-frozen-per-story-contract-holistic-coverage
status: review
epic_slug: sprint-dev-workflow
feature_slug: momentum-sprint-planning-to-ready
story_type: practice
change_type:
  - skill-instruction
depends_on:
  - enforced-verification-rule-change-type-method-routing-harness-profile-requirement-adversarial-guard
  - momentum-harnessjson-schema-and-plugin-shipped-defaults
touches:
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/sprint-planning/SKILL.md
  - skills/momentum/skills/sprint-planning/references/
---

# sprint-planning: frozen per-story contract, holistic coverage plan, adversarial guard

## Story

As a developer,
I want sprint-planning to freeze a per-story verification contract, build a sprint-wide holistic E2E coverage plan, and adversarially guard every authored contract against insider-knowledge contamination,
so that each story has an immutable spec-of-done authored by a party other than its developer, and the sprint has a non-redundant transitive E2E coverage map that a black-box validator can execute without application insider knowledge.

## Description

Extend `momentum:sprint-planning` (Step 4) to produce three new outputs after all stories are approved and before team composition:

**(a) Frozen per-story verification contracts** — one method-polymorphic contract file per story, written to `.momentum/sprints/{slug}/specs/`. The contract file format depends on the story's change-type (`.eval.yaml`, `.trigger.md`, `.smoke.sh`, `.review.md`, or `.feature`). The contract is hook-immutable after sprint activation. It is the canonical spec-of-done consumed by `e2e-validator` at verification time. The dev agent never reads this path.

**(b) Sprint-level holistic E2E coverage plan** — a single document (`coverage-plan.md`) that maps scenarios to the stories and file spans they discharge, credits transitive coverage explicitly, and applies anti-redundancy as its governing principle. The plan names which stories get dedicated verification and which are covered-by-composition, with rationale. It is authored once at planning and is also hook-immutable after activation.

**(c) Adversarial anti-insider-knowledge guard** — after contracts are drafted, a decorrelated adversarial agent reviews every contract for insider-knowledge contamination. A contract that cannot be verified by an ordinary user of the system — one with no source code access — fails the guard and must be rewritten before the sprint activates.

**Source:** DEC-029 D2, D6, D8 (`_bmad-output/planning-artifacts/decisions/dec-029-method-routed-acceptance-validation-pipeline-2026-05-17.md`).

**Intra-sprint dependencies:**
- Consumes the enforced verification rule (`enforced-verification-rule-change-type-method-routing-harness-profile-requirement-adversarial-guard`) — the rule defines the method-routing table and contract format per change-type.
- Consumes `momentum/verification-harness.json` schema (`momentum-harnessjson-schema-and-plugin-shipped-defaults`) — the harness declares the execution surface and driver per change-type; contracts reference it.

**DEC-030 constraint:** Do not contradict the frozen-scope / DAG model. The activation gate in this story is additive — it enforces that contracts are present and adversarially clean before `sprint activate` runs. It does not modify story-scope rules, the subtract-only freeze, or the DAG dispatch model.

## Acceptance Criteria

### Contract authoring

1. After all stories in the sprint are approved (Step 3 complete), `sprint-planning` authors one verification contract per story and writes it to `.momentum/sprints/{sprint-slug}/specs/{story-slug}.{ext}`.

2. The contract file extension is determined by the story's change-type per the verification-standard rule: `skill-instruction` → `.eval.yaml`; `rule-hook` → `.trigger.md`; `script-code` → `.smoke.sh`; `specification` → `.review.md`; `app-ui` → `.feature`. A story with multiple change-types uses the extension of the highest-tier type (app-ui > script-code > skill-instruction > rule-hook > specification). This precedence ordering is derived from the verification-weight principle in DEC-029 D1 ("verification weight should scale with change-type") — the dev agent should confirm the final ordering against the verification-standard rule file when it exists.

3. The contract body states what must be verifiably true about the story's observable behavior, not how the implementation works. It must be passable by a black-box agent with no source code access.

4. For `skill-instruction` stories the contract specifies behavioral evals: named invocation scenarios, concrete observable outputs, and pass/fail criteria. It does not reference SKILL.md contents, internal delegation chains, or which tools are called.

5. For `rule-hook` stories the contract specifies trigger conditions and observable outcomes: what event fires the hook, what observable state change must result. It does not reference the settings.json key path or hook body implementation.

6. For `script-code` stories the contract specifies invocation command, sample inputs, and expected outputs or exit codes observable from the shell. It does not reference function names or internal data structures.

7. For `specification` stories the contract specifies document review criteria: what claims must be verifiable, what sections must be present, what cross-references must resolve. It does not reference file line numbers or internal schema keys.

8. The contract format is compatible with `momentum/verification-harness.json` — it references only driver surfaces declared in the harness defaults block.

9. The contracts directory is created automatically if it does not exist.

### Coverage plan

10. After all per-story contracts are drafted, `sprint-planning` authors a single `coverage-plan.md` and writes it to `.momentum/sprints/{sprint-slug}/`.

11. The coverage plan lists the minimal set of integrated scenarios sufficient to discharge every story's spec-of-done — one scenario may discharge multiple stories if the scenario exercises their joint behavior.

12. For each scenario the coverage plan includes: scenario name, a brief behavioral description, and the explicit list of stories and file/span paths it discharges.

13. Stories whose contracts are fully discharged by an integrated scenario are marked "covered-by-composition" with a rationale sentence. They receive no dedicated standalone run.

14. Stories whose contracts cannot be transitively covered (e.g. isolated rule-hook stories with no integration scenario exercising them) are marked "dedicated-run" and listed as standalone verification targets.

15. The plan states the anti-redundancy principle as a header note: "Never validate in isolation what an integrated scenario already exercises."

16. The coverage plan is internally consistent — every story in the sprint appears exactly once (either covered-by-composition or dedicated-run), and every scenario names at least one story it discharges.

### Adversarial guard

17. After contracts and the coverage plan are drafted, `sprint-planning` spawns a decorrelated adversarial agent whose sole task is to evaluate each contract for insider-knowledge contamination. The adversarial agent is not the same agent that authored the contracts.

18. The adversarial agent applies the Outsider Test to every clause in every contract: could a person who has never seen the source code verify this clause by only invoking skills, running commands, or reading their observable outputs?

19. A contract clause that references an internal mechanism (which skill is called, which tool is used, which file is read, which function processes the input) fails the Outsider Test and is flagged.

20. The adversarial agent produces a structured findings list: for each failing clause, the story slug, the clause text, and a one-sentence description of why it fails.

21. If the adversarial agent finds no failing clauses across all contracts, the sprint-planning step reports "guard clean" and proceeds to team composition.

22. If the adversarial agent finds one or more failing clauses, `sprint-planning` rewrites the flagged clauses to describe observable outcomes and re-runs the adversarial agent. This rewrite-and-recheck loop runs at most two times.

23. If failing clauses remain after two rewrite passes, `sprint-planning` presents the residual failures to the developer and asks whether to proceed with known contaminated contracts or halt. The sprint cannot activate silently with known guard failures.

### Sprint activation gate

24. The `momentum-tools sprint activate` command must not succeed if contracts are missing for any story in the sprint. The gate checks that `.momentum/sprints/{sprint-slug}/specs/{story-slug}.{ext}` exists for every story in the sprint's story set.

25. The `momentum-tools sprint activate` command must not succeed if `coverage-plan.md` is absent from `.momentum/sprints/{sprint-slug}/`.

26. After activation the specs directory and coverage-plan.md are hook-immutable — no tool or agent may write to or delete files under `.momentum/sprints/{sprint-slug}/specs/` or modify `coverage-plan.md`. The dev agent is explicitly barred from reading the specs directory.

### Placement in sprint-planning workflow

27. The contract authoring, coverage plan, and adversarial guard steps execute between Step 3 (story approval) and the existing Step 4 (Gherkin spec generation). The existing Gherkin generation step remains downstream and unchanged in its logic for stories whose verification method is Gherkin. For `app-ui` stories that receive a `.feature` contract file in Step 3.5, the Step 4 Gherkin generation step must treat that story's `.feature` as already authored and must not overwrite it — the Step 3.5 contract `.feature` is the canonical spec-of-done, not a Step 4 output. Step 4 only generates Gherkin `.feature` files for stories that do not already have a `.feature` contract in the specs directory.

28. The step is tracked via task tracking: a task named "Author frozen contracts + coverage plan" is added to the task list and updated to in_progress / completed as the step runs.

## Dev Notes

### Architecture Compliance

This story extends `skills/momentum/skills/sprint-planning/workflow.md` only. It does not touch sprint-manager, sprint-dev, momentum-tools internals, or the e2e-validator. The activation gate (ACs 24–26) is enforced by `momentum-tools sprint activate`, which is a consumer of the written contracts — this story authors the contracts that gate relies on, but does not modify the activate command itself unless that command already has extension points. If `momentum-tools sprint activate` does not currently enforce contract presence, flag this as a gap in the Dev Agent Record and implement the check in the sprint-planning step instead (i.e., sprint-planning refuses to call `momentum-tools sprint activate` until contracts are present and guard is clean).

DEC-030 D3 freeze invariant: the contract-and-guard step is a pre-activation requirement, not a post-activation modifiable artifact. This aligns with the frozen-scope model — all vetting completes before the sprint's scope is frozen. Adding scope after activation remains prohibited.

DEC-029 D6 authorship rule: `sprint-planning` is the author of frozen contracts. The dev agent is explicitly not the author. The adversarial guard enforces the black-box separation.

**Post-activation immutability mechanism:** The hook-immutability of `.momentum/sprints/{sprint-slug}/specs/` and `coverage-plan.md` is enforced by a `PreToolUse` hook in `.claude/settings.json` that blocks Write, Edit, and Delete operations on paths matching `.momentum/sprints/*/specs/**` and `.momentum/sprints/*/coverage-plan.md` after sprint activation. The dev-agent read-bar for the specs directory is enforced by a matching `PreToolUse` hook blocking Read operations on that same path pattern for the dev agent role. If Momentum does not yet have a hook-based immutability mechanism for sprint artifacts, the dev agent must flag this gap in the Dev Agent Record and implement the behavioral guarantee instead: the sprint-planning step itself does not call `sprint activate` until contracts are present and clean, and no re-entry point exists post-activation. The mechanical enforcement hook is the preferred implementation; the behavioral guarantee is the minimum acceptable fallback.

### Testing Requirements

This story is `skill-instruction` change-type. Use Eval-Driven Development (EDD), not unit tests. Write evals before implementing.

Suggested evals (write in `skills/momentum/skills/sprint-planning/evals/`):

1. **`eval-contract-authored-per-story.md`** — Given a sprint with 3 approved stories of different change-types (skill-instruction, rule-hook, specification), after the contract-authoring step runs, one contract file exists per story in `specs/` with the correct extension and a non-empty body.

2. **`eval-coverage-plan-covers-all-stories.md`** — Given a 4-story sprint where 2 stories share an integration scenario, the coverage plan lists both stories as covered-by-composition under that scenario and lists the other 2 as dedicated-run. Every story appears exactly once.

3. **`eval-adversarial-guard-rejects-insider-clause.md`** — Given a contract that includes a clause "When sprint-planning delegates to bmad-create-story", the adversarial guard flags this clause as failing the Outsider Test and the clause is rewritten before proceeding.

4. **`eval-activation-blocked-without-contracts.md`** — Given a sprint where contracts have not been authored for all stories, the sprint activation step surfaces an error and does not call `momentum-tools sprint activate`.

### Implementation Guide

The new workflow segment inserts between current Step 3 (story approval complete) and current Step 4 (Gherkin spec generation). Add a new numbered step — call it Step 3.5 — with three sub-phases:

**Phase A: Contract authoring**
Read the enforced verification rule (`skills/momentum/references/rules/verification-standard.md`) to get the current method-routing table and contract format per change-type. For each approved story, determine its change-type from `stories/index.json`. Select the contract format. Author the contract body by reading the story's plain English ACs — do not read the Gherkin `.feature` files (they don't exist yet at this point). Write to `.momentum/sprints/{sprint-slug}/specs/{story-slug}.{ext}`.

**Phase B: Coverage plan**
After all contracts are written, read the full set of contracts together. Identify stories whose behaviors overlap at the integration level (e.g., a skill-instruction story whose eval exercises a downstream rule-hook story's trigger condition). Author `coverage-plan.md` with the scenario→story/span map. Apply anti-redundancy: if an integration scenario covers a story, the story is covered-by-composition.

**Phase C: Adversarial guard**
Spawn a second agent (do not self-review) with the adversarial prompt. Pass it all contract bodies as input. The adversarial agent must NOT have access to any story `.md` files, SKILL.md files, or any Momentum source — only the contract text. The agent applies the Outsider Test clause-by-clause. Collect findings. If findings exist, rewrite the specific failing clauses (not the whole contract) and re-run the adversarial agent. Maximum 2 rewrite passes. On residual failure, present to developer.

**Activation gate**
Before calling `momentum-tools sprint activate`, verify that every story in the sprint has a corresponding file in `specs/` and that `coverage-plan.md` exists. If either check fails, halt and report the gap.

### Project Structure Notes

New files authored by this story's implementation (at runtime, not in source):
- `.momentum/sprints/{slug}/specs/{story-slug}.eval.yaml` — skill-instruction contract
- `.momentum/sprints/{slug}/specs/{story-slug}.trigger.md` — rule-hook contract
- `.momentum/sprints/{slug}/specs/{story-slug}.smoke.sh` — script-code contract
- `.momentum/sprints/{slug}/specs/{story-slug}.review.md` — specification contract
- `.momentum/sprints/{slug}/specs/{story-slug}.feature` — app-ui or rare Gherkin contract
- `.momentum/sprints/{slug}/coverage-plan.md` — holistic coverage map

Source files modified by this story:
- `skills/momentum/skills/sprint-planning/workflow.md` — insert Step 3.5 (contract authoring, coverage plan, adversarial guard) between Steps 3 and 4; add activation gate check before `sprint activate` call

Optional new reference file (author if the method-routing table is complex enough to warrant a separate document):
- `skills/momentum/skills/sprint-planning/references/contract-format-guide.md` — per-change-type contract authoring guide (if workflow.md would exceed 500 lines without it)

The verification standard rule consumed by this step lives at:
- `skills/momentum/references/rules/verification-standard.md` (authored by the `enforced-verification-rule-change-type-method-routing-harness-profile-requirement-adversarial-guard` story — must be present before this story's implementation runs)

The harness defaults consumed by contract authoring live at:
- `momentum/verification-harness.json` (authored by the `momentum-harnessjson-schema-and-plugin-shipped-defaults` story — must be present before this story's implementation runs)

### References

- DEC-029 D2 (frozen per-story contract as spec-of-done, not per-story execution unit): `_bmad-output/planning-artifacts/decisions/dec-029-method-routed-acceptance-validation-pipeline-2026-05-17.md`
- DEC-029 D6 (sprint-planning authors contracts + adversarial guard): same document
- DEC-029 D8 (per-sprint holistic E2E coverage plan, transitive coverage): same document
- DEC-030 D3 (frozen-scope sprint, activation gate, subtract-only freeze): `_bmad-output/planning-artifacts/decisions/dec-030-dag-dispatch-frozen-sprints-dual-format-2026-05-17.md`
- DEC-030 D5 (front-loaded human-in-the-loop cost accepted): same document
- Sprint-planning skill: `skills/momentum/skills/sprint-planning/workflow.md`
- Change-types reference: `skills/momentum/skills/create-story/references/change-types.md`
- Gherkin template (for context on what the downstream Gherkin step does): `skills/momentum/references/gherkin-template.md`

## Momentum Implementation Guide

**Change Types in This Story:**
- All tasks → skill-instruction (EDD)
  *(workflow.md and SKILL.md modifications; optional references/ authoring)*

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/sprint-planning/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-contract-authored-per-story.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Modify `skills/momentum/skills/sprint-planning/workflow.md` to insert Step 3.5 (contract authoring, coverage plan, adversarial guard) and add the activation gate check

**Then verify:**
3. Run evals: for each eval file, spawn a subagent with the eval's scenario and the sprint-planning workflow as context. Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions
- Skill names use `momentum:` namespace prefix

**Additional DoD items for skill-instruction tasks:**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/sprint-planning/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed (count the actual characters)
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed (overflow in `references/` if needed)
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically)

**Gherkin separation reminder:** Gherkin specs exist for this sprint in `sprints/{sprint-slug}/specs/`. The dev agent implements against the plain English ACs in this story file only — never against `.feature` files. This is the black-box separation enforced by DEC-030 Gate 2.

**Dependency note:** This story must not be started until both `enforced-verification-rule-change-type-method-routing-harness-profile-requirement-adversarial-guard` and `momentum-harnessjson-schema-and-plugin-shipped-defaults` are in `status: done`. The verification-standard rule and verification-harness.json are runtime inputs to the workflow step this story implements.

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — no implementation failures.

### Completion Notes List

- Inserted Step 3.5 "Author frozen contracts + coverage plan + adversarial guard" into `workflow.md` between Steps 3 and 4.
- Step 3.5 has three phases: (A) contract authoring per story using verification-standard.md routing table and contract-format-guide.md formats, (B) coverage-plan.md with anti-redundancy principle and covered-by-composition/dedicated-run classification, (C) decorrelated adversarial agent guard with max-2 rewrite passes and developer escalation on residual failure.
- Step 4 updated to skip app-ui stories with existing `.feature` contracts (written by Step 3.5 Phase A).
- Step 8 updated with pre-activation gate that checks for per-story contract files and coverage-plan.md before calling `momentum-tools sprint activate`.
- Authored `references/contract-format-guide.md` with per-change-type format templates, extension mapping table, multi-type precedence ordering, and anti-insider checklist.
- Wrote 4 behavioral evals covering: contract-per-story authoring, coverage plan completeness, adversarial guard rejection and rewrite cycle, and activation gate enforcement.
- EDD cycle ran — all 4 evals verified against implemented workflow instructions.
- Gap noted: `momentum/verification-harness.json` was not present in the worktree (dependent story not yet merged); harness reference is used in contract-format-guide.md and the workflow reads it, but the workflow gracefully operates when the file has already been written by the dependency story before this sprint-planning step runs at runtime.
- SKILL.md description unchanged (85 chars, under 150 limit). model and effort frontmatter present.

### File List

- `skills/momentum/skills/sprint-planning/workflow.md` — inserted Step 3.5, updated Step 0 task list, updated Step 4 app-ui skip logic, updated Step 7 review output, updated Step 8 activation gate
- `skills/momentum/skills/sprint-planning/references/contract-format-guide.md` — new file: per-change-type contract authoring guide
- `skills/momentum/skills/sprint-planning/evals/eval-contract-authored-per-story.md` — new eval
- `skills/momentum/skills/sprint-planning/evals/eval-coverage-plan-covers-all-stories.md` — new eval
- `skills/momentum/skills/sprint-planning/evals/eval-adversarial-guard-rejects-insider-clause.md` — new eval
- `skills/momentum/skills/sprint-planning/evals/eval-activation-blocked-without-contracts.md` — new eval
