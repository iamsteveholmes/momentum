# Eval: Trivial Classification

## Scenario

**Given** a plan file at `~/.claude/plans/` with this content:

```markdown
# Plan: Research AVFL benchmark results

## Context

I want to understand how the AVFL benchmark results compare across models.

## Steps

1. Read `docs/research/avfl-benchmark-results.md`
2. Read `docs/research/phase-4-findings.md`
3. Summarize the key differences between Sonnet and Opus as Adversary validators
4. Present findings

## Verification

- Summary covers Sonnet vs. Opus adversary comparison
- No files created or modified
```

**And** the skill is invoked via `momentum-plan-audit`.

## Expected Behavior

The skill should:

1. **Load the plan** — read the most recently modified `.md` in `~/.claude/plans/`
2. **Classify as trivial** — plan involves ONLY read-only operations (Read tool calls, no Write/Edit/Bash that creates files)
3. **Skip Steps 3, 4, 5** — no spec file reads, no process story creation, no AVFL invocation
4. **Write `## Spec Impact`** to the plan file with exactly:
   - `Classification: trivial`
   - The reason (read-only operations only)
   - `Go/No-Go: Proceed.`
5. **NOT create** any process story file in `_bmad-output/stories/`
6. **NOT invoke** the `avfl` skill

## Pass Criteria

- `## Spec Impact` section present in plan file after skill runs
- Section contains `Classification: trivial`
- Section contains `Go/No-Go: Proceed.`
- No new files in `_bmad-output/stories/`
- No AVFL invocation occurred
