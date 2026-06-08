# Eval: Conductor pause-ask surface respects the cap and carries the self-sufficiency floor

**Surface under test:** Mid-flight escalation pause-ask — the single developer-facing card raised when a finding meets the stakes-and-timing bar.

**Standard:** Decision-Grade Presentation Standard (`skills/momentum/references/rules/decision-grade-presentation.md`), instantiated for this surface by the Pause-Ask Surface Contract in `references/escalation.md`.

## Scenario

**Given:** A build run produces a finding that meets the mid-flight escalation bar (stakes_class is non-routine AND timing_tier is mid-flight). The Conductor raises a pause-ask to the developer.

**When:** The pause-ask surface is presented to the developer.

**Then:**

1. **One card per finding:** Exactly one pause-ask card is raised for one finding — not a stream of prompts, not a bundled multi-finding card.
2. **Structure matches the template:** The card follows the Pause-Ask Surface Contract template from `references/escalation.md` — it identifies the paused story, the finding class, the timing tier, and provides What / Why / Evidence / Options.
3. **Cap respected:** The card is a single focused surface — not an expanded report. It does not include extensive background material or routine context beyond the What/Why/Evidence triple and the three options (Proceed / Change / Abort-that-branch).
4. **Floor present:** All three required fields are present inline:
   - **What** — the concrete change at stake, stated plainly
   - **Why** — the stakes class and why this qualifies as irreversible-and-imminent or build-invalidating
   - **Evidence** — the supporting detail from the pipeline result
5. **Self-sufficient:** The developer can decide (Proceed / Change / Abort-that-branch) from this surface alone without opening a file, reading a log, or recalling prior context.

## Pass Criteria

- The pause-ask is a single card (one finding = one pause)
- What / Why / Evidence are all present inline — the developer is self-sufficient on this surface
- The card does not expand into a long report (it uses the template structure, not free-form prose)
- The three options (Proceed / Change / Abort-that-branch) are present

## Fail Criteria

- Multiple findings are bundled into one pause-ask card
- Any of What, Why, or Evidence is missing or deferred (e.g., "see the log for details")
- The card is a lengthy report rather than a focused decision surface
- The developer must open a file or recall context to make the Proceed/Change/Abort decision

## Verification Note

This eval is verified by inspection. The verifier simulates a build scenario that would trigger a mid-flight escalation (or inspects the pause-ask template instructions in `references/escalation.md`), and confirms:
- The template structure is followed — all three required fields present
- The card is self-contained (no "see file X" deferrals in the What/Why/Evidence fields)
- One finding = one card

This eval does NOT require a live build run — inspection of the pause-ask output template against these criteria is sufficient verification.
