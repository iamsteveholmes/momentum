# Eval: Upgrade Detection and Execution

## Scenario

Given a developer's project has `.claude/momentum/installed.json` with `momentum_version: "1.0.0"` and the skill's `momentum-versions.json` has `current_version: "1.1.0"`, when they invoke `/momentum`, the skill should:

1. Read `momentum-versions.json` and detect `current_version = "1.1.0"`
2. Read `installed.json` and detect `momentum_version = "1.0.0"`
3. Detect a version mismatch (1.0.0 ≠ 1.1.0)
4. Collect the 1.1.0 version entry (the one with `"from": "1.0.0"`)
5. Display the upgrade summary in "what changed / what I need to do" format:
   ```
   Momentum has been updated to 1.1.0 — your project is configured for 1.0.0.

   Here's what changed and what I need to do:

     · authority-hierarchy.md — revised authority precedence rules
       → update ~/.claude/rules/authority-hierarchy.md

   No restart needed for these changes — they take effect immediately.

   Update now, or continue with 1.0.0 for this session?
   [U] Update · [S] Skip for now
   ```
6. On [U]: execute each action from the 1.1.0 entry, reporting each with ✓
7. Update `installed.json` with `momentum_version: "1.1.0"`, new `installed_at`, and updated component hashes
8. Confirm upgrade complete

## Expected Behavior

Version mismatch is detected immediately. The upgrade summary shows what changed and what will be done (paired). Developer must approve before any files are written. After [U], each action executes with ✓ confirmation. `installed.json` is updated to reflect the new version.

## NOT Expected

- Silently skipping the version mismatch
- Writing files before [U] approval
- Jumping directly to session orientation after detecting mismatch (old placeholder behavior)
- Updating `installed.json` when [S] is chosen
