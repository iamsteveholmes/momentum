# Eval: Resume suppresses duplicate stage3-escalation append

## Scenario A — step 2.S3 site (end-gate-expanded tier)

**Given** a durable build ledger pre-seeded with exactly one `stage3-escalation` row for story
`"story-x"` with `finding_id: "F-003"` and `timing_tier: "end-gate-expanded"`
(identity tuple `("story-x", "stage3-escalation", "F-003")`),
AND step 2.0 rehydration has bound this tuple into `{{ledger_seen_events}}`,
AND story `"story-x"` is NOT re-run (not reset to `ready-for-dev`) this pass,

**When** the conduct build resumes and reaches the step 2.S3 CASE-escalated path for finding `F-003`
— specifically the `Record in {{build_log}} (and the build ledger per standing rule): { event: "stage3-escalation", ... }` instruction —

**Then:**
1. The Conductor checks whether `("story-x", "stage3-escalation", "F-003")` is already in
   `{{ledger_seen_events}}` before appending.
2. Because the tuple IS present, the append is **skipped**.
3. After the resume pass, the ledger contains exactly **ONE** `stage3-escalation` row for
   `("story-x", "stage3-escalation", "F-003")`.
4. The resume completes without error.

## Scenario B — AVFL Phase 3 step 3.3 site (Group-A fixer escalations)

**Given** a durable build ledger pre-seeded with exactly one `stage3-escalation` row for
`story_slug: "sprint-integration"` with `finding_id: "L-001"`
(identity tuple `("sprint-integration", "stage3-escalation", "L-001")`),
AND step 2.0 rehydration has bound this tuple into `{{ledger_seen_events}}`,
AND the AVFL merge-review leftover `L` with `L.id == "L-001"` and `L.owning_stories[0] == null`
(so the fallback `"sprint-integration"` applies) is encountered again on resume,

**When** the Conductor reaches the `Append to {{build_log}} (and the build ledger per standing rule — REQUIRED so this escalation survives session death)` instruction for `L-001` in AVFL Phase 3 step 3.3,

**Then:**
1. The Conductor checks whether `("sprint-integration", "stage3-escalation", "L-001")` is already
   in `{{ledger_seen_events}}` before appending.
2. Because the tuple IS present, the append is **skipped**.
3. After the resume pass, the ledger contains exactly **ONE** `stage3-escalation` row for
   `("sprint-integration", "stage3-escalation", "L-001")`.
4. The resume completes without error.

## Expected outcome

- **PASS**: Duplicate appends are suppressed at both sites; each identity tuple has exactly 1 ledger row.
- **FAIL**: A second `stage3-escalation` row appears for either tuple, yielding 2 rows.
