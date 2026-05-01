---
title: Sprint Planning Synthesis-First — Lead with Recommendations Not Data Dumps
story_key: sprint-planning-synthesis-first
status: backlog
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum/skills/sprint-planning/workflow.md
change_type: skill-instruction
priority: high
---

# Sprint Planning Synthesis-First — Lead with Recommendations Not Data Dumps

## Problem

Sprint planning Step 1 dumps the entire backlog as a raw sorted list and asks the
developer to pick stories from it. The user's reaction at 03:04 was immediate:
"Good lord that is a wall of crap. What about making some suggestions from the
master plan and backlog?" At 14:45 the user also flagged staleness: "Are we
certain those ready for dev stories have not already been implemented?"

The current Step 1 is a data-presentation step when it should be a
synthesis-and-recommendation step. The developer wants an opinionated assistant
that has read the master plan, checked what's already done, and arrives with a
short list of recommendations — not an unfiltered inventory.

## Root Cause

Step 1 reads `stories/index.json`, filters/sorts, and presents everything that
isn't done or dropped. It never reads the master plan (`prd.md`,
`product-brief-momentum-2026-03-13.md`) to understand strategic priorities. It
never checks git history to see if "ready-for-dev" stories have actually been
implemented already. The result is a wall of undifferentiated items including
stale candidates.

## Solution

Restructure Step 1 into three sub-phases: (A) read the master plan and backlog,
(B) run a staleness check against git history, (C) synthesize and present
prioritized recommendations — followed by the full backlog as an expandable
reference, not the lead content.

## Acceptance Criteria (Plain English)

1. Sprint planning reads the master plan documents (`prd.md` and the product
   brief) before presenting any backlog data. The master plan informs which
   areas of the product are highest priority for the next sprint.

2. Before presenting stories as candidates, sprint planning runs a staleness
   check: for each story with status `ready-for-dev` or `in-progress`, check
   git history for commits that touch the story's `touches` paths. If
   substantial implementation commits exist, flag the story as potentially
   already implemented and exclude it from recommendations (surface it in a
   separate "Potentially stale" section with evidence).

3. Sprint planning leads with a synthesis section: 3-5 prioritized
   recommendations with brief rationale for each, informed by the master plan's
   current priorities, dependency readiness, and backlog state. Each
   recommendation explains *why* this story matters now.

4. The full backlog is still available below the recommendations as reference
   material, but it is clearly secondary — not the opening content. The
   developer sees recommendations first, full backlog second.

5. Stories flagged as potentially stale include the evidence (commit hashes
   and/or summary of changes touching their paths) so the developer can make
   an informed decision about whether to include, skip, or mark as done.

6. The synthesis considers dependency readiness: stories whose dependencies
   are all satisfied are preferred over stories with pending dependencies,
   and this is reflected in the recommendation rationale.

7. If the master plan documents are missing or empty, sprint planning falls
   back to the current behavior (sorted backlog) with a warning that
   recommendations require a master plan.

## Dev Notes

### What changes in workflow.md

**Step 1 restructure** — the current Step 1 (lines 33-65) becomes three
sub-phases within the same step:

**Phase A — Master plan read (new):**
- Read `{planning_artifacts}/prd.md` — extract current priorities, recent
  edit history (the frontmatter `editHistory` shows what was recently added
  or changed, indicating active areas)
- Read `{planning_artifacts}/product-brief-momentum-2026-03-13.md` — extract
  the product vision and strategic goals
- Store a mental model of "what matters most right now" based on these docs

**Phase B — Staleness check (new):**
- Read `{implementation_artifacts}/stories/index.json`
- For each story with status `ready-for-dev` or `in-progress`:
  - Get the story's `touches` paths
  - Run `git log --oneline --since="30 days ago" -- <touches paths>` to find
    recent commits touching those files
  - If commits exist, flag the story as potentially stale
  - Store the evidence (commit one-liners) for display
- Filter: exclude `done`, `dropped`, `closed-incomplete` as today
- Additionally mark stale candidates separately from clean candidates

**Phase C — Synthesis and display (replaces current raw dump):**
- From the clean (non-stale) candidate pool, select 3-5 top recommendations:
  - Weight by: priority field, master plan alignment, dependency readiness
    (all deps satisfied > some deps pending), recency of related PRD edits
  - Write a 1-2 sentence rationale for each recommendation
- Display format:

```
Sprint Planning — Recommendations

Based on the master plan and current backlog state:

  1. [H] story-slug — Title
     Why now: rationale based on master plan priorities and readiness

  2. [C] story-slug — Title
     Why now: rationale

  3. [H] story-slug — Title
     Why now: rationale

  ...

Potentially stale (may already be implemented):
  · story-slug — Title · recent commits: a1b2c3d "commit msg", e4f5g6h "commit msg"
  · story-slug — Title · recent commits: ...

Full backlog — N stories across M epics:
  [same format as current Step 1 output, but positioned as reference]

Select 3-8 stories for this sprint by number or slug.
```

### What stays the same

- The output of Step 1 still ends with the selection prompt
- Story numbering in the full backlog section stays the same (developers can
  still select by number)
- Steps 2-8 are unchanged
- The filtering logic (exclude done/dropped/closed-incomplete) stays the same
- The grouping by epic and sorting within epics stays the same for the full
  backlog section

### Tasks

1. Read and understand current Step 1 implementation in workflow.md (lines 33-65)
2. Add Phase A — master plan read actions before the backlog read
3. Add Phase B — staleness check with git log queries after index read
4. Rewrite Phase C — synthesis display with recommendations section, stale
   section, and full backlog as secondary reference
5. Update the step's `<output>` template to show the new three-section format
6. Update the log action to reflect the new synthesis behavior
7. Verify the step still ends with the same selection prompt for Step 2
