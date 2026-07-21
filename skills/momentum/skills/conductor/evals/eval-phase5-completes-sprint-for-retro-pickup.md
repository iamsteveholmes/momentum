# Eval: Phase 5 completes the sprint for retro pickup (regression)

**Surface under test:** Phase 5 approve — sprint-completion call between the terminal story-status
transitions and the push summary.

**Regression guard for:** the conduct-never-completes-its-own-sprint defect. `momentum-tools sprint
complete` is the transition that moves the active sprint into `sprints/index.json` `completed[]`
with `status: "done"` and `retro_run_at: null` (`momentum-tools.py:290-309`). Prior to this fix,
zero call sites in `conductor/workflow.md` invoked it — the legacy `momentum:sprint-dev` and
`momentum:retro`'s own closure step both call it, but the Conductor never did, so a conduct-built
sprint stayed outside `completed[]` and `momentum:retro` Step 1 (`retro/workflow.md:55,57-63`) HALTed
with "No sprint is awaiting a retrospective" — requiring hand-run `sprint complete` (evidenced by
`.momentum/handoffs/sprint-2026-06-28-retro-handoff-2026-07-06.md:12` and three further
un-completed conduct sprints flagged in `.momentum/handoffs/retro-sprint-2026-06-28-phase5-handoff-2026-07-06.md:56`).

## Scenario

**Given:** A sprint has been built by the Conductor, its stories have reached their terminal
review states (merged stories `review -> verify -> done`; stranded stories `-> closed-incomplete`),
and the sprint has not yet been marked complete anywhere.

**When:** The developer approves the Phase 5 end-gate (the `<check if="developer approves">`
branch runs to completion).

**Then:**

1. The Conductor calls `momentum-tools sprint complete` after the terminal story-status
   transitions and before the push summary (`git log @{u}..HEAD --oneline`).
2. `sprints/index.json` shows the sprint moved from `active` into `completed[]`, with that entry's
   `status == "done"` and `retro_run_at == null`.
3. No separate, manually-run completion command was needed to reach this state.
4. Invoking `momentum:retro` immediately afterward finds this sprint at Step 1 (`retro_run_at ==
   null` in `completed[]`) and proceeds into review — it does not HALT with "No sprint is awaiting
   a retrospective."

**And (resume-safety):** if the Phase 5 approve branch runs a second time against a sprint already
completed by a prior pass (a rehydrated or re-approved end-gate), `momentum-tools sprint complete`
returns `"No active sprint to complete"` (exit non-zero per `momentum-tools.py:296`), and the
Conductor treats this as an expected, non-fatal no-op — the approve sequence continues to the push
summary without surfacing an error or aborting.

## Pass Criteria

- The workflow text at Phase 5 approve (`conductor/workflow.md`, `<check if="developer approves">`)
  prescribes a `momentum-tools sprint complete` call positioned after the terminal story-transition
  action and before the push-summary action.
- An adjacent note states that a `"No active sprint to complete"` return is an expected, non-fatal
  no-op on resumed/re-approved runs, and that the sequence continues rather than aborting — mirroring
  the convention already documented at `retro/workflow.md:698`.
- A live check confirms the mechanism: seed an active sprint with all stories at `done`, run
  `momentum-tools sprint complete`, and observe `sprints/index.json` shows the sprint under
  `completed[]` with `status == "done"` and `retro_run_at == null`. A second `sprint complete` call
  returns `"No active sprint to complete"` without corrupting `sprints/index.json`.
- With the sprint in that completed-and-unreviewed shape, `momentum:retro` Step 1 identifies it by
  name and proceeds, rather than reporting nothing is awaiting a retrospective.

## Fail Criteria

- The workflow's Phase 5 approve branch contains no `sprint complete` call, or the call is placed
  before the terminal story-transition action or after the push summary/push confirmation.
- The workflow lacks the idempotency note, or treats a `"No active sprint to complete"` return as
  an error that aborts the approve sequence.
- After a live approve-sequence run, `sprints/index.json` still shows the sprint as `active` (or
  absent from `completed[]`), forcing a manual `momentum-tools sprint complete` call.
- `momentum:retro`, invoked immediately after approval, HALTs with "No sprint is awaiting a
  retrospective" even though a sprint was just completed.
- The terminal-transition logic, the MAJOR-RESIDUAL governance guard, or the push/ask sequence were
  altered by this change (out of scope for this story).

## Verification Method

**Inspection + targeted CLI exercise.**

1. Inspect `skills/momentum/skills/conductor/workflow.md` Phase 5 approve branch. Confirm a
   `momentum-tools sprint complete` action is present, ordered after the terminal story-transition
   action and before the push-summary action, with an adjacent idempotency note.

2. Exercise the tool directly:
   ```
   # Setup: sprints/index.json has an active sprint with all its stories at done
   momentum-tools sprint complete
   # Expect: exit 0; sprints/index.json now shows the sprint under completed[] with
   #         status == "done" and retro_run_at == null; active is cleared.

   momentum-tools sprint complete
   # Expect: exit non-zero, "No active sprint to complete" — no corruption of sprints/index.json.
   ```

3. With the completed-and-unreviewed sprint in place, invoke `momentum:retro` and confirm Step 1
   names that sprint and proceeds, rather than HALTing.

Both the workflow instruction and the tool/retro behavior must hold for this eval to pass.
