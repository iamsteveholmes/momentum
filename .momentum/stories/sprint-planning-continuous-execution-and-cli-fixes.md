---
title: "sprint-planning: fix continuous execution breaks and stale CLI namespace bugs"
story_key: sprint-planning-continuous-execution-and-cli-fixes
status: ready-for-dev
epic_slug: momentum-sprint-planning-to-ready
feature_slug: momentum-sprint-planning-to-ready
story_type: defect
priority: high
change_type:
  - skill-instruction
  - script-cli
verification_method_advisory: bash
depends_on: []
touches:
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/create-story/workflow.md
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
---

# sprint-planning: fix continuous execution breaks and stale CLI namespace bugs

## Story

As a developer,
I want the sprint-planning workflow to run continuously from invocation to an activated
sprint — pausing only at its genuine decision gates — and its CLI/skill calls to resolve
correctly on the first try,
so that a sprint-planning session completes in a single continuous run without manual
re-invocation, and no call fails on a stale subcommand, an unset planning slug, or a
bare (un-namespaced) skill name.

## Description

This is a two-leg defect fix against the current sprint-planning flow, consolidating two
overlapping defects that were ruled one story at sprint-2026-07-13 planning.

**Leg A — Continuous sequential execution.** On a clean run (no errors detected), the
planning workflow must proceed through its steps without gratuitous inter-step confirmation
gates. Only the designed decision gates block for developer input: (1) story selection,
(2) per-story A/R/J approval, and (3) the plan-gate sign-off. Genuine error-condition
escalations (e.g. AVFL GATE_FAILED, contaminated contracts, an unresolvable team-composition
gap) still pause — those require a real developer decision — but informational "proceed or
revise?" confirmations between steps do not. A secondary symptom is fragility to a mid-workflow
context reset (a `/model` switch was observed to reset execution state): load-bearing state
must live in durable, tool-queryable stores so a reset resumes rather than restarts.

**Leg B — Stale CLI / namespace surfaces.** The primary live bug: the planning sprint's
`slug` is read by `momentum-tools` (`planning.get("slug", ...)` at activation and in status
readouts) but is **never settable through the CLI** — `momentum-tools sprint plan` creates the
planning entry as `{"locked": false, "status": "planning", "stories": [], "waves": []}` with no
`slug` field, and no subcommand accepts a slug. The workflow computes `{{sprint_slug}}` as a
context variable (used for every `.momentum/sprints/{{sprint_slug}}/...` path) but has no CLI
path to persist it, forcing a **direct `sprints/index.json` edit** — which both violates
sprint-manager's "sole writer of index.json" invariant and is exactly the volatile state a
`/model` switch loses (connecting Leg B back to Leg A). Two further namespace instances confirmed
in source:
- `skills/momentum/skills/create-story/workflow.md:349` invokes the **bare `avfl`** skill name at
  the AVFL checkpoint. A live `Unknown skill: avfl` tool-use error was captured in errors.jsonl at
  2026-06-29 02:33Z and recurs on every create-story run reaching that step (folded from the
  sprint-2026-06-28 retro, approved at that retro's Phase 5 gate).
- The original stub's stale `sprint-current` / `sprint-stories` CLI refs and bare skill names in
  `sprint-planning/workflow.md` are **already fixed** in the current source (verified: sprint-planning
  already uses `momentum:avfl`, and every `momentum-tools sprint <subcommand>` it calls is registered).
  Those become **regression guards**, not new fixes.

Source provenance: sprint-2026-05-16 retro handoff iq-20260518043634 (Leg A + the original CLI
refs); sprint-2026-06-28 retro (the create-story:349 instance).

## Acceptance Criteria

1. **Continuous run pauses at exactly the three designed gates.** On a clean sprint-planning run
   (dependencies satisfied, contracts clean, team composition adequate, AVFL clean), the workflow
   proceeds from invocation to `momentum-tools sprint activate` and pauses for developer input at
   exactly three points: story selection, per-story A/R/J approval, and the plan-gate sign-off.
   No other step blocks with an informational "proceed / revise?" confirmation. Verifiable by
   inspection of `skills/momentum/skills/sprint-planning/workflow.md`: every `<ask>` / halt is
   either one of the three designed gates or a **genuine blocking error-escalation** — one whose
   `<check if>` guard is a defect/failure state that actually stops the plan (e.g. AVFL
   `GATE_FAILED` at ~line 1008, contaminated contracts, an unresolvable team-composition gap).
   A `<check if>` guard alone does NOT make an ask acceptable: an ask guarded on a **non-blocking
   warning/advisory state** — one the workflow itself says "can proceed" — is a gratuitous gate and
   must be converted to a non-blocking notice. Two such gates are named for conversion:
   (i) the dependency-warning gate ("Proceed with current selection, or revise?", ~line 240), and
   (ii) the AVFL `CHECKPOINT_WARNING` gate ("Address findings now, or proceed with warnings noted?",
   ~line 998, whose own output says "the plan can proceed"). Both become notices (surface the
   warning, continue); the AVFL `GATE_FAILED` HALT (~line 1008) is kept as a genuine escalation.

2. **Load-bearing state is durable across a context reset.** The sprint slug and the selected-story
   set are persisted to durable, tool-queryable stores (`sprints/index.json` via `momentum-tools`,
   plus the TaskCreate/TaskUpdate task list) at the moment they are computed — not held only as
   workflow context variables. Verifiable: after the story-selection step runs, reading
   `sprints/index.json` returns the planning entry's `slug` (a real `sprint-YYYY-MM-DD` value, not
   absent and not `"unknown"`), so a `/model` switch or context refresh can recover it.

