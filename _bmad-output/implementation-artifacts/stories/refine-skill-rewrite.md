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

1. **Planning artifacts drift silently.** The workflow treats PRD and
   architecture docs as static references. As sprints complete, requirements
   get implemented, decisions change, and these documents fall behind. Nothing
   detects or corrects the drift.

2. **No status hygiene.** Stories can be fully implemented (DoD items checked,
   Dev Agent Record complete) but still show `ready-for-dev` in index.json.
   Nothing detects the mismatch.

3. **Per-finding approval fatigue.** At scale (57+ stories, potentially
   dozens of findings), presenting each finding individually and asking
   A/M/R one at a time exhausts the developer. No batch operations exist.

4. **No epic-level analysis.** The workflow has no step for deduping
   overlapping epics, improving epic descriptions, or consolidating epics
   that cover the same domain.

5. **No stale-story triage.** Low-priority stubs accumulate in the backlog
   with no systematic way to evaluate whether they still carry value.

6. **Dependency analysis doesn't belong here.** Circular dependency detection,
   missing targets, and satisfied dependencies are sprint planning concerns,
   not refinement concerns.

## Acceptance Criteria

### AC1: Planning Artifact Discovery and Update

The workflow runs a two-wave process to keep PRD and architecture current.

**Wave 1 — Discovery (parallel).** Spawn two parallel subagents:
- PRD coverage agent: reads `_bmad-output/planning-artifacts/prd.md` and
  `stories/index.json`, identifies requirements that are missing, outdated,
  or no longer accurate given completed work
- Architecture coverage agent: reads
  `_bmad-output/planning-artifacts/architecture.md` and
  `stories/index.json`, identifies decisions that are missing, outdated,
  or no longer accurate given completed work

Each returns structured findings:
`[{id, description, action_needed (add/update/remove), rationale}]`

**Gate:** If neither agent finds required updates, skip wave 2.

**Wave 2 — Update (parallel).** If gaps found, the developer reviews the
discovery findings and approves before wave 2 runs. This is NOT automatic.
Then spawn two parallel update subagents:
- PRD update agent: reads prd.md, applies approved changes following
  existing format. Sole writer of prd.md.
- Architecture update agent: reads architecture.md, applies approved
  changes following existing format. Sole writer of architecture.md.

Planning artifacts are NOT optional and are NOT candidates for archiving.
They are authoritative documents that must stay current.

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
  candidates, planning artifact updates, epic issues)
- The developer can approve or reject entire categories at once:
  "approve all status mismatches", "reject all stale candidates"
- The developer can approve or reject by range within a category:
  "approve findings 1-5, reject 6"
- Individual A/M/R per finding is still available but not the only mode
- The interaction adapts to scale: 3 findings get individual treatment;
  20+ findings get batch-first presentation

### AC4: Epic-Level Analysis — Delegate to epic-grooming

- The workflow invokes `momentum:epic-grooming` as a substep for
  epic-level structural analysis (deduping, description quality,
  consolidation)
- Refine does not reimplement this logic
- If `momentum:epic-grooming` doesn't exist yet, flag it and skip the step

### AC5: Stale-Story Individual Evaluation

- The workflow identifies candidate stale stories: status `backlog`,
  priority `low`, no story file
- For each candidate, the workflow evaluates individually:
  - What value does this story represent?
  - Is that value captured elsewhere (other stories, codebase, planning
    docs)?
  - Recommendation: keep or drop, with rationale
- The developer reviews each evaluation and decides. No auto-dropping.

### AC6: No Dependency Analysis

- The workflow does NOT detect circular dependencies, missing dependency
  targets, or satisfied dependencies
- No findings are generated in a "dependency issues" category
- Dependency validation is explicitly deferred to sprint planning

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral evals (EDD: before rewriting the skill)
  - [ ] Create `skills/momentum/skills/refine/evals/eval-refine-planning-artifacts.md`
    — verifies the workflow runs two-wave planning artifact discovery and
    update, with developer approval gate between waves
  - [ ] Create `skills/momentum/skills/refine/evals/eval-refine-status-hygiene.md`
    — verifies the workflow detects stories with completed DoD but non-done
    status, and offers transitions via CLI
  - [ ] Create `skills/momentum/skills/refine/evals/eval-refine-no-dependency-no-logging.md`
    — verifies the workflow does NOT produce dependency-category findings
    and does NOT emit any `momentum-tools log` calls

- [ ] Task 2 — Rewrite workflow.md (AC: 1-6, main deliverable)
  - [ ] Step 0: Task tracking initialization
  - [ ] Step 1: Backlog presentation (group by epic, sort by priority,
    show summary)
  - [ ] Step 2: Planning artifact discovery — wave 1 (two parallel agents)
  - [ ] Step 3: Planning artifact update — wave 2 (two parallel agents,
    only if wave 1 found gaps, developer approval gate between waves)
  - [ ] Step 4: Status hygiene scan (read story files, detect completion
    mismatches)
  - [ ] Step 5: Delegate to momentum:epic-grooming (if available)
  - [ ] Step 6: Stale-story individual evaluation
  - [ ] Step 7: Consolidated findings with batch approval UX
  - [ ] Step 8: Apply approved changes via momentum-tools CLI
  - [ ] Step 9: Summary (before/after presentation)

