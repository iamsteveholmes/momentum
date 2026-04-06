# Retro Workflow

**Goal:** Close a completed sprint — read all agent logs, verify story completion, produce dual triage outputs, create story stubs from actionable findings, and call sprint closure commands.

**Invoked by:** Impetus Mode → "Run retrospective" or user runs `/momentum:retro` directly.

**Architecture references:** Decision 27 (Dual Triage Outputs), Decision 34 (Retro Owns Sprint Closure).

---

<workflow>
  <critical>Never write to sprints/index.json directly — all sprint state mutations go through momentum-tools.</critical>
  <critical>Story stubs require developer approval before being written to stories/index.json. Write stub entries directly to stories/index.json (no momentum-tools command exists for this operation).</critical>
  <critical>Log all retro events via `momentum-tools log --agent retro --sprint {{sprint_slug}}` at each phase transition.</critical>
  <critical>Use task tracking (TaskCreate/TaskUpdate) for retro phases — this prevents context drift in long runs.</critical>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 0: TASK TRACKING SETUP                           -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="0" goal="Initialize phase-level task tracking">
    <action>Create tasks for the 7 retro phases:
      1. Sprint identification — find the sprint to retro
      2. Log collection and correlation — read and sort all agent JSONL logs
      3. Story verification — check status of every sprint story
      4. Cross-log discovery — analyze timeline for patterns and findings
      5. Triage output generation — write momentum triage + project triage files
      6. Story stub creation — propose and approve actionable backlog items
      7. Sprint closure — call sprint complete + retro-complete, show summary
    </action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 1: SPRINT IDENTIFICATION                          -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="1" goal="Identify the sprint to retrospect">
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
    <action>Store {{sprint_completed}} = candidate.completed</action>

    <action>Log retro start:
      `momentum-tools log --agent retro --sprint {{sprint_slug}} --event decision --detail "Retrospective started for sprint {{sprint_slug}} (completed {{sprint_completed}})"`</action>

    <action>Update task 1 to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 2: LOG COLLECTION AND CORRELATION                 -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="2" goal="Read and correlate all agent JSONL logs">
    <action>Update task 2 to in_progress</action>

    <action>List all `.jsonl` files in `.claude/momentum/sprint-logs/{{sprint_slug}}/`</action>

    <check if="no log files found">
      <output>No agent logs found for sprint {{sprint_slug}} at `.claude/momentum/sprint-logs/{{sprint_slug}}/`.

The retrospective can continue without log data, but cross-log discovery will be limited to story status analysis only.</output>
      <ask>Continue without log data?</ask>
      <check if="developer says no">
        <action>HALT — developer can check log path or sprint slug.</action>
      </check>
      <action>Set {{log_events}} = [] (empty timeline)</action>
    </check>

    <check if="log files found">
      <action>For each `.jsonl` file:
        - Read all lines
        - Parse each line as JSON: {timestamp, agent, story, sprint, event, detail}
        - Append to a unified event list
      </action>
      <action>Sort all events by `timestamp` ascending — this produces a cross-agent chronological timeline</action>
      <action>Store {{log_events}} = sorted unified event list</action>
      <action>Store {{log_agents}} = distinct agent values found across all events</action>
      <output>Loaded {{log_events | length}} log events from {{log_files | length}} agent logs.
