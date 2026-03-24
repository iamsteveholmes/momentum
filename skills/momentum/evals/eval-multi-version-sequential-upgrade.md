# Eval: Multi-Version Sequential Upgrade

## Scenario

Given a developer's state files show component groups at version `"1.0.0"` and the skill's `momentum-versions.json` has `current_version: "1.2.0"` with two entries — `1.1.0` (`from: "1.0.0"`) and `1.2.0` (`from: "1.1.0"`) — when they invoke `/momentum`, the skill should:

1. Detect version mismatch (groups at 1.0.0, current is 1.2.0)
2. Resolve the upgrade chain: 1.0.0 → 1.1.0 → 1.2.0 (using `from` field links)
3. Present the 1.0.0→1.1.0 changes as the FIRST group with [U]/[S], organized by component group
4. On [U]: apply the 1.1.0 actions (using `add`/`replace`/`delete`/`migration` types)
5. Update both state files — per-component-group versions advance to 1.1.0
6. Present the 1.1.0→1.2.0 changes as the SECOND group with [U]/[S]
7. On [U]: apply the 1.2.0 actions
8. Update both state files — per-component-group versions advance to 1.2.0

## Expected Behavior

Each intermediate version is presented and confirmed separately — NOT as a combined diff from 1.0.0 to 1.2.0. The developer sees each step clearly. State files only advance per-group versions after each intermediate version's actions complete. The final state reflects all groups at `1.2.0` after both steps.

## NOT Expected

- Presenting a single diff from 1.0.0 to 1.2.0 (skipping 1.1.0 as an intermediate)
- Applying all actions at once without per-version grouping
- Advancing group versions to 1.2.0 before 1.1.0 actions complete
- Proceeding to session orientation without completing the upgrade chain
- Failing with an error when a multi-version gap is detected
- Using old action types (`write_file`, `update_file`, `write_config`, `update_config`)
