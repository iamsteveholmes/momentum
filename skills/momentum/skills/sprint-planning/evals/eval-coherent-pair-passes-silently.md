# Eval: Cross-Story Seam Coherence — Coherent Pair Passes Silently

**ID:** eval-coherent-pair-passes-silently
**Change-type:** skill-instruction
**Phase:** Step 3.6 (cross-story seam coherence check), feeding Step 7

## Scenario

Given a two-story sprint with `depends_on: consumer → producer`:

- Consumer story — its Acceptance Criteria state it renders "the response field carrying the
  suggestion copy" as sourced from the producer.
- Producer story — its frozen contract (Step 3.5 output) explicitly states the endpoint's
  response now includes that exact field.

When Step 3.6 runs over this pair, following `references/coherence-gate.md`

Then:
1. The edge is enumerated
2. The consumer's named external input is extracted (the response field)
3. The producer's deliverable text is matched and found to satisfy it
4. The edge is recorded as satisfied in `coherence-report.md` under "## Satisfied /
   Presence-only" — NOT under "## Open Coherence Failures"
5. No coherence-failure callout is produced for this pair anywhere in the step's output

When this pair reaches Step 7 (developer review)

Then:
6. No genuine fork is created for this pair
7. The pair is represented only in the "Defaulted to standards" collapsible (as part of the
   "all depends_on edges resolve cleanly" line), not as a decision card
8. The developer is not prompted to resolve anything about this pair

When Step 8 (activation) is reached

Then:
9. No coherence-related hold or halt fires for this pair
10. The run proceeds toward activation as if the pair were never in question

## Pass Criteria

- `coherence-report.md` lists this pair under "Satisfied / Presence-only," never under "Open
  Coherence Failures"
- No fork card, warning, or extra prompt referencing this pair appears at Step 7
- No block or halt referencing this pair appears at Step 8
- The step's own summary output uses the "no seam mismatch found" / "all resolve cleanly"
  form, not a failure form

## Fail Criteria

- Any callout, warning, or fork card about this pair appears despite the producer delivering
  exactly what the consumer names
- The pair is omitted entirely from `coherence-report.md` (silently dropped rather than
  recorded as satisfied)
- The developer is prompted for a decision about this pair at Step 7 or Step 8
