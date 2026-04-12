# Eval: Retro produces sprint-summary.md at retro close

## Scenario

Given a sprint (`sprint-2026-03-01`) has been retrospected through Phases 1–5, and Phase 6 has
called `momentum-tools sprint retro-complete` successfully, and the retro orchestrator has the
following state available:

- `{{sprint_slug}}` = "sprint-2026-03-01"
- `{{sprint_started}}` = "2026-03-01"
- `{{sprint_completed}}` = "2026-03-14"
- `{{verified_stories}}` = ["story-a", "story-b", "story-c"]
- `{{incomplete_stories}}` = []
- `{{force_closed_slugs}}` = []
- `{{approved_count}}` = 2 (story stubs from Phase 5)
- `{{today}}` = "2026-03-15"
- `momentum:feature-status` subagent ran successfully and `.claude/momentum/feature-status.md` exists
  with content showing "Feature X: in-progress → done" for this sprint

## Expected Behavior

The retro orchestrator should:

1. Invoke `momentum:feature-status` as a subagent after `retro-complete` and before writing the
   summary file.
2. Write a file at `_bmad-output/implementation-artifacts/sprints/sprint-2026-03-01/sprint-summary.md`
   using the Write tool directly (not via a subagent spawn).
3. The written file contains all required sections in order:
   - `# Sprint Summary — sprint-2026-03-01` header
   - `**Sprint completed:**` and `**Retro date:**` metadata lines
   - `## Features Advanced` section (present because feature-status ran and file exists)
   - `## Stories Completed vs. Planned` section showing 3/3 completed
   - `## Key Decisions` section
   - `## Unresolved Issues` section (reads "None." since no incomplete stories or stubs)
   - `## Narrative` paragraph (3–5 sentences)
4. The total word count of the written file is under 500 words.
5. The final output shown to the developer includes the confirmation line:
   `Sprint summary: _bmad-output/implementation-artifacts/sprints/sprint-2026-03-01/sprint-summary.md`

## What This Tests

- Phase 6 correctly spawns `momentum:feature-status` before writing the summary
- The summary is written directly by the retro orchestrator (not delegated to another agent)
- All required sections are present and in the correct order
- The 500-word cap is respected
- The completion output confirms the file path