Agents active this sprint: {{log_agents | join(", ")}}</output>
    </check>

    <action>Log correlation complete:
      `momentum-tools log --agent retro --sprint {{sprint_slug}} --event decision --detail "Log correlation complete: {{log_events | length}} events from {{log_agents | length}} agents"`</action>

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
      <action>Log force-closed stories:
        `momentum-tools log --agent retro --sprint {{sprint_slug}} --event decision --detail "Force-closed incomplete stories: {{force_closed_slugs | join(', ')}}"`
      </action>
    </check>

    <action>Log story verification:
      `momentum-tools log --agent retro --sprint {{sprint_slug}} --event decision --detail "Story verification: {{verified_stories | length}} done, {{incomplete_stories | length}} incomplete"`</action>

    <action>Update task 3 to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 4: CROSS-LOG DISCOVERY                           -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="4" goal="Analyze the unified timeline for patterns and findings">
    <action>Update task 4 to in_progress</action>

    <action>Scan {{log_events}} for the following signal patterns:

      **Error and retry patterns** — sequences where an `error` event is followed by a `retry` event from the same agent within a short time window. Count repetitions. High repetition count suggests a process gap.

      **Wrong assumptions** — `assumption` events followed later by `error` or `finding` events from the same agent on the same story. These indicate the assumption was not validated early enough.

      **Ambiguity blockers** — `ambiguity` events. Each one represents a moment where an agent had to stop or guess due to unclear spec or context.

      **High-impact decisions** — `decision` events that appear to have downstream consequences (referenced in later events by story slug or keyword matching).

      **Unaddressed quality findings** — `finding` events that do not have a corresponding later `decision` event indicating resolution.
    </action>

    <action>For each pattern found, record a discovery item:
      {
        type: "error-retry" | "wrong-assumption" | "ambiguity-blocker" | "high-impact-decision" | "unresolved-finding",
        agent: ...,
        story: ...,
        detail: ...,
        raw_events: [list of relevant event timestamps]
      }
    </action>

    <action>Store {{discoveries}} = list of all discovery items</action>

    <output>Cross-log discovery complete. Found {{discoveries | length}} items:
  · Error/retry patterns: {{error_retry_count}}
  · Wrong assumptions: {{wrong_assumption_count}}
  · Ambiguity blockers: {{ambiguity_count}}
  · High-impact decisions: {{high_impact_count}}
  · Unresolved findings: {{unresolved_count}}</output>

    <action>Log discovery:
      `momentum-tools log --agent retro --sprint {{sprint_slug}} --event finding --detail "Cross-log discovery: {{discoveries | length}} items found"`</action>

    <action>Update task 4 to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 5: TRIAGE OUTPUT GENERATION                       -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="5" goal="Classify discoveries into Momentum triage and Project triage">
    <action>Update task 5 to in_progress</action>

    <action>Classify each discovery in {{discoveries}} into one of two buckets:

      **Momentum triage** (practice/process improvements):
        - Workflow steps that failed repeatedly or caused retries
        - Agent behaviors that produced ambiguity
        - Sprint planning gaps (stories under-specified, missing context)
        - AVFL or team review misses
        - Tool or script issues in momentum-tools

      **Project triage** (code/spec/test improvements):
        - Architecture gaps uncovered during implementation
        - Test coverage holes
        - PRD or story spec inaccuracies
        - Integration or dependency issues
        - Documentation gaps
    </action>

    <action>Store {{momentum_findings}} = list of Momentum-classified items</action>
    <action>Store {{project_findings}} = list of Project-classified items</action>

    <action>Write Momentum triage file to:
      `_bmad-output/implementation-artifacts/sprints/{{sprint_slug}}/retro-momentum-triage.md`

      Format:
      ```
      # Momentum Triage — Sprint {{sprint_slug}}

      **Retro date:** {{today}}
      **Sprint completed:** {{sprint_completed}}

      ## Summary
      {{momentum_findings | length}} practice findings from cross-log analysis.

      ## Findings

      {{#each momentum_findings}}
      ### {{loop.index}}. {{type | humanize}} — {{agent}} / {{story}}

      **Detail:** {{detail}}
      **Evidence:** {{raw_events | length}} log event(s)
      **Suggested action:** [analyst fills in]

      ---
      {{/each}}
      ```
    </action>

    <action>Write Project triage file to:
      `_bmad-output/implementation-artifacts/sprints/{{sprint_slug}}/retro-project-triage.md`

      Format:
      ```
      # Project Triage — Sprint {{sprint_slug}}

      **Retro date:** {{today}}
      **Sprint completed:** {{sprint_completed}}

      ## Summary
      {{project_findings | length}} project findings from cross-log analysis.

      ## Findings

      {{#each project_findings}}
      ### {{loop.index}}. {{type | humanize}} — {{agent}} / {{story}}

      **Detail:** {{detail}}
      **Evidence:** {{raw_events | length}} log event(s)
      **Suggested action:** [analyst fills in]

      ---
      {{/each}}
      ```
    </action>

    <output>Triage outputs written:
  · `_bmad-output/implementation-artifacts/sprints/{{sprint_slug}}/retro-momentum-triage.md` ({{momentum_findings | length}} findings)
  · `_bmad-output/implementation-artifacts/sprints/{{sprint_slug}}/retro-project-triage.md` ({{project_findings | length}} findings)
