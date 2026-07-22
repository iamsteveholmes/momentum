# Eval: Cross-Story Seam Coherence — Surfaces and Names an Incoherent Pair (Regression Anchor)

**ID:** eval-surfaces-seam-failure-on-incoherent-pair
**Change-type:** skill-instruction
**Phase:** Step 3.6 (cross-story seam coherence check), feeding Step 7 and Step 8

## Scenario — replay of the nornspun sprint-2026-05-30 root cause

Given a two-story sprint with `depends_on: consumer → producer`:

- Consumer story `campaign-init-offered-suggestion-list-render-and-routes` — its Acceptance
  Criteria and Description state: "source the copy from the backend payload... not a
  hardcoded client string," naming the backend response as the externally-sourced input it
  depends on `backend-campaign-init-add-offered-suggestion-list-copy` to supply.
- Producer story `backend-campaign-init-add-offered-suggestion-list-copy` — its frozen
  contract (Step 3.5 output) describes ONLY an edit to the Urd system prompt. No payload
  field, no endpoint, no schema, no response shape change appears anywhere in its Part-A
  header or Part-B body.

When Step 3.6 (cross-story seam coherence check) runs over this pair, following
`references/coherence-gate.md`

Then:
1. The edge is enumerated (not silently dropped)
2. The consumer's named external input is extracted: a backend-payload/response field
   carrying the offered-suggestion copy
3. The producer's deliverable text (system-prompt edit only) is matched against that named
   input and found NOT to satisfy it — no reasonable reading of a system-prompt edit
   delivers a payload field
4. A coherence failure is recorded naming BOTH story slugs explicitly
5. The failure names the specific missing item — a backend payload/endpoint/schema
   deliverable that the producer does not provide
6. The failure is described using "seam coherence" / "cross-story coherence" wording — NOT
   "contract-freeze," "freeze," or "lock" wording
7. The failure card lists three distinct resolutions: amend the producer to deliver it,
   amend the consumer so it no longer needs it, or add a new story to own the missing piece

When this failure reaches Step 7 (developer review)

Then:
8. It appears as a mandatory genuine fork on the plan gate (not silently absorbed into a
   defaulted-choices line), carrying What/Why/Evidence/Recommendation/Options inline
9. The fork's Options include the three remediation choices plus an explicit override option

When Step 8 (activation) is reached with this failure still open and no override given

Then:
10. `momentum-tools sprint activate` is NOT called
11. The developer-facing output states the sprint is held because of the open mismatch,
    naming both slugs again

## Pass Criteria

- Both slugs (`campaign-init-offered-suggestion-list-render-and-routes` and
  `backend-campaign-init-add-offered-suggestion-list-copy`) appear by name in the failure
  output
- The specific missing deliverable (backend payload/endpoint/schema) is named, not just
  "a mismatch exists"
- "Seam coherence" / "cross-story coherence" wording is used; "contract-freeze" wording is
  absent from this check's output
- Three remediation options are present verbatim (amend producer / amend consumer / add
  wiring story)
- Activation is blocked with no override present

## Fail Criteria

- The edge is dropped or the failure is never surfaced
- The failure names only one story slug, or refers to it by a bare handle without the
  missing deliverable
- Only one or two resolution paths are offered, or a fourth silently substitutes for one of
  the three
- "Contract-freeze," "freeze," or "lock" wording is used to describe this check or failure
- `momentum-tools sprint activate` is called despite the open, unresolved mismatch
