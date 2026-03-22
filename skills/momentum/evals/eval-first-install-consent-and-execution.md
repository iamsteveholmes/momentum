# Eval: First Install — Consent and Execution

## Scenario

Given a developer has run `npx skills add` but `.claude/momentum/installed.json` does NOT exist in the project, when they invoke `/momentum`, the skill should:

1. Read `${CLAUDE_SKILL_DIR}/references/momentum-versions.json` and detect `current_version`
2. Detect absence of `.claude/momentum/installed.json` — identify as first install
3. Display the pre-consent summary showing exactly what will be written:
   - 3 global rules → `~/.claude/rules/`
   - Enforcement hooks → `.claude/settings.json`
   - MCP servers → `.mcp.json`
4. Wait for explicit developer approval before writing anything — present [Y] / [S] options
5. Upon [Y] approval: execute all actions from the versions manifest, reporting each with ✓
6. Write `.claude/momentum/installed.json` with `momentum_version`, `installed_at`, and component hashes
7. Confirm exactly which files were written
8. Surface a restart notice because `requires_restart: true` on the hooks action

## Expected Behavior

The skill shows the consent summary BEFORE writing any files, waits for input, then executes actions one by one with visible confirmation. Installed.json is written after all actions complete. A restart notice appears.

## NOT Expected

- Writing files before consent is given
- Skipping the consent step
- Proceeding to session orientation without completing setup
