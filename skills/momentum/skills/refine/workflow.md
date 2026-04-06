# momentum:refine Workflow

**Goal:** Read the full backlog holistically, run parallel discovery agents against the
PRD and architecture to identify gaps, present consolidated findings to the developer,
apply approved changes via the momentum-tools CLI, and delegate new story creation to
`momentum:create-story`.

**Voice:** Impetus voice — dry, confident, forward-moving. Symbol vocabulary: ✓ completed,
→ current, ◦ upcoming, ! warning, ✗ failed, ? proactive offer, · list item.

---

## INITIALIZATION

Load config from `{project-root}/_bmad/bmm/config.yaml` and resolve:
- `planning_artifacts` → path to `_bmad-output/planning-artifacts/`
- `implementation_artifacts` → path to `_bmad-output/implementation-artifacts/`

---

## EXECUTION

<workflow>
  <critical>All mutations to stories/index.json go through momentum-tools CLI only. Never use Edit or Write on stories/index.json or any planning artifact file.</critical>
  <critical>New story creation is always delegated to momentum:create-story. Never write story files directly.</critical>
  <critical>Dependency updates are out of scope — no CLI command exists for dependency mutation. Flag them for manual resolution only.</critical>
  <critical>Epic reassignment scope is limited to individual story classification corrections. Structural taxonomy changes (slug consolidations, category merges) are handled by momentum:epic-grooming, not this skill.</critical>
  <critical>All refinement decisions must be logged via momentum-tools log with event type decision.</critical>

  <step n="0" goal="Initialize task tracking">
    <action>Create tasks for the 5 workflow steps:
      1. Present backlog
      2. Run parallel gap discovery
      3. Consolidate and present findings
      4. Apply approved changes
      5. Summary
    </action>
    <action>Log workflow start:
      `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py log --agent impetus --event decision --detail "Refine workflow initiated" --sprint _unsorted`</action>
  </step>

  <step n="1" goal="Present backlog">
    <action>Read `{implementation_artifacts}/stories/index.json`</action>
    <action>Filter: exclude stories with status in {done, dropped, closed-incomplete}</action>
    <action>Store {{pre_refine_counts}} — count of stories by priority before any changes, for before/after comparison in Step 5</action>
    <action>Group remaining stories by `epic_slug`</action>
    <action>Within each epic, sort stories by:
      (1) priority — critical first, then high, medium, low (stories missing priority field treated as low)
      (2) dependency depth — leaves first (stories with no unsatisfied depends_on appear before those with pending dependencies)
      (3) alphabetical within the same priority and depth
    </action>
    <action>For each story, display:
      · priority badge: [C] for critical, [H] for high, [M] for medium, [L] for low
      · title
      · status (backlog, ready-for-dev, in-progress, review, verify)
      · dependency status: list depends_on slugs; mark each ✓ (status=done) or ◦ (pending)
      · story_file: true/false
    </action>
    <action>Display summary header: total stories, epics, priority distribution</action>

    <output>
Backlog — N stories across M epics (K critical, H high, M medium, L low)

[Epic: epic-slug-1]
  · [C] story-slug-a — Title · status · deps: [✓ dep1, ◦ dep2] · file: true
  · [L] story-slug-b — Title · status · deps: none · file: false
  ...

[Epic: epic-slug-2]
  · [M] story-slug-c — Title · status · deps: [✓ dep1] · file: true
  ...

Running gap discovery — analyzing PRD and architecture coverage.
    </output>

    <action>Log backlog presentation:
      `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py log --agent impetus --event decision --detail "Refine backlog presented: N stories across M epics" --sprint _unsorted`</action>
  </step>

  <step n="2" goal="Run parallel gap discovery">
    <action>Spawn two discovery subagents in parallel (model: sonnet, effort: medium):

    **PRD coverage agent:**
      Read `{planning_artifacts}/prd.md` and `{implementation_artifacts}/stories/index.json`.
      Cross-reference every functional requirement (FR) in the PRD against story titles,
      descriptions, and `touches` paths in stories/index.json.
      Identify FRs with no corresponding backlog story.
      Return a structured list: [{id, description, suggested_epic, suggested_priority}]
      where id is the FR identifier (e.g., "FR-12"), description is the requirement text,
      suggested_epic is the most relevant epic slug, and suggested_priority is one of
      critical/high/medium/low based on FR priority signals in the PRD.

    **Architecture coverage agent:**
      Read `{planning_artifacts}/architecture.md` and `{implementation_artifacts}/stories/index.json`.
      Cross-reference every architecture decision and component against story titles
      and `touches` paths in stories/index.json.
      Identify architecture decisions with no corresponding implementation story.
      Return a structured list: [{id, description, suggested_epic, suggested_priority}]
      where id is the decision identifier (e.g., "ADR-3" or a section heading),
      description is the decision or component description,
      suggested_epic is the most relevant epic slug, and suggested_priority is one of
      critical/high/medium/low based on architectural significance.
    </action>

    <action>Wait for both agents to complete before proceeding to Step 3</action>
    <action>Store {{prd_gaps}} = PRD coverage agent findings list</action>
    <action>Store {{arch_gaps}} = Architecture coverage agent findings list</action>

    <action>Log discovery completion:
      `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py log --agent impetus --event decision --detail "Gap discovery complete: {{prd_gap_count}} PRD gaps, {{arch_gap_count}} architecture gaps" --sprint _unsorted`</action>
  </step>

  <step n="3" goal="Consolidate and present findings">
    <action>Read `{implementation_artifacts}/stories/index.json` again to compute locally-detected issues</action>

    <action>Detect locally (from stories data):

    **Priority suggestions** — stories whose priority should change:
      · Stories with a high-priority (critical/high) unsatisfied dependency that are
        themselves medium or low: suggest raising priority to match the dependency
      · Stories on critical path (others depend on them) sitting at low priority:
        suggest raising to medium or high

    **Stale candidates** — stories to consider dropping:
      · Backlog stories with status=backlog, story_file=false, no other story depends
        on them, and priority low: flag as stale candidates

    **Dependency issues** — structural problems in depends_on:
      · Circular chains: A depends on B depends on A (flag, cannot auto-resolve)
      · Missing targets: depends_on references a slug not in stories/index.json
      · Satisfied dependencies: depends_on entries where the dependency status is
        done (informational noise — suggest removing the entry)
      Note: all dependency issues are flagged for manual resolution only — no CLI
      command applies changes to dependency fields.

    **Epic mismatches** — stories likely in the wrong epic:
      · Compare each story's touches paths against the epic's theme; flag stories
        whose paths align more strongly with a different epic

    **Coverage gaps** — from discovery agents:
      · All items from {{prd_gaps}} and {{arch_gaps}}
    </action>

    <action>Consolidate all findings into a single ordered list with categories:
      1. Priority suggestions
      2. Stale candidates
      3. Dependency issues (manual resolution)
      4. Epic mismatches
      5. PRD coverage gaps
      6. Architecture coverage gaps
    </action>

    <check if="no findings across all categories">
      <output>✓ Backlog is healthy — no priority, staleness, dependency, epic, or coverage issues detected.</output>
      <action>Log result: `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py log --agent impetus --event decision --detail "Refine findings: none — backlog is healthy" --sprint _unsorted`</action>
      <action>Skip to Step 5</action>
    </check>

    <check if="findings exist">
      <output>Findings — N items requiring review:

