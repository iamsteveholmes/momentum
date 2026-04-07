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
      7. Consolidated findings with batch approval
      8. Apply approved changes
      9. Summary
    </action>
  </step>

  <step n="1" goal="Present backlog">
    <action>Read `{implementation_artifacts}/stories/index.json`</action>
    <action>Filter: exclude stories with status in {done, dropped, closed-incomplete}</action>
    <action>Store {{pre}} — count of stories by priority before any changes (keys: critical, high, medium, low), for before/after comparison in Step 9</action>
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

  <step n="7" goal="Consolidated findings with batch approval">
    <action>Collect all findings into a single list grouped by category:
      1. Status mismatches (from Step 4)
      2. Epic issues (from Step 5, if epic-grooming ran)
      3. Stale-story evaluations (from Step 6)
    Note: planning artifact updates (Steps 2-3) are handled in their own approval
    gate and are NOT re-presented here.
    </action>

    <check if="no findings across all categories">
      <output>✓ Backlog is healthy — no issues detected requiring action.</output>
      <action>Skip to Step 9</action>
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

Override specific findings? Enter numbers or ranges, or 'done' to proceed.
      </output>
    </check>

    <action>Store {{approved_findings}} = all approved findings (with any modifications)</action>
    <action>Store {{rejected_count}} = count of rejected findings</action>
  </step>

  <step n="8" goal="Apply approved changes">
    <action>Process each finding in {{approved_findings}} by type:

    **Status transitions** — for each approved status mismatch:
      Run: `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py sprint status-transition --story SLUG --target done`

    **Story drops** — for each approved stale-story drop:
      Run: `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py sprint status-transition --story SLUG --target dropped`

    **Epic reassignments** — for each approved epic reassignment (from epic-grooming findings):
      Run: `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py sprint epic-membership --story SLUG --epic EPIC_SLUG`

    **New stories from findings** — for any finding that requires creating a new story:
      Confirm description, epic, and priority with the developer.
      Invoke `momentum:create-story` with the approved details.
      Wait for create-story to complete before moving to the next.
    </action>

    <action>Store {{changes_applied}} = {status_transitions: N, drops: N, epic_moves: N, new_stories: N}</action>
  </step>

  <step n="9" goal="Summary">
    <action>Read `{implementation_artifacts}/stories/index.json` to compute post-refine priority distribution</action>
    <action>Compute {{post}} — count of stories by priority after all changes (keys: critical, high, medium, low)</action>

    <output>✓ Refinement complete.

Changes applied:
  · Status transitions: {{changes_applied.status_transitions}}
  · Stories dropped: {{changes_applied.drops}}
  · Epic reassignments: {{changes_applied.epic_moves}}
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
