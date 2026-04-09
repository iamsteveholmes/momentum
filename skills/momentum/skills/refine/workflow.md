# momentum:refine Workflow

**Goal:** Read the full backlog holistically, run two-wave planning artifact discovery
and update, detect status hygiene mismatches, delegate epic-level analysis, evaluate
stale stories, present consolidated findings with batch approval UX, and apply approved
changes via momentum-tools CLI.

**Voice:** Impetus voice — dry, confident, forward-moving. Symbol vocabulary: ✓ completed,
→ current, ◦ upcoming, ! warning, ✗ failed, ? proactive offer, · list item.

---

## EXECUTION

<workflow>
  <critical>All mutations to stories/index.json go through momentum-tools CLI only. Never use Edit or Write on stories/index.json.</critical>
  <critical>Planning artifact writes are delegated to wave-2 subagents only. The refine orchestrator never uses Edit or Write on prd.md or architecture.md.</critical>
  <critical>New story creation is always delegated to momentum:create-story. Never write story files directly.</critical>
  <critical>No dependency analysis anywhere — no circular chain detection, no missing target detection, no satisfied dependency flagging. Dependency validation is sprint planning's job.</critical>
  <critical>No momentum-tools log calls anywhere in this workflow. Use TaskCreate/TaskUpdate for progress tracking.</critical>
  <critical>Planning artifacts (prd.md, architecture.md) are authoritative and never candidates for archiving or marking optional.</critical>

  <step n="0" goal="Initialize task tracking">
    <action>Create tasks for the workflow steps:
      1. Present backlog
      2. Planning artifact discovery (wave 1)
      3. Planning artifact update (wave 2)
      4. Status hygiene scan
      5. Epic grooming delegation
      6. Stale-story evaluation
      7. Re-prioritization analysis and conversation
      8. Assessment &amp; decision review
      9. Consolidated findings with batch approval
      10. Apply approved changes
      11. Summary
    </action>
  </step>

  <step n="1" goal="Present backlog">
    <action>Read `{implementation_artifacts}/stories/index.json`</action>
    <action>Filter: exclude stories with status in {done, dropped, closed-incomplete}</action>
    <action>Store {{pre}} — count of stories by priority before any changes (keys: critical, high, medium, low), for before/after comparison in Step 10</action>
    <action>Group remaining stories by `epic_slug`</action>
    <action>Within each epic, sort stories by:
      (1) priority — critical first, then high, medium, low (stories missing priority field treated as low)
      (2) alphabetical within the same priority
    </action>
    <action>For each story, display:
      · priority badge: [C] for critical, [H] for high, [M] for medium, [L] for low
      · title
      · status (backlog, ready-for-dev, in-progress, review, verify)
      · story_file: true/false
    </action>
    <action>Display summary header: total stories, epics, priority distribution</action>

    <output>
Backlog — N stories across M epics (K critical, H high, M medium, L low)

[Epic: epic-slug-1]
  · [C] story-slug-a — Title · status · file: true
  · [L] story-slug-b — Title · status · file: false
  ...

[Epic: epic-slug-2]
  · [M] story-slug-c — Title · status · file: true
  ...