[Priority suggestions]
  {{for each: · [story-slug] Title → suggest LEVEL (currently CURRENT_LEVEL) — rationale}}

[Stale candidates]
  {{for each: · [story-slug] Title — no activity, no dependents, low priority — consider dropping}}

[Dependency issues — manual resolution required]
  {{for each: · [story-slug] issue type — description of the problem}}

[Epic mismatches]
  {{for each: · [story-slug] Title — currently in CURRENT_EPIC, better fit: SUGGESTED_EPIC — rationale}}

[PRD coverage gaps]
  {{for each: · [FR-id] description — suggested epic: EPIC, priority: LEVEL}}

[Architecture coverage gaps]
  {{for each: · [id] description — suggested epic: EPIC, priority: LEVEL}}

For each finding, enter: A (approve), M (modify), or R (reject).
      </output>

      <action>For each finding, present individually and wait for developer response:
        A — approve the recommended action as-is
        M — approve with modifications (ask what change the developer wants)
        R — reject this finding (no action taken)
      </action>

      <action>Store {{approved_findings}} = findings approved (with any modifications applied)</action>
      <action>Store {{rejected_count}} = count of rejected findings</action>

      <action>Log findings review:
        `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py log --agent impetus --event decision --detail "Findings reviewed: {{approved_count}} approved, {{rejected_count}} rejected" --sprint _unsorted`</action>
    </check>
  </step>

  <step n="4" goal="Apply approved changes">
    <action>Process each finding in {{approved_findings}} by type:

    **Priority changes** — for each approved priority suggestion:
      Run: `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py sprint set-priority --story SLUG --priority LEVEL`
      Log: `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py log --agent impetus --event decision --detail "Priority change: SLUG → LEVEL" --sprint _unsorted`

    **Story drops** — for each approved stale drop:
      Run: `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py sprint status-transition --story SLUG --target dropped`
      Log: `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py log --agent impetus --event decision --detail "Story dropped: SLUG" --sprint _unsorted`

    **Epic reassignments** — for each approved epic mismatch correction:
      Run: `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py sprint epic-membership --story SLUG --epic EPIC_SLUG`
      Log: `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py log --agent impetus --event decision --detail "Epic reassignment: SLUG → EPIC_SLUG" --sprint _unsorted`

    **Dependency issues** — no CLI action available; these were already flagged for
      manual resolution in Step 3. Log the flag:
      `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py log --agent impetus --event decision --detail "Dependency issue flagged for manual resolution: SLUG — ISSUE_DESCRIPTION" --sprint _unsorted`

    **New stories from coverage gaps** — for each approved PRD or architecture gap:
      Ask the developer to confirm the story description, epic, and priority before delegating.
      Invoke `momentum:create-story` with the approved description, epic_slug, and priority.
      Wait for create-story to complete before moving to the next new story.
      Log: `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py log --agent impetus --event decision --detail "New story delegated to create-story: DESCRIPTION (epic: EPIC, priority: LEVEL)" --sprint _unsorted`
    </action>

    <action>Store {{changes_applied}} = {priority_changes: N, drops: N, epic_moves: N, new_stories: N}</action>
  </step>

  <step n="5" goal="Log decisions and present summary">
    <action>Read `{implementation_artifacts}/stories/index.json` to compute post-refine priority distribution</action>
    <action>Compute {{post_refine_counts}} — count of stories by priority after all changes</action>

    <output>✓ Refinement complete.

Changes applied:
  · Priority changes: {{changes_applied.priority_changes}}
  · Stories dropped: {{changes_applied.drops}}
  · Epic reassignments: {{changes_applied.epic_moves}}
  · New stories created: {{changes_applied.new_stories}}
  · Findings rejected: {{rejected_count}}

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

    <action>Log summary:
      `python3 ${CLAUDE_PROJECT_DIR}/skills/momentum/scripts/momentum-tools.py log --agent impetus --event decision --detail "Refine complete: {{priority_changes}} priority changes, {{drops}} drops, {{epic_moves}} epic moves, {{new_stories}} new stories, {{rejected_count}} rejected" --sprint _unsorted`</action>
  </step>

</workflow>
