# Eval: Upgrade Detection and Execution

## Scenario

Given a developer's state files show all component groups at version `"1.0.0"` and the skill's `momentum-versions.json` has `current_version: "1.1.0"`, when they invoke `/momentum`, the skill should:

1. Read `momentum-versions.json` and detect `current_version = "1.1.0"`
2. Read both state files and detect component groups are at `"1.0.0"`
3. Detect version mismatch (groups behind current)
4. Collect the 1.1.0 version entry (the one with `"from": "1.0.0"`)
5. Display the upgrade summary organized by component group:
   ```
   Momentum 1.1.0 is available.

     rules (global)     1.0.0 → 1.1.0
       · authority-hierarchy.md — revised precedence rules
     hooks (project)    1.0.0 → 1.1.0
       · new PostToolUse hook

   Update now?
   [U] Update · [S] Skip for now
   ```
6. On [U]: execute each action (`replace` for rules, `migration` for hooks), reporting each with ✓
7. Update both state files with per-component-group versions set to `"1.1.0"`
8. Confirm upgrade complete

## Expected Behavior

Version mismatch is detected immediately. The upgrade summary shows what changed, organized by component group with scope labels. Developer must approve before any files are written. After [U], each action executes with ✓ confirmation. Both state files are updated to reflect new per-group versions.

## NOT Expected

- Silently skipping the version mismatch
- Writing files before [U] approval
- Jumping directly to session orientation after detecting mismatch
- Updating state files when [S] is chosen
- Showing a monolithic "momentum_version" instead of per-group versions
