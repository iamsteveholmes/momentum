# Eval: Triage Routes Observations into Five Classes (No DISTILL)

## Purpose

Verify that `momentum:triage` classifies a mixed list of observations into exactly five
classes — ARTIFACT, DECISION, SHAPING, DEFER, REJECT — and does not produce a DISTILL
class in its output.

## Scenario

A developer invokes `/momentum:triage` and provides the following list of observations:

1. "We should add a `--dry-run` flag to the sprint activate command"
2. "The rule about never using git add -A should be in the global rules file, not repeated in each skill"
3. "Should we adopt DuckDB for all structured data queries across Momentum?"
4. "There's an idea about AI-assisted sprint planning that's interesting but I don't know what to do with it yet"
5. "The feature-status-hash command — come back to it after the feature layer is fully wired"
6. "The old `triage-inbox.md` approach — never mind, DEC-007 superseded it"

## Expected Behaviors

### B1: Classification Correctness (Five Classes Only)

Each item is classified correctly before any execution. No DISTILL class is produced:

- Item 1 → ARTIFACT (a bounded backlog item with clear deliverable)
- Item 2 → ARTIFACT (a practice improvement — now routes to backlog as a story, not distill)
- Item 3 → DECISION (a strategic adoption question requiring a recorded decision)
- Item 4 → SHAPING (vague intent, needs thinking)
- Item 5 → DEFER (valid but explicitly not now)
- Item 6 → REJECT (superseded, not worth pursuing)

### B2: No DISTILL Class in Output

The batch-approval display does not show a `[DISTILL]` section. The six-class table in the
workflow preamble does not include DISTILL. The triage summary output does not show a
"Distilled" count.

### B3: ARTIFACT Enrichment for Practice Improvement Items

For item 2 (practice rule improvement), the classification output includes:
- `story_type`: suggested (likely "maintenance")
- `epic_slug`: suggested (e.g., "impetus-core" or appropriate Momentum epic)
- `priority`: default "low" unless urgency signals present

### B4: Batch Approval Before Execution

All classified items are presented in a single batch-approval display grouped by class.
No downstream executor (intake, decision, append) is invoked until after the developer
approves.

### B5: No Gap-Check Performed

The skill does not evaluate whether classified items represent value-floor gaps,
backlog coverage, or North Star alignment. Classification only — per DEC-005 D10.

---

## Pass Criteria

- [ ] No DISTILL class produced in any output
- [ ] Item 2 (practice rule) classified as ARTIFACT, not DISTILL
- [ ] Batch approval shows five class groups max (ARTIFACT, DECISION, SHAPING, DEFER, REJECT)
- [ ] No "Distilled" count in triage summary
- [ ] ARTIFACT items include enrichment fields (story_type, epic_slug, priority)
- [ ] Batch approval required before execution

## Failure Criteria

- DISTILL class appears in batch-approval output for any item
- Item 2 classified as DISTILL instead of ARTIFACT
- Triage summary shows "Distilled: N" count
- `momentum:distill` invoked for any item
- Triage executes before batch approval
