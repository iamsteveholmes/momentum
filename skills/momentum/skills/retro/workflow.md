# Retro Workflow

**Goal:** Close a completed sprint — run transcript audit, verify story completion, produce findings document, create story stubs from audit findings, and call sprint closure commands.

**Invoked by:** Impetus Mode → "Run retrospective" or user runs `/momentum:retro` directly.

**Architecture references:** Decision 27 (Findings Document), Decision 34 (Retro Owns Sprint Closure).

---

<workflow>
  <critical>Never write to sprints/index.json directly — all sprint state mutations go through momentum-tools.</critical>
  <critical>Story stubs require developer approval before being written to stories/index.json. Write stub entries directly to stories/index.json (no momentum-tools command exists for this operation).</critical>
  <critical>Transcript audit (Phases 2-3) is the primary data source. Milestone logs are NOT the critical path — retro proceeds and produces findings even when zero log events exist.</critical>
  <critical>Use task tracking (TaskCreate/TaskUpdate) for retro phases — this prevents context drift in long runs.</critical>
  <critical>Phase 4 is a single dynamic-Workflow call. The orchestrator does NOT hand-spawn auditors. It invokes the Workflow tool ONCE with `audit-workflow.js`, which fans out internally (Discover: parallel lens auditors + per-story analysts → Verify: per-finding adversarial refute panels → Synthesize: ONE agent writes retro-transcript-audit.md). The Workflow runs in the background and RETURNS ONCE — it performs NO human-in-the-loop. Every retro gate stays in this main-loop prose, bracketing the Workflow call.</critical>
  <critical>The audit Workflow is read-mostly: it writes only retro-transcript-audit.md. It MUST NOT mutate stories/index.json or sprints/index.json and MUST NOT call momentum-tools sprint transitions — those stay in the main loop (Phases 3, 5, 6).</critical>

  <team-composition>
    <phase name="audit-workflow" step="4">
      The Phase-4 fan-out lives inside `skills/momentum/skills/retro/audit-workflow.js`, not here. Its
      three internal phases: Discover (`parallel()` lens auditors: human, execution, review, efficiency,
      coordination — plus one per-story analyst per sprint story), Verify (`pipeline(findings,
      f => parallel([…skeptics]))` adversarial refute panels), Synthesize (a single `agent()` that writes
      retro-transcript-audit.md and returns the structured contract). The synthesize-stage singleton is
      structural — one `agent()` call, never looped or parallelized.
    </phase>
  </team-composition>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 0: TASK TRACKING SETUP                           -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="0" goal="Initialize phase-level task tracking">
    <action>Create tasks for the 7 retro phases:
      1. Sprint identification — find the sprint to retro
      2. Transcript preprocessing — DuckDB extraction of session data into audit-extracts/
      3. Story verification — check status of every sprint story
      4. Audit engine — invoke the audit Workflow (one Workflow-tool call); it fans out internally and returns structured findings + writes the findings doc
      5. Story stub creation — propose and approve actionable backlog items from findings
      5.5. Handoff to practice ledger — write un-actioned findings to practice-ledger.jsonl for next planning cycle
      6. Sprint closure — call sprint complete + retro-complete, show summary
    </action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 1: SPRINT IDENTIFICATION                          -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="1" goal="Identify the sprint to retrospect">
    <action>Update task 1 to in_progress</action>

    <action>Read `.momentum/sprints/index.json`</action>
    <action>Search the `completed` array for entries where `retro_run_at == null`</action>

    <check if="no completed sprint with retro_run_at == null">
      <output>No sprint is awaiting a retrospective.

All completed sprints have already been retro'd, or no sprints have been completed yet.

To complete the active sprint first, run sprint-dev through Phase 7.</output>
      <action>HALT — nothing to retro.</action>
    </check>

    <check if="exactly one candidate found">
      <action>Store {{sprint_slug}} = candidate.slug</action>
      <output>## Sprint Awaiting Retrospective: `{{sprint_slug}}`

**Completed:** {{candidate.completed}}

