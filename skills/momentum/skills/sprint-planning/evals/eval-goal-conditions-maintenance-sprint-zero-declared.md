# Eval: Zero Declared Conditions Requires a Verified-Fix Goal (Maintenance Sprint)

**ID:** eval-goal-conditions-maintenance-sprint-zero-declared
**Change-type:** skill-instruction
**Phase:** Story selection (Step 2)

## Scenario A: Developer declares zero conditions and supplies a fix list

Given `.momentum/features.json` exists with candidate features presented, and the developer
declares zero goal conditions (this sprint is bug-fix / configuration work with no feature-shaped
goal)

When the workflow reaches the point of persisting the declaration

Then:

1. The workflow requires the developer to state a verified-fix list instead — each entry phrased
   as something a human can confirm by observing the running app (not "refactor X" or "improve
   Y" — an outcome check, e.g. "Re-running sprint plan no longer drops the declared wave").
2. The workflow persists this list into `{{goal}}` (as a lead-in line plus one line per fix) and
   persists `{{goal_conditions}}` as an empty selection via
   `momentum-tools sprint plan --goal "..." --goal-conditions ""`.
3. Re-reading the record shows `planning.goal_conditions == []` and `planning.goal` containing
   the fix-list text.

## Scenario B: Developer declares zero conditions and supplies no fix list

Given the same setup, but the developer declares zero conditions and, when asked for a
verified-fix list, provides nothing (or explicitly declines)

When the workflow attempts to advance past the declaration step

Then:

1. The workflow refuses to advance — it does not persist an empty goal and empty conditions
   together, and does not silently proceed to Step 3.
2. The workflow re-prompts, explaining that a sprint needs either at least one declared feature
   condition or a named verified-fix list — one of the two is required.
3. The workflow only proceeds once the developer supplies one or the other.

## Pass Criteria

- Zero conditions + a supplied fix list persists successfully with `goal_conditions == []` and a
  populated `goal`.
- Zero conditions + no fix list blocks advancement with a clear re-prompt.
- The fix-list entries are phrased as human-observable outcomes, not implementation tasks.

## Fail Criteria

- The workflow advances to Step 3 with both `goal` and `goal_conditions` empty.
- A maintenance sprint's fix list is accepted as vague implementation language ("refactor the
  parser") rather than an observable outcome.
- The zero-conditions path is treated as equivalent to skipping the declaration entirely.
