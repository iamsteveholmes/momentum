---
title: sprint-planning goal_conditions declaration + plan-gate leads with the capability fork
story_key: sprint-planning-goal-conditions-declaration-plan-gate-leads
status: ready-for-dev
epic_slug: momentum-sprint-planning-to-ready
feature_slug:
story_type: practice
priority: high
change_type:
  - skill-instruction
  - script-cli
verification_method_advisory: bash
depends_on: []
touches:
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/sprint-planning/references/plan-gate-renderer.md
  - skills/momentum/skills/sprint-planning/references/build-handoff-template.md
  - skills/momentum/skills/sprint-planning/evals/
  - skills/momentum/scripts/momentum-tools.py
---

# sprint-planning goal_conditions declaration + plan-gate leads with the capability fork

## Story

As a developer,
I want sprint planning to declare `goal_conditions` on the sprint record and have the plan gate's first fork be a plain-language capability sign-off,
so that a plan gate review can never again pass without anyone saying out loud what capability (if any) will actually change for the GM this sprint.

## Description

Sprint planning gains a goal-condition declaration step and the plan gate gains a capability
sign-off card that leads every other fork.

**Declaration.** Right after story selection and before contracts freeze, sprint planning asks the
developer to name the sprint's `goal_conditions` — 0..n feature slugs read from
`.momentum/features.json` whose acceptance conditions this sprint intends to flip from failing to
passing. A sprint with no feature-shaped goal (bug-fix or configuration work) declares an explicit
verified-fix list in the `goal` field instead. Both land on the planning sprint record.

**Plan gate.** The gate's FIRST decision card becomes a plain-language capability sign-off:
"After this sprint a GM will be able to ___ — approve / change / reject." It renders ahead of
coherence forks and every other fork, appears even when the plan has zero other forks, is never
dropped by the seven-fork cap, and counts toward the gate's anti-rubber-stamp requirement so the
plan cannot be approved without a written verdict on it. The purpose hero leads with the same
statement, so the first thing a reader sees is what will be different in the app.

**Why the CLI is in scope.** `.momentum/sprints/index.json` is a protected path whose sole writer
is `momentum-tools sprint` (architecture Read/Write Authority table; Protection Boundaries list) —
direct edits by any other agent are blocked. `momentum-tools sprint plan` today accepts only
`--operation`, `--stories`, `--wave`, and `--slug`; there is no path by which any skill can persist
a `goal` or `goal_conditions`. That gap is why the build-handoff template still carries a
`Sprint goal not captured at planning` fallback for a field DEC-039 D1 declared weeks ago.
This story closes it by extending the existing command, not by adding a new one.

**Read-only on the registry.** This story consumes `.momentum/features.json`; it never writes it.
The sole writer is `momentum-tools feature verify` (DEC-040 D1), delivered by
`momentum-tools-feature-verify-human-verdict-recorder-and` in this same sprint. Because that
registry does not exist yet, the declaration must behave correctly when the file is absent
(AC3) — this story carries no `depends_on` edge and must not acquire one.

**Cross-check during implementation.** `plan-gate-renderer-fork-id` (the ForkItem shape in
plan-gate-renderer.md §4 has no `id` field, yet workflow Step 8 and coherence-gate.md §5a both
address forks by a stable `id`) and `sprint-planning-pre-sprint-class-1-render-gate` touch the same
renderer surface. Do not resolve the ForkItem `id` gap here — it belongs to
`plan-gate-renderer-fork-id`. Add the capability fork without changing the ForkItem field set, so
neither effort conflicts with the other.

**Pain context.** Nornspun discovery: sprint-2026-07-13's plan gate asked only copy and scope
questions, and at the earlier MVP-roadmap adoption gate nobody said "nothing you can see will
change for two sprints" out loud. The developer
relies on the sprint goal as the ultimate requirement, and the gate never asked it. Ten sprints
produced zero of fifteen features.

## Acceptance Criteria

1. **Goal conditions are declared at planning time.** After story selection and before contracts
   are frozen, sprint planning asks the developer to name this sprint's goal conditions. It reads
   `.momentum/features.json` and shows each candidate feature's slug, name, and acceptance
   condition in plain language, then accepts a selection of zero or more slugs. Sprint planning
   never writes `.momentum/features.json`.