3. **Planning slug is settable through momentum-tools, and the workflow uses that path (no direct
   index edit).** `momentum-tools` exposes a CLI surface that sets `sprints.planning.slug`
   (e.g. `sprint plan` accepts `--slug`, or a dedicated subcommand creates/sets it). Running that
   command writes the slug into the planning entry. `sprint-planning/workflow.md` Step 2 calls this
   command to persist `{{sprint_slug}}`, and there is **no direct Write/Edit of `sprints/index.json`
   for the slug ANYWHERE in the file** — specifically, the `slug: {{sprint_slug}}` line is removed
   from the Step 8.B "edit directly" block (~line 1221), and the write goes through momentum-tools
   (sole writer of index.json). Verifiable by running the CLI (`bash`) and by grepping the **entire
   workflow file** (the grep is not scoped to Step 2) for any direct index-write of the slug — must
   find none. (The Step 8.B block's remaining direct writes of `team`/`planned` are out of scope for
   this story; `waves` is already CLI-stored. This story removes only the `slug` line.)

4. **create-story AVFL checkpoint uses the namespaced skill.** `skills/momentum/skills/create-story/workflow.md`
   invokes `momentum:avfl` (not bare `avfl`) at the AVFL checkpoint step (currently line 349). A
   create-story run that reaches the AVFL checkpoint produces zero `Unknown skill: avfl` errors.
   Verifiable: grep shows `momentum:avfl` and zero bare-`avfl` skill invocations in that file.

5. **Namespace regression guard — sprint-planning.** Every skill invocation in
   `skills/momentum/skills/sprint-planning/workflow.md` (avfl, create-story, agent-guidelines, and
   any other) uses the `momentum:` prefix. Verifiable: grep of the `<action>Invoke the \`...\` skill`
   lines shows all are namespaced; zero bare skill-invocations remain.

6. **Stale-subcommand regression guard.** Every `momentum-tools sprint <subcommand>` referenced in
   `sprint-planning/workflow.md` resolves to a subcommand registered in
   `skills/momentum/scripts/momentum-tools.py`; no `sprint-current`, `sprint-stories`, or other
   unregistered subcommand refs remain. Verifiable: the set of called subcommands is a subset of the
   registered subcommands (`sprint_sub.add_parser(...)`).

## Tasks / Subtasks

