---
title: Sprint closure refusal — recorded human verdicts per goal_conditions, honest FAILED terminal state
story_key: sprint-closure-refusal-recorded-human-verdicts-per-goal
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: practice
priority: high
change_type:
  - script-code
  - skill-instruction
verification_method_advisory: bash
depends_on:
  - momentum-tools-feature-verify-human-verdict-recorder-and
  - sprint-planning-goal-conditions-declaration-plan-gate-leads
  - conduct-merge-gate-completes-by-executing-merge-push-story
touches:
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
  - skills/momentum/skills/conductor/workflow.md
  - skills/momentum/skills/conductor/evals/eval-phase5-completes-sprint-for-retro-pickup.md
  - skills/momentum/skills/retro/workflow.md
  - skills/momentum/skills/sprint-dev/workflow.md
  - skills/momentum/references/sprint-tracking-schema.md
---

# Sprint closure refusal — recorded human verdicts per goal_conditions, honest FAILED terminal state

## Story

As a developer,
I want `momentum-tools sprint complete` to refuse closing a sprint unless every entry in the sprint record's `goal_conditions` carries a recorded human PASS/FAIL verdict, and for an honest FAILED terminal sprint state to exist alongside `done`,
so that sprints can never close on an unverified outcome, goal-critical work can't be silently punted without an explicit recorded decision, and maintenance sprints get an equivalent verified-fix confirmation gate.

## Description

This story builds **tier 2 of the DEC-040 D2/D3 two-tier gate**: sprint closure. Today
`cmd_sprint_complete` (`skills/momentum/scripts/momentum-tools.py:290`) closes any active sprint
unconditionally — it stamps `status: "done"`, appends the record to `completed[]`, and returns
success. Nothing anywhere asks whether the sprint's goal actually works. This story turns that
function into a gate: closure **refuses** unless every entry in the sprint record's
`goal_conditions` carries a recorded human PASS/FAIL verdict against a paired build, and adds
**FAILED** as an honest terminal sprint state alongside `done`.

**The three seams this story sits on.** This is the *consumer* side of two producers landing in
the same sprint, plus the tier-1 counterpart it must not overlap with:

| Seam | Producer (sibling story) | What this story consumes / assumes |
|---|---|---|
| Verdict record | `momentum-tools-feature-verify-human-verdict-recorder-and` | `momentum-tools feature verify` is the **sole writer** of `.momentum/features.json`, stamping `status` (`absent \| failing \| passing`) and `last_verified {date, build SHAs, verdict}` per feature slug. This story **reads that file only** — it never writes feature status by any path. |
| Condition declaration | `sprint-planning-goal-conditions-declaration-plan-gate-leads` | Sprint records gain `goal_conditions` — an array of 0..n feature slugs declared at planning and written by `momentum-tools sprint plan --goal-conditions`. This story keys its refusal off that array. **Neither `goal` nor `goal_conditions` exists on a sprint record today** — the `sprint-2026-08-03` planning record has only `locked, slug, status, stories, waves`. Treat a missing key exactly as `null`. |
| Tier-1 / tier-2 split | `conduct-merge-gate-completes-by-executing-merge-push-story` | That story makes the **merge gate** ("is this code something we are comfortable keeping on trunk?") complete only by executing merge + push + story status transitions. This story owns everything *after* that line: closure is a separate decision, possibly days later. Tier 2 is meaningless until tier 1 stops bundling the two questions. |

**What changes at the closure call site.** `skills/momentum/skills/conductor/workflow.md:2618-2622`
currently runs `momentum-tools sprint complete` inside the merge-approve branch, immediately after
the `git merge` (line 2599) and the per-story terminal status transitions (lines 2604–2617) — one
approval firing both gates. That is the exact bundling DEC-040 D2 dissolves. Tier 1 ends at the
executed merge and status transitions;
closure becomes its own invocation that only succeeds when the gate passes. When the refusal fires,
the sprint stays `active` and the Conductor reports closure-pending. (The *resume card* that carries
that pending question into the next session is DEC-040 D5 and belongs to a separate story — this
story emits the pending state, not the card.)

