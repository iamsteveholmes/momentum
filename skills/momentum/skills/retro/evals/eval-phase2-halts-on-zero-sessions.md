# Eval: Phase 2 Halts on Zero Session Matches

## Scenario

Given a retro invoked for sprint slug `sprint-2026-04-99` whose `started`/`completed` date
range (e.g., `2026-04-99` to `2026-04-99`) matches no Claude Code session files in the
transcripts directory, the retro skill executes Phase 2.

## Expected Behavior

The skill should:
1. Run the 4 extraction commands (user-messages, agent-summaries, errors, team-messages)
2. Detect that zero session files were found for the date range
3. Emit an explicit error message that names:
   - The sprint slug (`sprint-2026-04-99`)
   - The date range (`2026-04-99 → 2026-04-99`)
   - The standard diagnostic list (different project directory, date mismatch, deleted session files, unresolved script path)
4. HALT the retro workflow without prompting the developer to "continue with empty extracts"
5. NOT spawn the auditor team (Phase 3 and beyond are not reached)

## Verification

After Phase 2 completes (with zero sessions):
1. The output message contains the sprint slug `sprint-2026-04-99`
2. The output message contains the date range in `{{sprint_started}} → {{sprint_completed}}` format
3. The output message contains the diagnostic list (at least: project directory, date mismatch, deleted sessions)
4. No auditor team spawn occurs (no Phase 4 TeamCreate or Agent calls)
5. No `<ask>` prompt for "continue with empty extracts" is issued

## Pass Condition

Retro halts in Phase 2 with error output naming sprint slug and date range. Auditor team is
never spawned. Developer is not prompted to continue.

## Fail Condition

Any of the following:
- Retro continues past Phase 2 into Phase 3 or Phase 4 with empty data
- Developer is prompted to "continue with empty extracts"
- Error message omits the sprint slug or the date range
- Auditor team is spawned despite zero session matches

## Rationale

AC5 of `retire-sprint-log-final-cleanup`: "Given a sprint slug whose date range matches no
session files, the retro workflow halts in Phase 2 before spawning the auditor team —
preventing a false-positive audit against an empty dataset." RF-00 finding from
sprint-2026-04-11 retro identified this as the zero-session false-positive risk.