2. **Zero conditions means a maintenance sprint with a named fix list.** When the developer
   declares no goal conditions, sprint planning requires a verified-fix list in the sprint `goal`
   instead — each entry phrased as something a human can confirm in the running app. It refuses to
   advance when both the conditions list and the goal are empty.

3. **A missing registry routes to the maintenance path, never to a skip.** When
   `.momentum/features.json` does not exist or lists no features, sprint planning says so in one
   plain line and continues on the maintenance path from AC2. The declaration step is never
   silently skipped and never blocks the run.

4. **The declaration is persisted durably through the CLI.** The declared conditions and goal land
   on the planning sprint record as `goal_conditions` and `goal` by way of a `momentum-tools`
   command — never a direct edit of `.momentum/sprints/index.json`. After the command returns, both
   values read back from the record, so a context reset mid-run recovers them rather than losing
   them.

5. **`momentum-tools sprint plan` accepts the declaration.** The command takes `--goal` and
   `--goal-conditions` (comma-separated slugs, empty string allowed for a maintenance sprint),
   writes both onto the planning record, is idempotent when called again with the same values, and
   refuses on a locked sprint exactly as the existing flags do. Sprint activation carries both
   fields onto the active sprint record unchanged.

6. **The plan gate's first decision card is the capability sign-off.** Ahead of coherence forks and
   every other fork, the gate renders one card asking "After this sprint a GM will be able to ___",
   filled from the declared conditions in the developer's own plain language, carrying what is at
   stake, why it matters, the evidence behind it, a recommendation, and the three options approve,
   change, and reject. This card renders even when the plan has zero other forks, and the
   seven-fork cap never drops it.

7. **The gate cannot be approved without a written capability verdict.** The capability card counts
   toward the gate's anti-rubber-stamp requirement: the pasted sign-off block must carry a verdict
   line with written reasoning that names the capability being accepted or amended. A bare
   approval, a single-character verdict, or a blanket "approve all" is rejected with an
   explanation — non-empty alone does not satisfy this criterion.

8. **The purpose hero leads with the capability statement.** The first thing a reader sees in the
   rendered gate is what will be different in the app after this sprint, worded consistently with
   the capability card rather than restated differently.

9. **Change and reject have real effects.** Choosing change returns the developer to the
   goal-condition declaration and re-renders the gate from the amended conditions. Choosing reject
   stops the run without activating the sprint, with the reason recorded.

10. **The build handoff carries the declaration.** The handoff artifact's sprint-goal section
    renders the captured goal and lists the declared goal conditions beneath it. The
    `Sprint goal not captured at planning` fallback fires only when the developer genuinely
    declined to declare one.

## Tasks / Subtasks

- [ ] **Task 1 — Write behavioral evals first (EDD).** Add evals under
      `skills/momentum/skills/sprint-planning/evals/` covering: a feature-backed declaration
      (AC1), a maintenance sprint with zero conditions (AC2), an absent `features.json`
      (AC3), the capability card rendering first on a zero-other-fork plan (AC6), and a bare
      approval being rejected (AC7). One `.md` file per eval, behavioral phrasing only.
      *(ACs 1, 2, 3, 6, 7)*

- [ ] **Task 2 — Add `--goal` and `--goal-conditions` to `momentum-tools sprint plan`.** Extend
      `cmd_sprint_plan` and its argparse block in `skills/momentum/scripts/momentum-tools.py`
      (function at line 328; parser at line 2843). Follow the existing `--slug` pattern: optional,
      idempotent, applied before the locked-sprint guard's write. Parse `--goal-conditions` as a
      comma-separated slug list, normalizing an empty or omitted value to `[]`. Include both in the
      command's JSON result. *(ACs 4, 5)*

- [ ] **Task 3 — Add the goal-condition declaration to sprint-planning Step 2.** In
      `skills/momentum/skills/sprint-planning/workflow.md`, after the `momentum-tools sprint plan
      --operation add` call that persists the slug, add the declaration exchange: read
      `.momentum/features.json` read-only, present candidates, accept the selection, handle the
      absent-registry and zero-condition paths, then persist via the Task 2 flags. Store
      `{{goal}}` and `{{goal_conditions}}` for later steps. *(ACs 1, 2, 3, 4)*

- [ ] **Task 4 — Specify the capability fork in the renderer contract.** In
      `skills/momentum/skills/sprint-planning/references/plan-gate-renderer.md`, add the capability
      fork to §4 as a mandatory always-present fork that is prepended ahead of coherence forks and
      is exempt from the seven-fork cap, and extend §5.1 so the purpose hero's `.big` line states
      the declared capability. Do not alter the ForkItem field set. *(ACs 6, 8)*