**Retro pickup must survive both outcomes.** `momentum:retro` Step 1 keys on sprints in
`completed[]` with `retro_run_at: null`. A FAILED sprint is a closed sprint that needs a retro more
than a passing one does, so FAILED records land in `completed[]` with the same shape.

Source: DEC-040 D3 (`_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`),
completing DEC-039; architecture Decision 59 (Two-tier gate) and the Sprint `goal_conditions` field
paragraph already document the target schema — implement against it rather than re-deriving it.

**Pain context:** Nornspun discovery — the punt was institutionalized. The end-gate's own
recommendation for a broken keystone capability (2-of-7 reliability) was approve-and-defer; the
recommended hardening story was never created; no sprint ever closed on an outcome question. Ten
sprints, 91 done stories, 0 of 15 features verifiably working.

**Source:** triage — decision:DEC-040

## Acceptance Criteria

**Terminology used below.** "No conditions declared" means `goal_conditions` is a missing key, `null`,
or `[]` — the three are equivalent for every gate in this story, and a missing key is never treated
differently from `null`. A condition is **verified-PASS**, **recorded-FAIL**, or **unverified**; those
three states are exhaustive and mutually exclusive, and each AC below says which it governs.

1. **Closure refuses on an unverified condition.** When the active sprint declares conditions and any
   named feature slug is unverified, `momentum-tools sprint complete` refuses: it exits non-zero,
   leaves `active` untouched, appends nothing to `completed[]`, and its JSON output names every
   blocking condition with a machine-readable reason drawn from a single closed set —
   `missing-entry`, `no-verdict`, `no-build-shas`. A condition carrying a complete recorded FAIL is
   **not** reported here; it is `recorded-FAIL` and routes to AC 3.

2. **Verdict admissibility is explicit.** A condition is **verified-PASS** only when its
   `.momentum/features.json` entry has `status: "passing"` and a `last_verified` block carrying a
   verdict value and both paired build SHAs. It is **recorded-FAIL** when the entry carries a
   complete `last_verified` block (verdict plus both build SHAs) whose verdict is FAIL. Everything
   else is **unverified**, and every case maps to exactly one reason token: absent from the registry
   (`missing-entry`); `status: "absent"` (`missing-entry` — the slug is registered but has never been
   assessed, which is the same absence of evidence); `last_verified: null` (`no-verdict`); a verdict
   recorded without both build SHAs (`no-build-shas`). No state is ever treated as an implicit pass.

3. **A recorded FAIL blocks `done` but not closure itself.** When no condition is unverified and at
   least one is recorded-FAIL, closing as `done` is refused with a message naming the failing
   conditions, and the refusal states that FAILED closure is the available honest exit.

4. **FAILED is a real terminal state.** `momentum-tools sprint complete --verdict failed --reason "<text>"`
   closes the active sprint with `status: "failed"`, stamps the completion date, and requires a
   non-empty `--reason`. Invoking it without `--reason` is refused. FAILED closure succeeds even
   when conditions are unverified — that is the point of an honest terminal state — and records
   which conditions were unverified at the time. FAILED closure bypasses the verdict requirement in
   AC 1–3 **only**; it does not bypass AC 7, whose punt-decision requirement applies to `done` and
   `failed` closures alike.

5. **Retro pickup is identical for both terminal states.** A FAILED sprint is appended to
   `completed[]` with `retro_run_at: null`, exactly like a `done` sprint, so `momentum:retro`
   Step 1 discovers it without change. `--verdict done` (or no `--verdict` flag) remains the
   default path and still produces `status: "done"`.

