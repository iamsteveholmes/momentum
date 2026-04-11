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
  <critical>Phase 4 auditor team uses TeamCreate — auditors and documenter collaborate via SendMessage during analysis. This is the collaborative team pattern, not independent fan-out.</critical>

  <team-composition>
    <phase name="auditor-team" step="4">
      <role name="auditor-human" spawning="team-create" concurrency="parallel">
        Reads user-messages.jsonl. Sends findings to documenter via SendMessage. Responds to documenter queries.
      </role>
      <role name="auditor-execution" spawning="team-create" concurrency="parallel">
        Reads agent-summaries.jsonl and errors.jsonl. Sends findings to documenter via SendMessage. Runs ad-hoc DuckDB queries on request.
      </role>
      <role name="auditor-review" spawning="team-create" concurrency="parallel">
        Reads team-messages.jsonl. Sends findings to documenter via SendMessage. Correlates with other auditor findings.
      </role>
      <role name="documenter" spawning="team-create" concurrency="parallel">
        Receives findings from all auditors. Evaluates, requests clarification, synthesizes. Owns retro-transcript-audit.md exclusively.
      </role>
    </phase>
  </team-composition>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 0: TASK TRACKING SETUP                           -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="0" goal="Initialize phase-level task tracking">
    <action>Create tasks for the 6 retro phases:
      1. Sprint identification — find the sprint to retro
      2. Transcript preprocessing — DuckDB extraction of session data into audit-extracts/
      3. Story verification — check status of every sprint story
      4. Auditor team — spawn 3 auditors + 1 documenter to analyze extracts and write findings
      5. Story stub creation — propose and approve actionable backlog items from findings
      6. Sprint closure — call sprint complete + retro-complete, show summary
    </action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 1: SPRINT IDENTIFICATION                          -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="1" goal="Identify the sprint to retrospect">
    <action>Update task 1 to in_progress</action>

    <action>Read `_bmad-output/implementation-artifacts/sprints/index.json`</action>
    <action>Search the `completed` array for entries where `retro_run_at == null`</action>

    <check if="no completed sprint with retro_run_at == null">
      <output>No sprint is awaiting a retrospective.

All completed sprints have already been retro'd, or no sprints have been completed yet.

To complete the active sprint first, run sprint-dev through Phase 7.</output>
      <action>HALT — nothing to retro.</action>
    </check>

    <check if="exactly one candidate found">
      <action>Store {{sprint_slug}} = candidate.slug</action>
      <output>Found sprint awaiting retrospective: **{{sprint_slug}}**
Completed: {{candidate.completed}}

Proceeding with retrospective for {{sprint_slug}}.</output>
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
    <action>Store {{audit_dir}} = `_bmad-output/implementation-artifacts/sprints/{{sprint_slug}}/audit-extracts`</action>

    <action>Update task 1 to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 2: TRANSCRIPT PREPROCESSING (DuckDB)             -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="2" goal="Extract session transcript data into audit-extracts/ via transcript-query.py">
    <action>Update task 2 to in_progress</action>

    <note>transcript-query.py lives at `skills/momentum/scripts/transcript-query.py`.
    It auto-installs duckdb if missing. It discovers sessions by date range using --after / --before.
    All errors use actual error indicators (is_error flag, success=false), not string matching.</note>

    <action>Ensure `{{audit_dir}}` directory exists:
      Create `_bmad-output/implementation-artifacts/sprints/{{sprint_slug}}/audit-extracts/` if absent</action>

    <action>Run 4 extraction commands (can run in parallel):

      **1. User messages** — all human-typed prompts across all sprint sessions:
      ```
      python3 skills/momentum/scripts/transcript-query.py user-messages \
        --after {{sprint_started}} --before {{sprint_completed}} \
        --format json \
        --output {{audit_dir}}/user-messages.jsonl
      ```

      **2. Agent summaries** — per-subagent digest (prompt, outcome, tool counts, error count):
      ```
      python3 skills/momentum/scripts/transcript-query.py agent-summary \
        --after {{sprint_started}} --before {{sprint_completed}} \
        --format json \
        --output {{audit_dir}}/agent-summaries.jsonl
      ```

      **3. Errors** — tool errors using actual error indicators only:
      ```
      python3 skills/momentum/scripts/transcript-query.py errors \
        --after {{sprint_started}} --before {{sprint_completed}} \
        --format json \
        --output {{audit_dir}}/errors.jsonl
      ```

      **4. Team messages** — inter-agent SendMessage and teammate-message content:
      ```
      python3 skills/momentum/scripts/transcript-query.py team-messages \
        --after {{sprint_started}} --before {{sprint_completed}} \
        --format json \
        --output {{audit_dir}}/team-messages.jsonl
      ```
    </action>

    <check if="all 4 extracts written successfully">
      <action>Count lines in each extract file:
        {{user_msg_count}} = line count of user-messages.jsonl
        {{agent_count}} = line count of agent-summaries.jsonl
        {{error_count}} = line count of errors.jsonl
        {{team_msg_count}} = line count of team-messages.jsonl
      </action>
      <output>Transcript preprocessing complete:
  · user-messages.jsonl — {{user_msg_count}} human prompts
  · agent-summaries.jsonl — {{agent_count}} subagent digests
  · errors.jsonl — {{error_count}} tool errors (actual error indicators only)
  · team-messages.jsonl — {{team_msg_count}} inter-agent messages

