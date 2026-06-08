# Eval: Approve path routes merged stories through verify before done (regression)

**Surface under test:** Phase 5 approve — status-transition sequence for merged stories.

**Regression guard for:** verify-skip defect (conduct-core retro, critical finding). The defect was a
direct `review -> done` skip in the approve path. The fix (`conductor/workflow.md` ~L1212–1214,
commit `9e72bb2`) enforces the two-step `review -> verify -> done` sequence via two adjacent
`status-transition` calls.

## Scenario

**Given:** A story that has been merged during the sprint build. Its status is `review` when
the Phase 5 approve sequence begins.

**When:** The Conductor executes the status-transition block for this merged story during
Phase 5 approve (the `<check if="developer approves">` branch).

**Then:**

1. The Conductor calls `momentum-tools sprint status-transition --story {slug} --target verify`
   first, moving the story from `review` to `verify`.
2. The Conductor then calls `momentum-tools sprint status-transition --story {slug} --target done`,
   moving the story from `verify` to `done`.
3. The story's final recorded status is `done`.
4. The story passes through `verify` — it never jumps directly from `review` to `done`.

## Pass Criteria

- The workflow text at Phase 5 approve prescribes two sequential `status-transition` calls:
  first `--target verify`, then `--target done`.
- The note explicitly states that a direct `review -> done` skip is invalid.
- A live invocation of `momentum-tools sprint status-transition` with `--story <slug> --target verify`
  followed by `--target done` results in `status: done` with no error.

## Fail Criteria

- The workflow omits the intermediate `--target verify` step and transitions directly to `--target done`.
- A single `status-transition` call attempts `review -> done` and the tool accepts it (would indicate
  state machine regression in momentum-tools.py).
- The note about the two-step requirement is absent from the workflow text.

## Verification Method

**Inspection + targeted CLI exercise.**

1. Inspect `skills/momentum/skills/conductor/workflow.md` at the Phase 5 approve
   status-transition block (~L1209–1214). Confirm both `--target verify` and `--target done`
   steps are present and ordered correctly, and the note forbidding a direct `review -> done` skip
   is present.

2. Exercise the state machine directly:
   ```
   # Setup: story at review
   momentum-tools sprint status-transition --story test-slug --target verify
   # Expect: status becomes verify, exit 0

   momentum-tools sprint status-transition --story test-slug --target done
   # Expect: status becomes done, exit 0
   ```

3. Confirm that attempting a direct `review -> done` skip is rejected:
   ```
   momentum-tools sprint status-transition --story test-slug --target done
   # (from review state — skipping verify)
   # Expect: exit 1, error mentioning non-adjacent forward transition
   ```

Both the workflow instruction and the tool enforcement must hold for this eval to pass.