- [ ] **Task 1 — Add a CLI surface to set the planning sprint slug** (script-cli) — _AC3_
  - [ ] Extend `momentum-tools.py` so the planning sprint's `slug` is settable via the CLI. Prefer
        adding an optional `--slug` argument to the existing `sprint plan` subcommand (set
        `planning["slug"]` when supplied, idempotently), or add a dedicated subcommand if that reads
        cleaner. Keep `momentum-tools` the sole writer of `sprints/index.json`.
  - [ ] Preserve existing behavior: calls without a slug argument continue to work unchanged; a
        supplied slug never clobbers an already-activated/locked sprint.
  - [ ] Add a test to `skills/momentum/scripts/test-momentum-tools.py` proving the slug lands in
        `sprints.planning.slug` after the command runs (red → green).

- [ ] **Task 2 — Persist the sprint slug through the CLI; remove the direct index edit** (skill-instruction) — _AC2, AC3_
  - [ ] In `sprint-planning/workflow.md` Step 2, right after generating `{{sprint_slug}}` (~line 243)
        and registering stories (`momentum-tools sprint plan --operation add`), call the new CLI
        surface to persist the slug into the planning entry **early** — so it is durable for the rest
        of the run (this is what makes AC2's context-reset recovery possible).
  - [ ] Remove the `- slug: {{sprint_slug}}` line from the Step 8.B "edit directly" block at
        `sprint-planning/workflow.md:1221-1222` (`Then update .momentum/sprints/index.json planning
        section (edit directly): - slug: {{sprint_slug}}`). This is the actual live direct-index-edit
        of the slug; once the CLI (Task 1) owns slug persistence, this line must go, or AC3's
        "no direct Write/Edit of sprints/index.json for the slug" grep still fails.
        (Scope: only the `slug` line — the block's other direct writes of team/planned are out of
        scope for this story; `waves` is already noted as CLI-stored.)
  - [ ] Confirm the selected-story set and slug are reflected in durable stores (index.json +
        task list) so a mid-run context reset can recover them.

- [ ] **Task 3 — Remove gratuitous inter-step confirmation gates** (skill-instruction) — _AC1_
  - [ ] Audit every `<ask>` / halt in `sprint-planning/workflow.md`. Classify each as: a designed
        decision gate (selection / A-R-J / plan-gate), a genuine BLOCKING error-escalation (guarded
        by a `<check if>` on a defect/failure state that actually stops the plan), or a
        gratuitous/informational confirmation guarded on a non-blocking warning/advisory state.
        A `<check if>` guard alone does not make an ask acceptable — the guard must be a blocking
        defect, not a "can proceed" warning.
  - [ ] Convert the informational dependency-warning gate (`<ask>Proceed with current selection, or
        revise?`, ~line 240) into a non-blocking notice: surface the warning and continue.
  - [ ] Convert the AVFL `CHECKPOINT_WARNING` gate (`<ask>Address findings now, or proceed with
        warnings noted?`, ~line 998, inside `<check if="AVFL returns CHECKPOINT_WARNING">`) into a
        non-blocking notice: surface the findings and continue (the branch's own output already says
        "the plan can proceed"). Leave the `GATE_FAILED` HALT branch (~line 1008) unchanged — that
        is a genuine blocking escalation.
  - [ ] Add an explicit continuous-execution directive at the workflow top (e.g. a `<critical>`
        stating the workflow runs continuously and pauses only at the three designed gates plus
        genuine error-escalations), so the orchestrator does not insert its own inter-step pauses.

- [ ] **Task 4 — Fix the create-story AVFL namespace** (skill-instruction) — _AC4_
  - [ ] Change `skills/momentum/skills/create-story/workflow.md:349` from `Invoke the \`avfl\` skill`
        to `Invoke the \`momentum:avfl\` skill`.

- [ ] **Task 5 — Regression sweep: namespaces + CLI subcommands** (skill-instruction / verification) — _AC5, AC6_
  - [ ] Grep `sprint-planning/workflow.md` for every skill invocation; confirm all are `momentum:`-prefixed.
  - [ ] Grep `sprint-planning/workflow.md` for every `momentum-tools sprint <subcommand>`; confirm each
        is registered in `momentum-tools.py`; confirm no `sprint-current` / `sprint-stories` refs remain.

## Dev Notes

### Decision Authority

- **Epic:** `momentum-sprint-planning-to-ready` — "Sprint Planning — Backlog to Ready Sprint."
  Acceptance condition: a developer with populated backlog stubs invokes `momentum:sprint-planning`
  and receives an activated sprint with validated, Gherkin-specced, ready-for-dev stories — without
  manually specifying story selection criteria or review flow. A workflow that halts mid-run for
  gratuitous confirmations, or that fails on an unset slug / bare skill name, violates that
  "single continuous run" intent.
- **sprint-manager sole-writer invariant:** `momentum-tools` is the sole writer of
  `sprints/index.json` and `stories/index.json` (stated at `momentum-tools.py:8`). The slug fix must
  route through the CLI; the workflow must not edit index.json directly.
- **Verification standard:** change-type → method routing lives in
  `skills/momentum/references/rules/verification-standard.md` §1. `script-cli → bash`,
  `skill-instruction → skill-invoke`. Each change type applies its own method at verify time.

### Current State of Affected Files

- `skills/momentum/scripts/momentum-tools.py` (3127 lines) — `cmd_sprint_plan` (~line 328) creates
  the planning entry **without** a `slug` field; `cmd_sprint_activate` (~line 286) reads
  `planning.get("slug", "unknown")`. Registered `sprint` subcommands: status-transition, activate,
  complete, epic-membership, plan, ready, retro-complete, next-stories, migrate-priority,
  set-priority, story-add, story-approve, story-set-contract, compute-verification-method,
  verify-approvals, stories. **None sets the planning slug.**
- `skills/momentum/skills/sprint-planning/workflow.md` (1258 lines) — Step 2 (~line 243) generates
  `{{sprint_slug}} = sprint-YYYY-MM-DD` and registers stories via `sprint plan --operation add`
  (~line 253) but never persists the slug via CLI. Instead, the slug is written by a **direct
  `sprints/index.json` edit** in Step 8.B (~line 1221: `Then update .momentum/sprints/index.json
  planning section (edit directly): - slug: {{sprint_slug}}`) — this is the sole-writer-invariant
  violation and the volatile late-run state a `/model` switch loses (it is written only near
  activation, not when the slug is first known). Already uses `momentum:avfl` (line 977) and
  `momentum:create-story` (lines 273, 302); all called `sprint` subcommands are registered. The
  informational dependency-warning gate is at ~line 240. Line 16 already mandates TaskCreate/TaskUpdate
  for step state.
- `skills/momentum/skills/create-story/workflow.md` — line 349 invokes bare `avfl` (the AC4 fix).
- `skills/momentum/scripts/test-momentum-tools.py` — existing test harness for the CLI; add the
  slug-setter test here.

### Architecture Compliance

- The planning entry currently gets its slug only from an out-of-band index edit; routing it through
  `momentum-tools` restores the sole-writer invariant and, as a side effect, makes the slug durable
  across a `/model` switch (Leg A ↔ Leg B connection). Keep the CLI change backward-compatible: a
  slug-less call must behave as today.
- Do not broaden scope to the other `sprint-planning-*` stories in this epic
  (activation-gate, coherence-gate, story-size-heuristic, etc.) — this story is scoped to the
  continuous-execution and CLI/namespace defects only.

### Testing Requirements

- **Task 1 (script-cli → bash):** unit test in `test-momentum-tools.py` (red → green) asserting the
  slug lands in `sprints.planning.slug`; confirm no regression in the existing momentum-tools suite.
- **Tasks 2–5 (skill-instruction → skill-invoke):** behavioral evals under
  `skills/momentum/skills/sprint-planning/evals/` (dir exists — 10+ evals present) and
  `skills/momentum/skills/create-story/evals/`. Prefer an eval asserting a clean planning run pauses
  at exactly the three designed gates, and a grep-based regression check for namespaces / subcommands.
- The frozen verification contract for this sprint lives at
  `.momentum/sprints/{sprint-slug}/specs/sprint-planning-continuous-execution-and-cli-fixes.{ext}`.
  Dev reads the Part-A header (how_dev_self_checks, verification_method, harness_profile) as a
  self-check before signaling done; Dev never reads the verifier body (Part B) beyond sections
  named by how_dev_self_checks.

### Project Context Reference

- `momentum:sprint-planning` is the ignition for every sprint cycle; a broken continuous run blocks
  reliable sprint execution. `momentum:create-story` reaches the AVFL checkpoint on every run, so the
  bare-`avfl` bug recurs until fixed.

### References

- Epic context: `momentum-sprint-planning-to-ready` (from _bmad-output/planning-artifacts/epics.json)
- Absorbs `sprint-planning-enforce-continuous-sequential-execution` (merged at sprint-2026-07-13
  planning; overlapping scope ruled one story; stub dropped). This story's Leg A covers that stub's
  entire scope (continuous sequential execution without inter-step confirmation gates).
- Provenance: sprint-2026-05-16 retro handoff iq-20260518043634 (Leg A + original CLI refs);
  sprint-2026-06-28 retro Phase 5 gate (create-story:349 bare-`avfl`, live `Unknown skill: avfl`
  captured 2026-06-29 02:33Z).
- Verification routing: `skills/momentum/references/rules/verification-standard.md` §1.

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → script-cli (bash / TDD via bmad-dev-story)
- Tasks 2, 3, 4, 5 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for workflow.md files.** Skill instructions are non-deterministic LLM prompts —
unit tests do not apply. Use EDD:

**Before writing changes to the skill:**
1. Write/extend behavioral evals in the affected skill's `evals/` dir
   (`skills/momentum/skills/sprint-planning/evals/` and `skills/momentum/skills/create-story/evals/`
   both exist):
   - One `.md` file per eval, named descriptively (e.g.,
     `eval-clean-run-pauses-at-three-designed-gates.md`,
     `eval-avfl-checkpoint-uses-momentum-namespace.md`).
   - Format each as: "Given [input and context], the skill should [observable behavior]."
   - Test behaviors and decisions (does the run stop only at the three gates? is the invocation
     namespaced?), not exact output text.

**Then implement:**
2. Modify `sprint-planning/workflow.md` (Tasks 2, 3, 5) and `create-story/workflow.md` (Task 4).

**Then verify:**
3. Run evals: spawn a subagent per eval, give it the eval scenario plus the skill's SKILL.md +
   workflow.md as context, and observe whether behavior matches.
4. All match → task complete. Any fail → diagnose the instruction gap, revise, re-run (max 3 cycles).

**NFR compliance (every skill-instruction task):**
- SKILL.md `description` ≤ 150 chars (count precisely) — unchanged here, but re-confirm if touched.
- `model:` and `effort:` frontmatter present.
- workflow.md / SKILL.md body ≤ 500 lines / 5000 tokens; overflow → `references/`.
- Skill names use the `momentum:` namespace prefix (NFR12) — this is the crux of AC4/AC5.

**Additional DoD (skill-instruction):**
- [ ] Behavioral evals written/extended in the affected `evals/` dirs.
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented).
- [ ] Namespace grep clean: zero bare skill invocations in the two workflow files.
- [ ] Subcommand grep clean: every `momentum-tools sprint <subcommand>` referenced is registered.
- [ ] AVFL checkpoint on the produced artifact documented (momentum:dev runs it automatically).

---

### script-cli Task: TDD via bmad-dev-story (bash verification)

`momentum-tools.py` is a user-facing CLI; the slug-setter is verified by running the command
(`bash` method per verification-standard §1). bmad-dev-story handles TDD natively:

1. **Red:** add a failing test in `test-momentum-tools.py` asserting `sprints.planning.slug` is set
   by the new CLI surface. Confirm it fails first.
2. **Green:** implement the minimum change in `cmd_sprint_plan` (or a new subcommand) to set the slug.
3. **Refactor:** keep the change backward-compatible (slug-less calls unchanged; locked sprints not
   clobbered) and keep momentum-tools the sole writer of index.json.

**Additional DoD (script-cli):**
- [ ] New test written and passing; existing momentum-tools suite still green (no regressions).
- [ ] CLI run demonstrably sets `sprints.planning.slug` (bash verification).
- [ ] No direct `sprints/index.json` writes introduced anywhere outside momentum-tools.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
