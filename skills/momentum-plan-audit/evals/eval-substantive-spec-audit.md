# Eval: Substantive Plan — Spec Audit and Process Story Creation

## Scenario

**Given** a plan file at `~/.claude/plans/` with this content:

```markdown
# Plan: Add momentum-code-review Skill

## Context

We need a code review skill that runs adversarial review on git diffs before merge.

## Files to Create / Modify

| Action | Path |
|---|---|
| Create | skills/momentum-code-review/SKILL.md |
| Create | skills/momentum-code-review/workflow.md |
| Modify | .claude/settings.json (add PostToolUse hook for auto-review trigger) |

## Skill Design

### SKILL.md
name: momentum-code-review
description: Runs adversarial code review on staged changes before merge.
model: opus
effort: high

### Workflow
Step 1 — Get diff (git diff --staged)
Step 2 — Run three parallel review agents (blind hunter, edge case hunter, acceptance auditor)
Step 3 — Consolidate findings
Step 4 — Present findings with severity classification

## Verification

- Skill classifies staged diff correctly
- Three parallel agents run simultaneously
- Findings consolidated with severity: critical, high, medium, low
- Hook triggers on Write tool calls to .js and .ts files
```

**And** the skill is invoked via `momentum-plan-audit`.

**And** the current sprint is Sprint 1 (from epics.md).

**And** no `p1.N` process stories exist yet in `_bmad-output/stories/`.

## Expected Behavior

The skill should:

1. **Load the plan** — read the most recently modified `.md` in `~/.claude/plans/`
2. **Classify as substantive** — plan creates new skill files and modifies `.claude/settings.json`
3. **Create process story `p1.1`** at `_bmad-output/stories/p1.1.md` with:
   - Frontmatter: `story_id: p1.1`, `status: ready`, `type: process`, `epic: P1 — Process Sprint-1`, `sprint: 1`
   - Story body derived from plan Context
   - Acceptance criteria derived from plan Verification section
4. **Identify relevant spec sections** — read only the Hook Infrastructure section from architecture.md (plan touches `.claude/settings.json` hook config)
5. **Run single AVFL checkpoint** with:
   - `output_to_validate`: combined plan + process story (labeled `=== PLAN ===` and `=== PROCESS STORY ===`)
   - `source_material`: the Hook Infrastructure section text
   - `profile: checkpoint, stage: checkpoint`
6. **Write `## Spec Impact`** with: Classification, process story path, any upstream spec recommendations, AVFL result, Go/No-Go
7. **Ask the user** if AVFL returns critical findings — do not silently proceed

## Pass Criteria

- `## Spec Impact` section present in plan file
- `Classification: substantive`
- Process story `_bmad-output/stories/p1.1.md` exists with correct frontmatter (`type: process`, `epic: P1 — Process Sprint-1`)
- Story ACs are derived from plan's Verification section
- AVFL was invoked exactly once (single combined pass)
- AVFL `output_to_validate` contained both plan and story with `=== PLAN ===` and `=== PROCESS STORY ===` labels
- Hook Infrastructure was identified as the relevant spec section (not full architecture.md)
- Spec Impact section contains `Go/No-Go` conclusion
