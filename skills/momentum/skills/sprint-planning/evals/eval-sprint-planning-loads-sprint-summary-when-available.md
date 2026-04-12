# Eval: Sprint planning Step 1 loads sprint summary when available

## Scenario

Given sprint planning is running Step 1 (Synthesize recommendations from master plan and backlog),
and the sprints/index.json `completed` array contains entries where the most recently completed
sprint is `sprint-2026-03-01` with `retro_run_at: "2026-03-15"`,
and the file `_bmad-output/implementation-artifacts/sprints/sprint-2026-03-01/sprint-summary.md`
exists with content describing features advanced, stories completed, and key decisions.

## Expected Behavior

The sprint planning orchestrator should:

1. Read `_bmad-output/implementation-artifacts/sprints/index.json` early in Step 1,
   after reading PRD and product brief but before performing backlog staleness checks.
2. Find the most recently completed sprint with a non-null `retro_run_at` value
   (in this case: `sprint-2026-03-01`).
3. Read `_bmad-output/implementation-artifacts/sprints/sprint-2026-03-01/sprint-summary.md`.
4. Include the sprint summary content in its recommendation synthesis — the "what happened last
   sprint" signal informs which features advanced and which areas were in active development,
   thereby influencing which stories rank as high-priority candidates.
5. The recommendations shown to the developer reflect awareness of the previous sprint's outcomes
   (e.g., features that advanced last sprint may reduce urgency of related stories; incomplete
   areas may increase urgency of follow-on stories).

## What This Tests

- Step 1 reads sprints/index.json to find the most recently completed sprint with retro_run_at
- The sprint-summary.md is read and its content is incorporated into recommendation synthesis
- The sprint summary load occurs BEFORE the backlog staleness check (correct sequencing)
- The summary acts as additional context (not a replacement for PRD/backlog analysis)

---

# Eval: Sprint planning Step 1 continues gracefully when no sprint summary exists

## Scenario

Given sprint planning is running Step 1, and either:
  (a) `_bmad-output/implementation-artifacts/sprints/index.json` has no completed sprints with
      `retro_run_at` set, OR
  (b) The most recently completed sprint is `sprint-2026-02-01` with `retro_run_at` set, but
      `_bmad-output/implementation-artifacts/sprints/sprint-2026-02-01/sprint-summary.md`
      does not exist.

## Expected Behavior

The sprint planning orchestrator should:

1. Attempt to find the most recent completed sprint with `retro_run_at`.
2. When no summary file is found (case a or b), display a notice to the developer:
   `No sprint summary found for {sprint-slug} — context from previous sprint unavailable.`
   (or a similar non-blocking notice)
3. Continue Step 1 without halting — the sprint summary load is non-blocking.
4. Proceed to perform the backlog staleness check and recommendation synthesis using only
   PRD and product brief (the normal path).

## What This Tests

- Missing sprint summary does not block sprint planning
- The developer sees a notice so they know prior context is unavailable
- The workflow continues correctly without the summary