- [ ] **Task 5 — Build and render the capability fork in Step 7.** In workflow.md Step 7 Phase A,
      construct the capability ForkItem from `{{goal_conditions}}` and `{{goal}}` and place it at
      the head of `{{genuine_forks}}` before coherence forks are prepended. In Phase B, ensure it
      renders as the first decision card and that `FORK_COUNT` includes it so the anti-rubber-stamp
      JS and the pasted-block validation both require its verdict. *(ACs 6, 7, 8)*

- [ ] **Task 6 — Wire change and reject into Step 7's decision branches.** Map the capability
      card's change option onto a return to the Task 3 declaration followed by a full gate
      re-render through the existing `PLAN_GATE_SURFACE` reload path, and its reject option onto a
      halt that records the reason and does not proceed to Step 8. *(AC 9)*

- [ ] **Task 7 — Surface the declaration in the build handoff.** In
      `skills/momentum/skills/sprint-planning/references/build-handoff-template.md`, add the
      declared goal conditions beneath `{{goal}}` in the Sprint Goal section, add the field to the
      data-source table, and give it a fallback line for the empty case alongside the existing
      goal fallback. *(AC 10)*

- [ ] **Task 8 — Run the EDD cycle.** Execute the Task 1 evals against the modified skill, revise
      the instructions where behavior diverges, and re-run (maximum three cycles). Document results
      in the Dev Agent Record. *(ACs 1, 2, 3, 6, 7)*

## Dev Notes

### Decision Authority

`_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md` is the
source of truth for this story.

- **D1** establishes `.momentum/features.json` as a standalone acceptance-testing registry with
  exactly three integration seams. This story is seam one: "sprint planning declares
  `goal_conditions` (0..n feature slugs whose acceptance conditions this sprint intends to flip;
  maintenance sprints declare a verified-fix list instead)". The registry schema is D1's authority —
  consume it, do not define it.
- **D3** ties closure to the declaration: "The sprint goal (DEC-039 D1) binds to `goal_conditions`;
  closure requires a human verdict per condition against a correctly-paired build." Closure itself
  is a separate story; this story only produces the conditions closure will key against.
