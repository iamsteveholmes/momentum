# Epic Grooming Workflow

**Goal:** Produce a complete, value-oriented epic taxonomy — either bootstrapping `epics.json` from
scratch or refining an existing one — with every epic carrying a multi-paragraph `value_analysis`,
`system_context`, typed classification, and verifiable `acceptance_condition`. Also resolves
orphaned `epic_slug` values in `stories/index.json` so every slug maps to a registered epic.

**Sole write authority:** This skill is the only authorized writer of
`_bmad-output/planning-artifacts/epics.json`.

**Voice:** Impetus voice — oriented, factual, forward-moving. Symbol vocabulary: ✓ registered,
◦ orphaned/candidate, → current, ! warning, ⚠ deferred-value flag, · list item.

---

## EXECUTION

<workflow>
  <critical>epics.json is NOT written until the Step 5 approval gate is explicitly passed with "Y".
  No write occurs before this gate under any circumstance.</critical>
  <critical>Epics are categories — long-lived, never-closing groupings of related work. Do NOT
  propose closing or completing epics. Only propose merges, splits, renames, or new epic
  creation.</critical>
  <critical>No taxonomy mutations happen without explicit developer approval. Present proposals
  first; apply only after approval.</critical>
  <critical>All story reassignments go through `momentum-tools sprint epic-membership`. Never edit
  stories/index.json directly.</critical>
  <critical>Exactly 2 subagents are spawned in Step 2 — no more, no less. Both are launched in a
  single message (fan-out pattern, NOT TeamCreate). The orchestrator handles all synthesis, value
  analysis, developer interaction, and writing directly.</critical>
  <critical>Every epic written to epics.json must have a non-empty value_analysis (multi-paragraph),
  system_context, type in {flow, connection, quality}, and acceptance_condition string. Any epic
  missing these fields is rejected before write.</critical>
  <critical>In refine mode: epic entries whose proposals are rejected are left byte-identical. Only
  approved-change entries are modified.</critical>
  <critical>stories_done and stories_remaining are computed fresh from `.momentum/stories/index.json`
  at write time (Step 6). They are derived from each epic's `stories` array. Dropped and
  closed-incomplete stories are excluded from stories_remaining.</critical>

  <step n="1" goal="Mode detection, orphan scan, and task setup">
    <action>Check whether `_bmad-output/planning-artifacts/epics.json` exists. If it exists, read
    it and count epic entries.
      - Bootstrap mode: file absent OR file has fewer than 3 entries
      - Refine mode: file has 3 or more entries
    </action>
    <action>Announce the detected mode immediately — before any analysis or subagent spawning:
      "Epic Grooming — {bootstrap|refine} mode"
    </action>
    <action>Read `.momentum/stories/index.json`. Extract every unique `epic_slug` value with its
    story count. Build a complete slug → [story_slug, ...] map.
    </action>
    <action>Read `_bmad-output/planning-artifacts/epics.md` Epic List section to identify currently
    registered epic slugs and titles (for orphan cross-reference and context).
    </action>
    <action>Cross-reference stories/index.json slugs against epics.json keys (if in refine mode) or
    epics.md definitions (always):
      · Registered slugs — appear in epics.json (refine) or epics.md (always) with a definition
      · Orphaned slugs — appear in stories/index.json but have no epics.json or epics.md definition
    Report orphaned slug count.
    </action>
    <action>Create 4 tasks via TaskCreate:
      - TaskCreate: "Task 1 — Discovery" (parallel subagent data collection)
      - TaskCreate: "Task 2 — Synthesis + Value Analysis" (merge findings, produce candidate list)
      - TaskCreate: "Task 3 — Developer Review" (present candidates, collect feedback, approval gate)
      - TaskCreate: "Task 4 — Write + Post-write" (validate, write epics.json, commit)
    </action>
    <action>TaskUpdate Task 1 to in_progress.</action>
  </step>

  <step n="2" goal="Parallel discovery — spawn exactly 2 subagents in one message">
    <action>Spawn both subagents in a single message (fan-out — do NOT use TeamCreate):

      Agent A (model: haiku, effort: quick):
        Read `_bmad-output/planning-artifacts/prd.md` (use offset/limit for large files) and
        `_bmad-output/planning-artifacts/epics.md`.
        Extract all functional requirement (FR) clusters grouped by user-facing theme.
        For each theme cluster, propose an epic candidate with:
          - suggested slug (kebab-case)
          - suggested title
          - which FRs it covers
          - draft acceptance_condition ("A developer can [action] and [observe outcome]")
          - suggested type: flow / connection / quality
        Return a structured list of epic candidates.

      Agent B (model: haiku, effort: quick):
        Read `_bmad-output/planning-artifacts/architecture.md` (use offset/limit — commonly large),
        `.momentum/stories/index.json` (use offset/limit — commonly large), and
        `_bmad-output/planning-artifacts/epics.json` if it exists.
        Return:
          - Capability clusters from architectural components and story themes, grouped by epic_slug
          - Unmapped story groups: stories whose epic_slug doesn't align with any existing epic entry
          - Stale epic signals (if epics.json exists): epics with 0 stories_remaining but ongoing
            architectural investment
          - Quality NFR gaps: architectural NFR concerns not surfaced as standalone quality epics
        Return structured findings.
    </action>
    <action>Wait for both agents to complete. Merge their outputs for Step 3.</action>
    <action>TaskUpdate Task 1 to completed.</action>
    <action>TaskUpdate Task 2 to in_progress.</action>
  </step>

  <step n="3" goal="Foundation docs (bootstrap) or signal detection (refine)">
    <check if="bootstrap mode">
      <action>Before any synthesis output, create two foundation documents if they don't already
      exist from a prior epic-grooming session:

        1. Assessment: `_bmad-output/planning-artifacts/assessments/aes-NNN-epic-value-gap.md`
           Use the next available NNN sequence number (read existing files in assessments/).
           Content: value-gap analysis — what the product delivers today vs. full value vision,
           framed as the rationale for value-first epic design. Include current delivery gaps,
           dimensions of value beyond pain removal, and the philosophical anchor for why
           acceptance_conditions must be outcome-observable.

        2. Decision: `_bmad-output/planning-artifacts/decisions/dec-NNN-epic-value-first.md`
           Use the next available NNN sequence number.
           Content: record the decision to adopt value-first epic schema — slug + type +
           value_analysis + system_context + acceptance_condition as mandatory fields; rationale;
           alternatives; consequences.
      </action>
    </check>

    <check if="refine mode">
      <action>Scan the existing epics.json for all 6 signal types. Report counts for all 6
      (include zeros):
        - MERGE: epics whose scope overlaps substantially and could be combined
        - SPLIT: epics whose scope spans distinct concerns better tracked separately
        - DEDUP: epics with near-identical names or acceptance conditions
        - NEW: capability clusters from Agent B not represented in epics.json
        - RETIRE: epics with no remaining stories and no architectural investment
        - UPDATE: epics whose value_analysis or acceptance_conditions are stale

        Also report orphaned slugs from Step 1:
        - ORPHAN: epic_slug values in stories/index.json with no epics.json entry

        Output:
        Refine signals detected:
          · MERGE: {N}
          · SPLIT: {N}
          · DEDUP: {N}
          · NEW: {N}
          · RETIRE: {N}
          · UPDATE: {N}
          · ORPHAN: {N}
      </action>
    </check>
  </step>

  <step n="4" goal="Synthesis and value analysis">
    <action>Merge Agent A and Agent B findings. Deduplicate candidates (same theme under different
    names → pick the clearer slug).
    </action>
    <action>For each candidate epic, produce:
      - epic_slug: kebab-case, unique (this is the epics.json key)
      - name: clear noun phrase (display name)
      - description: one-line summary sentence
      - type: flow | connection | quality
        · flow — end-to-end user journeys and workflows
        · connection — integrations, data bridges, external system interactions
        · quality — NFR-driven concerns: performance, reliability, security, observability
      - value_analysis: multi-paragraph string (3 paragraphs minimum):
          Paragraph 1 — Current value delivered
          Paragraph 2 — Full vision including new capabilities (beyond pain removal)
          Paragraph 3 — Known gaps
      - system_context: 1–2 sentences explaining how this epic fits the overall product
      - acceptance_condition: single string — "A developer can [action] and [observe outcome]"
      - ⚠ flag: add if the epic has no current delivery — developer must confirm inclusion
    </action>

    <action>For orphaned slugs identified in Step 1, determine best resolution for each:
      (a) MERGE — orphaned slug's stories belong under an existing epic
      (b) CREATE — orphaned slug represents a coherent new category (≥3 stories)
      (c) SPLIT — stories under the slug span multiple concerns
    </action>

    <check if="bootstrap mode">
      <action>Count the candidates. If outside 8–25, output:
        ! WARNING: {N} candidates outside 8–25 range — review for gaps or over-segmentation.
      </action>
    </check>

    <action>TaskUpdate Task 2 to completed.</action>
    <action>TaskUpdate Task 3 to in_progress.</action>
  </step>

  <step n="5" goal="Developer review — holistic first, then approval gate">
    <action>Present the FULL candidate set with value_analysis and system_context for ALL epics
    before any per-epic gate. Do not ask for epic-by-epic approval at this stage.
    </action>

    <output>
