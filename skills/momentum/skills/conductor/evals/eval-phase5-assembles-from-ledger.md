# Eval: Phase 5 assembles from ledger

## Scenario

Given a conduct build for sprint `sprint-2026-06-10` has completed all phases (Build, AVFL-on-merge, E2E) and the build ledger contains rows for: 5 story launches, 5 merged terminal events, 12 finding-disposition events (8 fixed, 2 dismissed with rationale, 1 escalated to end-gate-expanded, 1 scope-reverted), 1 coverage-deferral-discharged event, 1 scorecard-revert-reconciliation override, and 2 mid-flight escalation records, the skill should assemble all Phase 5 end-gate variables from the ledger — not from in-context memory accumulators alone.

## Expected behavior

1. The Phase 5 assembly instructions explicitly state that the build ledger at `{{ledger_path}}` is the authoritative source for end-gate assembly.
2. `{{stakes_findings}}` Source 1 collects end-gate-expanded escalation entries from ledger rows with event type identifying escalations and timing_tier "end-gate-expanded" — not solely from the in-context `{{end_gate_escalations}}` accumulator.
3. The scorecard-revert-reconciliation scans ledger rows with event type `finding-disposition` to find records whose finding_id appears in `{{conductor_reverted_fixes}}` — not "per-story `{{finding_dispositions}}` records in `{{build_log}}`" (the phantom store instruction is eliminated).
4. The reconciliation override is expressed as a new appended override row in the ledger (event type `scorecard-revert-reconciliation`) rather than editing an existing row — consistent with the append-only corrections rule.
5. `{{routine_auto_fixed_count}}` is computed from ledger finding-disposition rows with disposition "fixed" (post-reconciliation, excluding scope-reverted).
6. `{{dismissed_findings}}` is derived from ledger finding-disposition rows with disposition "dismissed" — each carrying a non-empty dismissal_rationale.
7. `{{mid_flight_escalations}}` at Phase 5 is sourced from the Conductor-scoped accumulator rehydrated from ledger rows, not from the per-story transient that resets each story.
8. In-context accumulators may remain as a write-through convenience during the build, but the workflow explicitly declares the ledger as authoritative at end-gate assembly time.
