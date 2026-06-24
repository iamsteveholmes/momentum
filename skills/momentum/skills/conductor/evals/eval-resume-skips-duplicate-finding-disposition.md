# Eval: Resume suppresses duplicate finding-disposition append

## Scenario

**Given** a durable build ledger pre-seeded with exactly one `finding-disposition` row for story
`"story-x"` with `finding_id: "F-001"` (identity tuple `("story-x", "finding-disposition", "F-001")`),
AND the Conductor's step 2.0 rehydration has bound this tuple into `{{ledger_seen_events}}`,
AND story `"story-x"` is NOT reset to `ready-for-dev` by the resume reconcile (it is not in-progress;
it was already completed in the prior session),

**When** the conduct build resumes and processes the disposition pass (step 2.S3) for story-x
— encountering the same `F-001` finding with disposition `fixed`, `dismissed`, `triaged-out`,
`escalated`, or `scope-reverted` — and reaches the corresponding LEDGER (phantom-store closure) append instruction,

**Then:**
1. The Conductor checks whether `("story-x", "finding-disposition", "F-001")` is already in
   `{{ledger_seen_events}}` before appending.
2. Because the tuple IS present (rehydrated from the prior session), the append is **skipped** —
   no second `finding-disposition` row is written to the ledger for `("story-x", "finding-disposition", "F-001")`.
3. After the resume pass, the ledger contains exactly **ONE** `finding-disposition` row for that tuple
   — the original from the prior session, not a duplicate.
4. The in-context accumulators (`{{routine_auto_fixed_count}}` etc.) are NOT incremented a second time
   for this already-recorded finding.
5. The resume completes without error or a duplicate-row warning.

## Also covers: blocked disposition at budget-exhaustion path

The same skip behavior applies to the Phase-D budget-exhaustion (blocked) append site: if a
`finding-disposition` row with `disposition: "blocked"` and `finding_id: "F-002"` already exists
in the ledger for story `"story-x"`, the budget-exhaustion LEDGER append is skipped when the
tuple `("story-x", "finding-disposition", "F-002")` is found in `{{ledger_seen_events}}`.

## Expected outcome

- **PASS**: The duplicate append is suppressed; ledger row count for the identity tuple remains 1.
- **FAIL**: A second `finding-disposition` row is written, yielding 2 rows for the same tuple.
