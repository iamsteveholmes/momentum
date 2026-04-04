# Eval: First Install — Consent and Execution

## Scenario

Given a developer has run `npx skills add` but neither `~/.claude/momentum/global-installed.json` nor `.claude/momentum/installed.json` exists, when they invoke `/momentum`, the skill should:

1. Read `${CLAUDE_SKILL_DIR}/references/momentum-versions.json` and detect `current_version`
2. Check both state files — detect all component groups need installation
3. Display the pre-consent summary showing exactly what will be written:
   - 3 global rules → `~/.claude/rules/`
   - Enforcement hooks → `.claude/settings.json`
4. Wait for explicit developer approval before writing anything — present [Y] / [N] options
5. Upon [Y] approval: execute all actions from the versions manifest (`add` for rules, `migration` for hooks), reporting each with ✓
6. Write `~/.claude/momentum/global-installed.json` with per-component-group versions and hashes for global groups
7. Write `.claude/momentum/installed.json` with per-component-group versions for project groups
8. Confirm exactly which files were written
9. Surface a restart notice because `requires_restart: true` on the hooks migration

## Expected Behavior

The skill shows the consent summary BEFORE writing any files, waits for input, then executes actions one by one with visible confirmation. Both state files are written after all actions complete. A restart notice appears.

## NOT Expected

- Writing files before consent is given
- Skipping the consent step
- Proceeding to session orientation without completing setup
- Offering to install global rules that already exist at the current version
