---
title: Refine Workflow — Assessment & Decision Review Step
story_key: refine-assessment-decision-review
status: ready-for-dev
epic_slug: impetus-epic-orchestrator
depends_on:
  - assessment-skill
  - decision-skill
touches:
  - skills/momentum/skills/refine/workflow.md
change_type: skill-instruction
derives_from:
  - path: _bmad-output/planning-artifacts/assessments/index.md
    relationship: derives_from
    section: "Assessment Registry — staleness and traceability"
  - path: _bmad-output/planning-artifacts/decisions/index.md
    relationship: derives_from
    section: "Decision Registry — story coverage traceability"
---

# Refine Workflow — Assessment & Decision Review Step

## Story

As a developer running backlog refinement,
I want the refine workflow to review assessments and decisions for staleness and
missing story coverage,
so that the full pipeline from observation to implementation stays connected and
nothing falls through the cracks.

## Description

The refine workflow already reviews planning artifacts (PRD, architecture) and
story status (hygiene, staleness, epic classification). This story extends that
review to the two new planning artifact types: assessments (ASR) and decisions
(SDR).

Without this step, assessments can go stale without anyone noticing, decisions
can reference stories that were never created, and decision gates can pass their
trigger conditions without review. The pipeline breaks silently:

```
Research → Assessment → Decision → Stories
                 ↑ stale?     ↑ missing stories?   ↑ created?
```

This step checks each link in the chain and surfaces findings in the existing
consolidated findings batch approval UX.

## Acceptance Criteria (Plain English)

### AC1: Assessment Staleness Detection

- The step reads all ASR documents in `_bmad-output/planning-artifacts/assessments/`
- Assessments with status "current" and date older than 30 days are flagged as
  potentially stale
- Assessments with status "current" that have empty `decisions_produced` are
  flagged as assessments with unacted-on findings
- Findings are presented with: ASR id, title, date, age in days, and whether
  decisions were produced

### AC2: Assessment Next Steps Coverage

- For each assessment with status "current", read the Recommended Next Steps
  section
- Check whether recommended next steps have corresponding decisions (SDRs that
  reference this ASR) or stories in the backlog
- Flag unresolved next steps that have neither decisions nor stories

### AC3: Decision Story Coverage

- For each SDR document in `_bmad-output/planning-artifacts/decisions/`:
  - Check whether stories listed in `stories_affected` exist in stories/index.json
  - Check whether phased implementation plans suggest stories that don't yet exist
    in the backlog
  - Flag missing stories with: SDR id, decision title, missing story description

### AC4: Decision Gate Review

- For each SDR with decision gates:
  - Check if any gate's timing condition appears to be met (e.g., "Phase 1 done"
    and the relevant stories are all status "done")
  - Flag gates that appear ready for review
  - Present the gate's criteria so the developer can evaluate

### AC5: Findings Surface in Consolidated Findings

- Assessment and decision findings appear as new categories in the refine
  workflow's consolidated findings step alongside existing categories (status
  mismatches, epic issues, stale stories, priority recommendations)
- The existing batch approval UX (A/M/R per finding, batch operations for 5+)
  applies to these findings
- Approved findings result in: new story creation (via momentum:create-story),
  decision gate reviews (surfaced for developer evaluation), or assessment
  refresh recommendations

### AC6: Step Placement in Workflow

- The new step is added to the refine workflow after the re-prioritization step
  (from refine-reprioritization story) and before consolidated findings
- Step numbering is adjusted accordingly
- Step 0 task list is updated to reflect the new step count

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral eval (EDD: before implementation) (AC: 1-6)
  - [ ] Create eval verifying assessment staleness detection and decision story
    coverage checking

- [ ] Task 2 — Add assessment & decision review step to workflow.md (AC: 1-4)
  - [ ] Read all ASR documents, check staleness and decisions_produced
  - [ ] Read all SDR documents, check story coverage and gate conditions
  - [ ] Store results as {{assessment_decision_findings}}

- [ ] Task 3 — Integrate into consolidated findings (AC: 5, 6)
  - [ ] Add "Assessment & decision review" as a new category in consolidated
    findings
  - [ ] Include in batch approval UX
  - [ ] Update Step 0 task list

- [ ] Task 4 — Run eval and verify (AC: 1-6)

## Dev Notes

### Workflow Structure

The refine workflow after all stories in this sprint would be:

1. Present backlog
2. Planning artifact discovery (wave 1)
3. Planning artifact update (wave 2)
4. Status hygiene scan
5. Epic grooming delegation
6. Stale-story evaluation
7. Re-prioritization (from refine-reprioritization story)
8. **Assessment & decision review (this story)**
9. Consolidated findings with batch approval
10. Apply approved changes
11. Summary

### Data Sources

| Source | What to check |
|---|---|
| `assessments/*.md` | Staleness (>30 days), empty decisions_produced, unresolved next steps |
| `decisions/*.md` | Missing stories from stories_affected, phased plan gaps, gate conditions met |
| `stories/index.json` | Cross-reference for story existence checks |

### Important Constraints

- Read-only data access — mutations happen in the existing apply step via CLI
- New story creation delegates to momentum:create-story (existing pattern)
- Decision gate review is presentational only — the developer evaluates, the
  skill doesn't auto-close gates

### What NOT to Change

- Existing refine workflow steps — only insert a new step
- Assessment or decision document format — this step reads, doesn't write
- The consolidated findings batch approval UX pattern — reuse as-is

### References

- [Source: skills/momentum/skills/refine/workflow.md] — current workflow
- [Source: _bmad-output/planning-artifacts/assessments/index.md] — assessment registry
- [Source: _bmad-output/planning-artifacts/decisions/index.md] — decision registry
- [Source: nornspun asr-001] — reference ASR format
- [Source: nornspun sdr-001] — reference SDR format

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
