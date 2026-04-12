# Feature Grooming Workflow

**Goal:** Produce a complete, value-oriented feature taxonomy — either bootstrapping features.json from scratch or refining an existing one — with every feature carrying a multi-paragraph value_analysis, system_context, typed classification, and verifiable acceptance conditions.

**Voice:** Impetus voice — oriented, factual, forward-moving. Symbol vocabulary: ✓ confirmed, ◦ candidate, → current, ! warning, ⚠ deferred-value flag, · list item.

---

## EXECUTION

<workflow>
  <critical>features.json is NOT written until the Step 5 approval gate is explicitly passed with "Y". No write occurs before this gate under any circumstance.</critical>
  <critical>Exactly 2 subagents are spawned in Step 2 — no more, no less. Both are launched in a single message (fan-out pattern, NOT TeamCreate). The orchestrator handles all synthesis, value analysis, developer interaction, and writing directly.</critical>
  <critical>Every feature written to features.json must have a non-empty value_analysis (multi-paragraph), system_context, type in {flow, connection, quality}, and acceptance_condition string. Any feature missing these fields is rejected before write.</critical>
  <critical>In refine mode: feature entries whose proposals are rejected are left byte-identical. Only approved-change entries are modified.</critical>
  <critical>stories_done and stories_remaining are computed fresh from `_bmad-output/implementation-artifacts/stories/index.json` at write time (Step 6). They are derived from each feature's `stories` array — look up each story slug in the index, check its status. Dropped and closed-incomplete stories are excluded from stories_remaining.</critical>

  <step n="1" goal="Mode detection and task setup">
    <action>Check whether `_bmad-output/planning-artifacts/features.json` exists. If it exists, read it and count feature entries.
      - Bootstrap mode: file absent OR file has fewer than 3 entries
      - Refine mode: file has 3 or more entries
    </action>
    <action>Announce the detected mode immediately — before any analysis or subagent spawning:
      "Feature Grooming — {bootstrap|refine} mode"
    </action>
    <action>Create 4 tasks via TaskCreate:
      - TaskCreate: "Task 1 — Discovery" (parallel subagent data collection)
      - TaskCreate: "Task 2 — Synthesis + Value Analysis" (merge findings, produce candidate list)
      - TaskCreate: "Task 3 — Developer Review" (present candidates, collect feedback, approval gate)
      - TaskCreate: "Task 4 — Write + Post-write" (validate, write features.json, hash, commit)
    </action>
    <action>TaskUpdate Task 1 to in_progress.</action>
  </step>

  <step n="2" goal="Parallel discovery — spawn exactly 2 subagents in one message">
    <action>Spawn both subagents in a single message (fan-out — do NOT use TeamCreate):

      Agent A (model: haiku, effort: quick):
        Read `_bmad-output/planning-artifacts/prd.md` (use offset/limit for large files — it is commonly large) and `_bmad-output/planning-artifacts/epics.md`.
        Extract all functional requirement (FR) clusters grouped by user-facing theme.
        For each theme cluster, propose a feature candidate with:
          - suggested slug (kebab-case)
          - suggested title
          - which FRs it covers
          - draft acceptance_conditions array ("A developer can [action] and [observe outcome]")
          - suggested type: flow (end-to-end user journeys) / connection (integrations, data bridges) / quality (NFR-driven: performance, reliability, security)
        Return a structured list of feature candidates.

      Agent B (model: haiku, effort: quick):
        Read `_bmad-output/planning-artifacts/architecture.md` (use offset/limit — commonly large), `_bmad-output/implementation-artifacts/stories/index.json` (use offset/limit — commonly large), and `_bmad-output/planning-artifacts/features.json` if it exists.
        Return:
          - Capability clusters identified from architectural components and story themes, grouped by epic_slug
          - Unmapped story groups: stories whose themes don't align with any existing feature (if features.json exists) or any FR cluster
          - Stale feature signals (if features.json exists): features with 0 stories_remaining but ongoing architectural investment
          - Quality NFR gaps: architectural NFR concerns not surfaced as standalone quality features
        Return structured findings.
    </action>
    <action>Wait for both agents to complete. Merge their outputs for Step 3.</action>
    <action>TaskUpdate Task 1 to completed.</action>
    <action>TaskUpdate Task 2 to in_progress.</action>
  </step>

  <step n="3" goal="Foundation docs (bootstrap) or signal detection (refine)">
    <check if="bootstrap mode">
      <action>Before any synthesis output, create two foundation documents:

        1. Assessment: `_bmad-output/planning-artifacts/assessments/aes-NNN-feature-value-gap.md`
           Use the next available NNN sequence number (read existing files in assessments/ to find it).
           Content: capture the value-gap analysis — what the product delivers today vs. the full value vision, framed as the rationale for value-first feature design.
           Include: current delivery gaps identified from Agent A/B findings, dimensions of value beyond pain removal (new capabilities, knowledge, experience), and the philosophical anchor for why acceptance_conditions must be outcome-observable.

        2. Decision: `_bmad-output/planning-artifacts/decisions/dec-NNN-feature-value-first.md`
           Use the next available NNN sequence number.
           Content: record the decision to adopt value-first feature schema — slug + type + value_analysis + system_context + acceptance_conditions as mandatory fields; rationale; alternatives considered; consequences.
      </action>
    </check>

    <check if="refine mode">
      <action>Scan the existing features.json for all 6 signal types. Report counts for all 6 (include zeros):
        - MERGE: features whose scope overlaps substantially and could be combined
        - SPLIT: features whose scope spans distinct concerns better tracked separately
        - DEDUP: features with near-identical names or acceptance conditions
        - NEW: capability clusters from Agent B not represented in features.json
        - RETIRE: features with no remaining stories and no architectural investment
        - UPDATE: features whose value_analysis or acceptance_conditions are stale relative to current architecture/stories

        Output:
        Refine signals detected:
          · MERGE: {N}
          · SPLIT: {N}
          · DEDUP: {N}
          · NEW: {N}
          · RETIRE: {N}
          · UPDATE: {N}
      </action>
    </check>
  </step>

  <step n="4" goal="Synthesis and value analysis">
    <action>Merge Agent A and Agent B findings. Deduplicate candidates (same theme under different names → pick the clearer slug).</action>
    <action>For each candidate feature, produce:
      - feature_slug: kebab-case, unique (this is the features.json key)
      - name: clear noun phrase (display name)
      - description: one-line summary sentence
      - type: flow | connection | quality
        · flow — end-to-end user journeys and workflows
        · connection — integrations, data bridges, external system interactions
        · quality — NFR-driven concerns: performance, reliability, security, observability
      - value_analysis: multi-paragraph string (3 paragraphs minimum):
          Paragraph 1 — Current value delivered: what users/developers can do today because of this feature
          Paragraph 2 — Full vision including new capabilities: what this feature enables beyond pain removal — new workflows, new knowledge, new experiences made possible
          Paragraph 3 — Known gaps: what is missing, deferred, or not yet realized
        Do NOT reduce value_analysis to pain removal only. Explicitly consider capability expansion.
      - system_context: 1–2 sentences explaining how this feature fits and enhances the overall product architecture and user model
      - acceptance_condition: single string in format "A developer can [action] and [observe outcome]" — binary and verifiable
      - ⚠ flag: add if the feature has no current delivery (all value is deferred/aspirational) — developer must confirm inclusion
    </action>

    <check if="bootstrap mode">
      <action>Count the candidates. If count is outside 8–25, output:
        ! WARNING: {N} candidates outside 8–25 range — review for gaps or over-segmentation before proceeding.
      </action>
    </check>

    <action>TaskUpdate Task 2 to completed.</action>
    <action>TaskUpdate Task 3 to in_progress.</action>
  </step>

  <step n="5" goal="Developer review — holistic first">
    <action>Present the FULL candidate set with value_analysis and system_context for ALL features before any per-feature gate. Do not ask for feature-by-feature approval at this stage.</action>

    <output>
