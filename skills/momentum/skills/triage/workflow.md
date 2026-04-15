# momentum:triage Workflow

**Goal:** Process multiple observations in one pass. Classify each into the correct
class, enrich ARTIFACT items with feature/story metadata, batch-approve with the
developer, then delegate to the appropriate downstream executor or write capture
events to `intake-queue.jsonl`.

**Role:** Orchestrator between upstream sources (retro output, conversation, assessment
findings) and the per-item executors (`momentum:intake`, `momentum:distill`,
`momentum:decision`). Does NOT perform gap-check (DEC-005 D10). Does NOT write story
files directly — that is delegated to `momentum:intake`.

**Voice:** Impetus voice — dry, confident, forward-moving. Symbol vocabulary:
✓ completed, → current, ◦ upcoming, ! warning, ✗ failed, ? proactive offer, · list item.

---

## Classification Table

| Class | Meaning | Downstream action |
|-------|---------|-------------------|
| ARTIFACT | A story that should enter the backlog | Delegate to `momentum:intake` with enriched context |
| DISTILL | A practice learning ready to apply | Delegate to `momentum:distill` |
| DECISION | A strategic decision to record | Delegate to `momentum:decision` |
| SHAPING | Needs more thinking before classification | Write `kind: shape` event to `intake-queue.jsonl` |
| DEFER | Valid but not now — park it | Write `kind: watch` event to `intake-queue.jsonl` |
| REJECT | Not worth pursuing | Write `kind: rejected` event to `intake-queue.jsonl` |

---

<workflow>

  <critical>Do NOT perform gap-check on any item. Classification only — per DEC-005 D10.</critical>

  <critical>Never write story files, story index entries, or planning artifacts directly.
  ARTIFACT delegation goes to momentum:intake. DISTILL delegation goes to momentum:distill.
  DECISION delegation goes to momentum:decision. Only intake-queue.jsonl is written directly
  (for SHAPING, DEFER, REJECT classes).</critical>

  <critical>All mutations to stories/index.json go through momentum-tools CLI only via
  momentum:intake. Triage never calls momentum-tools story-add directly.</critical>

  <critical>Batch approval (Step 4) is required before any execution. Never skip it, even
  for a single-item triage session.</critical>

  <step n="1" goal="Surface source items and re-surface open queue items">
    <action>Read `_bmad-output/implementation-artifacts/intake-queue.jsonl` if it exists.
    Filter for open items: kind in {shape, watch} that have no `resolved_at` field.
    Store {{open_queue_items}} = list of open shape/watch events.
    </action>

    <check if="{{open_queue_items}} is non-empty">
      <output>
Open queue items from previous sessions ({{count}} pending):

