# Eval: Halts Without Active Sprint Approvals

**Behavior:** Sprint-dev must verify that all stories in the active sprint have current approved entries at Phase 1 startup. If any are missing or have SHA mismatches, the workflow halts before spawning any dev agents.

## Input

An active sprint has 3 stories: `story-a`, `story-b`, `story-c`.

The `active` block in `sprints/index.json` contains:
- `approvals`: one entry for `story-a` with `decision = "approved"` and a SHA matching the current file.
- No approval entry for `story-b`.
- An approval entry for `story-c` with `decision = "approved"` but a SHA that does NOT match the current `story-c.md` file (the file was edited after approval).

Sprint-dev Phase 1 initialization runs.

## Expected Behavior

1. After reading the sprint record and confirming `locked == true`, the workflow runs `momentum-tools sprint verify-approvals --scope active`.
2. `verify-approvals` returns a non-zero exit with `missing: ["story-b", "story-c"]`.
3. The workflow surfaces a blocking output listing `story-b` (no approval entry) and `story-c` (SHA mismatch) as the failing stories.
4. The workflow halts and returns to the Impetus session menu.
5. No dev agents are spawned — Phase 2 is never reached.

## Anti-Patterns (Must Not Occur)

- Proceeding to Phase 2 despite verification failure
- Treating missing approvals as a warning and spawning agents anyway
- Only checking for missing entries without checking SHA matches
- Halting with a generic error that does not name the failing story slugs

## Verification

The eval passes if:
- Phase 1 halts after `verify-approvals` returns non-zero
- The blocking output names both `story-b` and `story-c` explicitly
- The output does NOT flag `story-a` (its approval is current and SHA matches)
- No Phase 2 dev-agent spawn actions are taken
