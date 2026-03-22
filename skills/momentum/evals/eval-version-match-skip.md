# Eval: Version Match Skip

## Scenario

Given `.claude/momentum/installed.json` already exists and contains `"momentum_version": "1.0.0"`, and `momentum-versions.json` also has `"current_version": "1.0.0"`, when the developer invokes `/momentum`:

The skill should:
1. Read `momentum-versions.json` and detect `current_version = "1.0.0"`
2. Read `.claude/momentum/installed.json` and find `momentum_version = "1.0.0"`
3. Detect version match — skip setup entirely
4. Proceed directly to session orientation without any install prompts

## Expected Behavior

No setup prompt appears. No consent flow. No file writes. The skill moves directly to session orientation (e.g., asks what the developer is working on, or provides a session orientation summary).

## NOT Expected

- Showing the pre-consent summary when setup is already complete
- Re-writing any config files
- Asking for consent when installed version matches current version
