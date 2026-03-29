# Eval: Progress Bar Basic Rendering

## Scenario

Given:
- `sprint-status.yaml` exists with:
  - `epic-1: done`
  - `epic-2a: in-progress` (with 3 stories having status `ready-for-dev` or `in-progress`)
  - `epic-3: backlog`
- `session_stats.momentum_completions: 1` (repeat user, verbose threshold not met)
- No open journal threads (so Step 7 no-thread path executes)

When `/momentum` runs

Then Impetus should:
- Render the verbose multi-line progress bar as the **first visible output** (before orientation text or menu)
- Show `✓  Epic 1` for the done epic
- Show `→  Epic 2a` with a story count (e.g., `3 stories active`) for the in-progress epic
- Show `◦  Epic 3` for the next backlog epic
- Follow the bar with a blank line before the rest of Step 7 output
- Produce no narration before or around the bar (no "Reading sprint status..." or "Here's your progress:")

## What to Test

Behavioral: output ordering and content shape.
- Bar appears before "Everything's in place" or menu text
- Correct symbols: `✓`, `→`, `◦`
- Done epics, in-progress epics, and one backlog epic all appear
- No preamble text precedes the bar
