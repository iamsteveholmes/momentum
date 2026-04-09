# Eval: Refine Skill — Assessment & Decision Review Step

## Setup

Invoke `/momentum:refine` on a project where:
- `_bmad-output/planning-artifacts/assessments/` contains at least two ASR documents:
  - One with status "current" and date older than 30 days (stale candidate)
  - One with status "current" and date within 30 days (not stale)
  - The stale one has `decisions_produced: []` (unacted-on findings)
  - The current one has `decisions_produced: [SDR-001]` (acted-on)
  - The stale one has a "Recommended Next Steps" section with items not covered by
    any SDR or story
- `_bmad-output/planning-artifacts/decisions/` contains at least one SDR document:
  - `stories_affected` lists at least one story slug that does NOT exist in
    `stories/index.json` (missing story)
  - `stories_affected` lists at least one story slug that DOES exist (present story)
  - Has a "Decision Gates" section with one gate whose timing condition appears met
    (e.g., "Phase 1 done" and all Phase 1 stories are status "done")
- `_bmad-output/implementation-artifacts/stories/index.json` contains stories
  matching the SDR's present story refs and Phase 1 stories all marked done

Run the workflow through to the assessment & decision review step (between
re-prioritization and consolidated findings).

## Expected Behavior

### AC1: Assessment Staleness Detection

1. The workflow reads all ASR documents in
   `_bmad-output/planning-artifacts/assessments/`
2. The stale ASR (status "current", date > 30 days ago) is flagged as potentially
   stale with: ASR id, title, date, age in days
3. The within-30-days ASR is NOT flagged as stale
4. The stale ASR (with `decisions_produced: []`) is flagged as an assessment with
   unacted-on findings
5. The acted-on ASR (with `decisions_produced: [SDR-001]`) is NOT flagged as
   having unacted-on findings
6. Both staleness and unacted-on status are presented together per ASR (not in
   separate lists)

### AC2: Assessment Next Steps Coverage

7. For the stale ASR with status "current", the workflow reads its
   "Recommended Next Steps" section
8. Each next step is checked for coverage: is there an SDR referencing this ASR,
   or a story in the backlog addressing it?
9. Unresolved next steps (no SDR, no story) are flagged in the findings
10. The workflow does NOT flag next steps that are covered by existing SDRs or
    stories

### AC3: Decision Story Coverage

11. The workflow reads all SDR documents in
    `_bmad-output/planning-artifacts/decisions/`
12. For each SDR, `stories_affected` slugs are cross-referenced against
    `stories/index.json`
13. The missing story slug (not in index.json) is flagged with: SDR id, decision
    title, missing story description
14. The present story slug (in index.json) is NOT flagged as missing
15. If the SDR has a "Phased Implementation Plan", key stories from that table
    are also checked for existence and gaps are flagged

### AC4: Decision Gate Review

16. For each SDR with a "Decision Gates" section, each gate is evaluated
17. A gate whose timing condition appears met (Phase 1 stories all done) is
    flagged as ready for review
18. The gate's criteria are presented verbatim so the developer can evaluate
19. The workflow does NOT auto-close or auto-mark gates — it is presentational
    only
20. A gate whose timing condition is NOT met is NOT flagged as ready for review

### AC5: Findings Surface in Consolidated Findings

21. After the assessment & decision review step completes, all findings are
    stored in `{{assessment_decision_findings}}`
22. In the consolidated findings step, "Assessment & decision review" appears
    as a distinct category alongside existing categories:
    - Status mismatches
    - Epic issues
    - Stale stories
    - Priority changes
    - Assessment & decision review (new)
23. Each finding in this category has: id, description, and a recommended action
24. The batch approval UX (A=all / R=all / pick individually) applies to this
    category when total findings >= 5
25. The individual A/M/R prompt applies when total findings < 5
26. Approved findings that require a new story invoke `momentum:create-story`
    (delegated, not written directly)
27. Decision gate findings are surfaced for developer evaluation — no automated
    gate closure occurs

### AC6: Step Placement in Workflow

28. The new step appears between the re-prioritization step (Step 7) and the
    consolidated findings step (now renumbered to Step 9)
29. Step 0 task list reflects the full 11-step sequence including this new step
30. Existing step numbers before the new step are unchanged
31. The consolidated findings step is renumbered to Step 9 (was Step 8)
32. The apply step is renumbered to Step 10 (was Step 9)
33. The summary step is renumbered to Step 11 (was Step 10)

### Constraints: Read-Only Analysis

34. The assessment & decision review step does NOT call Edit or Write on any file
35. The step reads ASR and SDR files using Read/Grep tools only
36. Mutations (new story creation, gate updates) are deferred to the apply step
    or delegated to momentum:create-story
37. The step does NOT modify assessment or decision documents

## Verification

- Confirm an "Assessment & decision review" step exists between the
  re-prioritization step and the consolidated findings step in the workflow
- Confirm the step stores `{{assessment_decision_findings}}`
- Confirm consolidated findings includes "Assessment & decision review" as a
  category fed from `{{assessment_decision_findings}}`
- Confirm the step reads from `assessments/` and `decisions/` directories
- Confirm the step cross-references `stories/index.json` for story coverage checks
- Confirm Step 0 task list has 11 entries (or the correct count after all steps)
- Search all workflow actions in the assessment & decision review step for Edit/Write
  calls — there must be zero
- Search for `momentum:create-story` delegation — it must be in the apply step,
  not the review step
