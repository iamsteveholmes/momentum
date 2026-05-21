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
  <critical>Phase 4 auditor team: pure fan-out — NO TeamCreate, NO SendMessage. Spawn 3 auditors in parallel (foreground, one message), each returns structured findings as its final response. Orchestrator collects 3 findings blocks and passes them to a synthesizer agent that writes retro-transcript-audit.md. This is the correct shape per spawning-patterns.md: agents work independently and return results to the orchestrator.</critical>

  <team-composition>
    <phase name="auditor-team" step="4">
      <role name="auditor-human" spawning="individual" concurrency="parallel">
        Reads user-messages.jsonl. Returns human_findings JSON array as final response to orchestrator.
      </role>
      <role name="auditor-execution" spawning="individual" concurrency="parallel">
        Reads agent-summaries.jsonl and errors.jsonl. Returns execution_findings JSON array as final response to orchestrator.
      </role>
      <role name="auditor-review" spawning="individual" concurrency="parallel">
        Reads team-messages.jsonl. Returns review_findings JSON array as final response to orchestrator.
      </role>
      <role name="synthesizer" spawning="individual" concurrency="sequential">
        Receives all 3 findings blocks in prompt from orchestrator. Performs cross-cutting synthesis. Writes retro-transcript-audit.md.
      </role>
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
      4. Auditor team — fan-out 3 auditors (parallel), collect findings, spawn synthesizer to write findings doc
      5. Story stub creation — propose and approve actionable backlog items from findings
      5.5. Handoff to intake queue — write un-actioned findings to intake-queue.jsonl for next planning cycle
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
  <!-- PHASE 4: AUDITOR TEAM                                  -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="4" goal="Fan-out 3 auditors (parallel), collect findings, spawn synthesizer to write findings doc">
    <action>Update task 4 to in_progress</action>

    <note>Pure fan-out — no TeamCreate, no SendMessage. All 3 auditors run in parallel as foreground
    agents and return findings as structured text in their final response. The orchestrator collects
    all 3 findings blocks and passes them to a synthesizer agent that performs cross-cutting analysis
    and writes retro-transcript-audit.md. This is the correct spawning-patterns.md shape for independent
    parallel work with results collected by the orchestrator.</note>

    <action>Step 4a — Fan out 3 auditor Agent spawns in a single message (foreground, parallel).
    Each auditor reads its assigned extract files and returns all findings as its final text response.
    No SendMessage. No team_name. Results come back as tool return values to the orchestrator.

      **auditor-human** — System prompt:
      ```
      You are auditor-human for the {{sprint_slug}} retrospective.

      Read `{{audit_dir}}/user-messages.jsonl`. Each line is a JSON object with
      timestamp, session_file, content, and is_first_message fields.

      Large-file protocol (mandatory — follow before reading any file):
        1. Run `wc -l` on the file first to check its size.
        2. For files over 200 lines, read in 500-line chunks via Read offset/limit,
           or stream JSONL line-by-line via `python3`.
        3. Never attempt a full Read on these known-large files:
           agent-summaries.jsonl, errors.jsonl, prd.md, architecture.md, stories/index.json.
        4. If a Read fails with a token-limit error, do not retry the same read — narrow scope.

      Identify and categorize every notable pattern:
        - Corrections: user fixing agent behavior mid-task
        - Redirections: user changing approach or canceling agent work
        - Frustration signals: repeated asks, escalating tone, explicit complaints
        - Praise/approval: positive signals about what worked well
        - Decision points: human exercised judgment agents couldn't handle

      For each finding, record:
        - type (correction|redirection|frustration|praise|decision)
        - severity (high|medium|low)
        - quote or paraphrase of the message
        - what it reveals about practice gaps or strengths
        - recommendation (fix|keep|investigate)

      Return ALL findings as your final response in this exact format:
      HUMAN_FINDINGS_START
      [{"type":"correction","severity":"high","quote":"...","reveals":"...","recommendation":"fix"}, ...]
      HUMAN_FINDINGS_END

      Available tool: transcript-query.py for additional ad-hoc queries if needed:
        python3 {{transcript_query_path}} sql "SELECT ..." \
          --after {{sprint_started}} --before {{sprint_completed}}
      ```

      **auditor-execution** — System prompt:
      ```
      You are auditor-execution for the {{sprint_slug}} retrospective.

      Read:
        - `{{audit_dir}}/agent-summaries.jsonl` — per-subagent digests
        - `{{audit_dir}}/errors.jsonl` — tool errors (actual error indicators only)

      Large-file protocol (mandatory — follow before reading any file):
        1. Run `wc -l` on each file first to check its size.
        2. For files over 200 lines, read in 500-line chunks via Read offset/limit,
           or stream JSONL line-by-line via `python3`.
        3. Never attempt a full Read on these known-large files:
           agent-summaries.jsonl, errors.jsonl, prd.md, architecture.md, stories/index.json.
        4. If a Read fails with a token-limit error, do not retry the same read — narrow scope.

      Investigate patterns across the subagent population:
        - Duplication: multiple agents with identical or near-identical first prompts
        - Error recovery: which agents had high error counts, did they recover?
        - Tool efficiency: agents with high tool_results but low assistant_turns
        - Story iteration: stories with many dev agents (why did story X need N passes?)
        - Abandoned agents: agents with very low turn counts (< 3 assistant turns)

      Single-turn consolidator exception: some agent roles are designed to complete their
      full work in exactly one turn (receive inputs → process → return structured output → done).
      Examples: AVFL consolidator, retro synthesizer, format converters, result aggregators.
      Detection signal: single turn + non-empty output = consolidator pattern (correct behavior,
      do NOT flag). Single turn + empty output = anomaly (flag as abandoned).
      Do not flag single-turn consolidators as abandoned — flag only zero-turn or empty-output agents.

      For agents of interest, run ad-hoc queries via transcript-query.py sql "..." to
      investigate their full transcripts.

      For each finding, record:
        - type (duplication|error-pattern|efficiency|iteration|abandon)
        - affected agents or stories
        - evidence (counts, examples)
        - root cause hypothesis
        - recommendation (fix|keep|investigate)

      Return ALL findings as your final response in this exact format:
      EXECUTION_FINDINGS_START
      [{"type":"duplication","affected":"...","evidence":"...","hypothesis":"...","recommendation":"fix"}, ...]
      EXECUTION_FINDINGS_END

      Available tool: transcript-query.py for additional ad-hoc queries:
        python3 {{transcript_query_path}} sql "SELECT ..." \
          --after {{sprint_started}} --before {{sprint_completed}}
      ```

      **auditor-review** — System prompt:
      ```
      You are auditor-review for the {{sprint_slug}} retrospective.

      Read:
        - `{{audit_dir}}/team-messages.jsonl` — inter-agent SendMessage content
        - `{{audit_dir}}/agent-summaries.jsonl` — filter to review roles:
            agent_type containing "reviewer", "validator", "qa", "prompt-engineer"

      Large-file protocol (mandatory — follow before reading any file):
        1. Run `wc -l` on each file first to check its size.
        2. For files over 200 lines, read in 500-line chunks via Read offset/limit,
           or stream JSONL line-by-line via `python3`.
        3. Never attempt a full Read on these known-large files:
           agent-summaries.jsonl, errors.jsonl, prd.md, architecture.md, stories/index.json.
        4. If a Read fails with a token-limit error, do not retry the same read — narrow scope.

      Evaluate quality gate effectiveness:
        - Real issues caught: review findings that led to genuine fixes
        - False positives: review blocks that were overturned or unnecessary
        - Fix cycle quality: did fix passes converge or thrash?
        - Inter-agent coordination: clear handoffs, confusion, missing context
        - Reviewer prompt quality: were review agents well-instructed?

      For each finding, record:
        - type (real-catch|false-positive|thrash|coordination|prompt-quality)
        - evidence (message quotes, patterns)
        - impact on sprint velocity
        - recommendation (fix|keep|investigate)

      Return ALL findings as your final response in this exact format:
      REVIEW_FINDINGS_START
      [{"type":"real-catch","evidence":"...","impact":"...","recommendation":"fix"}, ...]
      REVIEW_FINDINGS_END
      ```
    </action>

    <action>Step 4b — Collect findings from the 3 auditor return values:
      - Extract the JSON array between HUMAN_FINDINGS_START / HUMAN_FINDINGS_END from auditor-human's output
      - Extract the JSON array between EXECUTION_FINDINGS_START / EXECUTION_FINDINGS_END from auditor-execution's output
      - Extract the JSON array between REVIEW_FINDINGS_START / REVIEW_FINDINGS_END from auditor-review's output
      Store as {{human_findings}}, {{execution_findings}}, {{review_findings}}.
    </action>

    <action>Step 4c — Spawn 1 synthesizer agent (foreground) that receives all findings in its prompt:

      **synthesizer** — System prompt:
      ```
      You are the synthesizer for the {{sprint_slug}} retrospective.

      You have received findings from 3 auditors:

      HUMAN FINDINGS:
      {{human_findings}}

      EXECUTION FINDINGS:
      {{execution_findings}}

      REVIEW FINDINGS:
      {{review_findings}}

      Perform a cross-cutting synthesis pass:
        - Identify themes that appear across multiple auditor reports
        - Prioritize findings by impact and actionability
        - Separate successes (preserve) from struggles (fix)

      Write the findings document to:
        `.momentum/sprints/{{sprint_slug}}/retro-transcript-audit.md`

      Document structure (required sections):

      # Sprint Transcript Audit — {{sprint_slug}}

      **Retro date:** {{today}}
      **Sprint completed:** {{sprint_completed}}
      **Data analyzed:** {{user_msg_count}} user messages | {{agent_count}} subagents | {{error_count}} errors | {{team_msg_count}} team messages

      ## Executive Summary
      [2-3 paragraph synthesis of the sprint — what happened, key themes, priority actions]

      ## What Worked Well
      [Each item: description, evidence, recommendation: KEEP]

      ## What Struggled
      [Each item: description, evidence, root cause, recommendation: FIX or INVESTIGATE]

      ## User Interventions
      [All corrections, redirections, frustration signals — with context and implications]

      ## Story-by-Story Analysis
      [For each story with notable patterns: what happened, iteration count, issues]

      ## Cross-Cutting Patterns
      [Themes that appear across human, execution, and review audits]

      ## Metrics
      | Metric | Value |
      |--------|-------|
      | User messages analyzed | {{user_msg_count}} |
      | Subagents analyzed | {{agent_count}} |
      | Tool errors detected | {{error_count}} |
      | Struggles identified | N |
      | Successes identified | N |
      | User interventions | N |
      | Cross-cutting patterns | N |

      ## Priority Action Items
      [Ranked list: item, priority (critical/high/medium/low), recommended story stub title]

      Each finding must include: what happened, evidence (quote or data), root cause, recommendation.
      ```
    </action>

    <check if="findings document written at `.momentum/sprints/{{sprint_slug}}/retro-transcript-audit.md`">
      <output>**Auditor team complete.** Findings document written:
  `.momentum/sprints/{{sprint_slug}}/retro-transcript-audit.md`</output>
    </check>

    <check if="findings document not found after synthesizer exits">
      <output>Warning: Synthesizer did not write findings document. Check agent logs.</output>
      <ask>Continue retro without findings document (story stubs will be manually specified)?</ask>
      <check if="developer says no">
        <action>HALT — investigate synthesizer failure.</action>
      </check>
    </check>

    <action>Update task 4 to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 5: STORY STUB CREATION                           -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="5" goal="Propose and approve story stubs from audit findings">
    <action>Update task 5 to in_progress</action>

    <action>Read `.momentum/sprints/{{sprint_slug}}/retro-transcript-audit.md`</action>
    <action>Extract all items under "Priority Action Items" section</action>

    <check if="no priority action items found">
      <output>No actionable items found in findings document. No story stubs to create.</output>
    </check>

    <check if="priority action items found">

      <action>For each priority action item, derive a story stub:
        {
          title: recommended story stub title from findings,
          epic_slug: "impetus-core" (for Momentum/practice findings) or appropriate project epic,
          status: "backlog",
          description: one-sentence summary of the finding,
          suggested_ac: bulleted acceptance criteria derived from the finding's recommendation
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

  <step n="5.5" goal="Write un-actioned retro findings to intake-queue.jsonl for next sprint planning">
    <action>Update task 5.5 to in_progress</action>

    <note>The intake-queue.jsonl is the unified artifact (per DEC-007) for cross-workflow
    handoffs. Retro writes `source: "retro"`, `kind: "handoff"` events so sprint-planning
    Step 1 can surface them without manual re-injection. Each finding carries feature-state
    transition context (DEC-005 D8) and failure-diagnosis framing (DEC-005 D7) when applicable.

    Write CLI: `python3 skills/momentum/scripts/momentum-tools.py intake-queue append --source retro --kind handoff ...`

    What goes into the queue:
      - Findings from the "Priority Action Items" section that were NOT stubbed
        (i.e., developer declined during Phase 5, or were low-priority observations worth watching)
      - Feature-state transitions observed during this retro (feature X regressed, feature Y ready
        for Done) — these carry `feature_state_transition` JSON
      - Specific failures diagnosed during auditor analysis (DEC-005 D7) — these carry
        `failure_diagnosis` JSON
      - Cross-cutting patterns the documenter elevated but which don't warrant immediate stub creation

    What DOES NOT go into the queue:
      - Stubs already approved and added to stories/index.json (Phase 5) — those are tracked there
      - The sprint-summary content — that stays in sprint-summary.md

    One event per finding. Use `python3 skills/momentum/scripts/momentum-tools.py intake-queue append` for each.</note>

    <action>Gather the items to hand off:
      1. From {{rejected_stubs}} (Phase 5 developer-declined stubs): these are un-actioned findings
         the developer chose not to stub but may want to revisit
      2. From Phase 4 findings: any feature-state transitions observed (DEC-005 D8) — features
         that regressed, partially advanced, or are candidates for Done/Shelved/Abandoned/Rejected
      3. From Phase 4 findings: any specific failures with diagnosed causes (DEC-005 D7)
      4. Any cross-cutting patterns from the documenter that aren't covered by approved stubs

      Store {{handoff_items}} = list of all items to write to queue
    </action>

    <check if="{{handoff_items}} is empty">
      <output>No un-actioned findings to hand off — all Priority Action Items were stubbed.</output>
      <action>Update task 5.5 to completed</action>
    </check>

    <check if="{{handoff_items}} is not empty">
      <output>{{handoff_items | length}} findings could carry forward to the next planning cycle:

{{#each handoff_items}}
  · {{title}}{{#if feature_slug}} (feature: {{feature_slug}}){{/if}}{{#if failure_diagnosis}} — failure diagnosed{{/if}}
{{/each}}

Carry these forward as handoff events in intake-queue.jsonl? (Y/N)</output>
      <ask>Approve handoff writes?</ask>
      <check if="developer declines">
        <output>Handoff skipped — no events written to intake-queue.jsonl.</output>
        <action>Update task 5.5 to completed</action>
      </check>

      <output>Writing {{handoff_items | length}} findings to intake-queue.jsonl...</output>

      <action>For each item in {{handoff_items}}, run one `python3 skills/momentum/scripts/momentum-tools.py intake-queue append` call:

        Required flags for every event:
          --source retro
          --kind handoff
          --title "{{item.title}}"
          --description "{{item.description}}"
          --sprint-slug "{{sprint_slug}}"

        Optional flags (include when the finding has this context):
          --feature-slug "{{item.feature_slug}}"            (when finding is tied to a feature)
          --story-type "{{item.suggested_story_type}}"      (when finding implies future story work)
          --feature-state-transition '{"feature_slug":"...","prior_state":"...","observed_state":"...","evidence":"..."}' (DEC-005 D8: feature state hygiene)
          --failure-diagnosis '{"attempted":"...","didnt_work":"...","learned":"..."}' (DEC-005 D7: failure naming)

        Example for a feature regression finding:
          python3 skills/momentum/scripts/momentum-tools.py intake-queue append \
            --source retro \
            --kind handoff \
            --title "M3 consistency regressed in sprint-2026-04-08" \
            --description "Material 3 design tokens are inconsistent across 3 surfaces that were previously aligned" \
            --sprint-slug "{{sprint_slug}}" \
            --feature-slug "material-3-design-system" \
            --story-type "defect" \
            --feature-state-transition '{"feature_slug":"material-3-design-system","prior_state":"partial","observed_state":"partial","evidence":"User reported token inconsistency in Settings, Profile, and Home screens"}'

        Example for a failure-diagnosis finding:
          python3 skills/momentum/scripts/momentum-tools.py intake-queue append \
            --source retro \
            --kind handoff \
            --title "E2E validator prompt produced false positives on UI stories" \
            --description "E2E validator repeatedly flagged valid UI states as failures due to overly strict selector assumptions" \
            --sprint-slug "{{sprint_slug}}" \
            --failure-diagnosis '{"attempted":"E2E validation via DOM selector matching","didnt_work":"Selectors assumed specific CSS class names that change with M3 theming","learned":"E2E specs must use semantic roles and aria-labels, not CSS classes"}'
      </action>

      <action>Verify all events were written:
        Run: `python3 skills/momentum/scripts/momentum-tools.py intake-queue list --source retro --kind handoff --status open`
        Confirm the returned count matches {{handoff_items | length}}
      </action>

      <output>Phase 5.5 complete — {{handoff_items | length}} findings written to intake-queue.jsonl:

{{#each handoff_items}}
  · {{title}} [{{#if feature_slug}}feature: {{feature_slug}}{{/if}}{{#if failure_diagnosis}} — failure diagnosed{{/if}}]
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

**Findings handed off:** {{handoff_items | length}} events written to intake-queue.jsonl (source: retro, kind: handoff)

**Sprint status:** closed (retro_run_at set to {{today}})

**Sprint summary:** `.momentum/sprints/{{sprint_slug}}/sprint-summary.md`

---
Review the findings document and backlog stubs when planning the next sprint.
Retro handoff items will surface automatically in sprint planning Step 1 (backlog synthesis).
</output>

    <action>Update task 6 to completed</action>
  </step>

</workflow>
