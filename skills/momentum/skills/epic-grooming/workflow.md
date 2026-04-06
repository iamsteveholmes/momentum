# Epic Grooming Workflow

**Goal:** Produce a clean, formally registered epic taxonomy — every `epic_slug` in use either maps to a registered epic definition or is resolved (merged, renamed, or removed) with explicit developer approval.

**Voice:** Impetus voice — oriented, factual, forward-moving. Symbol vocabulary: ✓ registered, ◦ orphaned, → current, ! warning, · list item.

---

## EXECUTION

<workflow>
  <critical>Epics are categories — long-lived, never-closing groupings of related work. Do NOT propose closing or completing epics. Only propose merges, splits, renames, or new epic creation.</critical>
  <critical>No mutations happen without explicit developer approval of each proposed change individually. Present proposals first; apply only after approval.</critical>
  <critical>All story reassignments go through `momentum-tools sprint epic-membership`. Never edit stories/index.json directly.</critical>
  <critical>Every approved change must be logged via `momentum-tools log --agent epic-grooming --event decision` before the workflow completes.</critical>
  <critical>Reassignment scope is limited to structural taxonomy changes (slug consolidations, category merges). Individual story classification corrections are handled by momentum:refine, not this skill.</critical>

  <step n="0" goal="Initialize task tracking">
    <action>Create tasks for the 4 workflow phases:
      1. Data collection — read all sources, enumerate slugs
      2. Taxonomy analysis — identify overlaps, draft proposals
      3. Developer review — present proposals, collect approval per change
      4. Apply changes — update epics.md, reassign stories, log decisions
    </action>
    <action>Log workflow start:
      `python3 skills/momentum/scripts/momentum-tools.py log --agent epic-grooming --event decision --detail "Epic grooming workflow started" --sprint sprint-2026-04-06`
    </action>
  </step>

  <step n="1" goal="Phase 1 — Data Collection">
    <action>Read `_bmad-output/implementation-artifacts/stories/index.json`. Extract every unique `epic_slug` value with its story count. Build a complete slug → [story_slug, ...] map.</action>
    <action>Read `_bmad-output/planning-artifacts/epics.md` Epic List section (the `### Epic N:` entries). Extract every registered epic slug and title. A registered slug is one that has a named section in epics.md.</action>
    <action>Cross-reference: produce two lists:
      · Registered slugs — appear in epics.md with a definition
      · Orphaned slugs — appear in stories/index.json but have no epics.md definition
    </action>
    <action>Read `_bmad-output/planning-artifacts/prd.md` FR/NFR inventory section (for FR and NFR coverage context to use during taxonomy analysis).</action>
    <action>Read `_bmad-output/planning-artifacts/architecture.md` first 100 lines (for architectural context).</action>
    <action>TaskUpdate Phase 1 to in_progress. After completing reads, TaskUpdate to completed.</action>

    <output>
Epic Taxonomy — Data Collection

Registered epics (N):
  ✓ {slug} — "{title}" · {M} stories
  ...

Orphaned slugs ({K}):
  ◦ {slug} · {M} stories · sample: [{story-1}, {story-2}, ...]
  ...

Total: {N+K} unique epic_slug values across {total} stories.

→ Proceeding to taxonomy analysis.
    </output>
  </step>

  <step n="2" goal="Phase 2 — Taxonomy Analysis">
    <action>TaskUpdate Phase 2 to in_progress.</action>
    <action>For each orphaned slug, determine the best resolution by examining the story titles and descriptions in its story list:
      (a) MERGE — if the orphaned slug's stories thematically belong under an existing registered epic (check for overlapping concerns, FR coverage alignment)
      (b) CREATE — if the orphaned slug represents a coherent category that doesn't fit any existing epic and has enough stories (≥3) to warrant a standalone definition
      (c) SPLIT — if stories under the orphaned slug span multiple distinct concerns that map to different existing or new epics
    </action>
    <action>Also examine large registered epics (≥15 stories) for potential split candidates — identify whether sub-themes exist that would benefit from separate tracking.</action>
    <action>For CREATE proposals, draft the full epic definition using the template at `skills/momentum/references/templates/epic-template.md`:
      · slug: the orphaned slug (or proposed renamed slug)
      · category: inferred from story themes
      · strategic intent: 2-3 sentences from story context and PRD alignment
      · boundaries: what this epic includes vs. adjacent epics
      · FRs covered: cross-reference story FR mentions against Requirements Inventory
      · NFRs covered: same
      · current state: {N done, M remaining}
    </action>
    <action>TaskUpdate Phase 2 to completed.</action>
  </step>

  <step n="3" goal="Phase 3 — Developer Review">
    <action>TaskUpdate Phase 3 to in_progress.</action>
    <action>Present all proposed changes to the developer, one at a time, in this order: MERGE proposals first (least disruptive), then CREATE proposals, then SPLIT proposals.</action>

    <output>
