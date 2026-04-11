# Eval: Three-Path Routing

**Behavioral expectation (AC3, AC4, AC5, AC6):** Distill classifies fix scope during discovery
and routes to the correct path without re-classification after the write.

## Scenario A — Path A (project-local)

**Input:**
- Learning: "Always check git status before any merge operation"
- Candidate: `.claude/rules/git-discipline.md` in a non-Momentum project

**Expected behavior:**
- Discovery classifies: Path A (project-local rule file)
- Phase 3 spawns write subagent to update `.claude/rules/git-discipline.md`
- Commits with `feat(rules): distill — ...`
- Does NOT bump plugin.json version
- Ledger entry: `{"path": "A", "origin": "distill", ...}`

## Scenario B — Path B (Momentum project)

**Input:**
- Learning: "The distill skill's Adversary should check for scope-fit in references too"
- Candidate: `skills/momentum/skills/distill/workflow.md`
- Working directory IS the Momentum project

**Expected behavior:**
- Discovery classifies: Path B (Momentum-level, in Momentum project)
- Phase 3 spawns write subagent to update workflow.md
- Phase 3 also spawns write subagent to bump `skills/momentum/.claude-plugin/plugin.json` patch version
- Commits include both file and version bump
- Developer is presented push summary before push
- Ledger entry: `{"path": "B", "origin": "distill", ...}`

## Scenario C — Path C (external project, Momentum target)

**Input:**
- Learning: "The quick-fix workflow should mention distill as an alternative for practice gaps"
- Candidate: `skills/momentum/skills/quick-fix/workflow.md` (Momentum file)
- Working directory is NOT the Momentum project

**Expected behavior:**
- Discovery classifies: Path C (Momentum-level, external project)
- Phase 2 presents two options: Defer (D) or Generate remote prompt (G)
- If D: ledger entry written with `disposition: deferred`, no files modified
- If G: remote prompt block presented in output, no files modified, ledger entry written
- Distill does NOT attempt to write to Momentum files from the external project

## Observable Verification

- Path A: `git log --oneline` shows `feat(rules): distill` commit without plugin.json in the diff
- Path B: `git log --oneline` shows commit with both the practice file and plugin.json
- Path C: No `git commit` occurs; ledger entry written; developer sees defer or remote-prompt output

## Failure Mode

- Path B without version bump → AC5 violation
- Path C attempting to write Momentum files → AC6 violation
- Classification happening AFTER the write → AC3 violation
