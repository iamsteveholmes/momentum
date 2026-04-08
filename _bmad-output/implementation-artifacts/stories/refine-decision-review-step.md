# Refine Workflow — Decision Review Step

Status: backlog
Epic: impetus-epic-orchestrator
Priority: medium
Depends on: decision-registry-skill

## What This Is

A new step in the `momentum:refine` workflow that reviews SDR documents to ensure decisions don't fall through the cracks between "we decided X" and "we have stories for X in the backlog."

## Why It Matters

SDRs list `stories_affected` and phased implementation plans that reference future work. Without periodic review, gaps accumulate: a decision says "Phase 3 needs new stories for Norn Content Protocol" but nobody creates them. Decision gates specify timing conditions ("after Phase 1 is done") but nobody checks whether the gate criteria are met.

Refine already catches status mismatches, epic issues, and stale stories. Decision review is the same class of hygiene — ensuring planning artifacts stay connected to actionable backlog work.

## What the Step Should Do

- Read all SDR documents in `_bmad-output/planning-artifacts/decisions/`
- For each SDR, check whether stories listed in `stories_affected` exist in the backlog
- Flag any `stories_affected` entries that have no matching story in the index
- Check phased implementation plans for references to work that doesn't have stories yet (e.g., "New stories needed" in a phase description)
- Check decision gates: if a gate's timing condition appears met (e.g., "Phase 1 done" and all Phase 1 stories are done), flag it for review
- Surface findings alongside existing refine output (status mismatches, epic issues, stale stories)
- Approved findings result in story creation (via momentum:create-story or momentum:intake) or decision gate reviews

## Where It Fits in the Refine Workflow

Between planning artifact discovery and the status hygiene scan — after refine has loaded context about the current backlog state but before it produces consolidated findings. Decision review findings merge into the same findings presentation.

## Design Decisions Already Made

- The decision registry format is defined by the decision-registry-skill story
- Refine already has a consolidated findings step with user approval before acting — decision review findings should integrate with that, not create a separate approval flow
- Gate timing detection is best-effort: match story statuses against phase descriptions, don't try to parse arbitrary timing conditions
