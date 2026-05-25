# momentum:triage Workflow

**Goal:** Process multiple observations in one pass. Run dedup gate (Phases 0–3), present
dedup + classification approval (Phase 5), then delegate to the appropriate downstream
executor or write capture events to `intake-queue.jsonl`.

**Role:** Orchestrator between upstream sources (retro output, conversation, assessment
findings) and the per-item executors (`momentum:intake`, `momentum:decision`). Does NOT
perform gap-check (DEC-005 D10). Does NOT write story files directly — that is delegated
to `momentum:intake`.

**Voice:** Impetus voice — dry, confident, forward-moving. Symbol vocabulary:
✓ completed, → current, ◦ upcoming, ! warning, ✗ failed, ? proactive offer, · list item.

---

## Classification Table

| Class | Meaning | Downstream action |
|-------|---------|-------------------|
| ARTIFACT | A story that should enter the backlog | Delegate to `momentum:intake` with enriched context |
| DECISION | A strategic decision to record | Delegate to `momentum:decision` |
| SHAPING | Needs more thinking before classification | Write `kind: shape` event to `intake-queue.jsonl` |
| DEFER | Valid but not now — park it | Write `kind: watch` event to `intake-queue.jsonl` |
| REJECT | Not worth pursuing | Write `kind: rejected` event to `intake-queue.jsonl` |

---

<workflow>

  <critical>Do NOT perform gap-check on any item. Classification only — per DEC-005 D10.</critical>

  <critical>Never write story files, story index entries, or planning artifacts directly.
  ARTIFACT delegation goes to momentum:intake. DECISION delegation goes to momentum:decision.
  Only intake-queue.jsonl is written directly (for SHAPING, DEFER, REJECT classes).</critical>

  <critical>All mutations to stories/index.json go through momentum-tools CLI only via
  momentum:intake. Triage never calls momentum-tools story-add directly.</critical>

  <critical>Batch approval (Step 4) is required before any execution. Never skip it, even
  for a single-item triage session.</critical>

  <critical>Phase 0 (prefilter) ALWAYS runs before classification, even for single-item
  batches. Never skip Phase 0.</critical>

  <critical>Phase 2 dedup subagents MUST be spawned in a single message (parallel foreground).
  Never spawn dedup agents sequentially. Never use TeamCreate or SendMessage.</critical>

  <step n="1" goal="Surface source items and re-surface open queue items">
    <action>Read `.momentum/intake-queue.jsonl` if it exists.
    Filter for open items: kind in {shape, watch, handoff} with `status == "open"`.
    Store {{open_queue_items}} = list of open shape/watch events.
    </action>

    <check if="{{open_queue_items}} is non-empty">
      <output>
Open queue items from previous sessions ({{count}} pending):

{{for each item:
  · [{{kind|upper}}] {{item.title}} — {{item.description}} (captured: {{item.timestamp}})
    Source: {{item.source}} · id: {{item.id}}
}}

