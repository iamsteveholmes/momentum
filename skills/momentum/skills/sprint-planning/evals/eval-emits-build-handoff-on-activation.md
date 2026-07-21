# Eval: Step 8 Emits the Build Handoff Artifact on Activation

**ID:** eval-emits-build-handoff-on-activation
**Change-type:** skill-instruction
**Phase:** Activate the sprint (Step 8, terminal step)

## Scenario

Given a sprint `sprint-2026-07-06` that has completed Steps 1–7: stories selected, waved, and
approved; verification contracts authored and frozen; AVFL result CLEAN; the developer has
signed off the plan gate with decision A (Approve).

When Step 8 runs `momentum-tools sprint ready` then `momentum-tools sprint activate` and
activation succeeds (no missing-approvals error)

Then, before the workflow reports success and returns:

1. A markdown file is written to `.momentum/handoffs/sprint-2026-07-06-build-handoff-<activation-date>.md`,
   where `<activation-date>` is today's date in `YYYY-MM-DD` form (the same date
   `momentum-tools sprint activate` stamps onto the sprint record's `started` field).
2. The `## ✓ Sprint Activated` success output names this file's path explicitly (not just "a
   handoff was written" — the literal path string appears in the output).
3. This write happens as part of Step 8 itself — no separate skill or later step is invoked to
   produce it, and it is not conditional on developer request.

## Pass Criteria

- The `.md` file exists at the documented name/location after Step 8 completes.
- The activation success output contains the file's path verbatim.
- The write occurs unconditionally on every successful activation, not only when explicitly asked.

## Fail Criteria

- No such file exists after activation.
- The file exists but uses a different name, a different date, or a different directory.
- Activation reports `## ✓ Sprint Activated` success without the artifact's path anywhere in
  that output.
- The artifact is produced by a separate, later invocation rather than as part of Step 8's
  terminal action.
