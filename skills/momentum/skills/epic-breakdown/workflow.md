# Epic Breakdown Workflow

**Goal:** Given an epic slug, enumerate the stories needed to ship that epic end to end,
present a deduplicated gap list for developer review, and delegate approved items to
`momentum:triage` for classification and routing.

**Role:** Pure orchestrator — discovers gaps, synthesizes a list, gates on developer approval,
delegates all writes to triage and its downstream executors. Never writes to planning artifacts
directly.

**Voice:** Impetus voice — dry, confident, forward-moving. Symbol vocabulary:
✓ completed, → current, ◦ upcoming, ! warning, ✗ failed, · list item.

---

## Initialization

Load config from `_bmad/bmm/config.yaml`. Resolve:
- `planning_artifacts` — path to `_bmad-output/planning-artifacts/`
- `implementation_artifacts` — path to `.momentum/`

<check if="_bmad/bmm/config.yaml is missing OR planning_artifacts OR implementation_artifacts keys are unresolved">
  <output>✗ Configuration error: _bmad/bmm/config.yaml is missing or incomplete.
Required keys: planning_artifacts, implementation_artifacts.
Ensure _bmad/bmm/config.yaml exists and both keys resolve to valid paths before running epic-breakdown.</output>
  <action>HALT.</action>
</check>

Store {{planning_artifacts}} and {{implementation_artifacts}} for use throughout.

---

<workflow>

  <critical>Orchestrator purity: This workflow MUST NOT write files directly. No Write or Edit
  actions against epics.json, stories/index.json, prd.md, epics.md, architecture.md, or any
  file under _bmad-output/planning-artifacts/ or .momentum/stories/.
  All writes happen via delegated subagents — triage routes to intake / decision / practice-ledger,
  which own their respective writes. This orchestrator reads, synthesizes, gates, and delegates only.</critical>

  <critical>Developer review gate (Step 5) is mandatory before any delegation to triage. No items
  are handed off until the developer explicitly approves.</critical>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- STEP 1: LOAD EPIC CONTEXT                               -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="1" goal="Load epic context — validate slug and capture required fields">

    <check if="epic_slug was not provided as an argument">
      <ask>Which epic do you want to break down? Provide an epic slug from epics.json.
      (Run /momentum:epic-grooming to view available slugs.)</ask>
      <action>Store {{epic_slug}} = developer's response.</action>
    </check>

    <check if="epic_slug was provided as an argument">
      <action>Store {{epic_slug}} = the argument value.</action>
    </check>

    <action>Check for an optional focus hint (e.g., "ingestion-side only") that narrows the
    gap search scope. If provided as an argument or alongside the slug, store as {{focus_hint}}.
    Otherwise {{focus_hint}} = null.</action>

    <action>Read `{{planning_artifacts}}/epics.json`. If the file does not exist:
      output "✗ epics.json not found at {{planning_artifacts}}/epics.json — run
      /momentum:epic-grooming to initialize the epic taxonomy." and HALT.
    </action>

    <check if="{{epic_slug}} is NOT a key in epics.json">
      <output>✗ Epic slug "{{epic_slug}}" not found in epics.json.

Available slugs: {{list all keys from epics.json}}

Run /momentum:epic-grooming to view the full epic list or add new epics.</output>
      <action>HALT.</action>
    </check>

    <action>Extract from epics.json[{{epic_slug}}] and store:
      - {{acceptance_conditions}} — the epic's acceptance_conditions array (list of condition strings)
      - {{value_analysis}} — the full value_analysis block (including any "known gaps" paragraph)
      - {{system_context}} — the system_context field
      - {{epic_stories}} — the current stories array (list of story slugs)
      - {{stories_done}} — the stories_done count
      - {{stories_remaining}} — the stories_remaining count
      - {{lifecycle}} — the lifecycle field
    </action>

    <output>## Epic Loaded: `{{epic_slug}}`

