# Eval: Sprint Goal Section Uses Explicit Not-Captured Wording When No Goal Exists

**ID:** eval-build-handoff-goal-not-captured-fallback
**Change-type:** skill-instruction
**Phase:** Activate the sprint (Step 8, terminal step)

## Scenario

Given a sprint `sprint-2026-07-06` whose sprint record has no `goal` value stored (the field is
absent or empty at the time Step 8 activates the sprint)

When Step 8 writes the build handoff artifact for this sprint

Then the artifact's **Sprint Goal** section:

1. Is still present, with its heading, in its normal position in the section order.
2. Reads exactly "Sprint goal not captured at planning" as its body — not blank, not omitted,
   not a paraphrase.

And the other three sections (Stories by Wave, Contract/Spec Locations, Planning-Time Cautions)
render normally, unaffected by the missing goal.

## Pass Criteria

- The Sprint Goal section is present and its body text is exactly "Sprint goal not captured at
  planning".
- No other section is affected by the missing goal value.

## Fail Criteria

- The Sprint Goal section is missing entirely.
- The section is present but left blank (no fallback text).
- The fallback text is present but paraphrased or reworded rather than the exact specified
  string.
