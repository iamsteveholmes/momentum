---
title: Refine Skill Rewrite — Practical Backlog Hygiene over Gap Analysis
story_key: refine-skill-rewrite
status: backlog
epic_slug: impetus-epic-orchestrator
depends_on: []
touches:
  - skills/momentum/skills/refine/SKILL.md
  - skills/momentum/skills/refine/workflow.md
  - _bmad-output/implementation-artifacts/stories/refine-skill.md
change_type: skill-instruction
priority: high
---

# Refine Skill Rewrite — Practical Backlog Hygiene over Gap Analysis

## Problem

The current `momentum:refine` workflow (at `skills/momentum/skills/refine/`)
is over-indexed on PRD/architecture gap analysis and under-indexed on
practical backlog hygiene. Specific problems:

1. **Stale planning artifact cross-referencing.** The workflow spawns parallel
   agents to cross-reference PRD and architecture docs against the backlog.
   These documents are increasingly stale — stories were already derived from
   them. Heavy cross-referencing burns tokens for marginal signal.

2. **No status hygiene.** Stories can be fully implemented (DoD items checked,
   Dev Agent Record complete) but still show `ready-for-dev` in index.json.
   Nothing detects the mismatch.

3. **Per-finding approval fatigue.** At scale (57+ stories, potentially
   dozens of findings), presenting each finding individually and asking
   A/M/R one at a time exhausts the developer. No batch operations exist.

4. **No epic-level analysis.** The workflow has no step for deduping
   overlapping epics, improving epic descriptions, or consolidating epics
   that cover the same domain.

5. **No bulk stale-story triage.** When an epic contains only low-priority
   stubs with no story files and no dependents, there is no way to drop them
   in bulk with a safety check.

6. **Dependency analysis doesn't belong here.** Circular dependency detection,
   missing targets, and satisfied dependencies are sprint planning concerns,
   not refinement concerns.

## Acceptance Criteria

### AC1: Planning Artifact Staleness Check (Not Cross-Reference)

- The workflow checks whether `_bmad-output/planning-artifacts/prd.md` and
  `_bmad-output/planning-artifacts/architecture.md` exist
- If they exist, it checks their last-modified date against the most recent
  sprint completion date
- If stale (older than the most recent completed sprint), it flags them to
  the developer: "Planning artifacts are stale — consider archiving or
  updating. Stories may not capture everything from these docs."
- The workflow does NOT spawn parallel agents to cross-reference these
  documents against the backlog
- If the developer decides to archive them, that is a manual action outside
  this workflow

### AC2: Status Hygiene Detection

- The workflow reads each non-terminal story in `stories/index.json`
- For stories with `story_file: true`, it reads the story file and checks
  for a Dev Agent Record section with all DoD items checked (every `- [x]`
  line, no `- [ ]` lines in the File List / DoD section)
- Stories where the file shows completion but index.json status is not
  `done` are flagged as status mismatches
- The developer can approve transitioning flagged stories to `done` via
  `momentum-tools sprint status-transition`

### AC3: Batch Approval Operations

- Findings are presented grouped by category (status mismatches, stale
  candidates, epic issues, planning staleness)
- The developer can approve or reject entire categories at once:
  "approve all status mismatches", "reject all stale candidates"
- The developer can approve or reject by range within a category:
  "approve findings 1-5, reject 6"
- Individual A/M/R per finding is still available but not the only mode
- The interaction adapts to scale: 3 findings get individual treatment;
  20+ findings get batch-first presentation

### AC4: Epic-Level Analysis

- The workflow compares all epic slugs for semantic overlap (e.g.,
  `research-knowledge` vs `research-knowledge-management`)
- It checks epic descriptions for vagueness or missing descriptions
- It identifies epics that could be consolidated based on their stories'
  `touches` paths clustering around the same directories
- Findings are presented as suggestions — the developer decides
- Scope is limited to individual classification corrections and container
  optimization. Structural taxonomy overhauls remain the domain of
  `momentum:epic-grooming`

### AC5: Bulk Stale-Story Triage with Safety Net