**Lifecycle:** {{lifecycle}}
**Progress:** {{stories_done}} done / {{stories_remaining}} remaining
**Stories on epic:** {{epic_stories | length}} ({{epic_stories | join ", "}})
{{#if focus_hint}}**Focus hint:** {{focus_hint}}{{/if}}</output>

  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- STEP 2: LOAD SURROUNDING CONTEXT                        -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="2" goal="Load surrounding context — PRD, epics, architecture, stories index (scoped reads)">

    <note>prd.md, epics.md, and architecture.md are commonly large files. Always use offset/limit
    on Read calls — never attempt a full read. For stories/index.json, read the full file once
    and filter in-memory; do not paginate.</note>

    <action>Read `{{planning_artifacts}}/prd.md`:
      - Use Grep to find sections relevant to {{epic_slug}} or the epic's known themes.
      - Read those sections with offset/limit targeting the identified line ranges.
      - Store {{prd_context}} = relevant excerpts (functional requirements, goals, constraints).
    </action>

    <action>Read `{{planning_artifacts}}/epics.md`:
      - Use Grep to identify epic definitions related to {{epic_slug}}.
      - Read those sections with offset/limit.
      - Store {{epics_context}} = relevant epic descriptions.
    </action>

    <action>Read `{{planning_artifacts}}/architecture.md`:
      - Use Grep to find sections related to the epic's system_context or acceptance_conditions.
      - Read those sections with offset/limit.
      - Store {{architecture_context}} = relevant architectural components and constraints.
    </action>

    <action>Read `.momentum/stories/index.json`:
      - Read full file (use offset/limit chunks if large — read in 300-line pages until complete).
      - Filter in-memory: keep stories where epic_slug == {{epic_slug}},
        OR where the story slug is in {{epic_stories}}.
      - Store {{related_stories}} = filtered list of {slug, title, status, epic_slug}.
    </action>

    <output>## Surrounding Context Loaded

- **PRD:** relevant sections captured
- **Epics:** {{epics_context | count}} relevant epics
- **Architecture:** relevant components captured
- **Stories index:** {{related_stories | length}} related stories filtered</output>

  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- STEP 3: PARALLEL GAP ANALYSIS (FAN-OUT)                 -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="3" goal="Parallel gap analysis — spawn 2 agents in a single message (fan-out)">

    <critical>Spawn BOTH agents in a single message using individual Agent tool calls.
    Do NOT use TeamCreate. These agents work independently — each analyzes the epic
    from a different lens and returns findings to the orchestrator. They do not need to
    communicate with each other during execution.
    Per ~/.claude/rules/spawning-patterns.md: "Can each agent complete its work without
    talking to any other agent? Yes → Fan-out (individual Agent spawns)."</critical>

    <action>Spawn Agent A — Acceptance-first (model: claude-sonnet-4-6, effort: medium):

      System prompt:
      ```
      You are an acceptance-first gap analyst for a Momentum epic breakdown.

      Epic slug: {{epic_slug}}
      Acceptance conditions: {{acceptance_conditions}}
      System context: {{system_context}}
      Existing stories on epic: {{epic_stories}}
      Related stories (from this epic): {{related_stories}}
      PRD context: {{prd_context}}
      Architecture context: {{architecture_context}}
      {{#if focus_hint}}Focus hint (narrow your analysis to this scope): {{focus_hint}}{{/if}}

      Your job — Acceptance-first analysis:
      1. Decompose each entry in the acceptance_conditions array into concrete, testable
         capabilities that must exist for those conditions to be satisfied.
      2. For each capability, check whether it is already covered by a story in {{epic_stories}}
         or {{related_stories}} (match by title, description, or obvious intent).
      3. Flag capabilities that are NOT covered — these are your gap findings.

      For each gap finding, return:
      {
        "title": "<short capability title — max 8 words>",
        "description": "<one-line description of what is missing>",
        "suggested_class": "ARTIFACT" | "DECISION" | "SHAPING",
        "rationale": "<why this class>"
      }

      Return ONLY the structured findings list. Do not explain your process.
      Suggested class must be one of: ARTIFACT, DECISION, SHAPING.
      Do not suggest DEFER or REJECT — those are triage's routing decisions.
      ```
    </action>

    <action>Spawn Agent B — Value-gap-first (model: claude-sonnet-4-6, effort: medium):

      System prompt:
      ```
      You are a value-gap analyst for a Momentum epic breakdown.

      Epic slug: {{epic_slug}}
      Value analysis: {{value_analysis}}
      System context: {{system_context}}
      Existing stories on epic: {{epic_stories}}
      Related stories (from this epic): {{related_stories}}
      Epics context: {{epics_context}}
      Architecture context: {{architecture_context}}
      {{#if focus_hint}}Focus hint (narrow your analysis to this scope): {{focus_hint}}{{/if}}

      Your job — Value-gap-first analysis:
      1. Identify the "known gaps" paragraph in {{value_analysis}} if present.
         If no explicit gaps paragraph exists, treat the full value_analysis as your source.
      2. For each gap or value dimension described, identify what implementation work is
         required to close it — and check whether any story in {{epic_stories}} or
         {{related_stories}} already covers that work.
      3. Flag implementation work that is NOT covered — these are your gap findings.

      For each gap finding, return:
      {
        "title": "<short capability title — max 8 words>",
        "description": "<one-line description of what is missing>",
        "suggested_class": "ARTIFACT" | "DECISION" | "SHAPING",
        "rationale": "<why this class>"
      }

      Return ONLY the structured findings list. Do not explain your process.
      Suggested class must be one of: ARTIFACT, DECISION, SHAPING.
      Do not suggest DEFER or REJECT — those are triage's routing decisions.
      ```
    </action>

    <action>Wait for both agents to return. Store:
      {{agent_a_findings}} = Agent A's structured list
      {{agent_b_findings}} = Agent B's structured list
    </action>

    <output>## Gap Analysis Complete

- **Agent A** (Acceptance-first): {{agent_a_findings | length}} findings
- **Agent B** (Value-gap-first): {{agent_b_findings | length}} findings</output>

  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- STEP 4: SYNTHESIZE GAP LIST                             -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="4" goal="Synthesize — merge, deduplicate, produce structured gap list">

    <action>Merge {{agent_a_findings}} and {{agent_b_findings}} into a combined list.
    Tag each item with its source: "A", "B", or "both".
    </action>

    <action>Deduplicate: items describing the same capability under different titles are
    merged into one entry. When merging:
      - Use the more descriptive title
      - Combine descriptions if they add distinct detail
      - Source becomes "both"
      - Suggested class: if they agree, use it; if they disagree, use the more specific class
        (ARTIFACT > DECISION > SHAPING)
    </action>

    <action>Assign sequential IDs to the final list: [1], [2], [3], ...
    Store as {{gap_list}} = list of:
    {
      "id": N,
      "title": "<short title>",
      "description": "<one-line description>",
      "source": "A" | "B" | "both",
      "suggested_class": "ARTIFACT" | "DECISION" | "SHAPING"
    }
    </action>

    <note>The suggested_class is a suggestion only — triage makes the binding classification.
    epic-breakdown emits only ARTIFACT / DECISION / SHAPING suggestions. The additional
    outcomes triage may assign (DEFER, REJECT) are triage's own routing decisions
    and appear only in the final report (Step 7), never in the gap list handed to triage.</note>

    <output>→ Gap list synthesized — {{gap_list | length}} items (after deduplication):

{{for each item in gap_list:
  [{{item.id}}] {{item.suggested_class}} — {{item.title}}
      {{item.description}}
      source: {{item.source}}
}}</output>

  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- STEP 5: DEVELOPER REVIEW GATE                           -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="5" goal="Developer review gate — present gap list, allow removals before delegation">

    <output>Epic: {{epic_slug}} · {{gap_list | length}} gap candidates identified.

These items will be handed to triage for classification and routing.
Remove any before we proceed?

{{for each item in gap_list:
  [{{item.id}}] {{item.suggested_class}} — {{item.title}}
      {{item.description}}
      source: {{item.source}}
}}

Enter item numbers to remove (e.g., "2, 4"), or press Enter / type "go" to approve all.</output>

    <ask>Remove any items before handing to triage?</ask>

    <action>If developer names items to remove, remove those IDs from {{gap_list}}.
    Re-number remaining items sequentially.
    Store {{approved_gap_list}} = remaining items after removals.
    </action>

    <action>If developer approves all (Enter or "go"), store {{approved_gap_list}} = {{gap_list}}.</action>

    <check if="{{approved_gap_list}} is empty">
      <output>✓ No gaps to triage — all items removed. Epic breakdown complete with no delegation.</output>
      <action>HALT cleanly — do not invoke triage.</action>
    </check>

    <output>> ✓ **{{approved_gap_list | length}} items** approved for triage. Proceeding to delegation.</output>

  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- STEP 6: DELEGATE TO TRIAGE                              -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="6" goal="Delegate to momentum:triage with pre-enumerated list and correct source_label">

    <action>Check that the triage skill file exists before invoking:
      Run: test -f skills/momentum/skills/triage/SKILL.md
    </action>

    <check if="skills/momentum/skills/triage/SKILL.md does not exist">
      <output>✗ momentum:triage is unavailable. Cannot delegate gap items.
Required dependency: skills/momentum/skills/triage/SKILL.md not found.
Resolve the missing skill file before proceeding.</output>
      <action>HALT.</action>
    </check>

    <action>Invoke `momentum:triage` using the Skill tool, passing the approved gap list as a
    pre-enumerated source. Match the input shape that triage Step 1 accepts for the
    "invoked from retro or assessment with a pre-enumerated list" branch:

      - raw_items: {{approved_gap_list}} — each item as a plain observation string:
          "{{item.title}} — {{item.description}}"
          (one string per item; do NOT include suggested_class in the payload)
      - source_label: "epic-breakdown:{{epic_slug}}"

    Triage will re-classify each item using its own heuristics (from original_text per its
    Step 3 contract), present a batch-approval UX to the developer, and delegate approved items
    to intake / decision / practice-ledger.
    </action>

    <note>Triage classifies items fresh from original_text per its Step 1 contract. The
    suggested_class values in {{approved_gap_list}} are synthesis suggestions used at the
    developer review gate (Step 5) only — they must not be forwarded to triage as that would
    pre-bias triage's independent classification pass.</note>

    <action>Wait for triage to complete. Store {{triage_output}} = triage's summary output.</action>

  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- STEP 7: REPORT                                          -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="7" goal="Report — summarize outcomes after triage returns">

    <action>Parse {{triage_output}} to extract the following counts. Triage Step 6 exposes
    these variables directly in its summary output. If a class was not present in this triage
    session, the count will be absent from the output — default any absent count to 0:
      - {{artifact_count}} — from "Stubbed to backlog (N)"; default 0 if absent
      - {{decision_count}} — from "Decisions recorded (N)"; default 0 if absent
      - {{shaping_count}} — from "N shaping"; default 0 if absent
      - {{defer_count}} — from "N deferred"; default 0 if absent
      - {{reject_count}} — from "N rejected"; default 0 if absent
      - {{story_paths}} — list of stub_path values from intake results; default []
      - {{decision_paths}} — list of outcome paths from decision results; default []
    </action>

    <output>✓ Epic breakdown complete — {{epic_slug}}

Gap analysis: {{gap_list | length}} candidates identified, {{approved_gap_list | length}} approved for triage.

Triage outcomes ({{approved_gap_list | length}} items):
  · ARTIFACT → {{artifact_count}} (stubbed to backlog)
  · DECISION → {{decision_count}} (decision docs created)
  · SHAPING  → {{shaping_count}} (parked in practice-ledger.jsonl)
  · DEFER    → {{defer_count}} (parked in practice-ledger.jsonl)
  · REJECT   → {{reject_count}} (logged in practice-ledger.jsonl)

{{#if story_paths | length > 0}}
New story stubs:
{{for each path in story_paths: · {{path}}}}
{{/if}}

{{#if decision_paths | length > 0}}
New decision docs:
{{for each path in decision_paths: · {{path}}}}
{{/if}}

</output>

  </step>

</workflow>