</output>

    <action>Log triage written:
      `momentum-tools log --agent retro --sprint {{sprint_slug}} --event decision --detail "Triage outputs written: {{momentum_findings | length}} momentum, {{project_findings | length}} project findings"`</action>

    <action>Update task 5 to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 6: STORY STUB CREATION                           -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="6" goal="Propose and approve story stubs for actionable findings">
    <action>Update task 6 to in_progress</action>

    <action>From {{momentum_findings}} and {{project_findings}}, identify actionable items:
      - Items that can be addressed as a discrete story
      - Each actionable item becomes a proposed story stub
    </action>

    <check if="no actionable items found">
      <output>No actionable items found in triage outputs. No story stubs to create.</output>
    </check>

    <check if="actionable items found">
      <action>For each actionable item, propose a story stub:
        {
          title: ...,
          epic_slug: "impetus-core" (for Momentum findings) or appropriate project epic (for Project findings),
          status: "backlog",
          description: one-sentence summary of the finding,
          suggested_ac: bulleted list of acceptance criteria derived from the finding
        }
      </action>

      <output>Proposed story stubs from retro findings:

{{#each proposed_stubs}}
**{{loop.index}}.** {{title}}
  Epic: {{epic_slug}}
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
        - Log stub creation: `momentum-tools log --agent retro --sprint {{sprint_slug}} --event decision --detail "Story stub created: {{slug}}"`
      </action>

      <output>Created {{approved_count}} story stubs in the backlog.</output>
    </check>

    <action>Log story stubs phase:
      `momentum-tools log --agent retro --sprint {{sprint_slug}} --event decision --detail "Story stub phase complete: {{approved_count}} approved, {{rejected_count}} rejected"`</action>

    <action>Update task 6 to completed</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 7: SPRINT CLOSURE                                 -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="7" goal="Call sprint closure commands and present final summary">
    <action>Update task 7 to in_progress</action>

    <action>Call sprint closure:
      `momentum-tools sprint complete`
    </action>

    <note>sprint complete transitions the active sprint to the completed list. If this sprint was already moved to completed by sprint-dev Phase 7, this command will report no active sprint — that is expected and safe to ignore.</note>

    <action>Call retro completion:
      `momentum-tools sprint retro-complete`
    </action>

    <action>Log sprint closure:
      `momentum-tools log --agent retro --sprint {{sprint_slug}} --event decision --detail "Sprint {{sprint_slug}} closed: sprint complete + retro-complete called"`</action>

    <output>## Retrospective Complete — Sprint {{sprint_slug}}

**Stories verified:** {{verified_stories | length}} / {{sprint_stories | length}} done
  {{#if incomplete_stories}}Stories closed-incomplete: {{force_closed_slugs | join(", ")}}{{/if}}

**Cross-log events analyzed:** {{log_events | length}} events from {{log_agents | length}} agents

**Findings:**
  · Momentum triage: {{momentum_findings | length}} practice findings
  · Project triage: {{project_findings | length}} project findings

**Story stubs created:** {{approved_count}} added to backlog

**Triage outputs:**
  · `_bmad-output/implementation-artifacts/sprints/{{sprint_slug}}/retro-momentum-triage.md`
  · `_bmad-output/implementation-artifacts/sprints/{{sprint_slug}}/retro-project-triage.md`

**Sprint status:** closed (retro_run_at set to {{today}})

---
Review the triage outputs and backlog stubs when planning the next sprint.
</output>

    <action>Update task 7 to completed</action>
  </step>

</workflow>