Epic Grooming — Candidate Set ({N} epics)

{For each candidate:}
◦ {epic_slug} — "{name}" [{type}]
  value_analysis:
    {paragraph 1 — current value}

    {paragraph 2 — full vision}

    {paragraph 3 — known gaps}
  system_context: {text}
  acceptance_condition: {A developer can [action] and [observe outcome].}
  {⚠ Deferred value — no current delivery. Confirm inclusion? if flagged}

{If orphaned slugs have taxonomy proposals:}
Taxonomy proposals ({M} orphaned slugs):
  [{i}/{M}] {CHANGE_TYPE}: `{old-slug}` ({K} stories)
    Into/New: `{target-slug}`
    Rationale: {1-2 sentences}

---
    </output>

    <action>Ask these questions together:
      1. Epic coverage: Are all important product capabilities represented? Any gaps, redundancies,
         or epics that should be split or merged?
      2. Value accuracy: Do the value analyses correctly reflect current value, full vision, gaps?
      3. Deferred-value confirmation: For each ⚠ flagged epic — include now or defer entirely?
      4. Taxonomy proposals: Approve or reject each orphan resolution proposal (Y/N/Modify).
    </action>

    <action>Wait for free-form developer feedback. Incorporate all requested changes.</action>

    <action>For each ⚠ flagged epic: if the developer did not explicitly confirm inclusion, remove
    it from the candidate set. Do not carry un-confirmed ⚠ epics to the approval gate.
    </action>

    <check if="developer requested more than 3 changes">
      <action>Re-present the full updated candidate set before proceeding to the approval gate.</action>
    </check>

    <action>Do NOT write epics.json before the following approval gate is passed.</action>

    <output>
