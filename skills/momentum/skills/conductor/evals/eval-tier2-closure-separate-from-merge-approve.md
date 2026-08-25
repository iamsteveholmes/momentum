# Eval: Tier-2 closure is separate from the tier-1 merge-approve sequence

**Surface under test:** Phase 5 approve — the merge-gate execution sequence (merge, branch
delete, per-story terminal transitions, push, post-execution read-back verification) versus the
sprint closure gate (`momentum-tools sprint complete`).

**Regression guard for:** DEC-040 D2/D3 (`sprint-closure-refusal-recorded-human-verdicts-per-goal`),
which dissolves the bundling `conduct-merge-gate-completes-by-executing-merge-push-story` (tier 1)
and this story (tier 2) previously shared: one developer approval used to both merge the code AND
close the sprint unconditionally in the same `momentum-tools sprint complete` call. Tier 1 ("is this
code something we are comfortable keeping on trunk?") and tier 2 ("did the sprint's goal actually
get verified by a human?") are now two independently-gated questions. The merge-gate execution
sequence itself (`conduct-merge-gate-completes-by-executing-merge-push-story`'s own scope — merge,
transitions, push, read-back verification) is unaffected by this story and must not be altered.

## Scenario

**Given:** A sprint has been built by the Conductor, its stories have reached their terminal
review states, and the developer approves the Phase 5 end-gate.

**When:** The merge-gate execution sequence runs (merge to `main`, branch delete, per-story
terminal transitions, push, post-execution read-back verification, and the
`end-gate-phase-complete` checkpoint).

**Then:**

1. `momentum-tools sprint complete` is NOT invoked anywhere inside that sequence — not before the
   merge, not between the transitions and the push, not after the read-back verification.
2. The merge-gate execution sequence completes and its outcome is recorded (`merge-gate-outcome`
   row with `outcome: "merged"`) without depending on, or being gated by, sprint closure at all.
3. A distinct step, reached only once the merge-gate outcome is `"merged"`, invokes
   `momentum-tools sprint complete` on its own — this is the tier-2 closure attempt, and it runs
   after the tier-1 sequence has already completed and been durably recorded.
4. Nothing in the merge-gate execution sequence's own success or failure output claims the sprint
   is "complete" or "closed" — those outputs describe the merge/push/transition outcome only, and
   any mention of the sprint's goal verdict explicitly defers it as a separate, still-open decision.

## Pass Criteria

- Inspecting `conductor/workflow.md`'s merge-gate execution sequence (the `<check if="NO row with
  event == 'end-gate-phase-complete' exists yet...">` block through the `PUSH` and
  `POST-EXECUTION READ-BACK VERIFICATION` actions) finds no `momentum-tools sprint complete` call.
- A separate step or check, gated on `merge-gate-outcome == "merged"`, contains the
  `momentum-tools sprint complete` call and is positioned after the merge-gate execution sequence
  (not interleaved inside it).
- Running the merge-gate execution sequence against a fixture sprint (all stories mergeable, no
  goal_conditions declared) leaves `sprints/index.json`'s `active` entry still `active` immediately
  after the merge/push/transitions complete — it does not move to `completed[]` until the separate
  tier-2 step runs.

## Fail Criteria

- `momentum-tools sprint complete` still appears as an action inside the merge-gate execution
  sequence (between the terminal transitions and the push, or anywhere else in that sequence).
- The tier-2 closure step is missing entirely, or is gated on something other than the merge-gate
  outcome being `"merged"` (e.g., gated on developer approval alone, which would let it run even
  when the merge itself failed).
- The merge-gate execution sequence's own action or output text asserts or implies that closing the
  sprint is part of what a successful merge accomplishes.

## Verification Method

**Skill-invoke (subagent behavioral check).** Spawn a subagent with the Phase 5 approve section of
`conductor/workflow.md` as context (SKILL.md + workflow.md). Task it with the scenario above: given
a sprint reaching the merge-approve branch with the developer approving, walk through what actions
it would take in sequence and in what order relative to `momentum-tools sprint complete`. Confirm
its described sequence matches the Pass Criteria and not the Fail Criteria.
