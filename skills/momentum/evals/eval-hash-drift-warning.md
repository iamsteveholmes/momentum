# Eval: Hash Drift Warning

## Scenario

Given a developer's project has `installed.json` with `momentum_version: "1.0.0"` (matching `current_version` — no upgrade needed) and `components.rules-global.hash: "abc123"`, but `~/.claude/rules/authority-hierarchy.md` has been manually edited so its current `git hash-object` output is `"def456"` (different from `"abc123"`), when they invoke `/momentum`, the skill should:

1. Detect versions match (no upgrade path triggered)
2. Compute `git hash-object ~/.claude/rules/authority-hierarchy.md`
3. Compare computed hash against `installed.json.components.rules-global.hash`
4. Detect mismatch — surface warning:
   ```
   ! Rules modified since Momentum installed them.
     authority-hierarchy.md has been changed (hash mismatch).

   Re-apply from the Momentum package, or keep your edits?
   [R] Re-apply · [K] Keep modified
   ```
5. On [R]: re-execute the `write_file` actions for rules, recompute hash, update `installed.json`
6. On [K]: proceed to session orientation without modifying the rule file or the stored hash

## Expected Behavior

Hash drift is detected BEFORE session orientation. The warning clearly identifies which file changed. The developer chooses to keep or re-apply. On [R], the file is overwritten with the bundled version and `installed.json` hash is updated. On [K], nothing is changed and the warning will appear again next session.

## NOT Expected

- Silently overwriting the developer's modified file without a warning
- Blocking session orientation when [K] is chosen
- Failing to detect the drift if `git hash-object` returns a different value
- Running hash drift detection during an upgrade (only runs on version-match path)
