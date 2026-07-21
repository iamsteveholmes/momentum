# Eval: End-gate render and approval ask are bound as one atomic turn

**Surface under test:** The transition from the end-gate report open action to the end-gate approval `<ask>` in `workflow.md` — at both the initial Phase 5 ask and the 5.RC.5 / redispatch ask.

**Standard:** DEC-035 (single mandatory human end-gate); decision-grade-presentation rule (pause-ask / gate surfaces must be self-sufficient and actually presented); the incident this story fixes (session `83ea46d8`, sprint-2026-06-28 conduct run, 2026-07-06 — turn ended after the report opened with no ask presented, leaving the sprint parked un-merged).

## Scenario

**Given:** The Conductor has just executed the report-open action — either the initial Phase 5 open, or the 5.RC.5 re-render open after a request-changes pass.

**When:** The Conductor reaches the point immediately following that open action.

**Then:**

1. **The ask is presented in the same turn.** The Conductor's very next act, in the same turn, is presenting the end-gate approval ask ("approve to merge to main, or request changes") — the turn does not end between the report opening and the ask appearing.
2. **This holds at both sites.** Both the initial gate (after the first report build) and the redispatch re-render (after a request-changes pass) exhibit the same behavior — no silent turn-end at either.
3. **The instruction makes this explicit and un-skippable.** At both ask sites in `workflow.md`, the text contains an explicit directive that the turn MUST NOT end between rendering/opening the report and presenting the ask — render and ask are described as one atomic unit, not two steps that could be separated by a turn boundary.

## Pass Criteria

- A simulated or live run shows the approval prompt appearing immediately after the report open, in the same turn, at both the initial gate and the redispatch re-render — with no gap where the session appears to stop with a pending, unpresented decision.
- The instruction text at both ask sites contains an explicit "turn MUST NOT end between render and ask" (or equivalent unambiguous) directive.

## Fail Criteria

- The turn ends after either report-open action without the approval ask appearing in the same turn.
- The atomicity directive is missing, present at only one of the two sites, or phrased as advisory rather than a MUST/binding instruction.

## Verification Note

Verified primarily by inspection: confirm the explicit atomicity directive is present immediately adjacent to both the initial Phase 5 `<ask>` and the 5.RC.5 redispatch `<ask>` in `workflow.md`. Cross-check behaviorally: a subagent walking through the Phase 5 steps (from report-open through to the ask) should not stop or summarize-and-end before emitting the ask — the ask must appear in the same response as the report-open confirmation.
