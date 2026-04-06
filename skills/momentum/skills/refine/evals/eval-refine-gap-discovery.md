# Eval: Refine Skill — Parallel Gap Discovery Agents

## Setup
Invoke `/momentum:refine` on a project that has `_bmad-output/planning-artifacts/prd.md`
and `_bmad-output/planning-artifacts/architecture.md`. Proceed past the backlog
presentation step to trigger gap discovery.

## Expected Behavior
1. The skill spawns exactly two discovery subagents in parallel (not sequentially):
   - A PRD coverage agent that reads prd.md and stories/index.json
   - An architecture coverage agent that reads architecture.md and stories/index.json
2. The PRD coverage agent returns structured findings: each finding has an identifier,
   description, suggested epic, and suggested priority
3. The architecture coverage agent returns structured findings in the same structure
4. Both agents return before the findings are consolidated — the skill waits for both
5. The consolidated findings report covers at minimum: coverage gaps from PRD,
   coverage gaps from architecture, and any locally detected issues (priority
   suggestions, stale candidates, dependency issues, epic mismatches)
6. Each finding includes: category, story/requirement reference, recommended action,
   and rationale
7. The developer is presented with findings and asked to approve, modify, or reject
   each finding individually — the skill does not bulk-apply all findings

## Verification
The skill must not proceed to applying changes until the developer has responded to
findings. Findings from both parallel agents must appear in the consolidated report.