## Approve Writing `epics.json`? [Y/N]

**{N} epics ready to write:**
  {list slugs}
    </output>

    <action>TaskUpdate Task 3 to completed.</action>

    <check if="developer does not confirm with Y">
      <action>TaskUpdate Task 4 to completed.</action>
      <output>> No write performed. `epics.json` unchanged. Workflow complete.</output>
      <action>STOP — do not proceed to Step 6.</action>
    </check>
  </step>

  <step n="6" goal="Write and post-write">
    <action>TaskUpdate Task 4 to in_progress.</action>

    <action>Validate all candidate types before writing. Reject any epic whose type is not in
    {flow, connection, quality}:
      ! REJECTED: {epic_slug} — invalid type "{bad_type}". Must be flow, connection, or quality.
      Remove rejected epics from the write set and notify the developer.
    </action>

    <action>Compute stories_done and stories_remaining for each epic from
    `.momentum/stories/index.json`:
      - stories_done: count of slugs in the epic's `stories` array with status "done"
      - stories_remaining: count with status not "done", "dropped", or "closed-incomplete"
      - Slugs not found in the index are excluded from both counts
    </action>

    <check if="bootstrap mode">
      <action>Ensure the aes-NNN and dec-NNN foundation docs were written in Step 3. If missing,
      write them now before writing epics.json.</action>
    </check>

    <check if="refine mode">
      <action>For epics whose proposals were not approved, copy the existing entry byte-identical
      from the current epics.json. Do not modify these entries.</action>
    </check>

    <action>Write `_bmad-output/planning-artifacts/epics.json`. epics.json is a JSON object (dict)
    keyed by epic_slug. Sort order: flow epics first (alpha by epic_slug), then connection, then
    quality. Each entry schema:
      {
        "epic_slug": "...",
        "name": "...",
        "type": "flow|connection|quality",
        "description": "...",
        "acceptance_condition": "A developer can [action] and [observe outcome].",
        "value_analysis": "...",
        "system_context": "...",
        "status": "working|partial|not-started",
        "stories": ["story-slug-1", ...],
        "stories_done": N,
        "stories_remaining": M,
        "last_verified": "YYYY-MM-DD",
        "notes": ""
      }
    </action>

    <action>Apply approved taxonomy changes (orphan resolutions):
      For each approved MERGE change:
        Call `python3 skills/momentum/scripts/momentum-tools.py sprint epic-membership
        --story {story-slug} --epic {target-slug}` for each story in the source slug.
      For each approved CREATE change:
        Add the new epic definition to `_bmad-output/planning-artifacts/epics.md`.
      For each approved SPLIT change:
        Call `python3 skills/momentum/scripts/momentum-tools.py sprint epic-membership
        --story {story-slug} --epic {target-slug}` for each story and its split destination.
    </action>

    <action>Compute unmapped stories: stories whose epic_slug does not appear in any epic's
    `stories` array in the written epics.json (excluding done/dropped/closed-incomplete).
    </action>

    <action>Commit the changes:
      git add _bmad-output/planning-artifacts/epics.json
      {In bootstrap mode: also add the aes-NNN and dec-NNN files}
      git commit -m "docs(epics): epic-grooming {bootstrap|refine} — {N} epics, {M} proposals applied"
    </action>

    <action>TaskUpdate Task 4 to completed.</action>

    <output>
## Epic Grooming — Complete

**Mode:** {bootstrap|refine}
**Epics written:** {N}
  - flow: {count} ({slugs})
  - connection: {count} ({slugs})
  - quality: {count} ({slugs})

**Taxonomy changes applied:**
  · Epics created (orphan resolutions): {N}
  · Stories reassigned: {M}

**Unmapped stories:** {count}
{If count > 0:}
> ! Stories not assigned to any epic:
>   {· story-slug-1}
>   {· story-slug-2}
>   Run `/momentum:epic-grooming` (refine) or add story slugs to the appropriate epic's
>   `stories` array to resolve.

{In bootstrap mode:}
**Foundation docs written:**
  · `{aes-NNN-epic-value-gap.md}`
  · `{dec-NNN-epic-value-first.md}`

**Committed:** `docs(epics): epic-grooming {bootstrap|refine} — {N} epics, {M} proposals applied`
    </output>
  </step>
</workflow>
