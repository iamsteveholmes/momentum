---
title: "retro audit-workflow.js: return structured process_findings (<=7 Keep/Stop/Change) + routine_process_count for the fused results gate"
story_key: retro-audit-workflow-process-findings-return
status: backlog
epic_slug: momentum-sprint-retro
feature_slug:
story_type: maintenance
priority: high
depends_on: [retro-phase4-dynamic-workflow-audit-engine]
touches: [skills/momentum/skills/retro/audit-workflow.js, skills/momentum/skills/retro/workflow.md]
---

# retro audit-workflow.js: return structured process_findings (<=7 Keep/Stop/Change) + routine_process_count for the fused results gate

<!-- BACKFILLED STUB: this index entry was a phantom (story_file:true, no .md).
     Backfilled by momentum:retro during the sprint-2026-06-28 retro (2026-07-06), which
     also raised priority medium->high and corrected the epic momentum-impetus-experience ->
     momentum-sprint-retro (approved at the Phase 5 gate). It is a stub, NOT a dev-ready
     story. All sections below marked DRAFT require full rewrite by create-story. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As the practice maintainer,
I want the retro audit Workflow to return structured `process_findings` (≤7 Keep/Stop/Change) and `routine_process_count`,
so that retro Phase 4.5 can fuse process findings into the post-sprint results gate instead of silently skipping.

## Description

`retro/workflow.md:304-305` documents the Phase 4.5 fused-re-render contract (`{{process_findings}}` / `{{routine_process_count}}` with a graceful-degradation branch), but `skills/momentum/skills/retro/audit-workflow.js` never emits these fields — its return schema requires exactly `{priority_action_items, handoff_candidates, metrics, doc_path, synthesize_status}`. The sprint-2026-06-28 retro's own Phase 4.5 silently skipped and fell back to "review separately" because of this gap (`fused_render_completed=false`, endgate HTML untouched).

**Relationship (from dedup verification, 2026-07-06):** `retro-phase4-dynamic-workflow-audit-engine` (ready-for-dev, high) authors/owns the same file and freezes the return contract WITHOUT these fields (its AC4). This story is the follow-on contract extension — it depends on that story and must extend the NEW engine's contract, not patch the pre-rewrite file. The model-pinning AC originally attached here was moved to that story (it owns the 4 `agent()` call sites).

## Acceptance Criteria

<!-- DRAFT: rough ACs from the retro audit return. NOT refined or validated.
     This section MUST be fully rewritten by create-story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- `audit-workflow.js` emits both `process_findings` (≤7 Keep/Stop/Change items) and `routine_process_count` per the documented workflow.md contract
- A retro run against a real sprint produces the fused re-render instead of the fallback path
- The extension lands on top of the `retro-phase4-dynamic-workflow-audit-engine` contract (no divergent second contract)

> Note: The ACs above are rough captures from the audit. Create-story will replace them
> with validated, testable acceptance criteria.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- Contract site: `skills/momentum/skills/retro/workflow.md` Phase 4.5 (`{{process_findings}}` binding, graceful-degradation branch)
- Owning rewrite story: `.momentum/stories/retro-phase4-dynamic-workflow-audit-engine.md` (AC4 return contract)
- Retro audit return: `.momentum/sprints/sprint-2026-06-28/audit-return.json` (priority item 4)

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
