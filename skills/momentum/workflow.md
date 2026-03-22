# Impetus Workflow

**Role:** Momentum practice orchestrator — session orientation, first-install setup, and upgrade management.

**Voice:** Guide's register — oriented, substantive, forward-moving. Synthesize before delivering. Return agency at completion. Never: "Step N/M", generic praise, or visible machinery. Symbol vocabulary: ✓ completed, → current, ◦ upcoming, ! warning, ✗ failed.

---

## EXECUTION

<workflow>

  <step n="1" goal="Startup routing — detect state and dispatch">
    <action>Read `${CLAUDE_SKILL_DIR}/references/momentum-versions.json`</action>
    <action>Extract `current_version` from the manifest</action>

    <action>Check whether `.claude/momentum/installed.json` exists in the project root</action>

    <check if="installed.json does NOT exist">
      <action>GOTO step 2 (first install)</action>
    </check>

    <check if="installed.json exists">
      <action>Read `.claude/momentum/installed.json`</action>
      <action>Extract `momentum_version` from installed.json</action>

      <check if="installed.momentum_version == current_version">
        <!-- AC6: version matches, but check if global rules exist on this machine -->
        <action>Check whether `~/.claude/rules/authority-hierarchy.md` exists on this machine</action>
        <check if="~/.claude/rules/authority-hierarchy.md does NOT exist">
          <action>GOTO step 8 (team member joining — global-only setup)</action>
        </check>
        <check if="~/.claude/rules/authority-hierarchy.md exists">
          <action>GOTO step 7 (session orientation — setup current, skip install)</action>
        </check>
      </check>

      <check if="installed.momentum_version != current_version">
        <!-- Note: Dev Notes say "HALT here with message" for mismatch (Story 1.4 scope).
             Deliberate deviation: proceeding to session orientation after notice is better UX
             than a hard halt. Story 1.4 will implement full upgrade flow. -->
        <output>Momentum {{current_version}} is available — you're running {{installed.momentum_version}}.
Upgrade support is coming in a future release. For now, re-run setup manually if needed.</output>
        <action>GOTO step 7 (session orientation — degraded upgrade state)</action>
      </check>
    </check>
  </step>

  <step n="2" goal="First-install consent — show what will happen, ask before acting">
    <action>Read the `versions["{{current_version}}"].actions` array from `momentum-versions.json`</action>
    <action>Count write_file actions targeting `~/.claude/rules/` — these are the global rules</action>
    <action>Identify write_config actions and their targets</action>

    <output>
  Momentum {{current_version}} — first time here

  Before we get started, I need to configure a few things for this project:

    · {{rules_count}} global rules → ~/.claude/rules/
      (authority hierarchy, anti-patterns, model routing)
    · Enforcement hooks → .claude/settings.json

  After setup, you'll need to restart Claude Code once for the
  enforcement hooks to activate. Rules are available immediately.

  Set up now?
  [Y] Yes · [S] I'll handle it manually
    </output>

    <ask>[Y] or [S]?</ask>

    <check if="developer chooses [S]">
      <action>GOTO step 6 (decline path)</action>
    </check>

    <check if="developer chooses [Y]">
      <action>GOTO step 3 (execute actions)</action>
    </check>
  </step>

  <step n="3" goal="Execute install actions">
    <output>  Setting up Momentum {{current_version}}...</output>
    <action>Set restart_required = false</action>
    <action>Iterate `versions["{{current_version}}"].actions` in order. For each action:</action>

    <!-- write_file: copy bundled file to target path -->
    <check if="action.action == 'write_file'">
      <action>Resolve source path: `${CLAUDE_SKILL_DIR}/references/{{action.source}}`</action>
      <action>Resolve target path for file write: expand `~` to `$HOME` in `{{action.target}}`</action>
      <action>Create parent directories if they don't exist</action>
      <action>Read source file content and write to resolved target path</action>
      <action>If `action.requires_restart == true`: set restart_required = true</action>
      <output>  ✓  {{action.target}}</output><!-- display ~-form, not resolved absolute path -->
    </check>

    <!-- write_config for .claude/settings.json: merge, never overwrite -->
    <check if="action.action == 'write_config' AND action.target == '.claude/settings.json'">
      <action>Read existing `.claude/settings.json` (start with `{}` if absent)</action>
      <action>Read `${CLAUDE_SKILL_DIR}/references/{{action.source}}`</action>
      <action>For each hook event key in hooks-config (`PostToolUse`, `PreToolUse`, `Stop`):
        - If key absent in settings.json → add it entirely
        - If key exists → append only Momentum entries not already present (match by `command` value — never duplicate)
      </action>
      <action>Set `showTurnDuration: true` at root of settings object</action>
      <action>Write merged result to `.claude/settings.json` — preserve ALL existing keys</action>
      <action>If `action.requires_restart == true`: set restart_required = true</action>
      <output>  ✓  .claude/settings.json — enforcement hooks configured</output>
    </check>

    <!-- After all actions complete: emit restart notice if any action required it -->
    <note>The following check runs ONCE after the full action loop completes — not inside the per-action iteration.</note>
    <check if="restart_required == true">
      <output>
  !  Restart Claude Code when ready — hooks activate on restart.
     Rules are working now.
      </output>
    </check>

    <action>GOTO step 4 (write installed.json)</action>
  </step>

  <step n="4" goal="Write installed.json — record what was installed">
    <action>Create `.claude/momentum/` directory if it doesn't exist</action>
    <action>Compute hash for rules-global: run `git hash-object ~/.claude/rules/authority-hierarchy.md` via Bash tool. If git command fails (not a git repo or file not found), use empty string.</action>
    <action>Write `.claude/momentum/installed.json`:
```json
{
  "momentum_version": "{{current_version}}",
  "installed_at": "{{ISO_8601_timestamp}}",
  "components": {
    "rules-global": { "version": "{{current_version}}", "hash": "{{rules_hash}}" },
    "hooks":        { "version": "{{current_version}}" }
  }
}
```
    </action>
    <action>GOTO step 5 (verify git tracking)</action>
  </step>

  <step n="5" goal="Verify installed.json git tracking">
    <action>Check `.gitignore` does not contain an entry excluding `.claude/momentum/installed.json` or `.claude/momentum/`</action>
    <check if=".gitignore excludes installed.json">
      <output>  !  .gitignore excludes .claude/momentum/installed.json — removing exclusion so team members can detect project setup state.</output>
      <action>Remove or comment out the exclusion from .gitignore</action>
    </check>
    <action>GOTO step 7 (session orientation)</action>
  </step>

  <step n="6" goal="Decline path — [S] chosen">
    <output>
  Understood. Setup is needed for enforcement hooks and rules to be active.
  You can invoke `/momentum` again any time to complete it.

  Continuing with session orientation — enforcement won't be active until setup runs.
    </output>
    <action>Do NOT write any files. Do NOT write installed.json.</action>
    <action>GOTO step 7 (session orientation — degraded)</action>
  </step>

  <step n="7" goal="Session orientation">
    <action>Load `${CLAUDE_SKILL_DIR}/references/practice-overview.md` for context</action>
    <output>What are you working on?</output>
    <note>Full session orientation (sprint status, thread management, active story detection) is Story 2.1 scope. For now: open the floor to the developer.</note>
  </step>

  <!-- Team member joining path (AC6) -->
  <step n="8" goal="Team member joining — global-only setup" tag="invoked-from-step-1-variant">
    <note>This step handles the case where installed.json EXISTS but global rules are absent from this machine. It is not part of the main flow above — it is an alternative dispatch from step 1 when: installed.json found AND installed version matches current version AND ~/.claude/rules/ files are absent.</note>
    <action>Check if `~/.claude/rules/authority-hierarchy.md` exists</action>
    <check if="~/.claude/rules/authority-hierarchy.md exists">
      <action>Global rules present — GOTO step 7 (normal orientation)</action>
    </check>
    <check if="~/.claude/rules/authority-hierarchy.md does NOT exist">
      <output>
  I see you've cloned a project with Momentum configured.
  I need to set up a few global tools on your machine:

    · 3 global rules → ~/.claude/rules/

  Project config (hooks) is already committed to the repo.
  Set up global rules now? [Y] Yes · [S] Skip
      </output>
      <ask>[Y] or [S]?</ask>
      <check if="[Y]">
        <action>Execute only `write_file` actions from the manifest (skip `write_config` actions). For each: resolve source from `${CLAUDE_SKILL_DIR}/references/{{action.source}}`, write to resolved target path.</action>
        <output>  ✓  {{action.target}}</output><!-- ~-form display -->
        <action>GOTO step 7</action>
      </check>
      <check if="[S]">
        <action>GOTO step 7 (orientation without global rules)</action>
      </check>
    </check>
  </step>

</workflow>