6. **Maintenance sprints get an equivalent gate.** When no conditions are declared, the sprint's
   verified-fix list is the gate instead. That list lives as free text inside the sprint record's
   existing `goal` string — the sibling planning story writes no separate structured field, so this
   story must not assume one. Closure enumerates the fix list by splitting `goal` on its line breaks
   and taking the entries after the fix-list lead-in, echoes the parsed entries in its output so a
   mis-parse is visible rather than silent, and requires one repeatable
   `--fix-confirmed "<entry text or 1-based index>"` per enumerated entry, together with
   `--build <backendSha>:<clientSha>`. It refuses while any enumerated entry is unconfirmed, naming
   the unconfirmed entries. Confirmations are written onto the closing sprint record.

7. **Punting goal-critical work requires a recorded decision.** When the sprint closes — as `done`
   **or** as `failed` — while any of its stories sits at a non-`done` terminal status
   (`closed-incomplete` or `dropped`) and at least one declared condition is not verified-PASS,
   closure requires `--punt-decision <ref>` naming a decision document under
   `_bmad-output/planning-artifacts/decisions/`. Closure refuses when the flag is absent or when the
   referenced document does not exist on disk. The reference is recorded on the closing sprint record.

8. **The closed record tells the truth about the outcome.** Every successful closure — `done` or
   `failed` — writes onto the sprint record a closure block containing: the closure verdict, the
   per-condition verdict snapshot (slug, status, verdict, build SHAs, or an explicit "no verdict
   recorded"), any maintenance fix confirmations, the FAILED reason when present, and the punt
   decision reference when present.

9. **A sprint with no declared outcome cannot close silently.** When no conditions are declared and
   the `goal` carries no verified-fix list, `done` closure is refused with a message that states
   both available exits: declare the sprint's conditions, or close FAILED with a reason. No path
   closes such a sprint as `done` without a declaration.

10. **Existing no-active behavior is unchanged.** With no active sprint, `momentum-tools sprint complete`
    still exits non-zero with "No active sprint to complete". The Conductor's and retro's documented
    idempotent-resume convention (treat that response as an expected no-op) continues to hold for
    both `done` and `failed` closures.

11. **The Conductor stops closing the sprint at merge time.** `skills/momentum/skills/conductor/workflow.md`
    no longer calls `momentum-tools sprint complete` as part of the tier-1 merge-approve sequence.
    Closure is a separate tier-2 step that invokes the gate; when the gate refuses, the sprint remains
    `active`, the Conductor surfaces the refusal's named unverified conditions in plain language, and
    the build ends in a closure-pending state rather than reporting the sprint done.

12. **Every caller and reference reflects the two-tier reality.** `momentum:retro`'s closure step,
    `momentum:sprint-dev`'s Phase 7 closure call, the conductor eval
    `eval-phase5-completes-sprint-for-retro-pickup.md` (which currently asserts Phase 5 calls
    `sprint complete`), and `skills/momentum/references/sprint-tracking-schema.md` (whose Sprint
    Record Fields table lists `status` as `planning | active | done`) are each updated so no artifact
    still describes closure as automatic or `failed` as an impossible status.

## Tasks / Subtasks

- [ ] **Task 1 — Read the verdict registry (AC 1, 2)**
  Add a read-only helper in `skills/momentum/scripts/momentum-tools.py` that resolves
  `.momentum/features.json` and classifies one feature slug into exactly one of AC 2's three states —
  `verified-PASS`, `recorded-FAIL`, or unverified with one of the three closed-set reasons
  (`missing-entry` / `no-verdict` / `no-build-shas`) — returning the entry's status, verdict, and
  build SHAs alongside. Use the same three reason tokens AC 1 emits; do not introduce a fourth.
  This helper never writes — the `momentum-tools feature verify` command from the sibling story is
  the sole writer.

- [ ] **Task 2 — Gate `cmd_sprint_complete` on goal_conditions (AC 1, 2, 3, 9)**
  Rewrite `cmd_sprint_complete` (currently `momentum-tools.py:290`) so the unconditional
  `status = "done"` path runs only after the gate passes. Evaluate every `goal_conditions` entry via
  Task 1's helper; on any unverified or FAIL condition, `error_result` with the per-condition
  breakdown and mutate nothing. Handle the undeclared-outcome case (both `goal_conditions` and the
  verified-fix list absent) with its own actionable refusal message.

- [ ] **Task 3 — Add the FAILED terminal state (AC 4, 5)**
  Add `--verdict {done,failed}` (default `done`) and `--reason` to the `complete` subparser at
  `momentum-tools.py:2833`. The `failed` path bypasses the PASS requirement, requires a non-empty
  `--reason`, sets `status: "failed"`, and otherwise follows the existing append-to-`completed[]`
  path including `retro_run_at: None` so retro discovery is untouched.

- [ ] **Task 4 — Maintenance-sprint verified-fix confirmations (AC 6)**
  Add repeatable `--fix-confirmed` and `--build` flags. When no conditions are declared, parse the
  verified-fix entries out of the sprint record's `goal` string, echo them, and require one
  confirmation per entry, refusing while any is unconfirmed.
  **Seam note — read this before designing the parser.** The producer story
  `sprint-planning-goal-conditions-declaration-plan-gate-leads` writes **no structured fix-list
  field**. Its AC 2 puts the verified-fix list in the prose `goal` string ("each entry phrased as
  something a human can confirm in the running app"), and its AC 5 gives `momentum-tools sprint plan`
  only `--goal` and `--goal-conditions`. So there are no machine-assigned fix IDs to match against:
  parse the `goal` text, key confirmations by entry text or 1-based index, and make the parse visible
  in the output. Do **not** invent a second producer field. Raise this at the cross-story coherence
  check — if that check instead adds a structured field to the producer, this task simplifies to
  reading it.

- [ ] **Task 5 — Punt-decision requirement (AC 7)**
  Add `--punt-decision <ref>`. Read `.momentum/stories/index.json` for the sprint's story statuses;
  when any sits at `closed-incomplete` or `dropped` and at least one declared condition is not
  verified-PASS, require the flag and verify the referenced decision document exists under
  `_bmad-output/planning-artifacts/decisions/`. Refuse on absent flag or unresolvable reference.
  This gate runs on **both** the `done` and the `failed` closure path — Task 3's FAILED path must
  fall through to it, not around it.

- [ ] **Task 6 — Write the closure record (AC 8)**
  On every successful closure, attach the closure block (verdict, per-condition snapshot, fix
  confirmations, FAILED reason, punt reference) to the record appended to `completed[]`.

- [ ] **Task 7 — Tests (AC 1–10)**
  Extend `skills/momentum/scripts/test-momentum-tools.py` following its existing
  `setup_project(sprints=...)` / `run_tool` / `assert_eq` pattern. Cover one case per AC 2 state and
  reason token: refusal on a slug absent from the registry (`missing-entry`); refusal on
  `status: "absent"` (`missing-entry`); refusal on `last_verified: null` (`no-verdict`); refusal on a
  verdict recorded without both build SHAs (`no-build-shas`); refusal of `done` on a recorded-FAIL
  condition (AC 3, which is a distinct message, not an AC 1 reason token); success when every
  condition is verified-PASS; FAILED closure with reason; FAILED closure rejected without reason; FAILED record lands in `completed[]` with `retro_run_at: null`;
  maintenance-sprint refusal and success; punt-decision refusal on both the `done` and `failed`
  paths; undeclared-outcome refusal; and the preserved no-active-sprint rejection.
  **Three existing tests assert today's unconditional closure and will break under the gate — all
  three must be updated, not left as-is:** `test_sprint_complete` (line 240),
  `test_sprint_complete_no_active` (line 258, which stays valid but must be re-confirmed), and
  `test_sprint_complete_sets_status_done` (line 445, whose fixture has no `goal_conditions` and
  asserts exit 0 — exactly the undeclared-outcome case AC 9 now refuses).

- [ ] **Task 8 — Split closure out of the Conductor's merge-approve branch (AC 11)**
  *EDD ordering: Tasks 8–10 are skill-instruction work, and the EDD guide below requires evals
  before edits. Write Task 10's evals first, then make the Task 8 and 9 edits. Task numbering here
  is a reading order, not an execution order.*
  Edit `skills/momentum/skills/conductor/workflow.md`. Three adjacent line groups need different
  treatment — do not delete the range wholesale:
  · **Lines 2618–2621** (`<action>Complete the sprint: … </action>`) — the closure call itself.
    Remove from the tier-1 merge-approve sequence.
  · **Line 2622** (`<note>Idempotency: …`) — this note is specifically about `sprint complete`
    returning "No active sprint". It travels with the call to the new tier-2 step; it does not stay
    behind in tier 1, and it must be re-worded there because a non-zero exit now also means "refused".
  · **Line 2623** (`END-GATE PHASE-COMPLETE CHECKPOINT`) — **preserve unchanged in tier 1.** It marks
    the approve-side merge mutations as durably done and is what makes a resume skip them.
  Then add a distinct tier-2 closure step that invokes the gate, renders the refusal's unverified
  conditions in plain language (Decision-Grade Presentation Standard — no wall of text), and leaves
  the sprint `active` on refusal.

- [ ] **Task 9 — Update callers, eval, and schema reference (AC 12)**
  Update `skills/momentum/skills/retro/workflow.md` (closure step ~line 695) and
  `skills/momentum/skills/sprint-dev/workflow.md` (~line 749) to invoke the gated closure and surface
  a refusal rather than treating any non-zero exit as the benign no-active no-op. Rewrite
  `skills/momentum/skills/conductor/evals/eval-phase5-completes-sprint-for-retro-pickup.md` to assert
  the tier-2 behavior. Add `failed` to the `status` row of the Sprint Record Fields table in
  `skills/momentum/references/sprint-tracking-schema.md` and document `goal_conditions` and the
  closure block.

- [ ] **Task 10 — Behavioral evals for the changed skill instructions (AC 11, 12)**
  Add evals under `skills/momentum/skills/conductor/evals/` covering: the Conductor does not close the
  sprint in the merge-approve branch, and a closure refusal leaves the sprint active with the
  unverified conditions surfaced.

## Dev Notes

### Decision Authority

DEC-040 D3 is the governing decision; DEC-040 D2 defines the tier split this story's half sits on.
Architecture `Decision 59` (Two-tier gate) and the Sprint `goal_conditions` field paragraph in the
Sprint Tracking Schema already carry the normative schema. The Two-tier gate paragraph closes with
*"**Implementation status:** conductor/sprint-manager/Impetus machinery **not yet implemented** —
applied manually until DEC-040 Phase 2 stories land"*; this story is part of what discharges that
marker. (The `goal_conditions` paragraph carries no such marker — its pending status is implied by
the same Phase 2 plan, not stated.) The ACs above are specified inline and are buildable on their
own — you should not need to open the architecture to implement them. If you do notice a divergence
between an AC and the architecture text, stop and flag it to the developer rather than reconciling
it yourself: the architecture is authoritative, so a real divergence means this story has a defect
that needs correcting, not silently coding around.

Two boundaries are deliberate and must not be crossed:
- **This story never writes `.momentum/features.json`.** DEC-040 D1 makes `momentum-tools feature verify`
  its sole writer. Closure reads verdicts; it does not record them.
- **This story does not build the resume card.** DEC-040 D5's resume card and Impetus pending-gate
  agenda are a separate story. This story produces the closure-pending *state*; that story renders it.

### Current State of Affected Files

- `skills/momentum/scripts/momentum-tools.py` (3091 lines) — `cmd_sprint_complete` at line 290 is 20
  lines and has no gate: it stamps `completed`, `status: "done"`, `retro_run_at: None`, appends to
  `completed[]`, clears `active`, returns success. Its only guard is "No active sprint to complete".
  The `complete` subparser at line 2833 takes zero arguments. `ORDERED_STATES` /`TERMINAL_STATES`
  (lines 46–47) govern *story* status, not sprint status — sprint status is a free string on the
  record and needs no state-machine change to add `failed`.
- `.momentum/sprints/index.json` — the `planning` record for `sprint-2026-08-03` has exactly these
  keys: `locked`, `slug`, `status`, `stories`, `waves`. **Neither `goal` nor `goal_conditions` is
  present**, so the gate must handle a missing key, not just a null value. (`jq '.planning.goal_conditions'`
  returns `null` for a missing key — do not mistake that for the field existing.) `active` is
  currently `null`; there is no active sprint to close today.
- `.momentum/features.json` — **does not exist yet**; created by the `feature verify` sibling story.
  Treat a missing registry as "no conditions verified," never as a pass.
- `skills/momentum/skills/conductor/workflow.md` — line 2619 runs `sprint complete` inside the
  merge-approve branch; line 2622 documents the "No active sprint" no-op convention; line 2623 is the
  `end-gate-phase-complete` ledger checkpoint that makes the approve-side mutations non-repeating on
  resume. Any edit must keep that checkpoint's meaning coherent once closure moves out of the branch.
- `skills/momentum/skills/retro/workflow.md:695` and `skills/momentum/skills/sprint-dev/workflow.md:749`
  both call `sprint complete` and both document the non-zero exit as safely ignorable — which becomes
  wrong once non-zero can mean "refused to close."
- `skills/momentum/references/sprint-tracking-schema.md` — Sprint Record Fields table lists `status` as
  `planning`, `active`, `done` and has no `goal_conditions` row.

### Architecture Compliance

- `momentum-tools.py sprint` remains the sole writer of `.momentum/sprints/index.json` (Read/Write
  Authority table) — no skill or agent writes sprint status directly.
- `.momentum/features.json` is read-only to everything except `momentum-tools feature verify`
  (architecture line 1351).
- Features integrate at exactly three seams and no others (DEC-040 D1); this story is seam 2
  (sprint-closure verdict). Do not add a fourth seam — in particular, do not make any epic-facing
  skill read `features.json`.
- Refusal surfaces follow the Decision-Grade Presentation Standard: lead with the decision, name each
  unverified condition with what/why/evidence, no wall of text. A wall-of-text gate surface is a defect.

### Testing Requirements

- Python CLI behavior is verified by `bash` per the verification standard's `script-code` routing:
  run `momentum-tools sprint complete` with representative sprint records and assert exit code, JSON
  output, and the resulting `.momentum/sprints/index.json` state.
- `skills/momentum/scripts/test-momentum-tools.py` is the existing harness; follow its
  `setup_project()` fixture convention (it accepts a `sprints=` dict) and its `assert_eq` style.
- Three existing tests exercise `sprint complete`: `test_sprint_complete` (line 240),
  `test_sprint_complete_no_active` (line 258), and `test_sprint_complete_sets_status_done` (line 445).
  The first and third assert unconditional closure on fixtures with no `goal_conditions` and must be
  updated to seed either a passing verdict registry or the AC 9 refusal — leaving either asserting
  unconditional closure would mean the suite passes while the gate is absent.
- Skill-instruction changes (conductor, retro, sprint-dev) are verified by evals, not unit tests.

### Project Structure Notes

All work is in-repo under `skills/momentum/`: the CLI and its test harness in `scripts/`, three
workflow files under `skills/`, one eval under `skills/conductor/evals/`, and one reference doc under
`references/`. No new directories are created. No project outside this repo is touched — the nornspun
features.json reconciliation named in DEC-040's phased plan is a different story in a different repo.

### Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1–7 → `script-code` (TDD)
- Tasks 8–10 → `skill-instruction` (EDD)

Multi-method note (verification-standard §2): this story's tasks route to two methods (`bash` for
`script-code`, `skill-invoke` for `skill-instruction`). The story's primary deliverable is the
`momentum-tools sprint complete` gate — a CLI behavior — so `bash` governs the story's verification.
The skill-instruction tasks are verified by their own evals per the EDD section below.

---

### script-code Tasks: TDD via bmad-dev-story

Script and code changes use standard TDD (red-green-refactor). bmad-dev-story handles TDD natively —
the implementation guidance below matches its standard approach:

1. **Red:** Write failing tests for the task's functionality first. Confirm they fail before implementing.
2. **Green:** Implement the minimum code to make tests pass. Run tests to confirm.
3. **Refactor:** Improve code structure while keeping tests green.

**Note:** Scripts in Momentum live under `skills/momentum/skills/[name]/scripts/` or
`skills/momentum/scripts/`. Follow the pattern in existing Momentum scripts for language choice and
structure — here, `momentum-tools.py`'s existing `cmd_*` / `result()` / `error_result()` convention.

**DoD items for script-code tasks (bmad-dev-story standard DoD applies — listed here for reference):**
- Tests written and passing
- No regressions in existing test suite (`test-momentum-tools.py` must pass in full, including the
  two updated `sprint complete` tests)
- Code quality checks pass if configured

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM
prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/conductor/evals/` (the directory exists):
   - One `.md` file per eval, named descriptively (e.g., `eval-merge-approve-does-not-close-sprint.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable
     behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify the workflow.md and reference files

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it the eval's scenario
   as its task and load the skill by passing the SKILL.md and workflow.md contents as context.
   Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles;
   surface to the developer if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with
  clear load instructions (NFR3)
- Skill names use the `momentum:` namespace prefix (NFR12)

*(No new skills are created here — only `conductor`, `retro`, and `sprint-dev` workflows are edited.
The NFR items apply to any SKILL.md touched; conductor's SKILL.md is expected to be unchanged.)*

**Additional DoD items for skill-instruction tasks:**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/conductor/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed, if any SKILL.md was touched
- [ ] `model:` and `effort:` frontmatter present and correct, if any SKILL.md was touched
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically)

---

**Frozen verification contract reminder.** A frozen verification contract exists for this sprint at
`.momentum/sprints/{sprint-slug}/specs/sprint-closure-refusal-recorded-human-verdicts-per-goal.{ext}`.
Read the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a
self-check before signaling done. Never read the verifier body (Part B: scenarios, assertion scripts,
Gherkin) beyond sections explicitly referenced by `how_dev_self_checks`.

### References

- DEC-040 D3 (governing) and D1/D2/D5 (seam context) — `_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`; completes DEC-039.
- Architecture Decision 59, "Two-tier gate (DEC-040 D2/D3)" — `_bmad-output/planning-artifacts/architecture.md`
- Architecture "Sprint goal_conditions field (added 2026-08-02, DEC-040 D3)" — Sprint Tracking Schema section
- Architecture Read/Write Authority table row for `momentum-tools feature verify` (sole writer of `.momentum/features.json`)
- Producer seam: `.momentum/stories/momentum-tools-feature-verify-human-verdict-recorder-and.md`
- Producer seam: `.momentum/stories/sprint-planning-goal-conditions-declaration-plan-gate-leads.md`
- Tier-1 counterpart: `.momentum/stories/conduct-merge-gate-completes-by-executing-merge-push-story.md`
- Pain evidence: `docs/research/nornspun-delivery-discovery-2026-08-02/synthesis.md`
- Epic context: `momentum-sprint-orchestration` (from _bmad-output/planning-artifacts/epics.json)

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