These will be included alongside new items for re-classification.
      </output>
    </check>

    <check if="invoked from retro or assessment with a pre-enumerated list">
      <action>Store {{raw_items}} = the pre-enumerated list passed in by the caller,
      prefixed with {{source_label}} (e.g., "retro Phase 5", "assessment finding").</action>
    </check>

    <check if="invoked directly by developer (no pre-enumerated list)">
      <ask>What observations do you want to triage? List them as plain items — one per
      line, bullet, or number. You can also paste retro findings, assessment recommendations,
      or any other multi-item list.</ask>
      <action>Store {{raw_items}} = developer's list. Store {{source_label}} = "conversation".</action>
    </check>

    <action>Merge {{open_queue_items}} and {{raw_items}} into {{all_items}}.
    Tag open queue items with `[QUEUED]` prefix for display distinction.
    Assign a stable local ID to each item (e.g., iq-temp-001, iq-temp-002 …) for matrix
    indexing when items do not already carry an `id` field.</action>
  </step>

  <step n="2" goal="Read context artifacts for enrichment">
    <action>Read `_bmad-output/planning-artifacts/features.json` to get the features list.
    Store {{features}} = map of feature_slug → name for suggestion during enrichment.</action>

    <action>Read `_bmad-output/planning-artifacts/epics.md` to get the epic list.
    Store {{epics}} = list of epic slugs for DDD boundary awareness.</action>

    <note>Use offset/limit if either file is large. features.json and epics.md are
    typically under the token limit but may grow.</note>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 0: DETERMINISTIC PREFILTER                        -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="2.1" goal="Phase 0 — run prefilter to build shortlists and similarity matrix">
    <note>Phase 0 always runs. Even for a single-item batch the similarity matrix is needed
    for Phase 1 branching logic.</note>

    <action>Serialize {{all_items}} as a JSON array. Each element must have at minimum:
      { "id": "...", "title": "...", "description": "...",
        "touches": [...], "epic_slug": "...", "feature_slug": "..." }
    Items from {{open_queue_items}} use their existing `id` field.
    Items from {{raw_items}} without an `id` use the temp IDs assigned in Step 1.
    </action>

    <action>Run prefilter CLI:
```
python3 skills/momentum/scripts/momentum-tools.py triage prefilter \
  --items-json '{{serialized_items_json}}' \
  --stories-index .momentum/stories/index.json
```
    </action>

    <action>Parse the JSON output.
    Store {{shortlists}} = output.shortlists  (map of item_id → top-K=10 candidates).
    Store {{similarity_matrix}} = output.similarity_matrix  (list of {item_i, item_j, cosine_similarity}).
    Store {{candidate_count}} = output.candidate_count.
    </action>

    <check if="prefilter command fails (non-zero exit or error field in output)">
      <output>! Phase 0 prefilter failed: {{error}}