- `_bmad-output/planning-artifacts/architecture.md` line 1627 already documents the field:
  sprint-record entries carry `goal_conditions`, an array of 0..n feature slugs; "The plan gate's
  first fork presents them in plain language ('after this sprint a GM will be able to ___ —
  approve/change/reject')." Verify implementation against that paragraph; do not re-derive the
  schema. The schema example at line 1641 shows the shape:
  `"goal_conditions": ["session-capture", "campaign-identity"]`.

### Current State of Affected Files

- **`skills/momentum/scripts/momentum-tools.py`** — `cmd_sprint_plan` (line 328) creates the
  planning entry with `{"locked": False, "status": "planning", "stories": [], "waves": []}`, applies
  an optional `--slug`, then adds or removes stories. The word "goal" does not appear anywhere in
  the file. The argparse block (line 2843) declares four flags. `cmd_sprint_activate` (line 260)
  moves the entire `planning` dict onto `active` wholesale, so any new field carries over with no
  extra work — AC5's activation clause needs verification, not new code.
- **`skills/momentum/skills/sprint-planning/workflow.md`** (1442 lines) — Step 2 ends at line 279
  after the `sprint plan --operation add` persistence call and its durability confirmation. No step
  in the workflow captures a sprint goal today; the only mention of `{{goal}}` is at lines 1413–1416
  where Step 8 assembles the build handoff.
- **`skills/momentum/skills/sprint-planning/references/plan-gate-renderer.md`** (484 lines) — §4
  lists seven genuine-fork triggers, all conditional on detection; none is unconditional. Coherence
  forks are the only ones with prepend-and-exempt treatment. The ForkItem shape (§4, lines 210–219)
  has seven fields and no `id`. §5.1 defines the purpose hero's four parts.
- **`skills/momentum/skills/sprint-planning/references/build-handoff-template.md`** (114 lines) —
  `## Sprint Goal` renders `{{goal}}`; the fallback table maps a null goal to
  `Sprint goal not captured at planning`; the data-source table sources it from `active.goal`.
- **`.momentum/sprints/index.json`** — the current `planning` entry has keys
  `locked, status, stories, waves, slug`. Neither `goal` nor `goal_conditions` is present.

### Architecture Compliance

- **Protected path.** `.momentum/sprints/index.json` is on the Protection Boundaries list
  (architecture.md line 1388): "sole writer is `momentum-tools.py sprint`. Direct edits by any
  other agent are blocked." Every write in this story goes through the CLI. A skill instruction
  that tells an agent to edit the file directly is a defect, not a shortcut.
- **Registry write authority.** `momentum-tools feature verify` is the sole writer of
  `.momentum/features.json` (architecture.md line 1351). Sprint planning appears there as a
  read-only consumer. Preserve that.
- **Presentation standard.** The plan gate is a companion decision surface under
  `~/.claude/rules/decision-grade-presentation.md` §2.2 row 9 and §5.1. The capability card must
  carry what, why it matters, and evidence inline — the self-sufficiency floor (§3) makes each of
  those a required field, and §4 makes the floor win over the seven-fork cap, which is the basis for
  AC6's cap exemption. Coherence forks already use this exact exemption; follow that precedent.
- **Two-tier gate.** Architecture.md line 3189 separates the merge gate from sprint closure.
  This story serves tier 2 only — it produces the conditions, and never asserts a verdict against
  them.

### Testing Requirements

Per `skills/momentum/references/rules/verification-standard.md` §1, `skill-instruction` routes to
`skill-invoke` and `script-cli` routes to `bash`, and a story carrying both "applies each type's
required method to the task(s) of that type." Both methods therefore apply here: the skill tasks
are verified by invoking sprint-planning, the CLI task by running the command. The frontmatter
advisory reads `bash` because that is what `momentum-tools sprint compute-verification-method`
derives from this story's `change_type` — the advisory records the computed routing rather than
contradicting it, and does not narrow the skill-side verification below.

- **Skill instructions** use EDD, not TDD — the evals in Task 1 are written before the workflow
  edits and re-run after (Task 8).
- **CLI flags** are verified by invoking `momentum-tools sprint plan` with a feature-backed
  conditions list, with an empty conditions list, twice with identical values (idempotence), and
  against a locked sprint (refusal), reading the record back each time.
- The frozen verification contract for this sprint lives at
  `.momentum/sprints/sprint-2026-08-03/specs/{story-slug}.{ext}`. Read the Part-A header
  (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before
  signaling done. Do not read the Part-B verifier body beyond what `how_dev_self_checks`
  explicitly references.

### Implementation Guide

Notes specific to this story, beyond the change-type guidance below:

- **Do not create `.momentum/features.json`.** It is absent today and is delivered by
  `momentum-tools-feature-verify-human-verdict-recorder-and` in this sprint. AC3 exists precisely
  so this story ships working while the registry is still missing. Creating a placeholder registry
  would silently claim D1's schema authority.
- **Declare, do not validate.** Nothing here checks that a declared slug exists in the registry or
  that its status is `failing`. D1 makes `epic_slugs` and similar links explicitly "never validated,
  never blocking"; the declaration is a statement of intent, and closure is where reality is
  checked.
- **Keep the ForkItem shape untouched.** Adding a field would collide with
  `plan-gate-renderer-fork-id`. If that story lands first and adds `id`, the capability fork's
  natural id is the literal `capability` — but do not add the field as part of this story.
- **Reuse the existing re-render path.** Step 7's M-branch already re-synthesizes Phase A,
  re-renders Phase B, and reloads through the stored `PLAN_GATE_SURFACE` ref rather than calling
  `cmux browser new` again. AC9's change path routes through that machinery; do not add a second
  render path.

### Project Structure Notes

All skill files live under `skills/momentum/skills/sprint-planning/` (SKILL.md, workflow.md,
`references/`, `evals/`). The CLI lives at `skills/momentum/scripts/momentum-tools.py` and is
exposed through the `skills/momentum/bin/momentum-tools` wrapper that
`/Users/steve/.local/bin/momentum-tools` resolves to — editing the script is sufficient; the
wrapper needs no change. Runtime state under `.momentum/` is written only through the CLI.

### Project Context Reference

Two other stories in `sprint-2026-08-03` touch adjacent surfaces, and the seams between them are
clean as scoped:

- `momentum-tools-feature-verify-human-verdict-recorder-and` owns `momentum-tools feature verify`
  and the `.momentum/features.json` schema. Its story file names sprint-planning's
  `goal_conditions` declaration as an explicitly out-of-scope read-only downstream consumer.
- `sprint-closure-refusal-recorded-human-verdicts-per-goal` owns `momentum-tools sprint complete`
  and reads the `goal_conditions` this story writes. No CLI subcommand overlap: this story extends
  `sprint plan`, that one extends `sprint complete`.

### References

- Source decision: `_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md` — D1 (features registry, three seams), D2 (two-tier gate), D3 (closure refusal)
- Sprint tracking schema: `_bmad-output/planning-artifacts/architecture.md` lines 1627 and 1641 (`goal_conditions` field and schema example)
- Write authority and protection: `_bmad-output/planning-artifacts/architecture.md` lines 1350, 1351, 1388
- Two-tier gate: `_bmad-output/planning-artifacts/architecture.md` line 3189
- Verification routing: `skills/momentum/references/rules/verification-standard.md` §1
- Presentation standard: `~/.claude/rules/decision-grade-presentation.md` §2.2 row 9, §3 (self-sufficiency floor), §4 (caps-vs-floor), §5.1 (presentation form)
- Renderer contract: `skills/momentum/skills/sprint-planning/references/plan-gate-renderer.md` §4 (fork detection and ForkItem shape), §5.1 (purpose hero), §5.5 (decision cards)
- Coherence fork precedent: `skills/momentum/skills/sprint-planning/references/coherence-gate.md` §5a
- Discovery receipt: memory `project_nornspun_delivery_discovery` — 10 sprints, 0 of 15 features
- Epic context: `momentum-sprint-planning-to-ready` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 3, 4, 5, 6, 7, 8 → skill-instruction (EDD)
- Task 2 → script-cli (TDD via bash verification)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write behavioral evals in `skills/momentum/skills/sprint-planning/evals/` (the directory already exists and holds 33 evals — follow their format):
   - One `.md` file per eval, named descriptively (e.g., `eval-goal-conditions-declared-before-contracts.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Modify `workflow.md`, `references/plan-gate-renderer.md`, and `references/build-handoff-template.md`

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it the eval's scenario as its task and load the skill by passing the SKILL.md and workflow.md contents as context. Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to the developer if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3)
- Skill names use `momentum:` namespace prefix (NFR12)

**Note on NFR3 for this story:** `workflow.md` is already 1442 lines. The 500-line ceiling governs SKILL.md, not workflow.md, and sprint-planning already pushes depth into `references/`. Follow that pattern — the renderer contract for the capability fork belongs in `plan-gate-renderer.md`, not inlined into the workflow step.

**Additional DoD items for skill-instruction tasks:**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/sprint-planning/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed — N/A for this story: no SKILL.md edits
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed — N/A for this story: no SKILL.md edits
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically)

---

### script-cli Tasks: TDD via bmad-dev-story

Note: `change-types.md` defines no dedicated `script-cli` injection template; the `script-code`
TDD discipline is adapted here.

The CLI change uses standard TDD (red-green-refactor). bmad-dev-story handles TDD natively:

1. **Red:** Write a failing check for `--goal` / `--goal-conditions` persistence first. Confirm it fails before implementing.
2. **Green:** Implement the minimum change to `cmd_sprint_plan` and its argparse block to make it pass.
3. **Refactor:** Improve structure while keeping the check green.

**Verification runs (AC5), reading the record back after each:**
- `--goal-conditions "slug-a,slug-b"` with a goal → both persist
- `--goal-conditions ""` with a verified-fix goal → conditions persist as `[]`
- The same call twice → idempotent, no duplication
- Against a locked sprint → refuses, matching the existing `--slug` behavior
- `momentum-tools sprint activate` afterward → both fields present on `active`

**DoD items for script-cli tasks:**
- Verification runs above executed and output recorded
- No regressions in existing `sprint plan` behavior (`--operation`, `--stories`, `--wave`, `--slug`)
- JSON result shape remains parseable by existing callers

---

### Frozen contract reminder

A frozen verification contract exists for this sprint at
`.momentum/sprints/sprint-2026-08-03/specs/sprint-planning-goal-conditions-declaration-plan-gate-leads.{ext}`.
Read the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a
self-check before signaling done. Never read the Part-B verifier body — scenarios, assertion
scripts, Gherkin — beyond the sections `how_dev_self_checks` explicitly references.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
