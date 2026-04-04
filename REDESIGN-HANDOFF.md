# Momentum Orchestration Redesign — Handoff

## Full Plan

The complete redesign plan is at `~/.claude/plans/ethereal-popping-sun.md`. It covers the full architecture: workflow modules, executor subagents, sub-commands, sprint execution, triage, refine, retro.

## What's Done (Epic 0 — Redesign Foundation, 2026-04-02)

Three foundation stories implemented:

1. **Story 0.1: Story ID Migration** — 70 story keys renamed from `N-N-slug` to plain kebab-case slugs. 34 story files renamed. All references updated.

2. **Story 0.2: Sprint-Status Decomposition** — `sprint-status.yaml` decomposed into:
   - `_bmad-output/implementation-artifacts/stories/index.json` — 68 story entries (status, title, epic_slug, depends_on, touches)
   - `_bmad-output/implementation-artifacts/stories/{slug}.md` — 68 stub story files
   - `_bmad-output/implementation-artifacts/sprints/index.json` — sprint tracking
   - `epics.md` trimmed to names/slugs/descriptions only (2682 → 595 lines)
   - Schema reference at `skills/momentum/references/sprint-tracking-schema.md`
   - 4 skill workflows updated to read from new locations

3. **Story 0.3: Sprint-Manager Skill** — `skills/momentum/skills/sprint-manager/` created. Sole writer of stories/index.json and sprints/index.json. 5 actions (status_transition, sprint_activate, sprint_complete, epic_membership, sprint_plan). State machine reference + 3 evals. Legacy `update-story-status.sh` deprecated.

## Current File Structure

```
_bmad-output/implementation-artifacts/
  stories/
    index.json          ← source of truth for story status + epic membership
    {slug}.md           ← one file per story (stub or fleshed out)
  sprints/
    index.json          ← active/planning/completed sprints
  sprint-status.yaml    ← DEPRECATED — kept for backward compat

_bmad-output/planning-artifacts/
  epics.md              ← epic names, slugs, descriptions only
  architecture.md       ← updated with new schema + write authority
  prd.md                ← updated with new story stages + FR55

skills/momentum/skills/sprint-manager/
  SKILL.md + workflow.md + references/ + evals/
```

## Key Architectural Decisions

- **Impetus is the sole orchestrator.** Communicates, orchestrates, delegates. Never writes files.
- **Sub-commands are workflow modules** Impetus loads — not separate agents. `/momentum:sprint-dev` and `/momentum` both result in Impetus orchestrating.
- **Executor subagents** spawned by Impetus from within workflows. Each has exclusive write authority over designated files. All first-level — no nesting.
- **Reads are free; writes are exclusive.** Subagents write output to files (durable, auditable).
- **Tools over agents for deterministic ops.** State machine validation, JSON mutations, JSONL appends, hash checks → Python CLI tool. LLM reasoning → agent.
- **Task tracking for structural state.** All multi-step workflows use TaskCreate/TaskUpdate/TaskList as the primary position/progress mechanism. Task state survives context compression — prevents drift in long sessions. Tasks = "where am I"; journal = "what happened and why."
- **`allowed-tools` restriction** on Impetus activated in Phase 4 (after all sub-commands exist).

## What's Next (Phase 2 — Impetus Core)

**Architecture Decision: Tools Over Agents.** Sprint-manager operations are purely
deterministic (state machine + JSON mutations). They become a Python CLI tool, not an
executor subagent. Same for triage-writer and version checking. The distinction:
deterministic logic → tool/script; requires judgment → agent.

| Story | What |
|-------|------|
| `momentum-tooling` | Python CLI with sprint subcommands (all 5 actions) + version check. Replaces `update-story-status.sh` and supersedes sprint-manager agent. PEP 723, cross-platform, unit tested. |
| `impetus-identity-redesign` | BMAD-informed Identity section, KITT-like servant character, first-install greeting with personality. Outcome-driven authoring. |
| `session-open-sprint-view` | Sprint-mode detection (3 modes), per-story 16-block fill bars, context menus, reads JSON directly. |

## What's Next (Phase 3 — Sprint Execution Core)

Four stories focused on the critical path to plan and execute sprints with teams:

| Story | What |
|-------|------|
| `agent-logging-tool` | Add `log` subcommand to momentum-tools.py. Every agent logs decisions, errors, retries, assumptions. JSONL append to `.claude/momentum/sprint-logs/`. Foundation for retros. |
| `momentum:dev` | Simplify existing executor: strip AVFL + sprint-status writes. Pure worktree + bmad-dev-story + logging. |
| `momentum:sprint-planning` | Story selection (3-8), create-story on stubs, team composition (which roles + project guidelines), dependency graph, execution plan. |
| `momentum-sprint-dev` | Spawn team of agents per sprint plan. Dependency-driven concurrency (not waves). Track via tasks, handle merges, AVFL, verify, status transitions. |

**Key architecture decisions:**
- **Agent logging** — every agent writes JSONL logs. Primary input for retros.
- **Teams over waves** — dependency-driven concurrency replaces rigid sequential tiers.
- **Two-layer agents** — Momentum provides generic roles; projects provide stack-specific guidelines.
- **Two-output retro** — analyzes logs, produces Momentum triage (practice issues) + Project triage (project issues).
- **Triage vs refinement** — triage = intake (new ideas in); refinement = organization (backlog health).
- **Gherkin separation** — story files have plain English ACs for devs. Detailed `.feature` specs at `sprints/{sprint-slug}/specs/` for verifiers only. Dev agents never see test criteria.
- **AVFL at sprint level** — validates complete sprint plan during planning, not per-story during create-story.

Deferred to Phase 5: triage, refinement, retro workflows + triage-writer tool + verify agent.
Phase 4: activate allowed-tools restriction on Impetus.
