# Eval: Phase 2 Proceeds on Non-Empty Sessions

## Scenario

Given a retro invoked for sprint slug `sprint-2026-04-10` whose `started`/`completed` date
range matches at least one Claude Code session file, so that at least one of the four
extraction commands (user-messages, agent-summaries, errors, team-messages) produces a
non-zero-line output file.

## Expected Behavior

The skill should:
1. Run the 4 extraction commands (user-messages, agent-summaries, errors, team-messages)
2. Detect that at least one session file was found for the date range
3. Log the four extract counts (user_msg_count, agent_count, error_count, team_msg_count)
4. Output "Transcript preprocessing complete" with the extract counts
5. Advance to Phase 3 without prompting the developer

## Verification

After Phase 2 completes (with at least one session found):
1. The output contains "Transcript preprocessing complete"
2. All four extract line counts are reported
3. No error or halt message is emitted
4. No `<ask>` prompt for "continue" is issued
5. Workflow advances to Phase 3 (story verification)

## Pass Condition

Phase 2 completes successfully with extract counts logged. Workflow advances to Phase 3
without any developer prompt.

## Fail Condition

Any of the following:
- Phase 2 emits an error or halt despite non-empty session data
- Developer is prompted before advancing to Phase 3
- Extract counts are not reported in the output
- Workflow does not advance to Phase 3

## Rationale

AC5 of `retire-sprint-log-final-cleanup`: the hard-fail triggers only when zero session
matches are found for the date range — not when some extracts happen to produce zero rows
while others have data. A sprint with real session data must proceed to the auditor team
without interruption.
