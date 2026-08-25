# Eval: A resolved card clears the agenda and restores the clean-start greeting

**Surface under test:** `.claude/rules/impetus.md`'s resume-card scan filter (`status == "pending"`
only) and the AC 12 no-pending-card baseline.

**Invariant guarded (AC 11, 12):** Once a card is resolved, Impetus stops surfacing it from the
next session onward. When no pending card exists anywhere, the greeting behaves exactly as it does
today — the pending-gate agenda adds nothing to a clean start.

## Scenario A — resolved card stops surfacing

**Given:** A `resume-card.json` whose `status` is `"resolved"` (with `resolved_at` and `resolution`
recorded), and a baseline greeting recorded from a session with no resume cards present anywhere.

**When:** A fresh session starts.

**Then:** The greeting does not mention the card at all — no pending question, no waited-for line —
and is behaviorally identical to the recorded no-card baseline (feature headline leads, as usual).

## Scenario B — no card anywhere is a true no-op

**Given:** No `resume-card.json` file exists under any `.momentum/sprints/*/` directory.

**When:** A fresh session starts.

**Then:** The greeting is unchanged from the documented pre-this-story baseline: the N-of-M feature
headline leads, followed by ledger counts and any recurring-pattern signal, with no mention of a
pending-gate agenda anywhere.

## Pass Criteria

Scenario A: the resolved card is never surfaced, and the greeting matches the no-card baseline
exactly. Scenario B: zero behavioral difference from the pre-story greeting.

## Fail Criteria

A resolved card is surfaced again in any later session; the greeting differs from baseline (extra
wording, an empty pending-gate section, or altered ordering) when no pending card exists.

## Verification Method

Inspection of the resume-card scan's `status == "pending"` filter in `.claude/rules/impetus.md`,
cross-checked with a subagent walkthrough: run once with a resolved-only card present, once with no
card file at all, and diff both greetings against a recorded baseline greeting.
