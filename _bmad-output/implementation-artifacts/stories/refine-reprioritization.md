---
title: Refine Reprioritization — Add Priority Change Phase to Backlog Refinement
story_key: refine-reprioritization
status: ready-for-dev
epic_slug: impetus-epic-orchestrator
depends_on:
  - refine-skill-rewrite
touches:
  - skills/momentum/skills/refine/workflow.md
change_type: skill-instruction
derives_from:
  - path: _bmad-output/implementation-artifacts/stories/refine-skill.md
    relationship: derives_from
    section: "AC4: Findings Presentation — Priority suggestions"
  - path: _bmad-output/implementation-artifacts/stories/refine-skill.md
    relationship: derives_from
    section: "AC5: Approved Changes Applied via CLI — set-priority"
---

# Refine Reprioritization — Add Priority Change Phase to Backlog Refinement

## Story

As a developer using Momentum,
I want the refine workflow to analyze my backlog and recommend priority changes,
so that story priorities stay aligned with actual project pain and I don't have to manually re-prioritize every sprint.

## Description

The original refine-skill story (AC4–AC5) designed priority change recommendations as
part of consolidated findings, and `momentum-tools sprint set-priority` already exists
in the CLI. But the refine workflow never implemented the re-prioritization phase — it
jumps from stale-story evaluation directly to consolidated findings without ever
collecting priority change recommendations.

Currently, re-prioritization is a manual process requiring significant prompting each
sprint. The workaround exists but adds friction and risks being forgotten, which leads
to priority drift (low-priority stories blocking critical-path work, pain points
staying low despite recurring every sprint).

This story adds a re-prioritization step to the refine workflow between stale-story
evaluation (Step 6) and consolidated findings (Step 7). The step analyzes the backlog
using practical heuristics, produces priority change recommendations, and feeds them
into the existing batch approval UX alongside status mismatches, epic issues, and
stale-story evaluations.

## Acceptance Criteria (Plain English)

### AC1: Re-prioritization Step Exists in Workflow

- A new step is added to `workflow.md` between the current Step 6 (stale-story
  evaluation) and Step 7 (consolidated findings)
- Step numbering is adjusted accordingly (all subsequent steps renumber)
- The step produces a list of priority change recommendations stored as
  `{{priority_recommendations}}`

### AC2: Recurrence Heuristic

- The step identifies stories related to pain points that have appeared in multiple
  sprints by checking:
  - Retro findings in `_bmad-output/implementation-artifacts/sprints/*/retro-*.md`
    that reference the same story slug or topic across sprints
  - Sprint logs in `.claude/momentum/sprint-logs/` for patterns of the same manual
    workaround being prompted repeatedly
- Stories connected to recurring pain points are recommended for priority promotion
  with rationale citing the recurrence evidence

### AC3: Workaround Burden Heuristic

- The step evaluates the manual effort of existing workarounds:
  - High burden: requires complex multi-step prompting, custom instructions, or
    significant developer attention each time
  - Medium burden: requires some prompting but straightforward
  - Low burden: trivial workaround or one-liner
- Stories with high workaround burden are recommended for stronger priority promotion
  than those with low burden
- The burden assessment is included in the recommendation rationale

### AC4: Forgetting Risk Heuristic

- The step assesses what happens when a workaround is forgotten:
  - High risk: silent failures, data quality degradation, or broken output
  - Medium risk: noticeable but recoverable failures
  - Low risk: cosmetic or easily caught issues
- Stories with high forgetting risk are recommended for priority promotion regardless
  of workaround burden

### AC5: Dependency Promotion Heuristic

- The step identifies stories where priority is misaligned with their role in
  dependency chains:
  - A low/medium priority story that blocks one or more critical/high priority stories
    should be promoted to match
  - A critical/high priority story whose blockers are all done (dependencies satisfied)
    but is still sitting at low priority
- Dependency-based recommendations cite the specific blocking/blocked relationship

### AC6: Recommendations Surface in Consolidated Findings

- Priority change recommendations appear as a new category in the Step 7 consolidated
  findings alongside existing categories (status mismatches, epic issues, stale stories)
- Each recommendation shows: story slug, current priority, recommended priority,
  heuristic(s) that triggered it, and rationale
- The existing batch approval UX (A/M/R per finding, batch operations for 5+) applies
  to priority recommendations the same way it applies to other finding categories

### AC7: Approved Changes Applied via CLI

- Approved priority changes are applied in the "Apply approved changes" step using:
  `momentum-tools sprint set-priority --story SLUG --priority LEVEL`
- The summary step shows priority distribution before/after (this already exists in
  the workflow)

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral eval (EDD: before implementation) (AC: 1-7)
  - [ ] Create `skills/momentum/skills/refine/evals/eval-refine-reprioritization.md`
    — verifies the re-prioritization step produces recommendations using the four
    heuristics and feeds them into consolidated findings

