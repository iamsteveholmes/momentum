# Eval: Resume does not double-count AVFL/E2E findings

## Scenario A — append-only override row (FR141 correction)

**Given** the build ledger for `sprint-2026-07-13` contains two `avfl-finding` rows sharing
`finding_id: "AV-007"` for story `story-x` — an earlier row with `disposition: "residual"` and
`ts: "2026-07-13T10:00:00Z"`, and a later append-only correction row with
`disposition: "fixed"` and `ts: "2026-07-13T10:05:00Z"` (both rows are legitimate; FR141
mandates corrections are appended, never rewritten),

**When** the Conductor resumes and step 2.0 rehydrates `{{avfl_findings}}` from the ledger,

**Then:**
1. `{{avfl_findings}}` contains exactly ONE entry for `finding_id: "AV-007"`.
2. That entry reflects the later row's `disposition: "fixed"` (last-write-wins by `ts`), not
   the earlier `"residual"` row.
3. The MAJOR-RESIDUAL GOVERNANCE GUARD and Phase 5 scorecard counts treat `AV-007` as resolved
   (fixed), not as an outstanding residual.

## Scenario B — re-run story leaves stale prior-attempt entries

**Given** story `story-y` was reset from `in-progress` to `ready-for-dev` by the step 2.0
reconcile (its prior attempt was interrupted mid-fix-loop), and the ledger already contains a
prior-attempt `e2e-stakes-escalation` row for `story-y` with `finding_id: "E2E-story-y-01"`
before the reset,

**When** the RE-RUN KEY CLEARING block executes for `story-y`, and the fresh re-run pass later
produces its own live `e2e-stakes-escalation` row for the same `finding_id: "E2E-story-y-01"`
(or a different one) for `story-y`,

**Then:**
1. The RE-RUN KEY CLEARING step removes every entry whose `story_slug == "story-y"` from
   `{{e2e_findings}}` (ACCUMULATOR CLEARING), not only from `{{ledger_seen_events}}`.
2. The fresh re-run's live finding for `story-y` is NOT layered on top of the stale
   prior-attempt entry still sitting in `{{e2e_findings}}` — it either upserts cleanly (if
   rehydration is re-run) or is the sole live entry (accumulator was cleared).
3. After the resume pass completes, `{{e2e_findings}}` contains exactly one entry per
   `finding_id` for `story-y` — no duplicate counting of `story-y`'s findings at Phase 5.

## Expected outcome

- **PASS**: Both scenarios show exactly one entry per `finding_id` in the relevant accumulator
  after resume, with the correct (latest) disposition retained.
- **FAIL**: Either scenario shows two entries for the same `finding_id` in `{{avfl_findings}}`
  or `{{e2e_findings}}`, or a stale prior-attempt disposition survives over a later one.