→ Running planning artifact discovery.
    </output>
  </step>

  <step n="2" goal="Planning artifact discovery — wave 1">
    <action>Spawn two discovery subagents in parallel (model: sonnet, effort: medium):

    **PRD coverage agent:**
      Read `{planning_artifacts}/prd.md` and `{implementation_artifacts}/stories/index.json`.
      Compare the PRD's requirements against the current backlog state — completed stories,
      changed priorities, dropped stories, new stories added since the PRD was written.
      Identify requirements that are:
        · Missing — not represented in any backlog story
        · Outdated — described differently than what was implemented
        · No longer accurate — contradicted by completed work or dropped stories
      Return structured findings:
      `[{id, description, action_needed (add/update/remove), rationale}]`

    **Architecture coverage agent:**
      Read `{planning_artifacts}/architecture.md` and `{implementation_artifacts}/stories/index.json`.
      Compare architecture decisions and component descriptions against the current backlog
      state — completed stories, changed technical approaches, new components.
      Identify decisions that are:
        · Missing — new architecture emerged that is not documented
        · Outdated — described differently than what was implemented
        · No longer accurate — contradicted by completed work or changed direction
      Return structured findings:
      `[{id, description, action_needed (add/update/remove), rationale}]`
    </action>

    <action>Wait for both agents to complete before proceeding</action>
    <action>Store {{prd_findings}} = PRD coverage agent findings list</action>
    <action>Store {{arch_findings}} = Architecture coverage agent findings list</action>

    <check if="neither agent found required updates (both findings lists empty)">
      <output>✓ Planning artifacts are current — no drift detected. Skipping wave 2.</output>
      <action>Skip to Step 4</action>
    </check>
  </step>

  <step n="3" goal="Planning artifact update — wave 2">
    <action>Present wave 1 findings to the developer for review:

    {{if prd_findings non-empty:
    [PRD drift findings]
      {{for each: · [id] description — action_needed — rationale}}
    }}

    {{if arch_findings non-empty:
    [Architecture drift findings]
      {{for each: · [id] description — action_needed — rationale}}
    }}
    </action>

    <ask>Review the planning artifact findings above. Approve the changes to proceed with
    updates, or reject to skip wave 2.

    For each document with findings, respond:
      A — approve updates to this document
      R — reject (skip updates to this document)
    </ask>

    <check if="developer rejected all findings">
      <output>→ Wave 2 skipped — no planning artifact updates approved.</output>
      <action>Skip to Step 4</action>
    </check>

    <check if="developer approved at least one document's findings">
      <action>Spawn update subagents only for documents where findings were approved
      (both run in parallel if both were approved):

      **PRD update agent** (if PRD findings approved):
        Read `{planning_artifacts}/prd.md`.
        Apply the approved changes following the existing document format.
        You are the sole writer of prd.md — write the updated file.

      **Architecture update agent** (if architecture findings approved):
        Read `{planning_artifacts}/architecture.md`.
        Apply the approved changes following the existing document format.
        You are the sole writer of architecture.md — write the updated file.
      </action>

      <action>Wait for update agents to complete</action>
      <output>✓ Planning artifacts updated.</output>
    </check>
  </step>

  <step n="4" goal="Status hygiene scan">
    <action>Read `{implementation_artifacts}/stories/index.json`</action>
    <action>For each story where status is NOT in {done, dropped, closed-incomplete} AND story_file is true:
      · Read the story file
      · Look for a Dev Agent Record section containing a File List or DoD checklist
      · Check if all items are checked: every `- [x]` and no `- [ ]` lines in that section
      · If all items are checked but status is not `done`, flag as a status mismatch
    </action>
    <action>Store {{status_mismatches}} = list of flagged stories with their current status</action>

    <check if="no status mismatches found">
      <output>✓ Status hygiene clean — all story statuses match their completion state.</output>
    </check>

    <check if="status mismatches found">
      <output>
! Status mismatches detected — {{count}} stories appear complete but are not marked done:
  {{for each: · [story-slug] Title — status: CURRENT_STATUS, DoD: all checked}}
      </output>
    </check>
  </step>

  <step n="5" goal="Delegate to epic-grooming">
    <action>Check if `momentum:epic-grooming` skill exists (attempt to resolve the skill)</action>

    <check if="momentum:epic-grooming exists">
      <action>Invoke `momentum:epic-grooming` to perform epic-level structural analysis
      (deduplication, description quality, consolidation recommendations)</action>
      <action>Store {{epic_findings}} = findings returned by epic-grooming</action>
    </check>

    <check if="momentum:epic-grooming does NOT exist">
      <output>? epic-grooming skill not available — skipping epic-level analysis.</output>
      <action>Store {{epic_findings}} = empty list</action>
    </check>
  </step>

  <step n="6" goal="Stale-story individual evaluation">
    <action>Identify stale candidates from stories/index.json:
      · status = `backlog`
      · priority = `low`
      · story_file = false (no detailed spec written)
    </action>

    <check if="no stale candidates found">
      <output>✓ No stale story candidates — all low-priority backlog items have story files.</output>
      <action>Store {{stale_evaluations}} = empty list</action>
    </check>

    <check if="stale candidates found">
      <action>For each candidate, evaluate individually:
        · What value does this story represent?
        · Is that value captured elsewhere (other stories, codebase, planning docs)?
        · Recommendation: keep or drop, with rationale
      </action>

      <output>
