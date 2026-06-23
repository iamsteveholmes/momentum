# Eval: stage3-mid-flight-escalation batch dedup (null key) + re-run story still appends fresh rows

## Scenario A — stage3-mid-flight-escalation batch dedup

**Given** a durable build ledger pre-seeded with exactly one `stage3-mid-flight-escalation` row
for story `"story-x"` — a count-level batch row carrying `finding_count: 2` and NO per-finding
`finding_id` — identified by the agreed null key `("story-x", "stage3-mid-flight-escalation", null)`,
AND step 2.0 rehydration has bound this tuple into `{{ledger_seen_events}}`,
AND story `"story-x"` is NOT re-run this pass,

**When** the conduct build resumes and step 2.F processes mid-flight escalations for story-x
— reaching the `Record outcome in {{build_log}}: { story_slug: S.slug, event: "stage3-mid-flight-escalation", ... }` instruction —

**Then:**
1. The Conductor checks whether `("story-x", "stage3-mid-flight-escalation", null)` is already
   in `{{ledger_seen_events}}` before appending the batch row.
2. Because the tuple IS present, the append is **skipped** — no second `stage3-mid-flight-escalation`
   row is written.
3. After the resume pass, the ledger contains exactly **ONE** `stage3-mid-flight-escalation` row
   for `("story-x", "stage3-mid-flight-escalation", null)`.
4. The null `finding_id` component is the agreed identity component for this count-level event kind;
   both the producer (append site) and the consumer (dedup guard) agree on this field shape.
5. The resume completes without error or a duplicate-row warning.

**Key:** The `finding_id` component of the dedup tuple is explicitly `null` for this event kind —
consistent with the `(S.slug, "story-terminal", null)` precedent at the story-terminal guard.
This is stated explicitly in the workflow text at the append site so the semantics are reproducible.

## Scenario B — re-run story still produces fresh events (guard does NOT suppress new events)

**Given** a durable build ledger pre-seeded with prior-session rows for story `"story-y"` —
including `finding-disposition`, `stage3-escalation`, and `stage3-mid-flight-escalation` rows —
AND step 2.0 rehydration has bound ALL of those prior-session tuples into `{{ledger_seen_events}}`,
AND story `"story-y"` IS reset to `ready-for-dev` by the step 2.0 reconcile (it was `in-progress`
in the prior session and had a clean worktree),
AND the step 2.0 reconcile's RE-RUN KEY CLEARING action removes every `("story-y", *, *)` tuple
from `{{ledger_seen_events}}` immediately after the status reset — so `"story-y"`'s prior-session
tuples are no longer present in the set when the fresh build pass runs,

**When** the conduct build runs story `"story-y"` fresh this pass and the disposition pass
produces new `finding-disposition`, `stage3-escalation`, and/or `stage3-mid-flight-escalation` rows,

**Then:**
1. The Conductor appends the new rows — the tuples are NOT in `{{ledger_seen_events}}` (they were
   cleared by the reconcile's RE-RUN KEY CLEARING step), so the dedup guard does not suppress them.
2. After the pass, the ledger contains BOTH the prior-session rows (preserved, not deleted) AND the
   fresh current-session rows for story `"story-y"`.
3. Phase 5's SUPERSESSION RULE (latest row by `ts` wins per `(story_slug, event, finding_id)` tuple)
   correctly identifies the current-session rows as the superseding ones for `"story-y"`.
4. No prior-session rows for `"story-y"` are double-counted — the supersession rule handles them.

## Expected outcome

- Scenario A **PASS**: Batch row for `("story-x", "stage3-mid-flight-escalation", null)` appears exactly once.
- Scenario A **FAIL**: A second batch row is written, yielding 2 rows with duplicate identity.
- Scenario B **PASS**: Re-run story `"story-y"` produces its fresh finding rows; the guard does not suppress them.
- Scenario B **FAIL**: The guard incorrectly suppresses fresh events for a re-run story, leaving it without current-session rows.