Epic Taxonomy — Proposed Changes ({N} total)

[{i}/{N}] {CHANGE_TYPE} proposal
  From: {old-slug} ({M} stories)
  {Into/New epic/Split target}: {target-slug}
  Rationale: {1-2 sentences from story theme analysis and FR alignment}
  Stories affected: {story-slug-1}, {story-slug-2}, ...

  Approve? [Y]es / [N]o / [M]odify
    </output>

    <action>Wait for developer response to each proposal before presenting the next one.</action>

    <check if="developer says Modify">
      <action>Ask what the developer wants to change about the proposal (target slug, rationale, story subset). Incorporate the modification and confirm before marking as approved.</action>
    </check>

    <action>Track approval status for each proposal: approved, rejected, or modified-and-approved.</action>
    <action>After all proposals reviewed, show a summary before proceeding:

      Approved: N changes
      Rejected: M changes
      → Proceeding to apply {N} approved changes.

    </action>
    <action>TaskUpdate Phase 3 to completed.</action>

    <check if="no proposals were approved">
      <output>No changes approved. Taxonomy unchanged. Workflow complete.</output>
      <action>Log: `python3 skills/momentum/scripts/momentum-tools.py log --agent epic-grooming --event decision --detail "Taxonomy review complete — no changes approved by developer" --sprint sprint-2026-04-06`</action>
    </check>
  </step>

  <step n="4" goal="Phase 4 — Apply Approved Changes">
    <action>TaskUpdate Phase 4 to in_progress.</action>

    <action>For each approved MERGE change:
      1. For each story in the source slug, call:
         `python3 skills/momentum/scripts/momentum-tools.py sprint epic-membership --story {story-slug} --epic {target-slug}`
      2. Log the decision:
         `python3 skills/momentum/scripts/momentum-tools.py log --agent epic-grooming --event decision --detail "MERGE: {old-slug} → {target-slug} | story: {story-slug} | rationale: {reason}" --sprint sprint-2026-04-06`
    </action>

    <action>For each approved CREATE change:
      1. Add the new epic definition to `_bmad-output/planning-artifacts/epics.md` using the filled-out epic template. Insert in the Epic List section (condensed entry) and append the full body section.
      2. For each story in the new epic's slug, call:
         `python3 skills/momentum/scripts/momentum-tools.py sprint epic-membership --story {story-slug} --epic {new-slug}`
         (Only needed if the slug is being renamed — if the slug stays the same, epic-membership call is skipped as stories already belong to this slug)
      3. Log the decision:
         `python3 skills/momentum/scripts/momentum-tools.py log --agent epic-grooming --event decision --detail "CREATE: new epic {new-slug} registered | stories: {N} | rationale: {reason}" --sprint sprint-2026-04-06`
    </action>

    <action>For each approved SPLIT change:
      1. For each story and its target split destination, call:
         `python3 skills/momentum/scripts/momentum-tools.py sprint epic-membership --story {story-slug} --epic {target-slug}`
      2. Log the decision:
         `python3 skills/momentum/scripts/momentum-tools.py log --agent epic-grooming --event decision --detail "SPLIT: {source-slug} → {target-slug} | story: {story-slug} | rationale: {reason}" --sprint sprint-2026-04-06`
    </action>

    <action>After all changes applied, re-read stories/index.json and epics.md to verify:
      · Every epic_slug in stories/index.json now has a matching definition in epics.md
      · Or confirm which orphans remain (if some proposals were rejected)
    </action>
    <action>TaskUpdate Phase 4 to completed.</action>

    <output>
Epic Grooming — Complete

Applied changes:
  · Epics created: {N}
  · Epics updated (merge target): {M}
  · Stories reassigned: {K}

Taxonomy health:
  · Registered epics: {R}
  · Orphaned slugs remaining: {O} {— list them if O > 0}

{If O > 0:}
! Remaining orphans were not approved for resolution in this session.
  Run /momentum:epic-grooming again to address them.

All decisions logged to sprint log.
    </output>
  </step>
</workflow>