Feature Grooming — Candidate Set ({N} features)

{For each candidate:}
◦ {feature_slug} — "{name}" [{type}]
  value_analysis:
    {paragraph 1 — current value}

    {paragraph 2 — full vision}

    {paragraph 3 — known gaps}
  system_context: {text}
  acceptance_condition: {A developer can [action] and [observe outcome].}
  {⚠ Deferred value — no current delivery. Confirm inclusion? if flagged}

---
    </output>

    <action>Ask these three questions together, in order:
      1. Feature coverage: Are all important product capabilities represented? Are there gaps, redundancies, or features that should be split or merged?
      2. Value accuracy: Do the value analyses correctly reflect what each feature delivers — current value, full vision, and gaps?
      3. Deferred-value confirmation: For each ⚠ flagged feature — should it be included in features.json now, or deferred entirely?
    </action>

    <action>Wait for free-form developer feedback. Incorporate all requested changes into the candidate set.</action>

    <check if="developer requested more than 3 changes">
      <action>Re-present the full updated candidate set before proceeding to the approval gate.</action>
    </check>

    <action>Do NOT write features.json before the following approval gate is passed.</action>

    <output>
Approve writing features.json? [Y/N]

{N} features ready to write:
  {list slugs}
    </output>

    <action>TaskUpdate Task 3 to completed.</action>

    <check if="developer does not confirm with Y">
      <action>TaskUpdate Task 4 to completed.</action>
      <output>No write performed. features.json unchanged. Workflow complete.</output>
      <action>STOP — do not proceed to Step 6 or any further steps.</action>
    </check>
  </step>

  <step n="6" goal="Write and post-write">
    <action>TaskUpdate Task 4 to in_progress.</action>

    <action>Validate all candidate types before writing. Reject any feature whose type is not in {flow, connection, quality}:
      ! REJECTED: {feature_slug} — invalid type "{bad_type}". Must be flow, connection, or quality.
      Remove rejected features from the write set and notify the developer.
    </action>

    <action>Compute stories_done and stories_remaining for each feature from `_bmad-output/implementation-artifacts/stories/index.json` (use offset/limit — commonly large):
      - Each feature has a `stories` array listing story slugs assigned to it
      - stories_done: count of slugs in `stories` whose entry in the index has status "done"
      - stories_remaining: count of slugs in `stories` whose entry has status not "done", not "dropped", not "closed-incomplete"
      - If a slug in `stories` is not found in the index, exclude it from both counts
    </action>

    <check if="bootstrap mode">
      <action>Ensure the aes-NNN and dec-NNN foundation docs were written in Step 3. If not (due to an error), write them now before writing features.json.</action>
    </check>

    <check if="refine mode">
      <action>For features whose proposals were not approved by the developer, copy the existing entry byte-identical from the current features.json. Do not modify these entries.</action>
    </check>

    <action>Write `_bmad-output/planning-artifacts/features.json`. features.json is a JSON object (dict) keyed by feature_slug. Sort order: flow features first (alpha by feature_slug), then connection, then quality. Each entry schema:
      {
        "feature_slug": "...",
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
      Note: `acceptance_condition` is a string, not an array. `description` is a one-line summary; `value_analysis` is the multi-paragraph value content.
    </action>

    <action>Run: `python3 skills/momentum/scripts/momentum-tools.py feature-status-hash`
      Include the hash result in the output.
    </action>

    <action>Compute unmapped stories: read `_bmad-output/implementation-artifacts/stories/index.json` and find all stories where:
      - status is not "done" AND status is not "dropped" AND status is not "closed-incomplete"
      - the story slug does not appear in any feature's `stories` array in the written features.json
    </action>

    <action>Commit the changes:
      git add _bmad-output/planning-artifacts/features.json
      {In bootstrap mode: also add the aes-NNN and dec-NNN files by their exact paths from Step 3}
      git commit -m "docs(features): feature-grooming {bootstrap|refine} — {N} features, {M} proposals applied"
      (In bootstrap: M = number of candidates accepted. In refine: M = number of signal-driven proposals approved.)
    </action>

    <action>TaskUpdate Task 4 to completed.</action>

    <output>
Feature Grooming — Complete

Mode: {bootstrap|refine}
Features written: {N}
  flow: {count} ({slugs})
  connection: {count} ({slugs})
  quality: {count} ({slugs})

Feature status hash: {hash}

Unmapped stories: {count}
{If count > 0:}
  ! Stories not assigned to any feature:
    {· story-slug-1}
    {· story-slug-2}
    ...
  Run /momentum:feature-grooming (refine) or add story slugs to the appropriate feature's `stories` array to resolve.

{In bootstrap mode:}
Foundation docs written:
  · {aes-NNN-feature-value-gap.md}
  · {dec-NNN-feature-value-first.md}

Committed: docs(features): feature-grooming {bootstrap|refine} — {N} features, {M} proposals applied
    </output>
  </step>
</workflow>