{{for each item:
  · [{{kind|upper}}] {{item.title}} — {{item.description}} (captured: {{item.captured_at}})
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
    Tag open queue items with `[QUEUED]` prefix for display distinction.</action>
  </step>

  <step n="2" goal="Read context artifacts for enrichment">
    <action>Read `_bmad-output/planning-artifacts/features.json` to get the features list.
    Store {{features}} = map of feature_slug → name for suggestion during enrichment.</action>

    <action>Read `_bmad-output/planning-artifacts/epics.md` to get the epic list.
    Store {{epics}} = list of epic slugs for DDD boundary awareness.</action>

    <note>Use offset/limit if either file is large. features.json and epics.md are
    typically under the token limit but may grow.</note>
  </step>

  <step n="3" goal="Classify and enrich all items">
    <action>For each item in {{all_items}}, classify it into exactly one of six classes:
    ARTIFACT, DISTILL, DECISION, SHAPING, DEFER, REJECT.

    Classification heuristics:
    · ARTIFACT — a bounded piece of work that belongs in the story backlog. Signals:
        "we should build X", "X is missing", "add Y to Z", "story: ...", a feature request,
        a bug report, a task with a clear deliverable. DEC-005 D5 story types: feature /
        maintenance / defect / exploration / practice.
    · DISTILL — a practice insight, a rule to update, a pattern to capture, a workflow
        clarification. Signals: "we learned X", "rule: always Y", "update the skill to Z",
        "finding: ...", a retro Tier 1 finding.
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

  <step n="4" goal="Batch approval — present classification for developer review">
    <action>Present all classified items grouped by class with numbered IDs.
    Use batch-approval UX (same pattern as momentum:refine Step 9):
    · For each class group with items: show class name, count, and all items
    · Offer batch operation: "Approve all [CLASS]?" or individual overrides
    · Developer can re-classify any item, update enrichment fields, or split/merge items
    </action>

    <output>
Triage — {{total_count}} items classified:

{{if ARTIFACT items:}}
[ARTIFACT] — {{count}} items  →  will be sent to momentum:intake
{{for each:
  [N] {{title_or_summary}}
      type: {{story_type}} · feature: {{feature_slug|"(none)"}} · epic: {{epic_slug}} · priority: {{priority}}
      {{proposed_depends_on if non-empty: depends: {{proposed_depends_on}}}}
}}
  → Approve all? (A=all / R=all / pick individually by number)

{{if DISTILL items:}}
[DISTILL] — {{count}} items  →  will be sent to momentum:distill
{{for each: [N] {{description}} → target: {{candidate_artifact|"auto-detect"}}}}
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
    · "done" → finalize with current approvals
    </action>

    <action>Store {{approved_items}} = all approved classified items</action>
    <action>Store {{rejected_count}} = count of items rejected in approval step (not REJECT-class items)</action>

    <check if="{{open_queue_items}} contains items with no new action">
      <ask>Open queue items with no new classification will remain in the queue.
      Enter IDs to mark as resolved (e.g., "resolve 2, 5") or 'done' to leave them open.</ask>
      <action>Store {{resolved_queue_ids}} = IDs to mark as resolved</action>
    </check>
  </step>

  <step n="5" goal="Execute approved actions">
    <action>Process approved items in this order:

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

    **DISTILL items** — spawn momentum:distill per item (in parallel if multiple):
      Pass:
        - learning_description: item description + any recommended change captured
        - candidate_artifact: target practice file if identifiable
        - source: "triage — {{source_label}}"
      Wait for all distill spawns to complete.
      Store {{distill_results}} = list of {title, outcome} returned by distill.

    **DECISION items** — spawn momentum:decision per item (sequentially — decision is interactive):
      Pass context from item. Wait for each decision to complete before next.
      Store {{decision_results}} = list of {title, outcome}.

    **SHAPING items** — write to intake-queue.jsonl via CLI:
      For each approved SHAPING item:
        python3 skills/momentum/scripts/momentum-tools.py intake-queue queue-add \
          --kind shape \
          --title "{{title}}" \
          --description "{{description}}" \
          --source "{{source_label}}"

    **DEFER items** — write to intake-queue.jsonl via CLI:
      For each approved DEFER item:
        python3 skills/momentum/scripts/momentum-tools.py intake-queue queue-add \
          --kind watch \
          --title "{{title}}" \
          --description "{{description}}" \
          --source "{{source_label}}"

    **REJECT items** — write to intake-queue.jsonl via CLI:
      For each approved REJECT item:
        python3 skills/momentum/scripts/momentum-tools.py intake-queue queue-add \
          --kind rejected \
          --title "{{title}}" \
          --description "{{description}}" \
          --source "{{source_label}}"
    </action>

    <check if="any intake invocation returns an error">
      <output>! intake failed for: {{failed_title}} — {{error}}</output>
      <action>Continue processing remaining items. Record failure for summary.</action>
    </check>

    <check if="any queue-add CLI call fails">
      <output>! queue-add failed: {{error}} — item recorded here for manual capture:
        kind: {{kind}} · title: {{title}} · description: {{description}}</output>
      <action>Continue processing remaining items.</action>
    </check>

    <action>Mark resolved queue items:
      For each ID in {{resolved_queue_ids}}:
        python3 skills/momentum/scripts/momentum-tools.py intake-queue resolve \
          --id "{{queue_id}}"
    </action>
  </step>

  <step n="6" goal="Summary">
    <output>✓ Triage complete — {{total_processed}} items processed.

Stubbed to backlog ({{intake_count}}):
{{for each intake result: · {{slug}} — {{stub_path}}}}

Distilled ({{distill_count}}):
{{for each distill result: · {{title}} → {{outcome}}}}

Decisions recorded ({{decision_count}}):
{{for each decision result: · {{title}} → {{outcome}}}}

Parked to intake-queue.jsonl:
  · {{shaping_count}} shaping (kind: shape)
  · {{defer_count}} deferred (kind: watch)
  · {{reject_count}} rejected (kind: rejected)

{{if resolved_count > 0: ✓ {{resolved_count}} open queue items marked resolved.}}
{{if rejected_count_approval > 0: · {{rejected_count_approval}} items declined at approval — no action taken.}}
{{if failures: ! {{failure_count}} execution failures — see above for details.}}

Queue now has {{remaining_open_count}} open items (shape + watch) awaiting future triage.
    </output>
  </step>

</workflow>