- [ ] Task 2 — Add re-prioritization step to workflow.md (AC: 1, 2, 3, 4, 5)
  - [ ] Insert new step between current Step 6 and Step 7
  - [ ] Implement recurrence heuristic: scan retro findings and sprint logs for
    patterns
  - [ ] Implement workaround burden heuristic: assess manual effort level
  - [ ] Implement forgetting risk heuristic: assess failure mode severity
  - [ ] Implement dependency promotion heuristic: cross-reference priority vs.
    dependency chains
  - [ ] Store results as `{{priority_recommendations}}`
  - [ ] Renumber subsequent steps

- [ ] Task 3 — Integrate into consolidated findings (AC: 6)
  - [ ] Add "Priority recommendations" as a new category in Step 7 (renumbered Step 8)
  - [ ] Include recommendations in the batch approval UX
  - [ ] Update Step 0 task list to reflect new step count

- [ ] Task 4 — Add set-priority to the apply step (AC: 7)
  - [ ] Add priority change application in the "Apply approved changes" step using
    `momentum-tools sprint set-priority`
  - [ ] Verify the summary step already captures priority distribution delta (it does)

- [ ] Task 5 — Run eval and verify (AC: 1-7)
  - [ ] Run eval via subagent
  - [ ] Manually verify workflow step ordering and numbering

## Dev Notes

### What Already Exists

**CLI command (no changes needed):**
`momentum-tools sprint set-priority --story SLUG --priority LEVEL` exists at
`skills/momentum/scripts/momentum-tools.py:312` (`cmd_sprint_set_priority`). Tests
exist at `skills/momentum/scripts/test-momentum-tools.py:1392`. Accepts: critical,
high, medium, low. Validates story exists, validates priority level, idempotent.

**Workflow structure (modify, don't rewrite):**
The current workflow has steps 0–9. The new step slots in as Step 7 (between current
Step 6: stale-story evaluation and current Step 7: consolidated findings). All steps
from current Step 7 onward shift by +1.

**Consolidated findings pattern (reuse):**
Step 7 (current) already groups findings by category with batch approval. Add
"Priority recommendations" as a fourth category alongside status mismatches, epic
issues, and stale stories. No new UX pattern needed.

**Apply step pattern (reuse):**
Step 8 (current) already dispatches approved findings by type. Add a
"Priority changes" handler that calls `momentum-tools sprint set-priority`.

**Summary step (no changes needed):**
Step 9 (current) already computes before/after priority distribution from
`{{pre}}` and `{{post}}` — priority changes will automatically appear in the delta.

### Heuristic Data Sources

| Heuristic | Data source | What to look for |
|---|---|---|
| Recurrence | `_bmad-output/implementation-artifacts/sprints/*/retro-*.md` | Story slugs or topic keywords appearing in findings across 2+ sprint retros |
| Recurrence | `.claude/momentum/sprint-logs/**/*.jsonl` | Repeated manual prompting patterns for the same workaround |
| Workaround burden | Story description + current implementation | Complexity of the manual alternative |
| Forgetting risk | Story description + failure mode analysis | What breaks silently when the workaround is skipped |
| Dependency promotion | `stories/index.json` `depends_on` + `priority` fields | Low-priority stories blocking high-priority ones |

### Important Constraints

- **Read-only data access.** The re-prioritization step reads retro files, sprint
  logs, and stories/index.json but writes nothing. All mutations happen in the
  existing "Apply approved changes" step via CLI.
- **Orchestrator purity.** The refine workflow is an orchestrator (Decision 3d). The
  new step follows the same pattern: read → analyze → recommend → present. No direct
  file writes.
- **Human-approved only.** All priority changes require explicit developer approval
  through the existing batch approval UX. No automated priority changes.
- **Priority scale unchanged.** The four levels (critical, high, medium, low) are
  fixed. This story only changes which stories are at which level.

### What NOT to Change

- `momentum-tools.py` — `set-priority` already exists and is tested
- The consolidated findings batch approval UX pattern — reuse as-is
- The summary step's priority distribution delta — it already works
- Any other refine workflow steps — only insert a new step and update category lists

### Project Structure Notes

- Workflow file: `skills/momentum/skills/refine/workflow.md`
- Eval directory: `skills/momentum/skills/refine/evals/`
- CLI: `skills/momentum/scripts/momentum-tools.py`
- Retro files: `_bmad-output/implementation-artifacts/sprints/*/retro-*.md`
- Sprint logs: `.claude/momentum/sprint-logs/**/*.jsonl`

### References

- [Source: _bmad-output/implementation-artifacts/stories/refine-skill.md#AC4] — original design for priority suggestions in consolidated findings
- [Source: _bmad-output/implementation-artifacts/stories/refine-skill.md#AC5] — `set-priority` CLI command specified
- [Source: skills/momentum/scripts/momentum-tools.py:312] — `cmd_sprint_set_priority` implementation
- [Source: skills/momentum/skills/refine/workflow.md] — current workflow structure (Steps 0–9)
- [Source: _bmad-output/planning-artifacts/architecture.md] — refine skill data flow and write authority

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
