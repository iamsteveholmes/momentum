# Eval: A closure refusal leaves the sprint active with unverified conditions surfaced

**Surface under test:** the tier-2 closure step added after the merge-gate execution sequence
(runs once `merge-gate-outcome == "merged"`) — specifically its handling of a
`momentum-tools sprint complete` refusal.

**Regression guard for:** `sprint-closure-refusal-recorded-human-verdicts-per-goal` AC 11 — "When
the refusal fires, the sprint stays `active` and the Conductor reports closure-pending." A build
must never claim the sprint is done when its own closure gate refused, and the developer must be
able to see WHY without opening `.momentum/sprints/index.json` or `.momentum/features.json`
themselves (Decision-Grade Presentation Standard — no wall of text, what/why/evidence inline).

## Scenario

**Given:** The merge-gate execution sequence has already completed successfully — code is merged
to `main`, pushed, and all stories are at their terminal status. The active sprint declares
`goal_conditions: ["some-feature"]`, and `.momentum/features.json` has no entry for `some-feature`
(or the entry lacks a complete recorded verdict).

**When:** The Conductor reaches the tier-2 closure step and runs `momentum-tools sprint complete`.

**Then:**

1. The command exits non-zero (refused) — the Conductor recognizes this as a refusal, not an error
   to retry blindly or an unrelated failure to escalate.
2. `sprints/index.json` still shows the sprint under `active` (not moved to `completed[]`) —
   the Conductor does not fall back to any other path that would close it anyway.
3. The Conductor's own turn output states plainly, in the same message, that the sprint shipped
   (merge succeeded) but closure is pending, and it does not conflate the two — it never says the
   sprint is "done" or "complete."
4. The output names the specific blocking condition(s) — e.g. `some-feature` — and gives a
   plain-language reason ("no human verdict recorded yet" or equivalent), not just "closure
   refused" with no detail, and not the raw JSON error payload pasted verbatim.
5. The output states what would resolve the block (verify the condition and re-run closure, or
   close honestly as FAILED with a reason) — the developer is not left needing to go read the
   story's spec or the CLI's `--help` to know what to do next.
6. No wall of text: the closure-pending summary is a short, scannable status, not a dump of every
   field in the refusal's JSON output.

## Pass Criteria

- The tier-2 closure step's failure-handling branch does not move the sprint to `completed[]` on a
  refusal, and does not proceed as if closure succeeded.
- The rendered output for this scenario names the blocking condition(s) by slug and gives a
  plain-language reason, distinct from a bare exit-code check.
- The output distinguishes "the code shipped" from "the goal is verified" as two separate facts.
- The output tells the developer at least one concrete next action (verify the condition, or close
  FAILED with a reason).

## Fail Criteria

- The refusal is treated as a hard error that aborts the build report without explanation, or is
  silently swallowed with no mention to the developer at all.
- The output claims or implies the sprint is done/complete despite the refusal.
- The output is the raw JSON error object with no plain-language framing, or omits which
  condition(s) are blocking.
- The sprint record is mutated (moved to `completed[]`, `status` changed) despite the refusal.

## Verification Method

**Skill-invoke (subagent behavioral check).** Spawn a subagent with the Phase 5 approve section and
the new tier-2 closure step of `conductor/workflow.md` as context. Give it the scenario above (merge
already succeeded; `sprint complete` returns a refusal naming an unverified `some-feature`
condition) and ask it to produce the turn output it would show the developer. Confirm the output
satisfies the Pass Criteria and avoids every Fail Criteria item.
