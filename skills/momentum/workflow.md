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

  <!-- ═══════════════════════════════════════════════════════════════════════
       COMPLETION SIGNALS AND PRODUCTIVE WAITING (Story 2.4)
       Steps 11-14: These steps are invoked by workflow steps that complete
       a story cycle, dispatch a subagent, or synthesize subagent results.
       They are not part of the linear startup flow above.
       ═══════════════════════════════════════════════════════════════════════ -->

  <step n="11" goal="Workflow completion — deliver completion signal" tag="invoked-at-completion">
    <note>Invoke this step whenever a story cycle, workflow, or major workflow step completes. The completion signal follows the format defined in `${CLAUDE_SKILL_DIR}/references/completion-signals.md` §1.</note>

    <action>Collect all files produced or modified during the completed work</action>
    <action>Compose a completion signal with three required components:</action>

    <output>
  ✓  [what completed] — [one-line summary]

  What was produced:
    · [path/to/file1] — [brief description]
    · [path/to/file2] — [brief description]

  This is yours to review and adjust. What's next?
    </output>

    <note>Edge cases — refer to `${CLAUDE_SKILL_DIR}/references/completion-signals.md` §1 Edge Cases:
    - No file output: state what was validated/configured, omit file list, keep ownership return
    - Partial completion: use `→` instead of `✓`, list what was produced so far, state what remains
    - Many files (>6): show the most important, offer to expand</note>

    <note>Progress indicator integration: at final completion, show `✓ Built: [all steps]` with no `◦ Next:` line. At intermediate completion, include `→ Now:` and `◦ Next:` lines per Story 2.3 format.</note>

    <note>Never include: generic praise, step-count format ("Step N/M"), visible machinery. Follow the voice rules from the workflow header.</note>
  </step>

  <step n="12" goal="Review dispatch — deliver summary then dispatch subagent" tag="invoked-at-review-dispatch">
    <note>Invoke this step when implementation completes and a review process (AVFL, code review, etc.) is being dispatched. The summary follows `${CLAUDE_SKILL_DIR}/references/completion-signals.md` §4.</note>

    <action>Before dispatching the review subagent, compose and deliver an implementation summary containing: files created/modified with descriptions, key decisions made, how work maps to acceptance criteria, any deviations or open questions</action>

    <output>
  I've kicked off the review. Here's what was built:

    · [file1] — [description]
    · [file2] — [description]

  Key decisions:
    · [decision — rationale]

  This covers [AC list]. [Note any gaps or partial coverage.]

  I'll have review findings shortly. Anything you want to flag before they come in?
    </output>

    <action>Dispatch the review subagent with `run_in_background: true`</action>
    <note>The summary IS the substantive content during the wait — it transitions naturally into productive waiting (step 13).</note>
  </step>

  <step n="13" goal="Productive waiting — maintain dialogue during background tasks" tag="invoked-during-background-dispatch">
    <note>Invoke this step whenever a subagent is dispatched with `run_in_background: true`. Dead air is a failure mode. Refer to `${CLAUDE_SKILL_DIR}/references/completion-signals.md` §2.</note>

    <action>After dispatching a background subagent, immediately respond to the developer</action>

    <check if="substantive discussion is available (implementation details, AC coverage, architectural context)">
      <action>Deliver implementation summary or offer same-topic discussion</action>
      <note>If step 12 (review dispatch) already delivered a summary, continue the discussion thread — don't repeat the summary. Offer to discuss decisions, preview next steps, or answer questions about the work.</note>
    </check>

    <check if="no substantive discussion is available">
      <action>Explicitly acknowledge the wait — never go silent</action>
      <output>The review is running — I'll have results shortly.</output>
    </check>

    <note>"Same topic" constraint: all dialogue during productive waiting must relate to the work just completed, ACs being verified, architectural context, or what comes next. Never pivot to unrelated subjects.</note>
  </step>

  <step n="14" goal="Subagent result synthesis — process and present findings" tag="invoked-when-subagent-returns">
    <note>Invoke this step when a subagent returns results. Synthesize per `${CLAUDE_SKILL_DIR}/references/completion-signals.md` §3 and §5. Hub-and-spoke contract: subagent identity never surfaces.</note>

    <action>Read the subagent's structured JSON result: `{status, result, question, confidence}`</action>
    <action>Never present raw JSON to the developer</action>

    <!-- Tiered review depth: lead with micro-summary, offer depth -->
    <action>Compose a micro-summary: 1-3 sentences covering finding count (critical vs. minor), key outcomes, overall assessment</action>
    <action>Offer tiered review depth as a natural question — not a coded menu:</action>
    <output>
  [micro-summary — e.g., "The review found 2 items worth noting — one needs attention, one is minor."]
  Want me to walk through them, or are you good to continue?
    </output>

    <note>Three tiers the developer can choose (expressed in natural language):
    - Quick scan: the micro-summary is sufficient, move on
    - Full review: "Walk me through them" / "Show me the details"
    - Trust & continue: "Looks good, let's keep going"</note>

    <!-- When full review is selected: expand findings -->
    <check if="developer requests full review">
      <action>Present each finding with severity indicator and confidence-directed language:</action>
      <note>Severity indicators: `!` for critical/blocking, `·` for minor/informational</note>
      <note>Confidence-directed language (vary phrasing — avoid robotic repetition):
      - High confidence: "This comes directly from the architecture" / "The PRD specifies this explicitly"
      - Medium confidence: "Inferred from the architecture patterns — worth verifying" / "This follows from the design, though not stated explicitly"
      - Low confidence: surface as a question — "I'm not sure about this one — how do you want to handle it?"</note>
    </check>

    <!-- Flywheel integration for critical findings -->
    <check if="any finding has ! severity (critical)">
      <action>Check whether `momentum-upstream-fix` skill is available</action>
      <check if="momentum-upstream-fix is available">
        <action>Offer flywheel trace: "This looks like it could be traced upstream. Want me to run a flywheel trace?"</action>
      </check>
      <check if="momentum-upstream-fix is NOT available">
        <action>Include deferral note naturally in synthesis: "(flywheel processing deferred — Epic 6)"</action>
      </check>
    </check>

    <!-- Hub-and-spoke enforcement -->
    <note>Voice rules for synthesis — always: "the review found" / "I found" / "one issue to address". Never: subagent names, tool names, "the code reviewer said", "the VFL agent found", or any agent identity.</note>

    <!-- Handle subagent question field -->
    <check if="subagent.question is non-null">
      <action>Surface the question to the developer in Impetus's voice — do not attribute it to the subagent</action>
    </check>

    <!-- Handle needs_input or blocked status -->
    <check if="subagent.status == 'needs_input'">
      <action>Surface the blocking question to the developer, explain what information is needed to proceed</action>
    </check>
    <check if="subagent.status == 'blocked'">
      <action>Explain the blocker clearly and ask the developer how to proceed</action>
    </check>
  </step>

</workflow>
