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
          <action>GOTO step 10 (hash drift check)</action>
        </check>
      </check>

      <check if="installed.momentum_version != current_version">
        <action>GOTO step 9 (version upgrade)</action>
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

  <step n="7" goal="Session orientation — read journal and dispatch">
    <action>Load `${CLAUDE_SKILL_DIR}/references/practice-overview.md` for context</action>
    <action>Read `.claude/momentum/journal.jsonl` (if it exists). Parse per `${CLAUDE_SKILL_DIR}/references/journal-schema.md`: read all lines, group by thread_id, take last entry per thread_id to get current state. Filter for `status: "open"`.</action>

    <check if="journal.jsonl does not exist OR has zero open threads">
      <action>Skip journal display entirely — no mention of threads or journal</action>
      <output>What are you working on?</output>
      <note>Empty journal path — go directly to normal session (Story 2.1 menu)</note>
    </check>

    <check if="one or more open threads exist">
      <action>GOTO step 11 (Session Journal Display)</action>
    </check>
  </step>

  <!-- Session Journal Display and Thread Management (Story 2.2) -->

  <step n="11" goal="Session Journal Display — show open threads">
    <action>Sort open threads by `last_active` descending (most recent first)</action>
    <action>For each thread, compute elapsed time since `last_active` (e.g., "2h ago", "yesterday", "5d ago")</action>
    <output>
  {{thread_count}} threads in progress:

    1.  {{thread_1.context_summary_short}}   {{thread_1.phase}}   {{thread_1.elapsed}}
    2.  {{thread_2.context_summary_short}}   {{thread_2.phase}}   {{thread_2.elapsed}}
    [... one line per open thread ...]

  Continue (1/2/...) or tell me what you need?
    </output>

    <action>GOTO step 12 (thread hygiene checks)</action>
  </step>

  <step n="12" goal="Thread hygiene — concurrent, dormant, unwieldy, dependencies">
    <!-- Multi-tab concurrent work detection (AC4) -->
    <action>For each open thread: if `last_active` is within the last 30 minutes, flag it</action>
    <check if="any thread was active within 30 minutes">
      <output>
  !  Thread "{{thread.context_summary_short}}" appears active in another tab ({{minutes}} minutes ago).
     Opening here may cause conflicts. Proceed anyway?
      </output>
      <note>Warn, never block — developer decides. If developer proceeds on same story, confirm before starting a competing thread.</note>
    </check>

    <!-- Dormant thread hygiene (AC5) -->
    <action>For each open thread: if `last_active` is more than 3 days ago, surface it</action>
    <check if="any thread is dormant (>3 days inactive)">
      <output>
  {{thread.context_summary}} — {{days}} days inactive.
  Close this thread? [Y] Yes · [N] Keep open
      </output>
      <note>One confirmation per dormant thread. If developer confirms: append a new entry to journal.jsonl with same thread_id and `status: "closed"`. Then regenerate journal-view.md.</note>
    </check>

    <!-- Dependency-satisfied notification (AC6) -->
    <action>For each open thread with `depends_on_thread` set: check if the depended-on thread has `status: "closed"`</action>
    <check if="any dependency is now satisfied">
      <output>
  The work "{{depended_thread.context_summary_short}}" that thread "{{waiting_thread.context_summary_short}}" was waiting on is complete — ready to continue?
      </output>
      <note>Developer decides whether to activate the waiting thread.</note>
    </check>

    <!-- Unwieldy journal triage (AC7) -->
    <check if="more than 5 open threads">
      <output>
  !  {{open_count}} open threads — consider a quick triage before starting new work.
  I'll surface each with status and age. Close any that are stale?
      </output>
      <note>If developer agrees: iterate each open thread showing status + age + one-action close option. Each closure = single confirmation, then append closed entry to journal.jsonl.</note>
    </check>

    <action>Wait for developer input — thread selection (by number), new work request, or hygiene response</action>

    <check if="developer selects a thread by number or says 'continue'">
      <action>GOTO step 13 (workflow resumability)</action>
    </check>
    <check if="developer requests new work or something not in the journal">
      <note>Proceed to normal session flow — developer has oriented and chosen to start fresh work.</note>
    </check>
  </step>

  <step n="13" goal="Workflow resumability — re-orient and resume selected thread">
    <action>Read selected thread's `current_step`, `last_action`, `context_summary`, and `phase`</action>
    <output>
  {{thread.context_summary}}.

  Continue from here, or restart this step?
    </output>
    <ask>Continue or restart?</ask>

    <check if="developer chooses continue">
      <action>Resume workflow at `current_step` — proceed with the next action in that workflow phase</action>
      <action>Update the thread's `last_active` timestamp by appending a new journal entry</action>
      <action>Regenerate `.claude/momentum/journal-view.md`</action>
    </check>
    <check if="developer chooses restart">
      <action>Reset to the beginning of the current phase — append a new journal entry with `current_step` set to the phase start</action>
      <action>Update `last_active` timestamp</action>
      <action>Regenerate `.claude/momentum/journal-view.md`</action>
      <action>Begin the phase from its first step</action>
    </check>
  </step>

  <step n="14" goal="Journal write and view regeneration">
    <note>This step describes the journal write protocol invoked whenever any workflow step needs to update journal state. It is not reached by linear flow — it is a shared procedure.</note>
    <action>Append a new JSON line to `.claude/momentum/journal.jsonl` with all required fields per `${CLAUDE_SKILL_DIR}/references/journal-schema.md`</action>
    <action>After append, regenerate `.claude/momentum/journal-view.md`:
      - Read all journal entries
      - Reconstruct current state per thread_id (last entry wins)
      - Render a markdown table with columns: Thread ID, Story, Phase, Last Action, Last Active, Status
      - Include all open threads and threads closed within the last 7 days
      - Write to `.claude/momentum/journal-view.md` (overwrite)</action>
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

  <!-- Version upgrade path (AC1) -->
  <step n="9" goal="Version upgrade — sequential multi-version">
    <action>Read `${CLAUDE_SKILL_DIR}/references/momentum-versions.json`</action>
    <action>Store {{installed_version}} = `installed.json.momentum_version`</action>
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

    <action>Display upgrade summary for this version:
