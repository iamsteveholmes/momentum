# Eval: Multi-Version Sequential Upgrade

## Scenario

Given a developer's project has `installed.json` with `momentum_version: "1.0.0"` and the skill's `momentum-versions.json` has `current_version: "1.2.0"` with two entries — `1.1.0` (`from: "1.0.0"`) and `1.2.0` (`from: "1.1.0"`) — when they invoke `/momentum`, the skill should:

1. Detect version mismatch (1.0.0 → 1.2.0)
2. Resolve the upgrade chain: 1.0.0 → 1.1.0 → 1.2.0 (using `from` field links)
3. Present the 1.0.0→1.1.0 changes as the FIRST group with [U]/[S]
4. On [U]: apply the 1.1.0 actions
5. Present the 1.1.0→1.2.0 changes as the SECOND group with [U]/[S]
6. On [U]: apply the 1.2.0 actions
7. Update `installed.json` to `momentum_version: "1.2.0"` after both complete

## Expected Behavior

Each intermediate version is presented and confirmed separately — NOT as a combined diff from 1.0.0 to 1.2.0. The developer sees each step clearly. `installed.json` only advances to the next version after each group's actions complete. The final `installed.json` reflects `1.2.0` after both steps.

## NOT Expected

- Presenting a single diff from 1.0.0 to 1.2.0 (skipping 1.1.0 as an intermediate)
- Applying all actions at once without per-version grouping
- Updating `installed.json` to `1.2.0` before `1.1.0` actions complete
- Proceeding to session orientation without completing the upgrade chain
- Failing with an error when a multi-version gap is detected
