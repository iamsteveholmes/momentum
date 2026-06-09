# Eval: Impetus situational report stays within the 2-sentence cap while carrying required signals inline

**Surface under test:** Session situational report — the orientation greeting delivered after Impetus reads sprint state and the practice ledger.

**Standard:** Decision-Grade Presentation Standard (`skills/momentum/references/rules/decision-grade-presentation.md`)

## Scenario

**Given:** A practice state that includes:
- A current active sprint (non-null `sprints.active`)
- Open ledger entries (some this week, some older)
- At least one recurring-pattern signal (a topic that has appeared multiple times in the ledger)

**When:** Impetus reads sprint state and the practice ledger, then delivers its session situational report.

**Then:**

1. **Cap respected:** The situational report is ≤ 2 sentences. Countable on its face.
2. **Honest ledger counts present inline:** The report includes the ledger counts (e.g., N open entries, X this week) within the 2-sentence budget. The developer does not have to ask or open a file to learn the counts.
3. **Recurring-pattern signal present inline:** If a recurring-pattern signal exists (a topic closed_stale multiple times, a topic surfacing repeatedly), it appears in the report. It is not deferred to a follow-up or omitted to hit the sentence count.
4. **Floor wins over cap when in tension:** If the sentence count would exceed 2 to fit both the ledger counts and the recurring-pattern signal, the report trims other wording (voice framing, transition phrases) to fit — it does not drop the counts or the signal.
5. **No menus or narration:** The report does not include option menus, workflow suggestions, or narration of the reads performed.

## Pass Criteria

- The report is ≤ 2 sentences (countable)
- Honest ledger counts appear inline in the report
- Any recurring-pattern signal appears inline in the report
- The developer is oriented from the report alone — no follow-up needed to learn the basic counts and any signal

## Fail Criteria

- The report exceeds 2 sentences
- The ledger counts are absent — the developer learns the state only by asking or opening a file
- A recurring-pattern signal exists but is not included in the report (deferred, omitted, or sent to a follow-up)
- The report includes a menu of options or narrates the reads performed

## Verification Note

This eval is verified by inspection of the skill output in a session with real practice state data. The verifier:
1. Counts the sentences in the situational report (must be ≤ 2)
2. Confirms ledger counts appear inline (e.g., "N open entries")
3. Confirms any recurring-pattern signal appears inline
4. Confirms no menus or narration appear in the greeting

If the practice state has no active sprint and no ledger signal, use a state that does — the eval requires both to be present to test the floor.

This eval does NOT check exact wording or Impetus voice — it checks sentence count, presence of counts, and presence of signals.
