# Eval: Sprint summary omits Features Advanced section when feature-status unavailable

## Scenario

Given a sprint (`sprint-2026-02-01`) retro has completed Phase 6 and called `retro-complete`,
and `momentum:feature-status` either:
  (a) failed to run (subagent errored), OR
  (b) ran but `.claude/momentum/feature-status.md` does not exist afterward

The retro orchestrator proceeds to write the sprint summary.

## Expected Behavior

The retro orchestrator should:

1. Attempt to invoke `momentum:feature-status` as a subagent.
2. When feature-status fails or the output file is absent, NOT include the `## Features Advanced`
   section in the sprint-summary.md at all — the section is completely omitted (no heading,
   no "N/A" placeholder, no empty section).
3. Still write the sprint-summary.md file with the remaining required sections:
   - `# Sprint Summary — sprint-2026-02-01` header
   - Metadata lines
   - `## Stories Completed vs. Planned`
   - `## Key Decisions`
   - `## Unresolved Issues`
   - `## Narrative`
4. The final developer output still confirms the summary file path.

## What This Tests

- The `## Features Advanced` section is conditional — only present when feature-status data exists
- A failed or absent feature-status result does not block summary writing
- The summary is still complete and useful without the Features Advanced section
- The orchestrator does not raise an error or halt when feature-status is unavailable
