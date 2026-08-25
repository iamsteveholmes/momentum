# Eval: Absent or Empty features.json Routes to the Maintenance Path, Never a Skip

**ID:** eval-goal-conditions-absent-registry-routes-maintenance
**Change-type:** skill-instruction
**Phase:** Story selection (Step 2)

## Scenario A: `.momentum/features.json` does not exist

Given `.momentum/features.json` does not exist on disk (the registry has not been created yet —
e.g., its delivering story has not shipped in this project)

When Step 2 reaches the goal-condition declaration point

Then:

1. The workflow attempts to read the file, detects it is absent, and says so in one plain line
   (e.g., "No feature registry found — this sprint will declare a verified-fix goal instead.").
2. The workflow does not error, halt, or crash on the missing file.
3. The workflow continues directly on the maintenance path (Scenario A/B of
   `eval-goal-conditions-maintenance-sprint-zero-declared`) — it asks for a verified-fix list and
   persists `goal_conditions` as `[]`.
4. The declaration step is not silently skipped — the developer still sees the one-line notice
   and is still asked for the fix list before the run proceeds to Step 3.

## Scenario B: `.momentum/features.json` exists but lists zero features

Given the file exists and parses as valid JSON but contains no feature entries

When Step 2 reaches the declaration point

Then the same behavior as Scenario A applies: one plain line noting no candidates were found,
then the maintenance path.

## Pass Criteria

- A missing file produces one plain-language notice, not an error or stack trace.
- The run continues on the maintenance path in both the absent-file and empty-list cases.
- The developer is still asked for a verified-fix list — the step is never bypassed entirely.

## Fail Criteria

- The workflow halts, errors, or asks the developer to create `features.json` before proceeding.
- The declaration step is silently skipped (no notice, no fix-list prompt) when the file is
  missing or empty.
- The workflow creates a placeholder `.momentum/features.json` to work around the absence
  (sprint planning must never write this file).
