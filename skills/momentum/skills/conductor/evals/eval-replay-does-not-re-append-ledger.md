# Eval: Replay does not re-append the ledger

## Scenario

Given a build ledger for `sprint-2026-07-13` already contains 40 event rows from a prior,
interrupted session (story launches, stage transitions, finding dispositions, terminal
signals, an avfl-finding row, and an e2e-stakes-escalation row), and a fresh session
re-invokes the Conductor for the same sprint, the step 2.0 rehydration replay loop reads
all 40 rows and rebuilds `{{build_log}}` and the other in-context accumulators from them —
the skill should NOT re-append any of those 40 rows back to the durable ledger file during
this replay.

## Expected behavior

1. The replay action (step 2.0, `workflow.md` rehydration block) states inline, at the point
   where it routes ledger rows into `{{build_log}}`, that these replay appends are a REBUILD
   of the in-context cache only and do not also append to `{{ledger_path}}` — this restatement
   is adjacent to the routing itself, not only declared once at the top-level LEDGER-APPEND
   STANDING RULE / REHYDRATION EXEMPTION note.
2. After the resumed session completes rehydration (before any new live event occurs), the
   ledger file's line count is unchanged from the pre-resume count — still exactly 40 lines.
3. This holds for every routing clause in the replay loop, including the finding-accumulator
   clauses (`avfl-finding`, `e2e-stakes-escalation`, `e2e-finding-auto-fixed`) that additionally
   rebuild `{{avfl_findings}}`/`{{e2e_findings}}` — those clauses also only mutate in-context
   accumulators, never the ledger file.
4. Once rehydration completes and the live build resumes, only genuinely NEW events (a story
   that gets re-run, or a phase that has not yet completed) produce new ledger rows — appended
   after the pre-existing 40, never duplicating any of them.

## Expected outcome

- **PASS**: The ledger file contains exactly 40 rows immediately after resume/rehydration
  completes, and only grows by genuinely new live events afterward.
- **FAIL**: The ledger file's line count exceeds 40 immediately after rehydration (a replayed
  row was re-appended), or any of the original 40 rows appears duplicated.
