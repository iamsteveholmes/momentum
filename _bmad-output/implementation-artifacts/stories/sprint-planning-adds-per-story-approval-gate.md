---
title: Sprint-planning adds per-story approval gate
story_key: sprint-planning-adds-per-story-approval-gate
status: ready-for-dev
epic_slug: sprint-dev-workflow
feature_slug:
story_type: practice
depends_on: []
touches:
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/sprint-dev/workflow.md
  - skills/momentum/scripts/momentum-tools.py
  - .momentum/sprints/index.json
---

# Sprint-planning adds per-story approval gate

## Story

As a developer,
I want sprint-planning to open each fleshed-out story spec in a viewer and require an explicit per-story approval recorded persistently before the sprint can activate,
so that sprint-dev never runs against story specs I have not personally seen and approved.

## Description

momentum:sprint-planning currently fleshes stories out (Step 3) and presents a single sprint-wide approval gate (Step 7) after AVFL. The fleshed-out story spec is summarized in chat but never opened in a viewer, and there is no persistent per-story approval record. The Step 3 prompt "Approve, or revise?" is in-band only — by the time sprint-dev starts, there is no auditable evidence that each individual story spec was reviewed.

This story tightens Step 3 to a true blocking gate: each fleshed-out story is opened in a cmux markdown viewer (matching the pattern already in `quick-fix/workflow.md`), explicit per-story approval is recorded to disk, and sprint activation is blocked until every selected story has an approval record. sprint-dev verifies those records at start and refuses to execute if any are missing.

**Pain context:** auditor-human findings H20, H21, H22 from the nornspun sprint-2026-04-12 retro:
- "Why are we running sprint dev???!?!?!?"
- "Please stick to the plan."
- "I never saw the spec."

Sprint-dev ran before the developer had approved the individual story specs. The single sprint-level Step 7 approval was insufficient — the developer needs to see and approve each story spec on its own.

**Meta-recursion note:** This story modifies the very sprint-planning workflow that is currently planning it. When the change ships, future sprint-planning runs (including the next pass over this same story if it loops back) will gain this gate. That is intentional and acceptable — the change is additive and idempotent.

## Acceptance Criteria

1. **Per-story viewer opens before approval prompt.** During sprint-planning Step 3 (Flesh out stories), after each story is either confirmed-as-existing or freshly fleshed out via momentum:create-story, the story file at `{implementation_artifacts}/stories/{story_slug}.md` is opened in a cmux markdown surface with a clear title (e.g., `"Sprint Story Spec — {story_slug} — Review & Approve"`) before the approval prompt is presented.

2. **Per-story approval is explicit.** For each story, the developer is prompted with `A` (Approve), `R` (Revise), or `J` (Reject and remove from sprint). The prompt blocks workflow progress until a response is given.