Extracts written to: {{audit_dir}}/
</output>
    </check>

    <check if="extraction produced empty results (no session files found)">
      <output>Warning: No session files found for sprint date range ({{sprint_started}} to {{sprint_completed}}).

The transcript audit will not have raw data to analyze. This may happen if:
  · The sprint ran in a different project directory
  · Session dates don't match the sprint's started/completed dates
  · Claude Code session files have been deleted

The retro can continue but auditor findings will be limited.</output>
      <ask>Continue with empty extracts?</ask>
      <check if="developer says no">
        <action>HALT — developer can investigate session file location and re-run.</action>
      </check>
    </check>

    <action>Update task 2 to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 3: STORY VERIFICATION                             -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="3" goal="Verify every sprint story reached done status">
    <action>Update task 3 to in_progress</action>

    <action>Read `_bmad-output/implementation-artifacts/stories/index.json`</action>
    <action>For each story slug in {{sprint_stories}}:
      - Look up status in stories/index.json
      - If status == "done": mark as verified
      - If status != "done": mark as incomplete, note current status
    </action>

    <action>Store {{verified_stories}} = list of stories with status "done"</action>
    <action>Store {{incomplete_stories}} = list of stories not at status "done" (with their current status)</action>

    <check if="{{incomplete_stories}} is empty">
      <output>All {{sprint_stories | length}} sprint stories reached `done`. Story verification passed.</output>
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

  <step n="4" goal="Spawn auditor team via TeamCreate — collaborative analysis of extracts">
    <action>Update task 4 to in_progress</action>

    <note>Spawn all 4 agents as a collaborative team via TeamCreate. Auditors read their assigned
    extract files, send findings to the documenter via SendMessage, and respond to documenter
    queries for clarification or deeper investigation. The documenter evaluates findings as they
    arrive, may request additional DuckDB queries, and writes the final findings document.
    This is the collaborative team pattern — auditors and documenter iterate together.</note>

    <action>Spawn 4 agents via TeamCreate:

      **auditor-human** — System prompt:
      ```
      You are auditor-human for the {{sprint_slug}} retrospective.

      Read `{{audit_dir}}/user-messages.jsonl`. Each line is a JSON object with
      timestamp, session_file, content, and is_first_message fields.

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

      Send findings to the documenter agent via SendMessage as you discover them.
      Format as JSON array under key "human_findings".
      Respond to any follow-up queries from the documenter — they may ask you to dig deeper.

      Available tool: transcript-query.py for additional ad-hoc queries if needed:
        python3 skills/momentum/scripts/transcript-query.py sql "SELECT ..." \
          --after {{sprint_started}} --before {{sprint_completed}}
      ```

      **auditor-execution** — System prompt:
      ```
      You are auditor-execution for the {{sprint_slug}} retrospective.

      Read:
        - `{{audit_dir}}/agent-summaries.jsonl` — per-subagent digests
        - `{{audit_dir}}/errors.jsonl` — tool errors (actual error indicators only)

      Investigate patterns across the subagent population:
        - Duplication: multiple agents with identical or near-identical first prompts
        - Error recovery: which agents had high error counts, did they recover?
        - Tool efficiency: agents with high tool_results but low assistant_turns
        - Story iteration: stories with many dev agents (why did story X need N passes?)
        - Abandoned agents: agents with very low turn counts (< 3 assistant turns)

      For agents of interest, run ad-hoc queries via transcript-query.py sql "..." to
      investigate their full transcripts.

      For each finding, record:
        - type (duplication|error-pattern|efficiency|iteration|abandon)
        - affected agents or stories
        - evidence (counts, examples)
        - root cause hypothesis
        - recommendation (fix|keep|investigate)

      Send findings to the documenter agent via SendMessage as you discover them.
      Format as JSON array under key "execution_findings".
      Respond to any follow-up queries from the documenter — they may ask you to dig deeper.
      ```

      **auditor-review** — System prompt:
      ```
      You are auditor-review for the {{sprint_slug}} retrospective.

      Read:
        - `{{audit_dir}}/team-messages.jsonl` — inter-agent SendMessage content
        - `{{audit_dir}}/agent-summaries.jsonl` — filter to review roles:
            agent_type containing "reviewer", "validator", "qa", "prompt-engineer"

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

      Send findings to the documenter agent via SendMessage as you discover them.
      Format as JSON array under key "review_findings".
      Respond to any follow-up queries from the documenter — they may ask you to dig deeper.
      ```

      **documenter** — System prompt:
      ```
      You are the documenter for the {{sprint_slug}} retrospective.

      Wait for SendMessage findings from 3 auditors:
        - auditor-human → "human_findings" JSON array
        - auditor-execution → "execution_findings" JSON array
        - auditor-review → "review_findings" JSON array

      As findings arrive:
        - Evaluate each finding for evidence quality and actionability
        - Ask auditors to dig deeper when evidence is thin (via SendMessage)
        - Identify cross-cutting themes as patterns emerge
        - Request additional DuckDB queries from auditors when correlations need verification

      After receiving and evaluating all findings, perform a cross-cutting synthesis pass:
        - Identify themes that appear across multiple auditor reports
        - Prioritize findings by impact and actionability
        - Separate successes (preserve) from struggles (fix)

      Write the findings document to:
        `_bmad-output/implementation-artifacts/sprints/{{sprint_slug}}/retro-transcript-audit.md`

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

    <action>Wait for the team to complete (documenter signals completion by writing the findings file)</action>

    <check if="findings document written at `_bmad-output/implementation-artifacts/sprints/{{sprint_slug}}/retro-transcript-audit.md`">
      <output>Auditor team complete. Findings document written:
  `_bmad-output/implementation-artifacts/sprints/{{sprint_slug}}/retro-transcript-audit.md`</output>
    </check>

    <check if="findings document not found after documenter exits">
      <output>Warning: Documenter did not write findings document. Check agent logs.</output>
      <ask>Continue retro without findings document (story stubs will be manually specified)?</ask>
      <check if="developer says no">
        <action>HALT — investigate auditor team failure.</action>
      </check>
    </check>

    <action>Update task 4 to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 5: STORY STUB CREATION                           -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="5" goal="Propose and approve story stubs from audit findings; route Tier 1 findings to distill">
    <action>Update task 5 to in_progress</action>

    <action>Read `_bmad-output/implementation-artifacts/sprints/{{sprint_slug}}/retro-transcript-audit.md`</action>
    <action>Extract all items under "Priority Action Items" section</action>

    <check if="no priority action items found">
      <output>No actionable items found in findings document. No story stubs to create.</output>
    </check>

    <check if="priority action items found">

      <note>Tier classification: Before creating story stubs, each action item is classified
      as Tier 1 or Tier 2. Tier 1 findings with signal_type set route to momentum:distill for
      immediate application. Tier 2 findings (and Tier 1 without signal_type) continue through
      the existing stub creation path.

      Tier 1 heuristic: single-sentence rule addition, one reference entry update, or a prompt
      clarification. One file, minimal change, immediately expressible in a sentence or two.
      Tier 2 heuristic: multi-file coordination, new skill creation, workflow redesign, or any
      change requiring spec-level deliberation.

      signal_type values (from Phase 4 classification): Context | Instruction | Workflow | Failure
      Tier 1 applies only when signal_type is set AND the finding meets Tier 1 heuristics above.</note>

      <action>For each priority action item, classify before routing:
        1. Check if signal_type is set on the finding (from Phase 4 audit output)
        2. Apply Tier heuristics:
           - Tier 1 candidates: signal_type is set AND change is a single-sentence rule, reference
             entry, or prompt clarification affecting one file
           - Tier 2: signal_type not set OR change is multi-file, new skill, workflow redesign,
             or any structural change

        Store {{distill_candidates}} = items classified as Tier 1 with signal_type set
        Store {{stub_candidates}} = remaining items (Tier 2, or Tier 1 without signal_type)
      </action>

      <check if="distill_candidates is not empty">
        <output>Tier 1 findings identified for immediate distillation ({{distill_candidates | length}} items):

{{#each distill_candidates}}
  · **{{loop.index}}.** {{title}} [signal_type: {{signal_type}}]
    Finding: {{source_detail}}
    Proposed change: {{recommended_change}}
{{/each}}

These will be routed to momentum:distill for immediate application instead of stub creation.</output>

        <action>For each Tier 1 finding in {{distill_candidates}}:
          1. Invoke `momentum:distill` as an inline subagent spawn with:
             - learning_description: the finding description + recommended change
             - candidate_artifact: the target practice file identified in the finding
             - source: "retro Phase 5 — Tier 1 routing"
             (Do not ask the developer to describe the learning — it is provided from the finding)
          2. Wait for distill to complete and return its outcome (applied | deferred | stubbed)
          3. Record disposition for this finding: "distilled" if applied, or distill's own outcome
        </action>

        <action>Store {{distilled_dispositions}} = map of finding → distill outcome for each Tier 1 item</action>
      </check>

      <check if="stub_candidates is not empty">
        <action>For each item in {{stub_candidates}}, derive a story stub:
          {
            title: recommended story stub title from findings,
            epic_slug: "impetus-core" (for Momentum/practice findings) or appropriate project epic,
            status: "backlog",
            description: one-sentence summary of the finding,
            suggested_ac: bulleted acceptance criteria derived from the finding's recommendation
          }
        </action>

        <output>Proposed story stubs (Tier 2 / no-signal-type findings):

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
          - Read `_bmad-output/implementation-artifacts/stories/index.json`
          - Generate a slug from the title (kebab-case)
          - Add entry: { "title": ..., "status": "backlog", "epic_slug": ..., "depends_on": [] }
          - Write updated stories/index.json
        </action>
      </check>

      <output>Phase 5 complete — action item dispositions:

{{#each distill_candidates}}
  · {{title}} → **distilled** ({{distilled_dispositions[title]}})
{{/each}}
{{#each approved_stubs}}
  · {{title}} → **stubbed** (added to backlog)
{{/each}}
{{#each rejected_stubs}}
  · {{title}} → skipped (developer declined)
{{/each}}

Distilled: {{distill_candidates | length}} | Stubbed: {{approved_count}} | Skipped: {{rejected_count}}</output>

    </check>

    <action>Update task 5 to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 6: SPRINT CLOSURE                                 -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="6" goal="Call sprint closure commands and present final summary">
    <action>Update task 6 to in_progress</action>

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
  `_bmad-output/implementation-artifacts/sprints/{{sprint_slug}}/retro-transcript-audit.md`

**Story stubs created:** {{approved_count}} added to backlog

**Sprint status:** closed (retro_run_at set to {{today}})

---
Review the findings document and backlog stubs when planning the next sprint.
</output>

    <action>Update task 6 to completed</action>
  </step>

</workflow>