Proceeding with retrospective for `{{sprint_slug}}`.</output>
    </check>

    <check if="multiple candidates found">
      <output>Multiple completed sprints have not been retro'd:
{{#each candidates}}
  · {{slug}} — completed {{completed}}
{{/each}}

Which sprint should we retrospect?</output>
      <ask>Enter sprint slug:</ask>
      <action>Store {{sprint_slug}} = user selection</action>
    </check>

    <action>Store {{sprint_stories}} = candidate.stories (list of story slugs)</action>
    <action>Store {{sprint_started}} = candidate.started (ISO date for session discovery)</action>
    <action>Store {{sprint_completed}} = candidate.completed (ISO date for session discovery)</action>
    <action>Store {{audit_dir}} = `.momentum/sprints/{{sprint_slug}}/audit-extracts`</action>

    <action>Update task 1 to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 2: TRANSCRIPT PREPROCESSING (DuckDB)             -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="2" goal="Extract session transcript data into audit-extracts/ via transcript-query.py">
    <action>Update task 2 to in_progress</action>

    <note>transcript-query.py is resolved dynamically — the highest-semver plugin-cache copy wins,
    with an in-repo fallback for dogfood runs. It auto-installs duckdb if missing.
    It discovers sessions by date range (--after / --before) with UTC end-of-day inclusive semantics
    for --before. It also discovers sessions from git worktrees automatically.
    All errors use actual error indicators (is_error flag, success=false), not string matching.</note>

    <action>Resolve the script path (store as {{transcript_query_path}}):
      ```
      TRANSCRIPT_QUERY=$(ls -d ~/.claude/plugins/cache/momentum/momentum/*/scripts/transcript-query.py 2>/dev/null \
        | sort -V | tail -n1)
      [ -z "$TRANSCRIPT_QUERY" ] && [ -f skills/momentum/scripts/transcript-query.py ] \
        && TRANSCRIPT_QUERY=skills/momentum/scripts/transcript-query.py
      ```
      Store {{transcript_query_path}} = $TRANSCRIPT_QUERY
      Log the resolved path: "Using transcript-query.py at: {{transcript_query_path}}"
    </action>

    <action>Ensure `{{audit_dir}}` directory exists:
      Create `.momentum/sprints/{{sprint_slug}}/audit-extracts/` if absent</action>

    <action>Build the slug filter argument:
      If {{sprint_stories}} is non-empty: set {{slug_filter_arg}} = `--story-slugs "{{sprint_stories | join(',')}}"`
      If {{sprint_stories}} is empty: set {{slug_filter_arg}} = "" (omit the flag)
    </action>

    <action>Run 4 extraction commands (can run in parallel):

      **1. User messages** — all human-typed prompts across all sprint sessions:
      ```
      python3 {{transcript_query_path}} user-messages \
        --after {{sprint_started}} --before {{sprint_completed}} \
        {{slug_filter_arg}} \
        --format json \
        --output {{audit_dir}}/user-messages.jsonl
      ```

      **2. Agent summaries** — per-subagent digest (prompt, outcome, tool counts, error count):
      ```
      python3 {{transcript_query_path}} agent-summary \
        --after {{sprint_started}} --before {{sprint_completed}} \
        {{slug_filter_arg}} \
        --format json \
        --output {{audit_dir}}/agent-summaries.jsonl
      ```

      **3. Errors** — tool errors using actual error indicators only:
      ```
      python3 {{transcript_query_path}} errors \
        --after {{sprint_started}} --before {{sprint_completed}} \
        {{slug_filter_arg}} \
        --format json \
        --output {{audit_dir}}/errors.jsonl
      ```

      **4. Team messages** — inter-agent SendMessage and teammate-message content:
      ```
      python3 {{transcript_query_path}} team-messages \
        --after {{sprint_started}} --before {{sprint_completed}} \
        {{slug_filter_arg}} \
        --format json \
        --output {{audit_dir}}/team-messages.jsonl
      ```
    </action>

    <check if="all 4 extracts written successfully AND at least one session file was discovered">
      <action>Count lines in each extract file:
        {{user_msg_count}} = line count of user-messages.jsonl
        {{agent_count}} = line count of agent-summaries.jsonl
        {{error_count}} = line count of errors.jsonl
        {{team_msg_count}} = line count of team-messages.jsonl
      </action>
      <output>## Transcript Preprocessing Complete

- **`transcript-query.py` path:** `{{transcript_query_path}}`
- **`user-messages.jsonl`** — {{user_msg_count}} human prompts
- **`agent-summaries.jsonl`** — {{agent_count}} subagent digests
- **`errors.jsonl`** — {{error_count}} tool errors (actual error indicators only)
- **`team-messages.jsonl`** — {{team_msg_count}} inter-agent messages
{{#if slug_filter_arg}}- **Slug filter applied:** {{sprint_stories | join(', ')}}{{/if}}

**Extracts written to:** `{{audit_dir}}/`
</output>
    </check>

    <check if="extraction produced empty results (no session files found)">
      <output>ERROR: Retro for sprint "{{sprint_slug}}" found zero session files for date range {{sprint_started}} → {{sprint_completed}}.

Proceeding with empty extracts would produce false-positive audit findings. The retro is halted.

Investigate one of the following before re-running:
  · The sprint ran in a different project directory — session files may be elsewhere
  · Session dates don't match the sprint's started/completed dates — check sprint record
  · Claude Code session files have been deleted
  · transcript-query.py path could not be resolved: {{transcript_query_path}}

Re-run `momentum:retro` after resolving the session file location.</output>
      <action>HALT — do NOT spawn auditor team. Do NOT prompt developer to continue with empty extracts. The retro must stop here until the developer resolves the session file issue and re-runs.</action>
    </check>

    <action>Update task 2 to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 3: STORY VERIFICATION                             -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="3" goal="Verify every sprint story reached done status">
    <action>Update task 3 to in_progress</action>

    <action>Read `.momentum/stories/index.json`</action>
    <action>For each story slug in {{sprint_stories}}:
      - Look up status in stories/index.json
      - If status == "done": mark as verified
      - If status != "done": mark as incomplete, note current status
    </action>

    <action>Store {{verified_stories}} = list of stories with status "done"</action>
    <action>Store {{incomplete_stories}} = list of stories not at status "done" (with their current status)</action>

    <check if="{{incomplete_stories}} is empty">
      <output>> ✓ All **{{sprint_stories | length}} sprint stories** reached `done`. Story verification passed.</output>
    </check>

    <check if="{{incomplete_stories}} is not empty">
      <output>Some sprint stories did not reach `done`:

{{#each incomplete_stories}}
  · **{{slug}}** — current status: {{status}}
{{/each}}

For each of these, choose:
  F — Force-close as `closed-incomplete` (calls `momentum-tools sprint status-transition --story SLUG --target closed-incomplete`)
  I — Investigate (skip closure for now — story remains at current status)
</output>
      <ask>For each incomplete story, enter F or I (e.g. "retro-skill: F, sprint-planning: I"):</ask>

      <action>For each story where developer chose F:
        `momentum-tools sprint status-transition --story {{slug}} --target closed-incomplete`
      </action>
    </check>

    <action>Update task 3 to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 4: AUDIT ENGINE (dynamic Workflow)                                  -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="4" goal="Invoke the audit Workflow (one Workflow-tool call); consume its structured return">
    <action>Update task 4 to in_progress</action>

    <note>Phase 4 is a SINGLE dynamic-Workflow call. The Workflow runs in the background and returns
    ONCE — it does NO human-in-the-loop. The orchestrator does not hand-spawn auditors; the fan-out
    (Discover -> Verify -> Synthesize) lives inside audit-workflow.js (see the team-composition block).
    This step is reached only after the Phase 2 zero-session HALT has passed, so the Workflow never
    runs on empty extracts.</note>

    <action>Resolve the audit Workflow script path (store {{audit_workflow_path}}) — highest-semver
    plugin-cache copy wins, with an in-repo fallback for dogfood runs:
      ```
      AUDIT_WF=$(ls -d ~/.claude/plugins/cache/momentum/momentum/*/skills/retro/audit-workflow.js 2>/dev/null \
        | sort -V | tail -n1)
      [ -z "$AUDIT_WF" ] && [ -f skills/momentum/skills/retro/audit-workflow.js ] \
        && AUDIT_WF=skills/momentum/skills/retro/audit-workflow.js
      ```
      Store {{audit_workflow_path}} = $AUDIT_WF. Log: "Using audit-workflow.js at: {{audit_workflow_path}}".
    </action>

    <action>Invoke the **Workflow** tool EXACTLY ONCE (this is the explicit Workflow opt-in — do NOT
    fall back to hand-spawning Agent calls) with:
      - scriptPath: {{audit_workflow_path}}
      - args (a real JSON object, not a string):
        {
          "sprint_slug": "{{sprint_slug}}",
          "sprint_started": "{{sprint_started}}",
          "sprint_completed": "{{sprint_completed}}",
          "sprint_stories": {{sprint_stories}},
          "audit_dir": "{{audit_dir}}",
          "transcript_query_path": "{{transcript_query_path}}"
        }
    </action>

    <action>Bind the Workflow's structured return:
      {{priority_action_items}} = return.priority_action_items   (consumed by Phase 5)
      {{handoff_candidates}}    = return.handoff_candidates       (consumed by Phase 5.5)
      {{audit_metrics}}         = return.metrics
      {{audit_doc_path}}        = return.doc_path
      {{synthesize_status}}     = return.synthesize_status
      {{user_msg_count}}, {{agent_count}}, {{error_count}}, {{team_msg_count}} remain as bound in
      Phase 2 (authoritative extract line counts). Additionally bind {{struggle_count}} =
      audit_metrics.struggles and {{success_count}} = audit_metrics.successes for the Phase 6 summary.
    </action>

    <check if="{{synthesize_status}} == 'ok' AND a findings document exists at {{audit_doc_path}}">
      <output>**Audit engine complete.** Findings document written:
  `{{audit_doc_path}}`
  ({{struggle_count}} struggles, {{success_count}} successes; {{priority_action_items | length}} priority action items)</output>
    </check>

    <check if="{{synthesize_status}} != 'ok' OR {{audit_doc_path}} is null/absent">
      <output>Warning: the audit Workflow did not confirm a findings document (synthesize_status = {{synthesize_status}}). Inspect the run via `/workflows`.</output>
      <ask>Continue retro without a findings document (story stubs will be manually specified)?</ask>
      <check if="developer says no">
        <action>HALT — investigate the audit Workflow failure.</action>
      </check>
    </check>

    <action>Update task 4 to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 5: STORY STUB CREATION                           -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="5" goal="Propose and approve story stubs from audit findings">
    <action>Update task 5 to in_progress</action>

    <action>Use {{priority_action_items}} bound from the Phase 4 audit Workflow return (the structured
    list). Do NOT re-read or re-parse retro-transcript-audit.md — the returned contract is authoritative.
    Each item already carries: title, priority, source_detail, suggested_ac[], and optional epic_slug.</action>

    <check if="{{priority_action_items}} is empty">
      <output>No actionable items in the audit return. No story stubs to create.</output>
    </check>

    <check if="{{priority_action_items}} is non-empty">

      <action>For each item in {{priority_action_items}}, derive a story stub directly from its fields:
        {
          title: item.title,
          epic_slug: item.epic_slug (or "impetus-core" for Momentum/practice findings when absent),
          status: "backlog",
          description: item.source_detail (one-sentence summary),
          suggested_ac: item.suggested_ac
        }
      </action>

      <output>Proposed story stubs:

{{#each proposed_stubs}}
**{{loop.index}}.** {{title}}
  Epic: {{epic_slug}}
  Priority: {{priority}}
  Finding: {{source_detail}}
  Suggested ACs:
{{#each suggested_ac}}
  - {{this}}
{{/each}}

Approve this stub? (Y/N)
{{/each}}</output>

      <ask>For each stub, enter Y or N:</ask>

      <action>For each approved stub:
        - Read `.momentum/stories/index.json`
        - Generate a slug from the title (kebab-case)
        - Add entry: { "title": ..., "status": "backlog", "epic_slug": ..., "depends_on": [] }
        - Write updated stories/index.json
      </action>

      <output>Phase 5 complete — action item dispositions:

{{#each approved_stubs}}
  · {{title}} → **stubbed** (added to backlog)
{{/each}}
{{#each rejected_stubs}}
  · {{title}} → skipped (developer declined)
{{/each}}

Stubbed: {{approved_count}} | Skipped: {{rejected_count}}</output>

    </check>

    <action>Update task 5 to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 5.5: HANDOFF TO INTAKE QUEUE                      -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="5.5" goal="Write un-actioned retro findings to practice-ledger.jsonl for next sprint planning">
    <action>Update task 5.5 to in_progress</action>

    <note>The practice-ledger.jsonl is the unified event log (per DEC-033) for cross-workflow
    handoffs. Retro writes `source: "retro"`, `event_type: "created"` events with
    `payload.intent: "handoff"` so sprint-planning Step 1 can surface them via
    `practice-ledger by-source retro` without manual re-injection. Each finding carries
    feature-state transition context (DEC-005 D8) and failure-diagnosis framing (DEC-005 D7)
    when applicable.

    <!-- Migration note (DEC-033): the legacy --kind handoff flag is replaced by
         --event-type created + --payload '{"intent":"handoff"}'. The 'kind' field
         no longer exists in the DEC-033 schema. Handoff semantics are preserved via
         payload so sprint-planning can distinguish retro handoffs from other created
         events by filtering on source:retro + payload.intent:handoff. -->

    Write CLI: `python3 skills/momentum/scripts/momentum-tools.py practice-ledger append --source retro --event-type created --payload '{"intent":"handoff","origin_skill":"retro"}' ...`

    What goes into the ledger:
      - Findings from the "Priority Action Items" section that were NOT stubbed
        (i.e., developer declined during Phase 5, or were low-priority observations worth watching)
      - Feature-state transitions observed during this retro (feature X regressed, feature Y ready
        for Done) — these carry `feature_state_transition` JSON
      - Specific failures diagnosed during auditor analysis (DEC-005 D7) — these carry
        `failure_diagnosis` JSON
      - Cross-cutting patterns the audit surfaced but which don't warrant immediate stub creation

    What DOES NOT go into the ledger:
      - Stubs already approved and added to stories/index.json (Phase 5) — those are tracked there
      - The sprint-summary content — that stays in sprint-summary.md

    One event per finding. Use `python3 skills/momentum/scripts/momentum-tools.py practice-ledger append` for each.</note>

    <action>Gather the items to hand off:
      1. From {{rejected_stubs}} (Phase 5 developer-declined stubs): these are un-actioned findings
         the developer chose not to stub but may want to revisit
      2. From {{handoff_candidates}} (the Phase 4 audit Workflow return): feature-state transitions
         observed (DEC-005 D8) and specific failures with diagnosed causes (DEC-005 D7). Each item
         already carries title/slug/description plus optional epic_slug/failure_diagnosis/feature_state_transition.
      3. Any cross-cutting patterns surfaced by the audit that aren't covered by approved stubs

      Store {{handoff_items}} = list of all items to write to queue
    </action>

    <check if="{{handoff_items}} is empty">
      <output>No un-actioned findings to hand off — all Priority Action Items were stubbed.</output>
      <action>Update task 5.5 to completed</action>
    </check>

    <check if="{{handoff_items}} is not empty">
      <output>{{handoff_items | length}} findings could carry forward to the next planning cycle:

{{#each handoff_items}}
  · {{title}}{{#if epic_slug}} (epic: {{epic_slug}}){{/if}}{{#if failure_diagnosis}} — failure diagnosed{{/if}}
{{/each}}

Carry these forward as handoff events in practice-ledger.jsonl? (Y/N)</output>
      <ask>Approve handoff writes?</ask>
      <check if="developer declines">
        <output>Handoff skipped — no events written to practice-ledger.jsonl.</output>
        <action>Update task 5.5 to completed</action>
      </check>

      <output>Writing {{handoff_items | length}} findings to practice-ledger.jsonl...</output>

      <action>For each item in {{handoff_items}}, run one `python3 skills/momentum/scripts/momentum-tools.py practice-ledger append` call:

        Required flags for every event:
          --event-type created
          --entity-id "retro-{{sprint_slug}}-{{item.slug}}"
          --source retro
          --actor retro
          --payload '{"intent":"handoff","origin_skill":"retro","sprint_slug":"{{sprint_slug}}","title":"{{item.title}}","description":"{{item.description}}"}'

        Optional payload fields (include when the finding has this context — merge into --payload JSON):
          "epic_slug": "{{item.epic_slug}}"                 (when finding is tied to an epic)
          "story_type": "{{item.suggested_story_type}}"     (when finding implies future story work)
          "feature_state_transition": {"epic_slug":"...","prior_state":"...","observed_state":"...","evidence":"..."} (DEC-005 D8: feature state hygiene)
          "failure_diagnosis": {"attempted":"...","didnt_work":"...","learned":"..."}  (DEC-005 D7: failure naming)

        Example for a feature regression finding:
          python3 skills/momentum/scripts/momentum-tools.py practice-ledger append \
            --event-type created \
            --entity-id "retro-{{sprint_slug}}-m3-consistency" \
            --source retro \
            --actor retro \
            --payload '{"intent":"handoff","origin_skill":"retro","sprint_slug":"{{sprint_slug}}","title":"M3 consistency regressed in sprint-2026-04-08","description":"Material 3 design tokens are inconsistent across 3 surfaces that were previously aligned","epic_slug":"material-3-design-system","story_type":"defect","feature_state_transition":{"epic_slug":"material-3-design-system","prior_state":"partial","observed_state":"partial","evidence":"User reported token inconsistency in Settings, Profile, and Home screens"}}'

        Example for a failure-diagnosis finding:
          python3 skills/momentum/scripts/momentum-tools.py practice-ledger append \
            --event-type created \
            --entity-id "retro-{{sprint_slug}}-e2e-false-positives" \
            --source retro \
            --actor retro \
            --payload '{"intent":"handoff","origin_skill":"retro","sprint_slug":"{{sprint_slug}}","title":"E2E validator prompt produced false positives on UI stories","description":"E2E validator repeatedly flagged valid UI states as failures due to overly strict selector assumptions","failure_diagnosis":{"attempted":"E2E validation via DOM selector matching","didnt_work":"Selectors assumed specific CSS class names that change with M3 theming","learned":"E2E specs must use semantic roles and aria-labels, not CSS classes"}}'
      </action>

      <action>Verify all events were written:
        Run: `python3 skills/momentum/scripts/momentum-tools.py practice-ledger by-source retro`
        Filter results to entities where payload.intent == "handoff" and event is non-terminal.
        Confirm the returned count matches {{handoff_items | length}}
      </action>

      <output>Phase 5.5 complete — {{handoff_items | length}} findings written to practice-ledger.jsonl:

{{#each handoff_items}}
  · {{title}} [{{#if epic_slug}}epic: {{epic_slug}}{{/if}}{{#if failure_diagnosis}} — failure diagnosed{{/if}}]
{{/each}}

These will be surfaced automatically in the next sprint planning session (Step 1 — backlog synthesis).</output>

      <action>Update task 5.5 to completed</action>
    </check>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 6: SPRINT CLOSURE                                 -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="6" goal="Call sprint closure commands and present final summary">
    <action>Update task 6 to in_progress</action>

    <!-- ─── SPRINT SUMMARY PRODUCTION ─── -->

    <action>Invoke `momentum:feature-status` as a subagent to refresh `.claude/momentum/feature-status.md`
      and supply Features Advanced data for the sprint summary.
      This is the only delegation in Phase 6 — all other summary content is assembled inline.</action>

    <action>After `momentum:feature-status` completes (or if it fails), assemble the sprint summary:

      **Features Advanced section (conditional):**
      - If `momentum:feature-status` ran successfully AND `.claude/momentum/feature-status.md` exists:
        Include `## Features Advanced` section. List features whose status changed or advanced during
        this sprint, drawn from the feature-status output. If no changes found, write:
        "No features advanced this sprint."
      - If feature-status failed or file is absent: omit the `## Features Advanced` section entirely.

      **Stories Completed vs. Planned:**
      Count of stories that reached `done` out of {{sprint_stories | length}} originally planned.
      List any stories in {{force_closed_slugs}} (closed-incomplete) or still in progress at retro time.

      **Key Decisions:**
      Read decision files in `_bmad-output/planning-artifacts/decisions/`. Include decisions whose
      frontmatter `date` falls between {{sprint_started}} and {{sprint_completed}} (inclusive).
      Format each as: `- DEC-XXX: {title} ({date})`
      If none found, write: "No decisions recorded this sprint."

      **Unresolved Issues:**
      List story stubs added to backlog in Phase 5 (approved_count titles) plus any stories in
      {{force_closed_slugs}}. If none, write: "None."

      **Narrative:**
      Write a single paragraph (3–5 sentences) summarising what the sprint accomplished, the primary
      focus, and what changed in the practice or product as a result.

      **Word count enforcement:**
      After drafting, count total words. If over 500:
        1. Shorten the Narrative paragraph first
        2. Trim Key Decisions to most significant items
        3. Trim Stories list to most significant items
      The 500-word limit is a hard cap — summary is orientation, not a full report.
    </action>

    <action>Write the sprint summary to:
      `.momentum/sprints/{{sprint_slug}}/sprint-summary.md`

      Required structure (sections in this order):
      ```
      # Sprint Summary — {{sprint_slug}}

      **Sprint completed:** {{sprint_completed}}
      **Retro date:** {{today}}

      {## Features Advanced — ONLY include if feature-status ran and feature-status.md exists}

      ## Stories Completed vs. Planned
      ...

      ## Key Decisions
      ...

      ## Unresolved Issues
      ...

      ## Narrative
      [single paragraph, 3–5 sentences]
      ```
    </action>

    <!-- ─── END SPRINT SUMMARY PRODUCTION ─── -->

    <action>Call sprint closure:
      `momentum-tools sprint complete`
    </action>

    <note>sprint complete transitions the active sprint to the completed list. If this sprint was already moved to completed by sprint-dev Phase 7, this command will report no active sprint — that is expected and safe to ignore.</note>

    <action>Call retro completion:
      `momentum-tools sprint retro-complete`
    </action>

    <output>## Retrospective Complete — Sprint {{sprint_slug}}

**Stories verified:** {{verified_stories | length}} / {{sprint_stories | length}} done
  {{#if incomplete_stories}}Stories closed-incomplete: {{force_closed_slugs | join(", ")}}{{/if}}

**Transcript data analyzed:**
  · {{user_msg_count}} user messages
  · {{agent_count}} subagent digests
  · {{error_count}} tool errors (actual indicators)
  · {{team_msg_count}} inter-agent messages

**Findings document:**
  `.momentum/sprints/{{sprint_slug}}/retro-transcript-audit.md`

**Story stubs created:** {{approved_count}} added to backlog

**Findings handed off:** {{handoff_items | length}} events written to practice-ledger.jsonl (source: retro, event_type: created, intent: handoff)

**Sprint status:** closed (retro_run_at set to {{today}})

**Sprint summary:** `.momentum/sprints/{{sprint_slug}}/sprint-summary.md`

---
Review the findings document and backlog stubs when planning the next sprint.
Retro handoff items will surface automatically in sprint planning Step 1 (backlog synthesis).
</output>

    <action>Update task 6 to completed</action>
  </step>

</workflow>