3. **Approval is recorded persistently.** When the developer chooses Approve for a story, the workflow records an approval entry containing: `story_slug`, `approved_at` (ISO-8601 timestamp), `decision: "approved"`, and `story_file_sha` (SHA-256 of the story file's contents at approval time). Records are written via a new `momentum-tools sprint story-approve` subcommand into the planning sprint's `approvals` array in `.momentum/sprints/index.json` (under `planning.approvals`).

4. **Revision invalidates prior approval.** If the developer chooses Revise for a story, momentum:create-story re-runs with the feedback. After the revision the viewer re-opens with a "Revised" title and the approval prompt is re-presented. Any prior approval entry for that story_slug in the planning sprint is replaced (overwritten) when the new approval is written — the new entry carries the new file SHA, so the old SHA-based record is gone in a single update.

5. **Rejection halts and removes the story.** If the developer chooses Reject, the workflow:
   - removes the story from the planning sprint's `stories` array via `momentum-tools sprint plan --operation remove --stories {slug}`,
   - records a rejection entry (`decision: "rejected"`) in `planning.approvals`,
   - re-validates that the remaining selection still satisfies the 2–8 story bound; if it falls below 2, the workflow HALTs with an explanatory message and the developer must add or replace stories before continuing.

6. **Activation is blocked until all stories are approved.** `momentum-tools sprint activate` checks that for every slug in `planning.stories` there is a corresponding entry in `planning.approvals` with `decision == "approved"` and `story_file_sha` matching the current file SHA on disk. If any story lacks an approval, or the SHA differs (file was edited after approval), `sprint activate` exits non-zero with `error_result("sprint_activate", "Stories missing approval: {slugs}")` and the workflow HALTs.

7. **sprint-dev verifies approvals at start.** sprint-dev Phase 1 (Initialization), after reading the active sprint record, checks that the `approvals` array on the active sprint contains an `approved` entry for every story in `stories`, with each `story_file_sha` matching the current file SHA. If verification fails, sprint-dev HALTs with a message naming the offending slugs — it does not transition any story to in-progress.

8. **Approval records survive sprint activation.** When `cmd_sprint_activate` promotes `planning` to `active`, the `approvals` array is carried over verbatim (it is part of the sprint object that gets reassigned). It also persists into `sprints.completed[]` when the sprint completes, so historical sprints carry their approval audit trail.

9. **Idempotent re-approval.** Re-approving a story that already has an `approved` entry replaces the prior entry (same slug, new timestamp, same SHA). Re-approving across a file edit (different SHA) is treated as a fresh approval — overwrites the prior entry.

10. **Approval records are visible to sprint-dev via the same `sprints/index.json` it already reads.** sprint-dev Phase 1 already reads `sprints/index.json` and stores `active.*` (workflow.md line 125–126); the new `approvals` array lives on that same `active` object. sprint-dev's verification step (Task 4) reads `sprints["active"]["approvals"]` from the same load — no new file is introduced. The per-sprint record `sprints/{sprint_slug}.json` (read at line 141 for `locked` and `team`) is unchanged by this story.

## Tasks / Subtasks

- [ ] **Task 1: Add `story-approve` and `verify-approvals` subcommands to `momentum-tools.py`** (AC 3, 6, 9)
  - [ ] Subtask 1.1: Add `cmd_sprint_story_approve(args)` — accepts `--slug`, `--decision {approved|rejected}`, computes `story_file_sha` from `{implementation_artifacts}/stories/{slug}.md`, writes/replaces an entry in `sprints["planning"]["approvals"]` in `.momentum/sprints/index.json` (initialize array if absent). Errors if no planning sprint exists or if the slug is not in `planning["stories"]`.
  - [ ] Subtask 1.2: Add `cmd_sprint_verify_approvals(args)` — reads `sprints["active"]` (or `planning` when invoked with `--scope planning`), confirms every story in `stories` has an `approvals` entry with `decision=="approved"` and a current-matching `story_file_sha`. Returns structured success/failure with the offending slugs.
  - [ ] Subtask 1.3: Update `cmd_sprint_activate` — call the verify logic before promoting `planning` → `active`. If verification fails, `error_result("sprint_activate", "Stories missing approval: {slugs}", missing=...)` and exit non-zero.
  - [ ] Subtask 1.4: Wire both subcommands into the argparse subcommand router at the bottom of `momentum-tools.py`.

- [ ] **Task 2: Update sprint-planning Step 3 to open viewer, prompt per-story, and persist approval** (AC 1, 2, 3, 4, 5)
  - [ ] Subtask 2.1: After each story is confirmed/fleshed-out, run `cmux markdown open {{implementation_artifacts}}/stories/{{story_slug}}.md --title "Sprint Story Spec — {{story_slug}} — Review & Approve"` before the approval prompt.
  - [ ] Subtask 2.2: Replace the existing two-option `Approve, or revise?` prompt with a three-option prompt: `A — Approve | R — Revise | J — Reject (remove from sprint)`.
  - [ ] Subtask 2.3: On Approve: run `momentum-tools sprint story-approve --slug {{story_slug}} --decision approved`.
  - [ ] Subtask 2.4: On Revise: re-spawn momentum:create-story with feedback; re-open the viewer with the title `"Sprint Story Spec — {{story_slug}} — Revised — Review & Approve"`; re-present the prompt. Loop until the developer chooses A or J.
  - [ ] Subtask 2.5: On Reject: run `momentum-tools sprint plan --operation remove --stories {{story_slug}}` then `momentum-tools sprint story-approve --slug {{story_slug}} --decision rejected`; re-validate the 2–8 story bound; if the remaining selection is below 2, HALT with an explanatory message.

- [ ] **Task 3: Update sprint-planning Step 8 (Activate) to rely on the activation-time check** (AC 6)
  - [ ] Subtask 3.1: Verify the `momentum-tools sprint activate` call now performs the approval verification (see Task 1.3) — no extra workflow logic needed beyond surfacing a clear error message if activation fails. Add an explicit `<check>` after `momentum-tools sprint activate` that surfaces the missing-approvals error and HALTs the workflow rather than proceeding.

- [ ] **Task 4: Update sprint-dev Phase 1 to verify approvals before transitioning any story** (AC 7, 10)
  - [ ] Subtask 4.1: After reading the per-sprint record in sprint-dev step n=1, run `momentum-tools sprint verify-approvals --scope active`.
  - [ ] Subtask 4.2: If verification fails, output the error with the offending slugs and HALT before any in-progress transitions or worktree creation. The HALT message must direct the developer back to sprint-planning.
  - [ ] Subtask 4.3: Confirm the `approvals` array is part of the per-sprint structure read at the top of Phase 1 (it carries over from `planning` to `active` per Task 1.3 and AC 8) — adjust the read to capture it if needed.

- [ ] **Task 5: Behavioral evals for the workflow change**
  - [ ] Subtask 5.1: Create `skills/momentum/skills/sprint-planning/evals/eval-blocks-activation-without-per-story-approval.md` — given a planning sprint with two stories where only one has an approval record, the workflow must NOT activate the sprint and must surface the missing-approval slug.
  - [ ] Subtask 5.2: Create `skills/momentum/skills/sprint-planning/evals/eval-revision-invalidates-prior-approval.md` — given a story already approved, when the developer chooses Revise and the file SHA changes, activation must require a fresh approval against the new SHA.
  - [ ] Subtask 5.3: Create `skills/momentum/skills/sprint-dev/evals/eval-halts-without-active-sprint-approvals.md` — given an active sprint where the on-disk SHA of one story file no longer matches its approval record, sprint-dev Phase 1 must HALT before any in-progress transition.

- [ ] **Task 6: Tests for the new momentum-tools subcommands**
  - [ ] Subtask 6.1: Add unit-style tests in `skills/momentum/scripts/test-momentum-tools.py` (matching the existing patterns there) covering: approve writes the entry; reject writes a rejection entry; activate fails when an approval is missing; activate fails when SHA mismatches; activate succeeds when all approved with matching SHAs; verify-approvals returns offending slugs.

## Dev Notes

### Wave Sequencing

> **Wave sequencing note:** This story runs in Wave 2, after `impetus-momentum-state-migration`
> (Wave 1). Sprint state lives at `.momentum/sprints/index.json` post-migration. Do not read
> or write `_bmad-output/implementation-artifacts/sprints/index.json` — that path no longer
> exists at dev time.

### Architecture Compliance

Aligns with Epic 12 (Sprint Execution Workflow): "How does the workflow gate on MANUAL scenarios that require developer sign-off?" — this story is the canonical example of a manual sign-off gate the workflow must enforce.

The approval-record location is chosen to fit the existing data model:
- `.momentum/sprints/index.json` already holds `planning`, `active`, and `completed` sprint objects.
- Adding an `approvals: []` array on the planning/active sprint object is a strict extension — no existing field changes shape.
- `cmd_sprint_activate` already moves `planning` to `active`; the new approval entries ride along automatically.

This avoids creating a separate `sprints/{slug}/specs/approvals.md` file (the alternative the stub mentioned). A JSON array on the sprint object is structurally simpler, queryable from a tool, and survives activation/completion without a second writer.

### Testing Requirements

This story has three change types — see Momentum Implementation Guide for type-specific test/verification requirements.

- skill-instruction tasks (Tasks 2, 3, 4): EDD via behavioral evals (Task 5).
- script-code tasks (Task 1): TDD with red-green-refactor; tests in `test-momentum-tools.py` (Task 6).
- specification: none — there are no doc-only changes in this story.

### Implementation Guide

See the **Momentum Implementation Guide** section below — it is the authoritative source.

### Project Structure Notes

Files this story will modify:
- `skills/momentum/skills/sprint-planning/workflow.md` — Step 3 viewer-and-approval logic; Step 8 activate error surfacing.
- `skills/momentum/skills/sprint-dev/workflow.md` — Phase 1 (step n=1) approval-verification gate.
- `skills/momentum/scripts/momentum-tools.py` — `cmd_sprint_story_approve`, `cmd_sprint_verify_approvals`, modified `cmd_sprint_activate`, argparse wiring.
- `skills/momentum/scripts/test-momentum-tools.py` — new tests.

Files this story will create:
- `skills/momentum/skills/sprint-planning/evals/eval-blocks-activation-without-per-story-approval.md`
- `skills/momentum/skills/sprint-planning/evals/eval-revision-invalidates-prior-approval.md`
- `skills/momentum/skills/sprint-dev/evals/eval-halts-without-active-sprint-approvals.md`

### Cross-Reference: Existing Approval Pattern

`skills/momentum/skills/quick-fix/workflow.md` already implements the "open in cmux + blocking gate" pattern at Step 1 (lines 44–66). Sprint-planning Step 3 should follow the same shape, scaled to a per-story loop. Reuse the title format and prompt structure for consistency.

### Gherkin / Black-Box Reminder

Gherkin specs for this sprint are in `sprints/{sprint-slug}/specs/` and are off-limits to the dev agent. The dev agent implements against the plain English ACs in this file only — never against `.feature` files (Decision 30: black-box separation). The QA Reviewer and E2E Validator agents will use the Gherkin specs in Phase 5 of sprint-dev.

### References

- Epic 12 (Sprint Execution Workflow): `_bmad-output/planning-artifacts/epics.md` lines 682–696
- Existing approval pattern: `skills/momentum/skills/quick-fix/workflow.md` lines 44–66
- Sprint activation logic: `skills/momentum/scripts/momentum-tools.py` `cmd_sprint_activate` lines 133–152
- sprint-dev Phase 1: `skills/momentum/skills/sprint-dev/workflow.md` step n=1 lines 123–191
- Pain source: nornspun sprint-2026-04-12 retro auditor-human findings H20, H21, H22

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 2, 3, 4 → skill-instruction (EDD)
- Task 1, Task 6 → script-code (TDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/sprint-planning/evals/` and `skills/momentum/skills/sprint-dev/evals/` (these directories already exist):
   - One `.md` file per eval, named descriptively (the three filenames are listed in Task 5)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Modify the workflow.md files (sprint-planning and sprint-dev) per Tasks 2, 3, 4.

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context. Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely (sprint-planning and sprint-dev SKILL.md files are unchanged in this story; only their workflow.md files change, but verify the description line did not drift).
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23).
- workflow.md body should stay reasonable; both files are already at the long end — keep additions focused.
- Skill names use `momentum:` namespace prefix (NFR12) — already in place; no new skills introduced.

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 3 behavioral evals written (Task 5 enumerates the exact filenames)
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] sprint-planning and sprint-dev SKILL.md descriptions still ≤150 characters
- [ ] `model:` and `effort:` frontmatter present and unchanged
- [ ] AVFL checkpoint on produced artifacts documented (momentum:dev runs this automatically — validates the implemented workflow.md against story ACs)

---

### script-code Tasks: TDD via bmad-dev-story

Script and code changes use standard TDD (red-green-refactor). bmad-dev-story handles TDD natively — the implementation guidance below matches its standard approach:

1. **Red:** Write failing tests in `skills/momentum/scripts/test-momentum-tools.py` for: `story-approve` writes a record; `verify-approvals` returns offending slugs; `activate` rejects unapproved sprints; SHA mismatch invalidates approval; activation succeeds when all approvals match. Confirm the tests fail before implementing.
2. **Green:** Implement `cmd_sprint_story_approve`, `cmd_sprint_verify_approvals`, and the `cmd_sprint_activate` modification. Run tests to confirm green.
3. **Refactor:** Extract a shared helper (e.g., `_compute_story_sha(slug)`) if both new commands need it.

**Note:** Scripts in Momentum live under `skills/momentum/scripts/`. Follow the patterns in existing functions (`cmd_sprint_activate`, `cmd_sprint_plan`, `cmd_sprint_complete`) for argument parsing, error reporting via `error_result`, and JSON writes via `write_json`.

**DoD items for script-code tasks (bmad-dev-story standard DoD applies — listed here for reference):**
- Tests written and passing
- No regressions in the existing momentum-tools.py test suite
- Code style consistent with surrounding functions

---

### Reminder

Gherkin specs exist for this sprint at `sprints/{sprint-slug}/specs/` and are off-limits to the dev agent — implement against the plain English ACs in this file only, never against `.feature` files (Decision 30 black-box separation).

## Dev Agent Record

_DRAFT — this section is populated by the dev agent during and after implementation._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