- The workflow identifies epics where ALL remaining stories are: status
  `backlog`, priority `low`, no story file, and no other stories depend
  on them
- For such epics, it offers to drop all stories in bulk
- Before dropping, it checks whether any story titles or descriptions
  reference concepts not captured elsewhere (in other stories, in the
  codebase via `touches` paths, or in planning docs if they still exist)
- If uncaptured concepts are found, it lists what would be lost and asks
  for confirmation before proceeding
- If all content is captured elsewhere, it drops without the extra warning

### AC6: No Dependency Analysis

- The workflow does NOT detect circular dependencies, missing dependency
  targets, or satisfied dependencies
- No findings are generated in a "dependency issues" category
- Dependency validation is explicitly deferred to sprint planning

### AC7: Decisions Logged and Summarized

- All refinement decisions (status transitions, drops, epic suggestions
  accepted) are logged via `momentum-tools log` with event type `decision`
- A summary is presented at the end: changes applied by type, findings
  rejected, before/after priority distribution

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral evals (EDD: before rewriting the skill)
  - [ ] Create `skills/momentum/skills/refine/evals/eval-refine-status-hygiene.md`
    — verifies the workflow detects stories with completed DoD but non-done
    status, and offers transitions via CLI
  - [ ] Create `skills/momentum/skills/refine/evals/eval-refine-batch-approval.md`
    — verifies the workflow supports batch approve/reject operations and
    adapts presentation to finding count
  - [ ] Create `skills/momentum/skills/refine/evals/eval-refine-no-dependency-analysis.md`
    — verifies the workflow does NOT produce dependency-category findings
    and does NOT spawn PRD/architecture cross-reference agents

- [ ] Task 2 — Rewrite workflow.md (AC: 1-7, main deliverable)
  - [ ] Step 0: Task tracking initialization
  - [ ] Step 1: Backlog presentation (reuse existing pattern — group by epic,
    sort by priority, show summary)
  - [ ] Step 2: Planning artifact staleness check (light — no subagent spawns)
  - [ ] Step 3: Status hygiene scan (read story files, detect completion
    mismatches)
  - [ ] Step 4: Epic-level analysis (overlap detection, description quality,
    consolidation candidates)
  - [ ] Step 5: Stale-story triage with safety net (bulk epic drops with
    content-loss check)
  - [ ] Step 6: Consolidated findings with batch approval UX
  - [ ] Step 7: Apply approved changes via momentum-tools CLI and delegate
    new story creation if needed
  - [ ] Step 8: Log decisions and present summary

- [ ] Task 3 — Update SKILL.md description (AC: 1)
  - [ ] Update description to reflect the rewritten workflow's focus on
    backlog hygiene over gap analysis
  - [ ] Confirm description is under 150 characters

- [ ] Task 4 — Run evals and verify (AC: 1-7)
  - [ ] Run each eval via subagent
  - [ ] Confirm status hygiene detection works
  - [ ] Confirm batch approval UX works
  - [ ] Confirm no dependency analysis or heavy cross-referencing occurs

## Dev Notes

### What Changes from the Current Workflow

| Current (v1) | Rewritten (v2) |
|---|---|
| Step 2: Parallel PRD + architecture discovery agents | Step 2: Light staleness check (file date only, no agents) |
| Step 3: Dependency analysis (circular, missing, satisfied) | Removed entirely — sprint planning's job |
| Step 3: Per-finding A/M/R approval loop | Step 6: Batch-first approval with category and range support |
| No status hygiene | Step 3: Story completion vs index.json status mismatch detection |
| No epic analysis | Step 4: Epic overlap, description quality, consolidation candidates |
| No bulk triage | Step 5: Bulk stale-epic drops with safety net |

### Workflow Structure (9 Steps)

**Step 0: Initialize task tracking**
- Create tasks for the 8 workflow steps
- Log workflow start

**Step 1: Present backlog**
- Same as current v1 — read index.json, filter terminal states, group by
  epic, sort by priority, display summary
- Store pre-refine priority distribution for before/after comparison

**Step 2: Planning artifact staleness check**
- Check if prd.md and architecture.md exist
- If they exist, compare last-modified date to the most recent completed
  sprint date from `sprints/index.json`