Falling back to classification without dedup gate. Backlog hygiene note: dedup skipped this run.</output>
      <action>Store {{shortlists}} = {} (empty). Store {{similarity_matrix}} = [].
      Continue to Step 2.2 with empty prefilter output — Phase 1 will assign all items to
      one cluster, Phase 2 will spawn one dedup agent with no candidates.</action>
    </check>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 1: INLINE CLUSTERING                              -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="2.2" goal="Phase 1 — cluster incoming items using similarity matrix">
    <action>Count N = total items in {{all_items}}.</action>

    <check if="N ≤ 5">
      <action>Skip clustering. Assign all items to a single cluster: {{clusters}} = [{{all_items}}].
      One dedup agent will process the whole batch.</action>
    </check>

    <check if="N > 5">
      <action>Greedy threshold clustering using {{similarity_matrix}}:
      1. Extract all (item_i, item_j, cosine_similarity) pairs where item_i ≠ item_j.
      2. Sort pairs by cosine_similarity descending.
      3. Initialize each item as unassigned. Maintain {{clusters}} = [].
      4. For each pair (i, j) in sorted order:
           a. Skip if both i and j are already in the SAME cluster.
           b. If both unassigned: create a new cluster containing {i, j}.
           c. If one is assigned and the other is unassigned AND the assigned cluster has
              fewer than 7 members: add the unassigned item to that cluster.
           d. If both are in different clusters AND merging would not exceed 7 members:
              merge the two clusters.
           e. If a cluster would exceed 7 members: start a new cluster for the unassigned item.
      5. Any item still unassigned after processing all pairs gets its own singleton cluster.
      Target cluster size: 3–7. Clusters of 1–2 are acceptable for tail items.
      </action>
    </check>

    <action>Store {{clusters}} = final list of clusters. Each cluster is a list of items.</action>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 2: DEDUP FAN-OUT (PARALLEL SUBAGENT SPAWN)        -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="2.3" goal="Phase 2 — spawn dedup subagent per cluster in parallel">
    <note>CRITICAL: all dedup agent spawns go in ONE message (parallel foreground agents).
    Do not loop and spawn sequentially. Do not use TeamCreate or SendMessage.
    This mirrors retro/workflow.md Phase 4 auditor fan-out exactly.</note>

    <action>For each cluster in {{clusters}}, build the dedup agent prompt:

      Compute union_shortlist for this cluster:
        union = {} (keyed by slug)
        for each item in cluster:
          for each candidate in {{shortlists}}[item.id]:
            if candidate.slug not in union OR candidate.combined_score > union[candidate.slug].combined_score:
              union[candidate.slug] = candidate
        union_shortlist = list(union.values()), sorted by combined_score descending

      For each candidate slug in union_shortlist, load full story metadata from
      `.momentum/stories/index.json` (title, description, status, epic_slug,
      feature_slug, touches, depends_on).

      PROMPT:
      ---
      You are a dedup specialist reviewing incoming work items against an existing story backlog.

      ## Cluster items ({{cluster_size}} items — analyze each one)

      {{for each item in cluster:
        ---
        Item ID: {{item.id}}
        Title: {{item.title}}
        Description: {{item.description}}
        Touches: {{item.touches | join(", ")}}
        Epic: {{item.epic_slug}}
        ---
      }}

      ## Prefiltered candidate stories (union shortlist for this cluster — {{union_count}} candidates)

      {{for each candidate in union_shortlist:
        Slug: {{slug}}
        Title: {{title}}
        Status: {{status}} · Epic: {{epic_slug}}
        Score: combined={{combined_score}} (tfidf={{tfidf_score}}, jaccard={{jaccard_score}})
        Description: {{description}}
        ---
      }}

      ## Task

      For EACH item in the cluster, produce one or more per-theme findings.
      If an item covers multiple distinct concerns, produce a separate finding per theme
      (this surfaces it as a split candidate).

      Return a JSON array as your FINAL RESPONSE. Each element must conform exactly to:
      {
        "source_item_id": "the item id from above",
        "theme": "short label for this theme (≤10 words)",
        "match_type": "duplicate | supersedes | extends | unique",
        "matched_story_slug": "slug-of-matched-story OR null if unique",
        "evidence": "1-2 sentence justification",
        "recommended_action": "consume | merge | replace | continue",
        "consolidation_hint": {
          "target_slug_or_theme": "slug or theme label",
          "rationale": "why these should be consolidated"
        } or null
      }

      Rules:
      - match_type "duplicate" → recommended_action "consume"
      - match_type "supersedes" → recommended_action "replace"
      - match_type "extends" → recommended_action "merge" or "continue"
      - match_type "unique" → recommended_action "continue", matched_story_slug null
      - Only recommend "consume" if the incoming item adds nothing beyond what the existing
        story already covers.

      Return ONLY the JSON array. No preamble, no explanation, no markdown code fence.
      ---
    </action>

    <action>Spawn ALL dedup subagents in a SINGLE message (parallel foreground agents).
    Collect all JSON array responses.
    Flatten into {{dedup_findings}} = single list of all per-theme finding objects.
    </action>

    <check if="any agent returns malformed JSON or non-array response">
      <output>! Dedup agent for cluster {{cluster_index}} returned malformed output — findings skipped for that cluster.</output>
      <action>Continue with findings from other clusters. Record the gap for summary.</action>
    </check>
  </step>

  <!-- ═══════════════════════════════════════════════════════ -->
  <!-- PHASE 3: CONSOLIDATION CANDIDATE GROUPING               -->
  <!-- ═══════════════════════════════════════════════════════ -->

  <step n="2.4" goal="Phase 3 — inline consolidation-candidate grouping">
    <note>Pure inline pass — no subagent. Flags groups for Story B; no merge execution here.</note>

    <action>Group {{dedup_findings}} by consolidation_hint.target_slug_or_theme:
    For each finding where consolidation_hint is non-null:
      Add finding to group keyed by consolidation_hint.target_slug_or_theme.
    Groups with 2+ members → merge candidate.
    Store {{merge_candidates}} = list of {target, members: [findings...], rationale}.
    </action>

    <action>Also scan {{similarity_matrix}} for cross-cluster consolidation signals:
    For any (item_i, item_j) pair with cosine_similarity ≥ 0.4 where item_i and item_j
    were NOT in the same cluster in Phase 1 — append a merge candidate:
      { target: "cross-cluster-pair", members: [item_i, item_j],
        rationale: "high intra-batch similarity (cosine {{score}})" }
    </action>

    <action>Store {{split_candidates}} = items where {{dedup_findings}} contains
    2+ findings with the same source_item_id.
    Each: { item_id: "...", themes: [list of theme strings] }
    </action>

    <action>Store {{survivor_items}}:
    For each item in {{all_items}}:
      findings_for_item = [f for f in {{dedup_findings}} where f.source_item_id == item.id]
      if all(f.recommended_action == "consume" for f in findings_for_item):
        → consumed (excluded from classification)
      else:
        → survivor (proceed to Step 3 classification)
    Items with no findings at all → survivors (treated as unique).
    </action>
  </step>

  <step n="3" goal="Classify and enrich survivor items">
    <action>For each item in {{survivor_items}}, classify it into exactly one of five classes:
    ARTIFACT, DECISION, SHAPING, DEFER, REJECT.

    Classification heuristics:
    · ARTIFACT — a bounded piece of work that belongs in the story backlog. Signals:
        "we should build X", "X is missing", "add Y to Z", "story: ...", a feature request,
        a bug report, a task with a clear deliverable. DEC-005 D5 story types: feature /
        maintenance / defect / exploration / practice.
    · DECISION — a strategic question that needs a recorded decision document. Signals:
        "we need to decide X", "should we adopt Y?", "the architecture question is Z".
    · SHAPING — interesting but needs thinking before it can be classified. Signals:
        vague intent, unclear scope, "I'm not sure if this is...", "maybe someday X".
    · DEFER — valid item but explicitly not now. Signals: "park this", "not this sprint",
        "come back to X when Y is done", future-phase items.
    · REJECT — not worth pursuing. Signals: "never mind", "this was wrong", duplicates
        already in backlog, superseded by something else.
    </action>

    <action>For each ARTIFACT item, enrich with:
    · {{feature_slug}}: suggest from {{features}} — pick the closest match by name/description.
        If none fits, leave blank and flag as "no feature match — may need a new feature".
    · {{story_type}}: heuristic from description — default "feature"; use "defect" for bugs,
        "maintenance" for upgrades/refactors, "exploration" for research spikes,
        "practice" for Momentum meta-work.
    · {{epic_slug}}: suggest from {{epics}} based on DDD boundary alignment.
    · {{priority}}: default "low"; promote to "medium" or "high" if urgency signals present.
    · {{proposed_depends_on}}: flag obvious blockers if mentioned; default empty.
    </action>

    <action>Store {{classified_items}} = list of {original_text, class, enrichment (if ARTIFACT), suggested_action}</action>
  </step>

  <step n="4" goal="Batch approval — present dedup findings + classification for developer review">
    <output>
