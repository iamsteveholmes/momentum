# Eval: Phase 5 completes the sprint for retro pickup (regression)

**Surface under test:** the tier-2 closure step at the end of Phase 5, reached once the
`merge-gate-outcome` for the sprint is `"merged"` (per
`conduct-merge-gate-completes-by-executing-merge-push-story`) — distinct from the tier-1
merge-gate execution sequence itself, per `sprint-closure-refusal-recorded-human-verdicts-per-goal`
(DEC-040 D2/D3).

**Regression guard for:** the conduct-never-completes-its-own-sprint defect, updated for the
two-tier gate. `momentum-tools sprint complete` is the (now gated) transition that moves the active
sprint into `sprints/index.json` `completed[]` with `status: "done"` (or `"failed"`) and
`retro_run_at: null`. Prior to the original fix, zero call sites in `conductor/workflow.md` invoked
it at all, leaving conduct-built sprints outside `completed[]` and `momentum:retro` Step 1 HALTing
with "No sprint is awaiting a retrospective." That defect must not resurface, but the call itself
has since moved: it is no longer bundled into the tier-1 merge-approve sequence (that bundling was
itself the punt-institutionalizing defect DEC-040 identifies — a single developer approval closing
the sprint's goal-verdict question with no verification). This eval now guards two things at once:
(a) the sprint still reaches `completed[]` for retro pickup, on either terminal state, and
(b) it only does so once the tier-2 closure gate actually passes — not automatically alongside the
merge.

## Scenario

**Given:** A sprint has been built by the Conductor, its stories have reached their terminal
review states (merged stories `review -> verify -> done`; stranded stories `-> closed-incomplete`),
and the sprint has not yet been marked complete anywhere. The active sprint's `goal_conditions` are
all verified-PASS in `.momentum/features.json` (or, for a maintenance sprint, no `goal_conditions`
are declared and its verified-fix list can be confirmed).

**When:** The developer approves the Phase 5 end-gate, the merge-gate execution sequence completes
and its outcome is recorded as `"merged"`, and the Conductor reaches the tier-2 closure step
described in `eval-tier2-closure-separate-from-merge-approve.md`.

**Then:**

1. The tier-2 closure step calls `momentum-tools sprint complete` — after the merge-gate outcome
   is already durably recorded as `"merged"`, not as part of the merge-gate execution sequence
   itself (that sequence contains no such call — see the sibling eval above).
2. Because every declared condition is verified-PASS, the call succeeds: `sprints/index.json` shows
   the sprint moved from `active` into `completed[]`, with that entry's `status == "done"` and
   `retro_run_at == null`.
3. No separate, manually-run completion command was needed to reach this state.
4. Invoking `momentum:retro` immediately afterward finds this sprint at Step 1 (`retro_run_at ==
   null` in `completed[]`) and proceeds into review — it does not HALT with "No sprint is awaiting
   a retrospective."

**And (the honest-failure variant — AC 5):** if instead the developer (or a later session) closes
the sprint with `momentum-tools sprint complete --verdict failed --reason "..."` because the goal
was never verified, the resulting record lands in `completed[]` with `status == "failed"` and
`retro_run_at == null` — identical retro-pickup shape to the `done` case. `momentum:retro` Step 1
must discover a FAILED sprint exactly as readily as a done one; a sprint that ships code but never
gets its goal verified needs a retrospective more than one that closes clean.

**And (resume-safety):** if the tier-2 closure step runs a second time against a sprint already
completed by a prior pass, `momentum-tools sprint complete` returns `"No active sprint to
complete"` (exit non-zero). The Conductor treats this exact message as an expected, non-fatal
no-op — it renders the completion summary from the existing `completed[]` record rather than
treating the exit code alone as a refusal to investigate.

## Pass Criteria

- The workflow text contains no `momentum-tools sprint complete` call inside the merge-gate
  execution sequence (the "NO row with event == 'end-gate-phase-complete'" block through PUSH and
  POST-EXECUTION READ-BACK VERIFICATION) — see `eval-tier2-closure-separate-from-merge-approve.md`
  for that assertion in full.
- A distinct tier-2 step, gated on `merge-gate-outcome == "merged"`, prescribes the
  `momentum-tools sprint complete` call.
- An adjacent note distinguishes the exact "No active sprint to complete" message (expected no-op
  on resume) from any other non-zero exit (a genuine gate refusal — see
  `eval-tier2-closure-refusal-leaves-sprint-active.md`).
- A live check confirms the mechanism: seed an active sprint with all stories at `done` and a
  verified-PASS `goal_conditions` registry, run `momentum-tools sprint complete`, and observe
  `sprints/index.json` shows the sprint under `completed[]` with `status == "done"` and
  `retro_run_at == null`. A second `sprint complete` call returns `"No active sprint to complete"`
  without corrupting `sprints/index.json`.
- The same live check repeated with `--verdict failed --reason "..."` instead shows `status ==
  "failed"` and `retro_run_at == null` in `completed[]`.
- With the sprint in either completed-and-unreviewed shape (`done` or `failed`), `momentum:retro`
  Step 1 identifies it by name and proceeds, rather than reporting nothing is awaiting a
  retrospective.

## Fail Criteria

- `momentum-tools sprint complete` appears inside the merge-gate execution sequence rather than as
  a distinct tier-2 step.
- The workflow lacks the idempotency note, or treats a `"No active sprint to complete"` return the
  same as any other refusal (or vice versa — treats a genuine refusal as a benign no-op).
- After a live approve-sequence-then-closure run, `sprints/index.json` still shows the sprint as
  `active` (or absent from `completed[]`) when every declared condition was verified-PASS, forcing
  a manual `momentum-tools sprint complete` call.
- A FAILED closure (`--verdict failed --reason "..."`) does not land in `completed[]`, or lands with
  a non-null `retro_run_at`, or is otherwise treated differently from a `done` closure for retro
  discovery purposes.
- `momentum:retro`, invoked immediately after either terminal closure, HALTs with "No sprint is
  awaiting a retrospective" even though a sprint was just closed.
- The terminal-transition logic, the MAJOR-RESIDUAL governance guard, or the merge-gate execution
  sequence's ordering were altered by this change (out of scope for this story) beyond removing the
  `sprint complete` call and relocating it to the new tier-2 step.

## Verification Method

**Inspection + targeted CLI exercise.**

1. Inspect `skills/momentum/skills/conductor/workflow.md`. Confirm no `momentum-tools sprint
   complete` action exists inside the merge-gate execution sequence, and confirm a distinct tier-2
   step (gated on `merge-gate-outcome == "merged"`) prescribes the call, with an adjacent
   idempotency note distinguishing "No active sprint to complete" from a genuine refusal.

2. Exercise the tool directly:
   ```
   # Setup: sprints/index.json has an active sprint with all its stories at done,
   # goal_conditions: ["demo-feature"], and .momentum/features.json has a verified-PASS
   # entry for demo-feature.
   momentum-tools sprint complete
   # Expect: exit 0; sprints/index.json now shows the sprint under completed[] with
   #         status == "done" and retro_run_at == null; active is cleared.

   momentum-tools sprint complete
   # Expect: exit non-zero, "No active sprint to complete" — no corruption of sprints/index.json.
   ```

   And the honest-failure variant:
   ```
   # Setup: a fresh active sprint, goal_conditions declared but unverified.
   momentum-tools sprint complete --verdict failed --reason "goal never verified in the running app"
   # Expect: exit 0; sprints/index.json shows the sprint under completed[] with
   #         status == "failed" and retro_run_at == null.
   ```

3. With either completed-and-unreviewed sprint in place, invoke `momentum:retro` and confirm Step 1
   names that sprint and proceeds, rather than HALTing.

Both the workflow instruction and the tool/retro behavior must hold for this eval to pass.