- If stale, flag to developer. No subagent spawns. No cross-referencing.
- Store finding if stale

**Step 3: Status hygiene scan**
- For each non-terminal story with `story_file: true`, read the story file
- Look for Dev Agent Record section with a File List or DoD checklist
- If all items are `[x]` (checked) and the story status is not `done`,
  flag as a status mismatch
- Store mismatches as findings

**Step 4: Epic-level analysis**
- Compare epic slugs pairwise for semantic similarity
- Check for epics with no description or very short descriptions
- Analyze `touches` paths across stories within each epic — if stories in
  different epics cluster around the same directories, suggest consolidation
- Store findings

**Step 5: Stale-story triage**
- Find epics where all remaining stories meet: backlog status, low priority,
  no story file, no dependents
- For each such epic, check story titles/descriptions for concepts not
  captured in other stories or the codebase
- If uncaptured content found: flag what would be lost
- If all captured: mark as safe to bulk-drop
- Store findings

**Step 6: Consolidated findings with batch approval**
- Present all findings grouped by category:
  1. Planning artifact staleness (if any)
  2. Status mismatches
  3. Epic issues (overlap, descriptions, consolidation)
  4. Stale-story bulk drops
- Scale-adaptive UX:
  - Under 5 findings: present individually, ask A/M/R per finding
  - 5+ findings: present by category, offer batch operations first
    ("approve all status mismatches?"), then allow individual overrides
- Developer can: approve/reject entire categories, approve/reject by range
  (e.g., "1-5"), or go finding-by-finding

**Step 7: Apply approved changes**
- Status transitions: `momentum-tools sprint status-transition --story SLUG --target done`
- Story drops: `momentum-tools sprint status-transition --story SLUG --target dropped`
- Epic reassignments: `momentum-tools sprint epic-membership --story SLUG --epic SLUG`
- New stories from findings: delegate to `momentum:create-story`
- Log each change via `momentum-tools log`

**Step 8: Summary**
- Changes applied by type, findings rejected
- Before/after priority distribution
- Epic distribution changes if any

### Orchestrator Purity

Same rule as v1 — the workflow reads files and presents information, but
all mutations go through `momentum-tools` CLI or `momentum:create-story`
delegation. No Edit/Write on index.json or any project file.

### Existing Evals to Replace

The current evals at `skills/momentum/skills/refine/evals/` test the v1
behavior (gap discovery agents, CLI-only mutations). The v2 rewrite changes
the workflow's analysis steps, so evals must be rewritten to test:
- Status hygiene detection (new)
- Batch approval UX (new)
- Absence of dependency analysis and heavy cross-referencing (regression guard)

The CLI-only mutation eval (`eval-refine-cli-mutations.md`) is still valid
in spirit but should be updated to cover status-transition to `done` (new
use case in v2).

### What NOT to Change

- `momentum-tools.py` — no new CLI commands needed
- `momentum:create-story` — invoke it, don't modify it
- Sprint-planning or sprint-dev workflows
- `stories/index.json` directly

## Momentum Implementation Guide

**Change Types in This Story:**
- All tasks -> skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Before writing a single line of the skill:**
1. Write 3 behavioral evals in `skills/momentum/skills/refine/evals/`:
   - One per eval above, testing status hygiene, batch approval, and absence
     of dependency analysis
   - Format: "Given [input/context], the skill should [observable behavior]"

**Then implement:**
2. Rewrite workflow.md and update SKILL.md description

**Then verify:**
3. Run evals via subagent, confirm behaviors match

**NFR compliance:**
- SKILL.md `description` must be <=150 characters (NFR1)
- `model:` and `effort:` frontmatter must be present
- SKILL.md body <=500 lines / 5000 tokens (workflow.md can be longer)

**DoD items for skill-instruction tasks:**
- [ ] 3 behavioral evals written in `skills/momentum/skills/refine/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented)
- [ ] SKILL.md description <=150 characters confirmed
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body <=500 lines confirmed
- [ ] AVFL checkpoint on produced artifact documented