Triage — {{total_count}} items · {{dedup_findings | length}} dedup findings · {{survivor_count}} survivors proceeding to classification

<!-- ── SECTION A: DEDUP ACTIONS ─────────────────────────── -->
{{if dedup_findings is non-empty:}}
## Dedup Actions

{{if consume group (recommended_action == "consume"):}}
**consume** ({{count}} — confirmed duplicates — will be removed from classification):
{{for each finding:
  · [{{source_item_id}}] {{theme}}
    match: {{match_type}} → `{{matched_story_slug}}`
    evidence: {{evidence}}
    → 'consume {{N}}' to confirm · 'skip {{N}}' to override
}}

{{if merge group (recommended_action == "merge"):}}
**merge** ({{count}} — should be combined with existing story):
{{for each finding:
  · [{{source_item_id}}] {{theme}}
    match: {{match_type}} → `{{matched_story_slug}}`
    evidence: {{evidence}}
}}

{{if replace group (recommended_action == "replace"):}}
**replace** ({{count}} — supersedes existing story):
{{for each finding:
  · [{{source_item_id}}] {{theme}}
    match: {{match_type}} → `{{matched_story_slug}}`
    evidence: {{evidence}}
}}

{{if continue group (recommended_action == "continue"):}}
**continue** ({{count}} — unique, proceeding to classification):
{{for each finding:
  · [{{source_item_id}}] {{theme}} — no backlog match
}}

