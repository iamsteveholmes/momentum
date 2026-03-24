# Eval: Hash Drift Warning

## Scenario

Given all component groups are at `current_version` in both state files, but `~/.claude/momentum/global-installed.json` records `components.rules.hash: "abc123"` while the actual `git hash-object ~/.claude/rules/authority-hierarchy.md` returns `"def456"` (file was manually edited), when the developer invokes `/momentum`, the skill should:

1. Detect all groups are current (no upgrade path triggered)
2. Compute `git hash-object ~/.claude/rules/authority-hierarchy.md`
3. Compare computed hash against `global-installed.json.components.rules.hash`
4. Detect mismatch — surface warning:
   ```
   ! Rules modified since Momentum installed them.
     rules files have been changed (hash mismatch).

   Re-apply from the Momentum package, or keep your edits?
   [R] Re-apply · [K] Keep modified
   ```
5. On [R]: re-execute the `add`/`replace` actions for the rules group, recompute hash, update `global-installed.json`
6. On [K]: proceed to session orientation without modifying the rule file or the stored hash

## Expected Behavior

Hash drift is detected BEFORE session orientation. The warning clearly identifies which component group changed. The developer chooses to keep or re-apply. On [R], the file is overwritten with the bundled version and `global-installed.json` hash is updated. On [K], nothing is changed and the warning will appear again next session.

## NOT Expected

- Silently overwriting the developer's modified file without a warning
- Blocking session orientation when [K] is chosen
- Failing to detect the drift if `git hash-object` returns a different value
- Running hash drift detection during an upgrade (only runs when all groups are current)
- Reading hash from per-project installed.json (hash lives in global-installed.json)