```
  Momentum has been updated to {{version_entry.version}} — your project is configured for {{prev_version}}.

  Here's what changed and what I need to do:

    · {{action.source}} → {{action.target}}
    [... one line per action in version_entry.actions ...]

  {{version_entry.description}}

  {{restart_notice_or_no_restart}}

  Update now, or continue with {{prev_version}} for this session?
  [U] Update · [S] Skip for now
```
Where: `{{action_target_display}}` = expand `~` in action.target; restart_notice = "! Restart Claude Code after applying." if any action has `requires_restart: true`, else "No restart needed for these changes — they take effect immediately."
    </action>
    <ask>[U] or [S]?</ask>

    <check if="developer chooses [S]">
      <output>  Skipping upgrade to {{version_entry.version}} for this session.
  Upgrade will be offered again next time.</output>
      <action>Do NOT update installed.json for this or any remaining versions in the chain</action>
      <action>GOTO step 7 (session orientation)</action>
      <note>[S] exits the entire upgrade chain — remaining versions are also skipped. This is intentional: partial upgrades (applying 1.1.0 but skipping 1.2.0) would leave installed.json at an intermediate version, which is valid but may confuse users. A full skip is cleaner.</note>
    </check>

    <check if="developer chooses [U]">
      <output>  Updating to Momentum {{version_entry.version}}...</output>
      <action>Set restart_required = false</action>

      <!-- Execute each action in this version entry -->
      <action>For each action in {{version_entry.actions}}, in order:</action>

      <check if="action.action == 'write_file' OR action.action == 'update_file'">
        <action>Resolve source path: `${CLAUDE_SKILL_DIR}/references/{{action.source}}`</action>
        <action>Resolve target path: expand `~` to `$HOME` in `{{action.target}}`</action>
        <action>Create parent directories if they don't exist</action>
        <action>Read source file content and write to resolved target path (replace entirely)</action>
        <action>If `action.requires_restart == true`: set restart_required = true</action>
        <output>  ✓  {{action.target}}</output>
      </check>

      <check if="action.action == 'write_config' OR action.action == 'update_config'">
        <action>Read existing target file (start with `{}` if absent)</action>
        <action>Read `${CLAUDE_SKILL_DIR}/references/{{action.source}}`</action>
        <check if="action.target == '.claude/settings.json'">
          <action>For each hook event key in source hooks: if absent in existing → add; if exists → append Momentum entries not already present (match by `command`). Never remove existing keys.</action>
        </check>
        <check if="action.target != '.claude/settings.json'">
          <action>Merge: for each key in source, add to existing if absent; skip if already present</action>
        </check>
        <action>Write merged result to target — preserve ALL existing keys</action>
        <action>If `action.requires_restart == true`: set restart_required = true</action>
        <output>  ✓  {{action.target}}</output>
      </check>

      <!-- After all actions for this version complete -->
      <action>Update `installed.json`:
        - Set `momentum_version` = {{version_entry.version}}
        - Set `installed_at` = current ISO 8601 timestamp
        - For each component touched by this version's actions, update its `version` field to {{version_entry.version}}
        - Recompute hash for `rules-global` if any `write_file` action targets `~/.claude/rules/`: run `git hash-object ~/.claude/rules/authority-hierarchy.md`; update `components.rules-global.hash`
        - Write updated `installed.json`
      </action>

      <output>  Project is now on Momentum {{version_entry.version}}.</output>

      <check if="restart_required == true">
        <output>  !  Restart Claude Code for updated enforcement hooks to activate.</output>
      </check>

      <!-- Store prev_version for next iteration display -->
      <action>Set {{prev_version}} = {{version_entry.version}}</action>
      <!-- End of [U] branch — loop continues to next {{version_entry}} in {{upgrade_chain}} -->
    </check>
    <!-- === End of per-version iteration. If more versions remain in {{upgrade_chain}}, loop back to the display/consent block above. === -->

    <!-- Chain complete -->
    <action>GOTO step 7 (session orientation)</action>
  </step>

  <!-- Hash drift check (AC2) — runs on version-match path, before session orientation -->
  <!-- Note: Hash drift currently tracks only authority-hierarchy.md (the primary rules file).
       anti-patterns.md and model-routing.md are not hash-tracked. This matches the installed.json
       schema which stores a single hash for the rules-global component. Expanding to composite
       hash tracking across all rule files is a future enhancement. -->
  <step n="10" goal="Hash drift detection — check for manually modified rules">
    <action>Compute current hash: run `git hash-object ~/.claude/rules/authority-hierarchy.md` via Bash tool. If the command fails (file not found, not a git repo), treat computed hash as empty string.</action>
    <action>Read stored hash from `installed.json.components.rules-global.hash`</action>

    <check if="computed hash == stored hash OR stored hash is empty string OR computed hash is empty string">
      <action>No drift detected — GOTO step 7 (session orientation)</action>
    </check>

    <check if="computed hash != stored hash">
      <output>
  ! Rules modified since Momentum installed them.
    authority-hierarchy.md has been changed (hash mismatch).

  Re-apply from the Momentum package, or keep your edits?
  [R] Re-apply · [K] Keep modified
      </output>
      <ask>[R] or [K]?</ask>

      <check if="developer chooses [R]">
        <action>Re-execute the `write_file` actions from the current version's action list where `action.target` starts with `~/.claude/rules/`. For each: resolve source from `${CLAUDE_SKILL_DIR}/references/{{action.source}}`, write to resolved target path.</action>
        <output>  ✓  {{action.target}}</output><!-- one line per re-applied rules file -->
        <action>Recompute hash: run `git hash-object ~/.claude/rules/authority-hierarchy.md`</action>
        <action>Update `installed.json.components.rules-global.hash` with new hash. Write updated installed.json.</action>
        <action>GOTO step 7 (session orientation)</action>
      </check>

      <check if="developer chooses [K]">
        <action>Do NOT modify the rule file or the stored hash</action>
        <note>Warning will recur next session since hash remains mismatched</note>
        <action>GOTO step 7 (session orientation)</action>
      </check>
    </check>
  </step>

</workflow>