Stale story evaluations — {{count}} candidates:
  {{for each:
  · [story-slug] Title
    Value: {{value assessment}}
    Captured elsewhere: {{yes/no — where}}
    Recommendation: {{keep/drop}} — {{rationale}}
  }}
      </output>

      <action>Store {{stale_evaluations}} = list of evaluations with recommendations</action>
    </check>
  </step>

  <step n="7" goal="Re-prioritization analysis and conversation">
    <action>Read `{implementation_artifacts}/stories/index.json` — extract all active
    stories (exclude done, dropped, closed-incomplete) with their `priority` and
    `depends_on` fields</action>
    <action>Read `{planning_artifacts}/prd.md` (if exists) to extract current
    project goals and strategic direction for grounding recommendations</action>

    <action>Run four heuristic analyses:

    **Recurrence heuristic:**
      · Glob `{implementation_artifacts}/sprints/*/retro-*.md`
      · For each retro file found, scan for story slugs and topic keywords in findings
      · Identify stories or topics that appear in findings across 2 or more sprint retros
      · These are recurring pain points — recommend promotion with citation of which
        sprint retros surfaced the pattern

    **Workaround burden heuristic:**
      · For each active story, assess the complexity of the manual workaround if the
        story is not yet implemented:
        - High burden: requires complex multi-step prompting, custom instructions, or
          significant developer attention each time
        - Medium burden: some prompting but straightforward
        - Low burden: trivial or one-liner workaround
      · High-burden stories are candidates for stronger priority promotion than low-burden

    **Forgetting risk heuristic:**
      · For each active story with a workaround, assess what breaks when the workaround
        is forgotten:
        - High risk: silent failures, data quality degradation, broken output
        - Medium risk: noticeable but recoverable failures
        - Low risk: cosmetic or easily caught issues
      · High forgetting risk stories are candidates for promotion regardless of burden

    **Dependency promotion heuristic:**
      · Cross-reference `depends_on` fields against story priorities
      · Identify: a low or medium priority story that is listed in the `depends_on` of
        one or more critical or high priority stories (it is blocking critical-path work)
      · Recommend promoting the blocker to match the priority of the highest-priority
        story it blocks
      · Cite the specific blocker/blocked story slug relationship in the rationale
    </action>

    <action>Synthesize heuristic findings into an initial recommendation set.
    Each recommendation includes:
      · story-slug
      · current priority
      · recommended priority
      · heuristics triggered (recurrence / burden / forgetting-risk / dependency)
      · rationale citing specific evidence (retro file names, sprint cycles, story slugs)
    </action>

    <action>Open a back-and-forth conversation with the developer — NOT a fixed approval
    list. Present the initial assessment and invite dialogue:

    Framing: reference goals from prd.md where relevant ("In line with your goal to
    [X], I recommend promoting [story-slug] because [evidence]")

    The developer may:
      · Agree with recommendations
      · Disagree and explain why ("that story is blocked externally, keep it low")
      · Redirect ("I've changed focus — prioritize stories that help us ship X faster")
      · Refine ("yes, and also promote these others because...")

    Adapt recommendations based on developer input. The conversation is not a checklist —
    it is an informed discussion grounded in heuristic evidence and the developer's
    stated direction. Continue the conversation until the developer explicitly signals
    they are satisfied.
    </action>

    <action>Store {{priority_recommendations}} = final agreed-upon list of priority
    changes from the conversation. Each entry: {story_slug, current_priority,
    new_priority, rationale}</action>

    <check if="no heuristic findings and developer confirms no priority changes needed">
      <output>✓ No priority changes identified — backlog priorities look well-aligned.</output>
      <action>Store {{priority_recommendations}} = empty list</action>
    </check>
  </step>

  <step n="8" goal="Assessment and decision review">
    <action>Glob `{planning_artifacts}/assessments/*.md` to find all ASR documents.
    For each ASR with status "current":
      · Parse frontmatter: id, title, date, decisions_produced
      · Compute age = today minus date in days
      · Flag as potentially stale if age > 30 days
      · Flag as unacted-on if decisions_produced is empty or []
      · Read the "Recommended Next Steps" section of the ASR
      · For each next step: check whether an SDR exists that references this ASR id
        (via source_research) OR a story in stories/index.json addresses it by
        searching story titles and descriptions for keyword overlap
      · Flag next steps with no SDR coverage and no backlog story as unresolved
    </action>

    <action>Glob `{planning_artifacts}/decisions/*.md` to find all SDR documents.
    Read `{implementation_artifacts}/stories/index.json` (use offset/limit if large).
    For each SDR:
      · Parse frontmatter: id, title, date, status, stories_affected
      · For each slug in stories_affected: check whether it exists in stories/index.json
      · Flag missing slugs with: SDR id, decision title, missing story slug
      · If a "Phased Implementation Plan" table exists, extract "Key Stories" column
        slugs and check each against stories/index.json — flag gaps
      · If a "Decision Gates" section exists, for each gate:
        - Parse gate timing condition (e.g., "Phase 1 done")
        - Identify the stories associated with that phase (from Phased Implementation
          Plan or stories_affected)
        - Check if all those stories are status "done" in stories/index.json
        - If all gate-associated stories are done, flag gate as ready for review
          with gate criteria quoted verbatim
    </action>

    <action>Collect all findings into {{assessment_decision_findings}}:
      · Assessment staleness findings: {type: "stale-assessment", asr_id, title,
        date, age_days, has_decisions: bool}
      · Unacted-on assessment findings: {type: "unacted-assessment", asr_id, title,
        date, decisions_produced: []}
      · Unresolved next steps: {type: "unresolved-next-step", asr_id, next_step_text}
      · Missing story from SDR: {type: "missing-story", sdr_id, decision_title,
        missing_slug}
      · Decision gate ready: {type: "gate-ready", sdr_id, gate_name, timing,
        criteria_text}
    </action>

    <check if="no assessment or decision files found">
      <output>✓ No assessments or decisions found — skipping assessment &amp; decision review.</output>
      <action>Store {{assessment_decision_findings}} = empty list</action>
    </check>

    <check if="assessments and decisions exist but no findings">
      <output>✓ Assessments and decisions look healthy — no staleness, coverage gaps, or ready gates detected.</output>
      <action>Store {{assessment_decision_findings}} = empty list</action>
    </check>

    <check if="findings exist">
      <output>
Assessment &amp; decision review — {{count}} findings:

{{if stale or unacted-on assessments:
[Assessments]
  {{for each stale: ! [ASR-NNN] title — {{age_days}} days old{{", no decisions produced" if unacted-on}}}}
  {{for each unresolved next step: · [ASR-NNN] unresolved next step: "{{next_step_text}}"}}
}}

{{if SDR findings:
[Decisions]
  {{for each missing story: · [SDR-NNN] title — missing story: {{missing_slug}}}}
  {{for each gate: ! [SDR-NNN] gate "{{gate_name}}" appears ready for review — criteria: {{criteria_text}}}}
}}
      </output>
    </check>
  </step>

  <step n="9" goal="Consolidated findings with batch approval">
    <action>Collect all findings into a single list grouped by category:
      1. Status mismatches (from Step 4)
      2. Epic issues (from Step 5, if epic-grooming ran)
      3. Stale-story evaluations (from Step 6)
      4. Priority changes (from Step 7 — {{priority_recommendations}})
      5. Assessment &amp; decision review (from Step 8 — {{assessment_decision_findings}})
    Note: planning artifact updates (Steps 2-3) are handled in their own approval
    gate and are NOT re-presented here.
    </action>

    <check if="no findings across all categories">
      <output>✓ Backlog is healthy — no issues detected requiring action.</output>
      <action>Skip to Step 11</action>
    </check>

    <check if="total findings fewer than 5">
      <action>Present each finding individually and ask for a decision:
        A — approve the recommended action
        M — approve with modifications (ask what the developer wants changed)
        R — reject this finding (no action taken)
      </action>

      <output>
Findings — {{count}} items:

{{for each finding:
  [{{N}}] [{{category}}] {{description}}
    Recommendation: {{action}}
    → A / M / R?
}}
      </output>
    </check>

    <check if="total findings 5 or more">
      <action>Present findings grouped by category with batch operations first:

      For each category with findings:
        · Show category name and count
        · List all findings in the category with numbered IDs
        · Offer batch operation: "Approve all {{category}}?" or "Reject all {{category}}?"
        · After batch decisions, allow individual overrides:
          "Override specific findings? Enter numbers (e.g., 3, 7-9) or 'done' to proceed."
        · Support range operations: "approve 1-5", "reject 6-8"
      </action>

      <output>
Findings — {{total_count}} items across {{category_count}} categories:

[Status mismatches] — {{count}} items
  {{for each: [N] story-slug — currently CURRENT_STATUS, DoD complete → transition to done}}
  → Approve all? (A=all / R=all / pick individually)

[Epic issues] — {{count}} items
  {{for each: [N] description — recommendation}}
  → Approve all? (A=all / R=all / pick individually)

[Stale stories] — {{count}} items
  {{for each: [N] story-slug — recommendation: keep/drop — rationale}}
  → Approve all? (A=all / R=all / pick individually)

[Priority changes] — {{count}} items
  {{for each: [N] story-slug — priority: CURRENT → NEW — rationale}}
  → Approve all? (A=all / R=all / pick individually)

[Assessment &amp; decision review] — {{count}} items
  {{for each stale assessment: [N] [ASR-NNN] title — stale ({{age_days}} days){{", no decisions" if unacted-on}}}}
  {{for each unresolved next step: [N] [ASR-NNN] unresolved next step — create story or decision}}
  {{for each missing story: [N] [SDR-NNN] missing story: {{missing_slug}} — create story}}
  {{for each gate ready: [N] [SDR-NNN] gate "{{gate_name}}" ready for review — criteria: {{criteria_text}}}}
  → Approve all? (A=all / R=all / pick individually)

Override specific findings? Enter numbers or ranges, or 'done' to proceed.
      </output>
    </check>

    <action>Store {{approved_findings}} = all approved findings (with any modifications)</action>
    <action>Store {{rejected_count}} = count of rejected findings</action>
  </step>

  <step n="10" goal="Apply approved changes">
    <action>Process each finding in {{approved_findings}} by type:

    **Status transitions** — for each approved status mismatch:
      Run: `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py sprint status-transition --story SLUG --target done`

    **Story drops** — for each approved stale-story drop:
      Run: `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py sprint status-transition --story SLUG --target dropped`

    **Epic reassignments** — for each approved epic reassignment (from epic-grooming findings):
      Run: `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py sprint epic-membership --story SLUG --epic EPIC_SLUG`

    **Priority changes** — for each approved priority recommendation (from Step 7):
      Run: `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py sprint set-priority --story SLUG --priority LEVEL`

    **New stories from assessment/decision findings** — for each approved finding
    of type missing-story or unresolved-next-step:
      Confirm description, epic, and priority with the developer.
      Invoke `momentum:create-story` with the approved details.
      Wait for create-story to complete before moving to the next new story.

    **Decision gate reviews** — for each approved gate-ready finding:
      Present the gate criteria to the developer and ask them to evaluate and
      document their decision. Do NOT modify the SDR document automatically.

    **New stories from other findings** — for any other finding that requires
    creating a new story:
      Confirm description, epic, and priority with the developer.
      Invoke `momentum:create-story` with the approved details.
      Wait for create-story to complete before moving to the next.
    </action>

    <action>Store {{changes_applied}} = {status_transitions: N, drops: N, epic_moves: N, priority_changes: N, new_stories: N}</action>
  </step>

  <step n="11" goal="Summary">
    <action>Read `{implementation_artifacts}/stories/index.json` to compute post-refine priority distribution</action>
    <action>Compute {{post}} — count of stories by priority after all changes (keys: critical, high, medium, low)</action>

    <output>✓ Refinement complete.

Changes applied:
  · Status transitions: {{changes_applied.status_transitions}}
  · Stories dropped: {{changes_applied.drops}}
  · Epic reassignments: {{changes_applied.epic_moves}}
  · Priority changes: {{changes_applied.priority_changes}}
  · New stories created: {{changes_applied.new_stories}}
  · Findings rejected: {{rejected_count}}
  · Planning artifacts updated: {{prd_updated (yes/no)}}, {{arch_updated (yes/no)}}

Priority distribution (before → after):
  [C] critical: {{pre.critical}} → {{post.critical}}
  [H] high:     {{pre.high}} → {{post.high}}
  [M] medium:   {{pre.medium}} → {{post.medium}}
  [L] low:      {{pre.low}} → {{post.low}}

{{if epic moves occurred:
Epic distribution changes:
  {{for each affected epic: · EPIC_SLUG: N → M stories}}
}}

The backlog is ready for sprint planning.
    </output>
  </step>

</workflow>
