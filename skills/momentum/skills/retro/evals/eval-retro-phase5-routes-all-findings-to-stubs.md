# Eval: Retro Phase 5 Routes All Findings to Story Stubs

## Purpose

Verify that `momentum:retro` Phase 5 routes all priority action items to story stub creation
— no items are classified as Tier 1 for distill routing. The two-lane model (sprint stories
or quick-fix) is the sole path for applying practice fixes.

## Scenario

A developer has completed Phases 1–4 of a retro. The retro-transcript-audit.md contains
a "Priority Action Items" section with three items:

1. "Add a standing rule that AVFL evals must be written before skill files are modified"
   - signal_type: Instruction
   - recommended_change: "Add a one-sentence rule to dev-skills.md"

2. "Refactor the triage workflow to support five classes instead of six — remove DISTILL"
   - signal_type: Workflow
   - recommended_change: "Rewrite triage/workflow.md classification table and delegation logic"

3. "Update impetus dispatch.md to remove the momentum:distill row"
   - signal_type: Context
   - recommended_change: "Replace distill row with two-lane guidance in dispatch.md"

Phase 5 is invoked to process these items.

## Expected Behaviors

### B1: No Tier Classification

Phase 5 does not classify items into Tier 1 / Tier 2. There is no "distill_candidates"
extraction step. All priority action items proceed directly to story stub creation regardless
of signal_type or change scope.

### B2: All Items Route to Stub Creation

All three items are presented as proposed story stubs. Each stub includes:
- `title`: derived from the finding
- `epic_slug`: appropriate for Momentum practice changes
- `status`: "backlog"
- `description`: one-sentence summary of the finding
- `suggested_ac`: bulleted acceptance criteria derived from the finding

### B3: No momentum:distill Invocation

Phase 5 never invokes `momentum:distill` or any distill subagent. The output contains
no references to "distilled" dispositions or distill count.

### B4: Developer Approves Stubs

The developer is asked "Approve this stub? (Y/N)" for each proposed stub. Approved
stubs are added to `.momentum/stories/index.json`. Rejected stubs are skipped.

### B5: Output Summary Shows Only Stubs and Skipped

The Phase 5 completion output shows:
- Stubbed: N items (added to backlog)
- Skipped: M items (developer declined)
- No "Distilled: X" count

---

## Pass Criteria

- [ ] No Tier 1 / Tier 2 classification performed on any item
- [ ] All three items presented as story stub proposals
- [ ] No `momentum:distill` invoked at any point
- [ ] No `{{distill_candidates}}` or `{{distilled_dispositions}}` template vars used
- [ ] Output summary does not mention "Distilled" count
- [ ] Approved stubs added to stories/index.json

## Failure Criteria

- Any item classified as Tier 1 for distill routing
- `momentum:distill` invoked for any item
- Output summary contains a "Distilled" count
- Items with signal_type bypass stub creation proposal
