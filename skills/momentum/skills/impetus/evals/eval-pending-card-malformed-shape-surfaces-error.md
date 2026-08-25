# Eval: A malformed resume card surfaces a shape error, never a silent clean start

**Surface under test:** The malformed-card handling in `.claude/rules/impetus.md`'s resume-card
scan, per `references/resume-card.md`'s "Malformed card handling" section — the seam-drift
protection this contract exists to provide.

**Invariant guarded:** A card file that exists but is missing or renames its `status` or `question`
field is not silently treated as "no card." The developer is told a card was found but is
unreadable, naming the file.

## Scenario

**Given:** A `resume-card.json` exists under some `.momentum/sprints/{slug}/` whose `status` field
(or `question` field) is absent, or is present under a different key name than this contract
defines.

**When:** A fresh session starts and Impetus runs its resume-card scan.

**Then:**

1. The greeting names the offending file path and states that a resume card was found but its
   shape is unreadable/incompatible with the expected contract.
2. The session does NOT proceed as if no card existed — the malformed card is named, not silently
   skipped, and the rest of the greeting (feature headline, ledger counts) still renders normally
   after that notice.

## Pass Criteria

The greeting visibly and specifically reports the shape incompatibility with the file path named,
so the developer knows a gate may be waiting behind a broken card and can investigate.

## Fail Criteria

The greeting is indistinguishable from a clean no-card start; the malformed card is silently
ignored; no file path is named; the session errors out entirely instead of degrading to a named
warning plus a normal rest-of-greeting.

## Verification Method

Inspection of `.claude/rules/impetus.md`'s resume-card scan instructions for the malformed-card
branch, cross-checked with a subagent walkthrough: write a fixture card missing its `status` field,
start a fresh session, and confirm the greeting names the file and states the shape problem rather
than proceeding silently.