- [ ] Task 3 — Update SKILL.md description (AC: 1)
  - [ ] Update description to reflect the rewritten workflow's focus on
    backlog hygiene over gap analysis
  - [ ] Confirm description is under 150 characters

- [ ] Task 4 — Run evals and verify (AC: 1-6)
  - [ ] Run each eval via subagent
  - [ ] Confirm planning artifact discovery+update works
  - [ ] Confirm status hygiene detection works
  - [ ] Confirm no dependency analysis and no logging occurs

## Dev Notes

### What Changes from the Current Workflow

| Current (v1) | Rewritten (v2) |
|---|---|
| Step 2: Parallel PRD + architecture gap-discovery agents | Step 2-3: Two-wave discovery+update with developer approval gate |
| Step 3: Dependency analysis (circular, missing, satisfied) | Removed entirely — sprint planning's job |
| Step 3: Per-finding A/M/R approval loop | Step 7: Batch-first approval with category and range support |
| No status hygiene | Step 4: Story completion vs index.json status mismatch detection |
| Inline epic analysis | Step 5: Delegated to momentum:epic-grooming |
| No stale-story triage | Step 6: Individual story evaluation with keep/drop recommendation |
| AC7: Decisions logged via momentum-tools log | Removed — no logging calls anywhere |

### Workflow Structure (10 Steps)

**Step 0: Initialize task tracking**
- Create tasks for the workflow steps

**Step 1: Present backlog**
- Same as current v1 — read index.json, filter terminal states, group by
  epic, sort by priority, display summary
- Store pre-refine priority distribution for before/after comparison

**Step 2: Planning artifact discovery (wave 1)**
- Spawn two parallel subagents:
  - PRD coverage agent: reads prd.md + stories/index.json, returns
    structured findings `[{id, description, action_needed, rationale}]`
  - Architecture coverage agent: reads architecture.md +
    stories/index.json, returns structured findings
- Each agent identifies what is missing, outdated, or no longer accurate
- If neither agent finds required updates, skip to step 4

**Step 3: Planning artifact update (wave 2)**
- Present wave 1 findings to the developer for review and approval
- Developer sees exactly what will change and confirms
- Spawn two parallel update subagents:
  - PRD update agent: sole writer of prd.md, applies approved changes
  - Architecture update agent: sole writer of architecture.md, applies
    approved changes
- Only runs if wave 1 found gaps AND developer approved

**Step 4: Status hygiene scan**
- For each non-terminal story with `story_file: true`, read the story file
- Look for Dev Agent Record section with a File List or DoD checklist
- If all items are `[x]` (checked) and the story status is not `done`,
  flag as a status mismatch
- Store mismatches as findings

**Step 5: Delegate to epic-grooming**
- Invoke `momentum:epic-grooming` for epic-level structural analysis
- If the skill doesn't exist yet, flag it and skip this step

**Step 6: Stale-story individual evaluation**
- Identify candidates: status `backlog`, priority `low`, no story file
- For each candidate, evaluate:
  - What value does this story represent?
  - Is that value captured elsewhere?
  - Recommendation: keep or drop, with rationale
- Store evaluations as findings for developer review

**Step 7: Consolidated findings with batch approval**
- Present all findings grouped by category:
  1. Planning artifact updates (from wave 1, if any remain unapplied)
  2. Status mismatches
  3. Epic issues (from epic-grooming, if run)
  4. Stale-story evaluations
- Scale-adaptive UX:
  - Under 5 findings: present individually, ask A/M/R per finding
  - 5+ findings: present by category, offer batch operations first
    ("approve all status mismatches?"), then allow individual overrides
- Developer can: approve/reject entire categories, approve/reject by range
  (e.g., "1-5"), or go finding-by-finding

**Step 8: Apply approved changes**
- Status transitions: `momentum-tools sprint status-transition --story SLUG --target done`
- Story drops: `momentum-tools sprint status-transition --story SLUG --target dropped`
- Epic reassignments: `momentum-tools sprint epic-membership --story SLUG --epic SLUG`
- New stories from findings: delegate to `momentum:create-story`

**Step 9: Summary**
- Changes applied by type, findings rejected
- Before/after priority distribution
- Epic distribution changes if any

### Orchestrator Purity

Same rule as v1 — the workflow reads files and presents information, but
all mutations go through `momentum-tools` CLI or delegated skills. No
Edit/Write on index.json or any project file.

### Existing Evals to Replace

The current evals at `skills/momentum/skills/refine/evals/` test the v1
behavior (gap discovery agents, CLI-only mutations). The v2 rewrite changes
the workflow's analysis steps, so evals must be rewritten to test:
- Planning artifact discovery and update with approval gate (new)
- Status hygiene detection (new)
- Absence of dependency analysis and logging (regression guard)

### What NOT to Change

- `momentum-tools.py` — no new CLI commands needed
- `momentum:create-story` — invoke it, don't modify it
- Sprint-planning or sprint-dev workflows
- `stories/index.json` directly
- Planning artifacts are authoritative — never archive or mark optional

## Momentum Implementation Guide

**Change Types in This Story:**
- All tasks -> skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Before writing a single line of the skill:**
1. Write 3 behavioral evals in `skills/momentum/skills/refine/evals/`:
   - Planning artifact discovery+update with approval gate
   - Status hygiene detection and CLI transitions
   - No dependency analysis and no logging
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
