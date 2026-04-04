# Agent vs Skill Audit — Discovery and Implementation

## Context

Momentum has two kinds of things in its architecture (per the master plan at `docs/planning-artifacts/momentum-master-plan.md`, Part 1):

1. **Skills** — SKILL.md files invoked by users or other skills. Multi-step workflows.
2. **Executor subagents** — spawned by skills via the Agent tool. Each has a role, tool constraints, and exclusive write authority.

The master plan defines an executor subagent roster (6 entries) and a separate list of user-facing skills. But in the current implementation, almost everything is a SKILL.md file — even things the plan calls "subagents." Only one proper agent definition file exists: `module/canonical/agents/code-reviewer.md`.

Additionally, the Team Review phase (Decision 34) introduces QA, E2E Validator, and Architect Guard roles that have no agent files or skill files at all.

## Your Task

**Start with thorough discovery.** Do NOT assume the summary above is complete or correct. Spawn multiple subagents to independently investigate:

1. **Architecture and plan discovery** — Read the master plan (`docs/planning-artifacts/momentum-master-plan.md`), architecture doc (`_bmad-output/planning-artifacts/architecture.md`), and PRD (`_bmad-output/planning-artifacts/prd.md`). Map every place that mentions agents, subagents, executor roles, skills, or spawning. Identify what the specs SAY about the agent-vs-skill boundary.

2. **Implementation discovery** — Find every SKILL.md file under `skills/`, every agent definition file under `module/` and anywhere else, and every place in workflow files where the Agent tool is used to spawn something. Map what ACTUALLY EXISTS and how it's wired.

3. **Claude Code capability discovery** — Research how Claude Code agent definition files work vs SKILL.md files. What are the actual mechanical differences? What does `context: fork` do? What does `allowed-tools` enforce? Can agent files have tool restrictions that SKILL.md files can't? Check the Claude Code documentation or skill files for guidance.

4. **Gap analysis** — Compare what the specs promise with what exists. Identify: roles with no file at all, roles implemented as the wrong type, missing tool/write constraints, and the QA/E2E Validator roles that appear in Decision 34 but have no implementation.

After discovery, synthesize your findings and propose:
- A clear decision framework: when should something be an agent file vs a SKILL.md vs both?
- Which existing files need to change type (agent → skill or skill → agent)
- Which new files need to be created
- How this affects the plugin migration (the active sprint is restructuring the skills directory)
- A draft architecture decision to formalize this

Then implement: create the agent files, update the architecture doc with the decision, and update any cross-references.

## Key Files

- Master plan: `docs/planning-artifacts/momentum-master-plan.md`
- Architecture: `_bmad-output/planning-artifacts/architecture.md`
- PRD: `_bmad-output/planning-artifacts/prd.md`
- Existing agent file: `module/canonical/agents/code-reviewer.md`
- All skills: `skills/momentum*/SKILL.md` and `skills/momentum/skills/*/SKILL.md` (plugin migration may be in progress)
- Sprint-dev workflow: `skills/momentum/workflows/sprint-dev.md`
- Sprint-planning workflow: `skills/momentum/workflows/sprint-planning.md`
- Impetus workflow: `skills/momentum/workflow.md`

## Constraints

- Follow the git discipline rules in `~/.claude/rules/git-discipline.md`
- We are currently on branch `sprint/sprint-2026-04-04-2` — work on main or create your own branch
- Commits are autonomous — don't ask, just commit at each logical unit
- This work should result in an architecture decision (numbered, following the existing pattern in the architecture doc)