<!-- ── SECTION B: SPLIT CANDIDATES ─────────────────────── -->
{{if split_candidates is non-empty:}}
## Split Candidates (multi-theme items — consider splitting before intake)

{{for each split candidate:
  · [{{item_id}}] covers {{theme_count}} themes:
    {{for each theme: - {{theme}}}}
}}

<!-- ── SECTION C: MERGE CANDIDATES ─────────────────────── -->
{{if merge_candidates is non-empty:}}
## Merge Candidates — flagged for Story B (display only, no action available)

{{for each group:
  · target: {{target_slug_or_theme}}  ({{member_count}} items)
    members: {{member_item_ids | join(", ")}}
    rationale: {{rationale}}
}}

<!-- ── SECTION D: FIVE-CLASS CLASSIFICATION ─────────────── -->
## Classification — {{survivor_count}} survivors

{{if ARTIFACT items:}}
[ARTIFACT] — {{count}} items  →  will be sent to momentum:intake
{{for each:
  [N] {{title_or_summary}}
      type: {{story_type}} · feature: {{feature_slug|"(none)"}} · epic: {{epic_slug}} · priority: {{priority}}
      {{proposed_depends_on if non-empty: depends: {{proposed_depends_on}}}}
}}
  → Approve all? (A=all / R=all / pick individually by number)

{{if DECISION items:}}
[DECISION] — {{count}} items  →  will be sent to momentum:decision
{{for each: [N] {{description}}}}
  → Approve all? (A=all / R=all / pick individually by number)

{{if SHAPING items:}}
[SHAPING] — {{count}} items  →  will be written to intake-queue.jsonl (kind: shape)
{{for each: [N] {{description}}}}
  → Approve all? (A=all / R=all / pick individually by number)

{{if DEFER items:}}
[DEFER] — {{count}} items  →  will be written to intake-queue.jsonl (kind: watch)
{{for each: [N] {{description}}}}
  → Approve all? (A=all / R=all / pick individually by number)

{{if REJECT items:}}
[REJECT] — {{count}} items  →  will be written to intake-queue.jsonl (kind: rejected)
{{for each: [N] {{description}}}}
  → Approve all? (A=all / R=all / pick individually by number)

