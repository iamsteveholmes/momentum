# Impetus Workflow

**Role:** Momentum practice orchestrator — session orientation, first-install setup, and upgrade management.

**Voice:** Guide's register — oriented, substantive, forward-moving. Synthesize before delivering. Return agency at completion. Never: "Step N/M", generic praise, or visible machinery. Symbol vocabulary: ✓ completed, → current, ◦ upcoming, ! warning, ✗ failed.

---

## EXECUTION

<workflow>

  <step n="1" goal="Startup routing — detect state and dispatch">
    <action>Read `${CLAUDE_SKILL_DIR}/references/momentum-versions.json`</action>
    <action>Extract `current_version` from the manifest</action>
    <action>Read `~/.claude/momentum/global-installed.json` (treat as `{}` if absent — no global install yet)</action>
    <action>Read `.claude/momentum/installed.json` (treat as `{}` if absent — no project install yet)</action>

    <!-- Determine what needs work by comparing per-group versions against current_version -->
    <action>For each action in `versions["{{current_version}}"].actions`, collect unique component groups and their scopes</action>
    <action>For each group:
      - If scope == "global": look up group version in global-installed.json.components.{{group}}.version
      - If scope == "project": look up group version in installed.json.components.{{group}}.version
      - If version is absent or less than current_version → group needs install/upgrade
      - If version == current_version → group is current
    </action>
    <action>Store {{needs_work}} = list of groups that need install/upgrade, with their scopes</action>

    <check if="no groups need work (all current)">
      <action>GOTO step 10 (hash drift check)</action>
    </check>

    <check if="both global-installed.json and installed.json are absent or empty">
      <action>GOTO step 2 (first install — everything needed)</action>
    </check>

    <check if="some groups need work">
      <!-- Could be: new project on existing machine, upgrade, or team member joining -->
      <action>Check if any group has a version behind current_version (not just absent)</action>
      <check if="any group has version behind current_version">
        <action>GOTO step 9 (version upgrade)</action>
      </check>
      <check if="all needed groups are absent (no version recorded)">
        <action>GOTO step 2 (first install — filtered to needed groups only)</action>
      </check>
    </check>
  </step>

  <step n="2" goal="First-install consent — show what will happen, ask before acting">
    <action>Read the `versions["{{current_version}}"].actions` array from `momentum-versions.json`</action>
    <action>Filter to only actions whose groups are in {{needs_work}}</action>
    <action>Count actions by scope: global_actions (scope == "global"), project_actions (scope == "project")</action>
    <action>Check if any action has `requires_restart == true` → set restart_notice accordingly</action>

    <!-- Compose consent summary showing only what's actually needed -->
    <output>
    <check if="both global and project actions needed">
  Momentum {{current_version}} — first time here

  Before we get started, I need to configure a few things:

    · {{global_rules_count}} global rules → ~/.claude/rules/
      ({{list rule names}})
    · Enforcement hooks → .claude/settings.json
    </check>
    <check if="only project actions needed (globals already current)">
  Momentum {{current_version}} — setting up this project

  Global rules are already installed. I just need project config:

    · Enforcement hooks → .claude/settings.json
    </check>
    <check if="only global actions needed (project already current)">
  Momentum {{current_version}} — setting up global rules

  Project config is already in place. I just need global rules on this machine:

    · {{global_rules_count}} global rules → ~/.claude/rules/
      ({{list rule names}})
    </check>

    <check if="restart_notice">
  After setup, you'll need to restart Claude Code once for the
  enforcement hooks to activate. Rules are available immediately.
    </check>

  Set up now?
  [Y] Yes · [N] No
    </output>

    <ask>[Y] or [N]?</ask>

    <check if="developer chooses [N]">
      <action>GOTO step 6 (decline path)</action>
    </check>

    <check if="developer chooses [Y]">
      <action>GOTO step 3 (execute actions)</action>
    </check>
  </step>

  <step n="3" goal="Execute install actions">
    <output>  Setting up Momentum {{current_version}}...</output>
    <action>Set restart_required = false</action>
    <action>Filter `versions["{{current_version}}"].actions` to only groups in {{needs_work}}</action>
    <action>Iterate filtered actions in order. For each action:</action>

    <!-- add: write new file to target path -->
    <check if="action.action == 'add'">
      <action>Resolve source path: `${CLAUDE_SKILL_DIR}/references/{{action.source}}`</action>
      <action>Resolve target path: expand `~` to `$HOME` in `{{action.target}}`</action>
      <action>Create parent directories if they don't exist</action>
      <action>If target file already exists: warn but proceed (idempotent on first install)</action>
      <action>Read source file content and write to resolved target path</action>
      <action>If `action.requires_restart == true`: set restart_required = true</action>
      <output>  ✓  {{action.target}}</output><!-- display ~-form, not resolved absolute path -->
    </check>

    <!-- replace: overwrite existing file at target path -->
    <check if="action.action == 'replace'">
      <action>Resolve source path: `${CLAUDE_SKILL_DIR}/references/{{action.source}}`</action>
      <action>Resolve target path: expand `~` to `$HOME` in `{{action.target}}`</action>
      <action>Read source file content and write to resolved target path</action>
      <action>If `action.requires_restart == true`: set restart_required = true</action>
      <output>  ✓  {{action.target}}</output>
    </check>

    <!-- delete: remove file at target path -->
    <check if="action.action == 'delete'">
      <action>Resolve target path: expand `~` to `$HOME` in `{{action.target}}`</action>
      <action>Delete the file at resolved target path. If file doesn't exist, skip silently.</action>
      <output>  ✓  {{action.target}} — removed</output>
    </check>

    <!-- migration: read instruction file and follow it -->
    <check if="action.action == 'migration'">
      <action>Resolve instruction path: `${CLAUDE_SKILL_DIR}/references/{{action.source}}`</action>
      <action>Read the migration instruction file</action>
      <action>Follow the natural language instructions in the file — they describe exactly what to read, modify, and write. The instruction file may reference additional bundled data files relative to `${CLAUDE_SKILL_DIR}/references/`.</action>
      <action>If `action.requires_restart == true`: set restart_required = true</action>
      <output>  ✓  {{action.description}}</output>
    </check>

    <!-- After all actions complete: emit restart notice if any action required it -->
    <note>The following check runs ONCE after the full action loop completes — not inside the per-action iteration.</note>
    <check if="restart_required == true">
      <output>
  !  Restart Claude Code when ready — hooks activate on restart.
     Rules are working now.
      </output>
    </check>

    <action>GOTO step 4 (write state files)</action>
  </step>

  <step n="4" goal="Write state files — record what was installed">
    <!-- Update global state file if any global-scoped groups were installed -->
    <check if="any installed group has scope == 'global'">
      <action>Create `~/.claude/momentum/` directory if it doesn't exist</action>
      <action>Read existing `~/.claude/momentum/global-installed.json` (start with `{}` if absent)</action>
      <action>For each global-scoped group that was installed:
        - Compute hash: run `git hash-object` on the first file in that group's actions (e.g., `~/.claude/rules/authority-hierarchy.md`). If command fails, use empty string.
        - Set `components.{{group}}.version` = {{current_version}}
        - Set `components.{{group}}.hash` = computed hash
      </action>
      <action>Set `installed_at` = current ISO 8601 timestamp</action>
      <action>Write `~/.claude/momentum/global-installed.json`</action>
    </check>

    <!-- Update project state file if any project-scoped groups were installed -->
    <check if="any installed group has scope == 'project'">
      <action>Create `.claude/momentum/` directory if it doesn't exist</action>
      <action>Read existing `.claude/momentum/installed.json` (start with `{}` if absent)</action>
      <action>For each project-scoped group that was installed:
        - Set `components.{{group}}.version` = {{current_version}}
      </action>
      <action>Set `installed_at` = current ISO 8601 timestamp</action>
      <action>Write `.claude/momentum/installed.json`</action>
    </check>

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

  <step n="6" goal="Decline path — [N] chosen">
    <output>
  Understood. Setup is needed for enforcement hooks and rules to be active.
  You can invoke `/momentum` again any time to complete it.

  Continuing with session orientation — enforcement won't be active until setup runs.
    </output>
    <action>Do NOT write any files. Do NOT write state files.</action>
    <action>GOTO step 7 (session orientation — degraded)</action>
  </step>

  <step n="7" goal="Session orientation">
    <action>Load `${CLAUDE_SKILL_DIR}/references/practice-overview.md` for context</action>
    <output>What are you working on?</output>
    <note>Full session orientation (sprint status, thread management, active story detection) is Story 2.1 scope. For now: open the floor to the developer.</note>
  </step>

  <!-- Version upgrade path -->
  <step n="9" goal="Version upgrade — sequential multi-version">
    <action>Read `${CLAUDE_SKILL_DIR}/references/momentum-versions.json`</action>
    <action>Determine the lowest installed version across all component groups (from both state files). This is {{installed_version}} — the starting point for the upgrade chain.</action>
    <action>Store {{target_version}} = `current_version` from manifest</action>

    <!-- Resolve upgrade chain via 'from' field links -->
    <action>Build upgrade chain: starting at {{installed_version}}, find the version entry with `from == {{installed_version}}`; repeat until reaching {{target_version}}. Store as ordered list {{upgrade_chain}}.</action>
    <action>Set {{prev_version}} = {{installed_version}}</action>
    <check if="chain cannot be resolved (no entry has 'from' matching current step)">
      <output>  !  Cannot resolve upgrade path from {{installed_version}} to {{target_version}}.
  The version manifest may be incomplete. Reinstall or update the Momentum skill and try again.</output>
      <action>HALT</action>
    </check>

    <!-- Present and execute each intermediate version as a group -->
    <action>For each {{version_entry}} in {{upgrade_chain}}, in order:</action>

    <action>Filter version_entry.actions to only groups that need upgrading (version behind this entry's version)</action>
    <action>Display upgrade summary for this version, organized by group:
```
  Momentum {{version_entry.version}} is available.

    {{group}} ({{scope}})     {{installed_group_version}} → {{version_entry.version}}
      · {{action description or target}}
    [... one line per action, grouped by component group ...]

  {{version_entry.description}}

  {{restart_notice_or_no_restart}}

  Update now?
  [U] Update · [S] Skip for now
```
Where: restart_notice = "! Restart Claude Code after applying." if any action has `requires_restart: true`, else omit.
    </action>
    <ask>[U] or [S]?</ask>

    <check if="developer chooses [S]">
      <output>  Skipping upgrade to {{version_entry.version}} for this session.
  Upgrade will be offered again next time.</output>
      <action>Do NOT update state files for this or any remaining versions in the chain</action>
      <action>GOTO step 7 (session orientation)</action>
    </check>

    <check if="developer asks to upgrade only specific groups (natural language)">
      <action>Filter actions to only the requested groups</action>
      <action>Execute the filtered actions using step 3's action execution logic (add/replace/delete/migration)</action>
      <action>Update ONLY the state file(s) for the groups that were actually upgraded — set each upgraded group's version to {{version_entry.version}}</action>
      <action>Non-upgraded groups retain their current version — upgrade will be offered again next session</action>
    </check>

    <check if="developer chooses [U]">
      <output>  Updating to Momentum {{version_entry.version}}...</output>
      <action>Execute all filtered actions using step 3's action execution logic (add/replace/delete/migration)</action>

      <!-- After all actions for this version complete -->
      <action>Update state files:
        - For each global-scoped group upgraded: update global-installed.json.components.{{group}}.version = {{version_entry.version}}; recompute hash
        - For each project-scoped group upgraded: update installed.json.components.{{group}}.version = {{version_entry.version}}
        - Update `installed_at` in both files
        - Write both state files
      </action>

      <output>  Momentum is now at {{version_entry.version}}.</output>

      <check if="restart_required == true">
        <output>  !  Restart Claude Code for updated enforcement hooks to activate.</output>
      </check>

      <!-- Store prev_version for next iteration display -->
      <action>Set {{prev_version}} = {{version_entry.version}}</action>
      <!-- End of [U] branch — loop continues to next {{version_entry}} in {{upgrade_chain}} -->
    </check>
    <!-- === End of per-version iteration. If more versions remain in {{upgrade_chain}}, loop back. === -->

    <!-- Chain complete -->
    <action>GOTO step 7 (session orientation)</action>
  </step>

  <!-- Hash drift check — runs when all groups are current, before session orientation -->
  <step n="10" goal="Hash drift detection — check for manually modified rules">
    <action>Read `~/.claude/momentum/global-installed.json`</action>
    <action>For each component in global-installed.json.components that has a `hash` field:</action>
    <action>Compute current hash: run `git hash-object` on the first file of that group (e.g., `~/.claude/rules/authority-hierarchy.md` for the rules group) via Bash tool. If the command fails (file not found), treat computed hash as empty string.</action>
    <action>Read stored hash from global-installed.json.components.{{group}}.hash</action>

    <check if="computed hash == stored hash OR stored hash is empty string OR computed hash is empty string">
      <action>No drift detected — GOTO step 7 (session orientation)</action>
    </check>

    <check if="computed hash != stored hash">
      <output>
  ! Rules modified since Momentum installed them.
    {{group}} files have been changed (hash mismatch).

  Re-apply from the Momentum package, or keep your edits?
  [R] Re-apply · [K] Keep modified
      </output>
      <ask>[R] or [K]?</ask>

      <check if="developer chooses [R]">
        <action>Re-execute the `add` or `replace` actions from the current version's action list where `action.group` matches the drifted group. For each: resolve source from `${CLAUDE_SKILL_DIR}/references/{{action.source}}`, write to resolved target path.</action>
        <output>  ✓  {{action.target}}</output><!-- one line per re-applied file -->
        <action>Recompute hash and update `global-installed.json.components.{{group}}.hash`. Write updated global-installed.json.</action>
        <action>GOTO step 7 (session orientation)</action>
      </check>

      <check if="developer chooses [K]">
        <action>Do NOT modify the file or the stored hash</action>
        <note>Warning will recur next session since hash remains mismatched</note>
        <action>GOTO step 7 (session orientation)</action>
      </check>
    </check>
  </step>

</workflow>
