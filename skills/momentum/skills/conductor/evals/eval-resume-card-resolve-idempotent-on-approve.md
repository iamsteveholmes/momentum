# Eval: Approving the gate resolves the card exactly once, idempotently

**Surface under test:** The RESUME-CARD RESOLVE action following MERGE-GATE OUTCOME: MERGED, and
the RESUME-CARD RESOLVE action at the top of the request-changes branch (workflow.md), per
`references/resume-card.md`'s Resolution section.

**Invariant guarded (AC 11):** When the developer resolves the gate, the Conductor marks the card
resolved with timestamp and resolution, and the write is idempotent — resolving an already-resolved
card is a no-op, so a resumed session cannot double-write or regress the card to `pending`.

## Scenario A — first-time approve resolves the card

**Given:** A pending resume card with the approve-or-request-changes question, and a build that
reaches the approve branch for the first time.

**When:** The developer approves and the merge-gate outcome is verified `"merged"`.

**Then:** The card's `status` becomes `"resolved"`, `resolved_at` is set, `resolution` reads
`"approved"`, and every other field (phase, merged, blocked, question, waited_since,
resurface_count) is left exactly as it stood at approval.

## Scenario B — resumed session after a prior approve does not regress or double-write

**Given:** A card already `status: "resolved"`, `resolution: "approved"` from a prior pass (the
TERMINAL SUCCESS ALREADY ON RECORD resume path).

**When:** The session resumes and reaches the same RESUME-CARD RESOLVE action again.

**Then:** The action detects `status == "resolved"` and skips the write entirely — `resolved_at`
and `resolution` are byte-identical before and after.

## Scenario C — request-changes resolves the current question, then a fresh card begins waiting

**Given:** A pending card with the approve-or-request-changes question.

**When:** The developer answers with a change request; the autonomous fix pass completes and the
report is re-rendered.

**Then:** Immediately upon entering the request-changes branch, the card is resolved
(`resolution: "changes-requested"`). At the redispatched ask (after the re-render), a brand-new
pending card is written with the same question text but a **fresh** `waited_since` and
`resurface_count` reset to 0 — this is a new waiting period, not a continuation of the resolved one.

## Pass Criteria

Scenario A: resolved with the correct resolution and an unchanged snapshot of the other fields.
Scenario B: zero mutation on the resumed pass. Scenario C: a resolve immediately followed by a
fresh pending card with a reset counter and a new `waited_since`.

## Fail Criteria

Any scenario leaves the card `pending` after a genuine approve; Scenario B mutates
`resolved_at`/`resolution` a second time; Scenario C fails to resolve the answered question, or
carries the old `waited_since`/`resurface_count` forward into the new pending card instead of
resetting them.

## Verification Method

Inspection of the three RESUME-CARD RESOLVE/REFRESH action sites in `workflow.md` for the
idempotency check and the fresh-vs-carried-forward `waited_since` logic, cross-checked with a
subagent walkthrough of each scenario against a fixture card.
