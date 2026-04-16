# Eval: Triage Classifies Items into Correct Classes

## Purpose

Verify that `momentum:triage` classifies a mixed list of observations into the correct
six classes — ARTIFACT, DISTILL, DECISION, SHAPING, DEFER, REJECT — before executing
any actions.

## Scenario

A developer invokes `/momentum:triage` and provides the following list of observations:

1. "We should add a `--dry-run` flag to the sprint activate command"
2. "The rule about never using git add -A should be in the global rules file, not repeated in each skill"
3. "Should we adopt DuckDB for all structured data queries across Momentum?"
4. "There's an idea about AI-assisted sprint planning that's interesting but I don't know what to do with it yet"
5. "The feature-status-hash command — come back to it after the feature layer is fully wired"
6. "The old `triage-inbox.md` approach — never mind, DEC-007 superseded it"

## Expected Behaviors

### B1: Classification Correctness

Each item is classified correctly before any execution:

- Item 1 → ARTIFACT (a bounded backlog item with clear deliverable)
- Item 2 → DISTILL (a practice learning — a rule to apply to a specific file)
- Item 3 → DECISION (a strategic adoption question requiring a recorded decision)
- Item 4 → SHAPING (vague intent, needs thinking)
- Item 5 → DEFER (valid but explicitly not now)
- Item 6 → REJECT (superseded, not worth pursuing)

### B2: ARTIFACT Enrichment

For item 1 (ARTIFACT), the classification output includes:

- `story_type`: suggested (likely "maintenance" or "feature")
- `feature_slug`: suggested from features.json or flagged as "no feature match"
- `epic_slug`: suggested DDD boundary-aligned epic
- `priority`: default "low" unless urgency signals present

### B3: Batch Approval Presented Before Execution

All six items are presented in a single batch-approval display grouped by class. No
downstream executor (intake, distill, decision, append) is invoked until after the
developer approves.

### B4: No Gap-Check Performed

The skill does not evaluate whether classified items represent value-floor gaps,
backlog coverage, or North Star alignment. Classification only — per DEC-005 D10.

### B5: Queue Items Distinguished

SHAPING, DEFER, REJECT items are displayed distinctly from ARTIFACT/DISTILL/DECISION
items in the batch approval output, with their target noted as "intake-queue.jsonl".

## Pass Criteria

B1–B5 must all be satisfied. Misclassification of any item is a failing eval.
