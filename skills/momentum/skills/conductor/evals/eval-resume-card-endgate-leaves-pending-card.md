# Eval: End-gate presentation leaves a durable pending resume card

**Surface under test:** Phase 5's MERGE-GATE PENDING CHECKPOINT resume-card refresh (workflow.md),
written per `references/resume-card.md`.

**Invariant guarded (AC 1, 2):** A resume card exists on disk before the end-gate is answered, with
status `pending` and exactly one question that states what it gates.

## Scenario

**Given:** A prepared sprint with at least one story that merged and at least one story left
blocked, built to the point where the Phase 5 end-gate ask is about to be presented (report not yet
built).

**When:** The Conductor reaches the MERGE-GATE PENDING CHECKPOINT and its immediately-following
RESUME-CARD REFRESH action, then the session ends before the developer answers.

**Then:**

1. `.momentum/sprints/{sprint_slug}/resume-card.json` exists — written before the HTML report was
   built or opened.
2. `status` reads `"pending"`.
3. `merged.count`/`merged.slugs` and `blocked.count`/`blocked.slugs` match the run's observable
   outcome (sourced from the build ledger, not an in-context accumulator).
4. `question` is a single object (never an array, never two questions) whose `text` is the
   approve-or-request-changes question, whose `gates` names the tier-1 merge gate, whose `options`
   are `["Approve", "Request changes"]`, and whose `report_path` points at the end-gate HTML report.
5. `waited_since` is a fresh timestamp (this question was not previously on the card) and
   `resurface_count` is `0`.

## Pass Criteria

Inspecting the card file after abandoning the gate shows all five items above. The card's contents
are traceable to the ledger's `merged`/`blocked` sets, not to a stale or hallucinated count.

## Fail Criteria

No card exists; the card is written only after the report is opened or after an answer is given;
`status` is anything other than `pending`; the card carries zero or more than one question; the
question omits `gates`, `options`, or `report_path`.

## Verification Method

Inspection of `workflow.md`'s MERGE-GATE PENDING CHECKPOINT / RESUME-CARD REFRESH ordering
(confirm the card write precedes BUILD THE END-GATE REPORT), cross-checked with a subagent
walkthrough of the scenario using a fixture build ledger with one merged and one blocked story.
