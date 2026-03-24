# Eval: Version Match Skip

## Scenario

Given `~/.claude/momentum/global-installed.json` exists with all global component groups at version `"1.0.0"`, and `.claude/momentum/installed.json` exists with all project component groups at version `"1.0.0"`, and `momentum-versions.json` has `"current_version": "1.0.0"`, when the developer invokes `/momentum`:

The skill should:
1. Read `momentum-versions.json` and detect `current_version = "1.0.0"`
2. Read both state files and find all component groups at `"1.0.0"`
3. Detect all groups are current — skip setup entirely
4. Proceed to hash drift check, then session orientation without any install prompts

## Expected Behavior

No setup prompt appears. No consent flow. No file writes. The skill moves to hash drift detection and then session orientation (e.g., asks what the developer is working on).

## NOT Expected

- Showing the pre-consent summary when setup is already complete
- Re-writing any config files
- Asking for consent when all component groups match current version
- Offering to install global rules that are already at the current version