Override specific items? Enter numbers to re-classify or edit, or 'done' to proceed.
    </output>

    <action>Handle developer input:
    · "A" or "approve all [class]" → mark all in class as approved
    · "R" or "reject all [class]" → mark all in class as rejected (no action taken)
    · "[N]" → re-classify or edit that item interactively
    · Ranges "2-5" → batch approve/reject that range
    · "consume N" → confirm item N as duplicate (remove from classification survivors)
    · "skip N" → override dedup finding for item N, keep in classification
    · "done" → finalize with current approvals
    </action>

    <action>Store {{approved_items}} = all approved classified survivors</action>
    <action>Store {{consumed_items}} = all items confirmed as duplicates</action>
    <action>Store {{rejected_count}} = count of items rejected in approval step (not REJECT-class items)</action>

    <check if="{{open_queue_items}} contains items with no new action">
      <ask>Open queue items with no new classification will remain in the queue.
      Enter IDs to mark as resolved (e.g., "resolve 2, 5") or 'done' to leave them open.</ask>
      <action>Store {{resolved_queue_ids}} = IDs to mark as resolved</action>
    </check>
  </step>

  <step n="5" goal="Execute approved actions">
    <action>Process approved items in this order:

    **Consumed duplicate items** — mark as consumed in intake-queue.jsonl (if from queue):
      For each item in {{consumed_items}} that originated from {{open_queue_items}}:
        python3 skills/momentum/scripts/momentum-tools.py intake-queue consume \
          --id "{{queue_id}}"
      Raw items (not from queue) with consume action: no further action needed.

    **ARTIFACT items** — spawn momentum:intake per item (in parallel if multiple):
      Pass enriched context to intake:
        - title: derived from item text
        - description: item text expanded
        - feature_slug: approved feature_slug
        - story_type: approved story_type
        - epic_slug: approved epic_slug
        - priority: approved priority
        - proposed_depends_on: approved depends_on list
        - pain_context: any urgency/recurrence signals from the item
        - source: "triage — {{source_label}}"
      Wait for all intake spawns to complete before proceeding.
      Store {{intake_results}} = list of {title, slug, stub_path} returned by intake.

    **DECISION items** — spawn momentum:decision per item (sequentially — decision is interactive):
      Pass context from item. Wait for each decision to complete before next.
      Store {{decision_results}} = list of {title, outcome}.

    **SHAPING items** — write to intake-queue.jsonl via CLI:
      For each approved SHAPING item:
        python3 skills/momentum/scripts/momentum-tools.py intake-queue append \
          --kind shape \
          --title "{{title}}" \
          --description "{{description}}" \
          --source "triage"

    **DEFER items** — write to intake-queue.jsonl via CLI:
      For each approved DEFER item:
        python3 skills/momentum/scripts/momentum-tools.py intake-queue append \
          --kind watch \
          --title "{{title}}" \
          --description "{{description}}" \
          --source "triage"

    **REJECT items** — write to intake-queue.jsonl via CLI:
      For each approved REJECT item:
        python3 skills/momentum/scripts/momentum-tools.py intake-queue append \
          --kind rejected \
          --title "{{title}}" \
          --description "{{description}}" \
          --source "triage"
    </action>

    <check if="any intake invocation returns an error">
      <output>! intake failed for: {{failed_title}} — {{error}}</output>
      <action>Continue processing remaining items. Record failure for summary.</action>
    </check>

    <check if="any intake-queue append call fails">
      <output>! append failed: {{error}} — item recorded here for manual capture:
        kind: {{kind}} · title: {{title}} · description: {{description}}</output>
      <action>Continue processing remaining items.</action>
    </check>

    <action>Mark resolved queue items:
      For each ID in {{resolved_queue_ids}}:
        python3 skills/momentum/scripts/momentum-tools.py intake-queue consume \
          --id "{{queue_id}}"
    </action>
  </step>

  <step n="6" goal="Summary">
    <output>## ✓ Triage Complete — {{total_processed}} Items Processed

**Dedup gate:**
  · {{consumed_count}} consumed (confirmed duplicates)
  · {{split_count}} split candidates surfaced
  · {{merge_candidate_count}} merge candidate groups flagged for Story B

**Stubbed to backlog ({{intake_count}}):**
{{for each intake result: · `{{slug}}` — `{{stub_path}}`}}

**Decisions recorded ({{decision_count}}):**
{{for each decision result: · {{title}} → {{outcome}}}}

**Parked to `intake-queue.jsonl`:**
  · {{shaping_count}} shaping (kind: shape)
  · {{defer_count}} deferred (kind: watch)
  · {{reject_count}} rejected (kind: rejected)

{{if resolved_count > 0: > ✓ {{resolved_count}} open queue items marked resolved.}}
{{if rejected_count_approval > 0: · {{rejected_count_approval}} items declined at approval — no action taken.}}
{{if failures: > ! {{failure_count}} execution failures — see above for details.}}

**Queue:** {{remaining_open_count}} open items (shape + watch) awaiting future triage.
    </output>
  </step>

</workflow>
